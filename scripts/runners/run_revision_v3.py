#!/usr/bin/env python
"""SEMTRA revision v3 enhanced prediction and vision-encoder runner."""

from __future__ import annotations

import argparse
import csv
import importlib.metadata as importlib_metadata
import json
import math
import platform
import re
import shutil
import sys
import tarfile
import time
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from PIL import Image
from scipy.io import loadmat

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))

from paper1_core import class_mode_signatures, fit_discretizers, fit_transition, quantize  # noqa: E402
from run_revision_v1 import (  # noqa: E402
    CONF_GRID,
    DERM_Q_GRID,
    SEED_DEFAULT,
    SUN_Q_GRID,
    append_jsonl,
    classifier_predictions,
    clean_name,
    evaluate_rulebook,
    fmt_num,
    group_derm_diagnosis,
    json_default,
    latex_table,
    load_awa2_parquet,
    load_xlsa_mat_dataset,
    mat_string,
    now_iso,
    package_versions,
    protocol_a_split,
    run_capture,
    select_attributes,
    sha256_file,
    tex_escape,
    write_csv,
    write_json_safe,
)
from run_revision_v2 import (  # noqa: E402
    copy_if_exists,
    copy_referenced_figures,
    duplicate_labels,
    file_record,
    latex_log_issues,
    missing_bib_keys,
    read_text,
    rel_to,
    write_text,
)


V3_VERSION = "3.0"
DEFAULT_SEED = 20260617
REQUIRED_ENHANCED_COLUMNS = [
    "eval_position",
    "source_row_index",
    "true_label",
    "true_class",
    "base_prediction",
    "base_class",
    "prediction",
    "rule_class",
    "mode",
    "abstained",
    "conflict",
    "activated_rules",
    "n_activated",
    "covered",
    "correct_when_covered",
    "faithful_to_base_when_covered",
]


@dataclass
class RunContext:
    root: Path
    v1: Path
    v2: Path
    out: Path
    manuscript: Path
    rng: np.random.Generator
    n_boot: int
    smoke: bool
    derm_batch_size: int
    derm_device: str
    force_rebuild: bool
    errors: list[str]
    warnings: list[str]


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_markdown(path: Path, lines: Iterable[str]) -> None:
    write_text(path, "\n".join(lines) + "\n")


def safe_reset_out_dir(out: Path, root: Path) -> None:
    resolved_out = out.resolve()
    default_out = (root.resolve() / "outputs" / "revision_v3").resolve()
    if resolved_out != default_out:
        raise RuntimeError(f"Refusing to delete non-default v3 output path: {resolved_out}")
    if resolved_out.exists():
        shutil.rmtree(resolved_out)


def package_versions_v3() -> dict[str, str]:
    versions = package_versions()
    for name in ["torch", "torchvision"]:
        try:
            versions[name] = importlib_metadata.version(name)
        except importlib_metadata.PackageNotFoundError:
            versions[name] = "not installed"
    return versions


def safe_class_name(class_names: list[str], label: int) -> str:
    return class_names[int(label)] if 0 <= int(label) < len(class_names) else ""


def bool_series(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes", "y"])


def enhanced_prediction_df(
    *,
    dataset: str,
    seed: int,
    scope: str,
    pred: pd.DataFrame,
    source_indices: np.ndarray,
    true_labels: np.ndarray,
    class_names: list[str],
    base_pred: np.ndarray,
    extra: pd.DataFrame | None = None,
) -> pd.DataFrame:
    pred_values = pd.to_numeric(pred["prediction"], errors="coerce").fillna(-1).astype(int).to_numpy()
    base_values = np.asarray(base_pred, dtype=int)
    y = np.asarray(true_labels, dtype=int)
    covered = pred_values >= 0
    rows = pd.DataFrame(
        {
            "dataset": dataset,
            "seed": int(seed),
            "scope": scope,
            "eval_position": np.arange(len(pred_values), dtype=int),
            "source_row_index": np.asarray(source_indices, dtype=int),
            "true_label": y,
            "true_class": [safe_class_name(class_names, int(v)) for v in y],
            "base_prediction": base_values,
            "base_class": [safe_class_name(class_names, int(v)) for v in base_values],
            "prediction": pred_values,
            "rule_class": [safe_class_name(class_names, int(v)) if int(v) >= 0 else "" for v in pred_values],
            "mode": pred["mode"].astype(str).to_numpy(),
            "abstained": bool_series(pred["abstained"]).to_numpy(dtype=bool),
            "conflict": bool_series(pred["conflict"]).to_numpy(dtype=bool),
            "activated_rules": pred["activated_rules"].astype(str).to_numpy(),
            "n_activated": pd.to_numeric(pred["n_activated"], errors="coerce").fillna(0).astype(int).to_numpy(),
            "covered": covered,
            "correct_when_covered": covered & (pred_values == y),
            "faithful_to_base_when_covered": covered & (pred_values == base_values),
        }
    )
    if extra is not None and len(extra) == len(rows):
        for col in extra.columns:
            if col not in rows.columns:
                rows[col] = extra[col].to_numpy()
    return rows


def enhanced_metrics(df: pd.DataFrame) -> dict[str, float]:
    pred = pd.to_numeric(df["prediction"], errors="coerce").fillna(-1).astype(int).to_numpy()
    true = pd.to_numeric(df["true_label"], errors="coerce").astype(int).to_numpy()
    base = pd.to_numeric(df["base_prediction"], errors="coerce").astype(int).to_numpy()
    covered = bool_series(df["covered"]).to_numpy(dtype=bool)
    conflict = bool_series(df["conflict"]).to_numpy(dtype=bool)
    abstained = bool_series(df["abstained"]).to_numpy(dtype=bool)
    out = {
        "n": float(len(df)),
        "coverage": float(covered.mean()) if len(df) else math.nan,
        "abstention_rate": float(abstained.mean()) if len(df) else math.nan,
        "conflict_rate": float(conflict.mean()) if len(df) else math.nan,
        "all_object_accuracy": float((pred == true).mean()) if len(df) else math.nan,
        "all_object_fidelity_to_base": float((pred == base).mean()) if len(df) else math.nan,
        "covered_accuracy": float((pred[covered] == true[covered]).mean()) if covered.any() else math.nan,
        "covered_fidelity_to_base": float((pred[covered] == base[covered]).mean()) if covered.any() else math.nan,
    }
    return out


def bootstrap_ci_metric(
    df: pd.DataFrame,
    metric: str,
    rng: np.random.Generator,
    n_boot: int,
) -> tuple[float, float, float]:
    n = len(df)
    if n == 0:
        return math.nan, math.nan, math.nan
    point = enhanced_metrics(df)[metric]
    if n == 1:
        return point, point, point
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        vals.append(enhanced_metrics(df.iloc[idx].reset_index(drop=True))[metric])
    arr = np.asarray([v for v in vals if np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return point, math.nan, math.nan
    return point, float(np.quantile(arr, 0.025)), float(np.quantile(arr, 0.975))


def generate_object_intervals(ctx: RunContext, enhanced_paths: list[Path]) -> None:
    interval_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    metrics = [
        "coverage",
        "covered_accuracy",
        "all_object_accuracy",
        "covered_fidelity_to_base",
        "all_object_fidelity_to_base",
        "conflict_rate",
        "abstention_rate",
    ]
    for path in enhanced_paths:
        df = pd.read_csv(path)
        base_summary = {
            "artifact": rel_to(path, ctx.root),
            "dataset": str(df["dataset"].iloc[0]) if "dataset" in df.columns and len(df) else path.parent.name,
            "scope": str(df["scope"].iloc[0]) if "scope" in df.columns and len(df) else "",
            "n_objects": int(len(df)),
        }
        values = enhanced_metrics(df)
        summary_rows.append({**base_summary, **values})
        for metric in metrics:
            mean, low, high = bootstrap_ci_metric(df, metric, ctx.rng, ctx.n_boot)
            interval_rows.append(
                {
                    **base_summary,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": low,
                    "ci_high": high,
                    "n_boot": ctx.n_boot,
                    "unit": "object",
                    "note": "Object-level bootstrap computed from enhanced prediction export with true labels and base predictions.",
                }
            )
    write_csv(ctx.out / "statistics" / "object_level_metric_summary.csv", summary_rows)
    write_csv(ctx.out / "statistics" / "object_level_bootstrap_intervals.csv", interval_rows)
    if not interval_rows:
        ctx.errors.append("No object-level bootstrap interval rows were generated.")


def run_awa2_enhanced(ctx: RunContext) -> list[Path]:
    ds = load_awa2_parquet(ctx.root)
    out = ensure_dir(ctx.out / "awa2")
    runtime_log = ctx.out / "runtime" / "runtime.jsonl"
    seeds = SEED_DEFAULT[:1] if ctx.smoke else SEED_DEFAULT
    enhanced_paths: list[Path] = []
    summary_rows: list[dict[str, Any]] = []
    combined: list[pd.DataFrame] = []

    write_json_safe(out / "awa2_dataset_manifest_v3.json", {**ds.meta, "seeds": seeds, "generated_at": now_iso(), "prediction_export": "enhanced"})
    for seed in seeds:
        t0 = time.time()
        train, val, test = protocol_a_split(ds.y, seed)
        tr = fit_transition(ds.A[train], ds.A[val], ds.A[test], ds.B_obj[train], ds.B_obj[val], ds.B_obj[test], n_components=64, seed=seed)
        attrs, attr_df = select_attributes(tr, ds.attr_names, q=18)
        selected_names = [ds.attr_names[j] for j in attrs]
        min_support = max(8, min(18, int(0.002 * len(train))))
        thresholds, threshold_df, _ = fit_discretizers(tr.Yhat_train, ds.y[train], attrs, alpha=0.65, max_depth=2, min_support=max(10, min_support))
        base_pred = classifier_predictions(tr.X_train, ds.y[train], tr.X_test)
        metrics, rules, pred = evaluate_rulebook(
            tr.Yhat_train,
            tr.Yhat_test,
            ds.y[train],
            ds.y[test],
            attrs,
            selected_names,
            ds.class_names,
            thresholds,
            base_pred,
            min_confidence=0.84,
            min_support=min_support,
            fallback_max_distance=0.45,
        )
        enhanced = enhanced_prediction_df(
            dataset="AwA2",
            seed=seed,
            scope="protocol_a_closed_world_test",
            pred=pred,
            source_indices=test,
            true_labels=ds.y[test],
            class_names=ds.class_names,
            base_pred=base_pred,
        )
        path = out / f"awa2_rule_predictions_enhanced_seed{seed}.csv"
        enhanced.to_csv(path, index=False)
        enhanced_paths.append(path)
        combined.append(enhanced)
        if seed == seeds[0]:
            attr_df.head(18).to_csv(out / f"awa2_selected_attributes_seed{seed}.csv", index=False)
            rules.to_csv(out / f"awa2_rulebook_seed{seed}.csv", index=False)
            if len(threshold_df):
                threshold_df.to_csv(out / f"awa2_wedd_thresholds_seed{seed}.csv", index=False)
        summary_rows.append({"dataset": "AwA2", "seed": seed, "scope": "protocol_a_closed_world_test", **metrics, "seconds": time.time() - t0})
        append_jsonl(runtime_log, {"dataset": "AwA2", "phase": "v3_enhanced_protocol_a", "seed": seed, "seconds": time.time() - t0, "status": "ok"})
    if combined:
        combined_path = out / "awa2_rule_predictions_enhanced.csv"
        pd.concat(combined, ignore_index=True).to_csv(combined_path, index=False)
    write_csv(out / "awa2_rulebook_seedwise_v3.csv", summary_rows)
    return enhanced_paths


def normalize_sun_path(value: Any) -> str:
    text = mat_string(value) if not isinstance(value, str) else value
    text = text.replace("\\", "/")
    marker = "/images/"
    if marker in text:
        text = text.split(marker, 1)[1]
    text = re.sub(r"^images/", "", text)
    return text.strip("/")


def load_sun_official_archive(root: Path) -> tuple[dict[str, int], list[str], np.ndarray | None]:
    archive = root / "data" / "raw" / "sun" / "SUNAttributeDB.tar.gz"
    if not archive.exists():
        return {}, [], None
    with tarfile.open(archive, "r:gz") as tf:
        images_mat = loadmat(BytesIO(tf.extractfile("SUNAttributeDB/images.mat").read()), squeeze_me=True, struct_as_record=False)
        attrs_mat = loadmat(BytesIO(tf.extractfile("SUNAttributeDB/attributes.mat").read()), squeeze_me=True, struct_as_record=False)
        labels_mat = loadmat(BytesIO(tf.extractfile("SUNAttributeDB/attributeLabels_continuous.mat").read()), squeeze_me=True, struct_as_record=False)
    images = [normalize_sun_path(x) for x in np.asarray(images_mat["images"], dtype=object).ravel()]
    attr_names = [clean_name(mat_string(x)) for x in np.asarray(attrs_mat["attributes"], dtype=object).ravel()]
    labels = np.asarray(labels_mat.get("labels_cv"), dtype=float) if "labels_cv" in labels_mat else None
    return {name: idx for idx, name in enumerate(images)}, attr_names, labels


def load_sun_image_metadata(ctx: RunContext, locs: dict[str, np.ndarray], class_names: list[str]) -> pd.DataFrame:
    base = ctx.root / "data" / "raw" / "xlsa17" / "data" / "SUN"
    res = loadmat(base / "res101.mat", squeeze_me=True, struct_as_record=False)
    image_files = np.asarray(res["image_files"], dtype=object).ravel()
    labels = np.asarray(res["labels"], dtype=int).ravel() - 1
    official_map, attr_names, _ = load_sun_official_archive(ctx.root)
    split_by_idx: dict[int, list[str]] = {}
    for split, idxs in locs.items():
        for i in np.asarray(idxs, dtype=int).ravel():
            split_by_idx.setdefault(int(i), []).append(split)
    rows = []
    for idx, raw in enumerate(image_files):
        norm = normalize_sun_path(raw)
        parts = norm.split("/")
        alpha = parts[0] if len(parts) > 0 else ""
        scene_category = "/".join(parts[1:-1]) if len(parts) > 2 else ""
        scene_leaf = parts[-2] if len(parts) > 1 else ""
        rows.append(
            {
                "source_row_index": idx,
                "normalized_image_path": norm,
                "alpha_bucket": alpha,
                "scene_category": scene_category,
                "scene_leaf": scene_leaf,
                "filename": parts[-1] if parts else "",
                "true_label": int(labels[idx]),
                "true_class": safe_class_name(class_names, int(labels[idx])),
                "split_membership": ";".join(sorted(split_by_idx.get(idx, []))),
                "official_attribute_row": official_map.get(norm, -1),
                "official_attribute_match": norm in official_map,
                "n_official_attributes": len(attr_names),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(ctx.out / "sun" / "sun_image_metadata.csv", index=False)
    category = (
        df.groupby(["alpha_bucket", "scene_category", "scene_leaf"], dropna=False)
        .agg(
            n_images=("source_row_index", "size"),
            n_classes=("true_label", "nunique"),
            official_attribute_matches=("official_attribute_match", "sum"),
            train_count=("split_membership", lambda s: int(s.astype(str).str.contains("train_loc").sum())),
            val_count=("split_membership", lambda s: int(s.astype(str).str.contains("val_loc").sum())),
            test_seen_count=("split_membership", lambda s: int(s.astype(str).str.contains("test_seen_loc").sum())),
            test_unseen_count=("split_membership", lambda s: int(s.astype(str).str.contains("test_unseen_loc").sum())),
        )
        .reset_index()
    )
    category.to_csv(ctx.out / "sun" / "sun_category_metadata.csv", index=False)
    return df


def run_sun_enhanced(ctx: RunContext) -> list[Path]:
    ds, locs = load_xlsa_mat_dataset(ctx.root, "SUN")
    out = ensure_dir(ctx.out / "sun")
    runtime_log = ctx.out / "runtime" / "runtime.jsonl"
    seed = 42
    t0 = time.time()
    image_meta = load_sun_image_metadata(ctx, locs, ds.class_names)
    train, val, seen = locs["train_loc"], locs["val_loc"], locs["test_seen_loc"]
    tr = fit_transition(ds.A[train], ds.A[val], ds.A[seen], ds.B_obj[train], ds.B_obj[val], ds.B_obj[seen], n_components=64 if not ctx.smoke else 32, seed=seed)
    attrs, attr_df = select_attributes(tr, ds.attr_names, q=18)
    selected_names = [ds.attr_names[j] for j in attrs]
    thresholds, threshold_df, _ = fit_discretizers(tr.Yhat_train, ds.y[train], attrs, alpha=0.65, max_depth=2, min_support=5)
    base_pred = classifier_predictions(tr.X_train, ds.y[train], tr.X_test)
    metrics, rules, pred = evaluate_rulebook(
        tr.Yhat_train,
        tr.Yhat_test,
        ds.y[train],
        ds.y[seen],
        attrs,
        selected_names,
        ds.class_names,
        thresholds,
        base_pred,
        min_confidence=0.60,
        min_support=5,
        fallback_max_distance=0.50,
        max_rules_per_class=2,
    )
    extra = image_meta.set_index("source_row_index").loc[seen].reset_index(drop=False)
    enhanced = enhanced_prediction_df(
        dataset="SUN",
        seed=seed,
        scope="closed_world_seen_test",
        pred=pred,
        source_indices=seen,
        true_labels=ds.y[seen],
        class_names=ds.class_names,
        base_pred=base_pred,
        extra=extra,
    )
    pred_path = out / "sun_rule_predictions_enhanced.csv"
    enhanced.to_csv(pred_path, index=False)
    attr_df.head(18).to_csv(out / "sun_selected_attributes_v3.csv", index=False)
    rules.to_csv(out / "sun_rulebook_v3.csv", index=False)
    if len(threshold_df):
        threshold_df.to_csv(out / "sun_wedd_thresholds_v3.csv", index=False)
    write_csv(out / "sun_rulebook_seedwise_v3.csv", [{"dataset": "SUN", "seed": seed, "scope": "closed_world_seen_test", **metrics, "seconds": time.time() - t0}])

    diag_rows = []
    for category, g in enhanced.groupby("scene_category", dropna=False):
        vals = enhanced_metrics(g)
        diag_rows.append(
            {
                "scene_category": category,
                "scene_leaf_examples": ";".join(sorted(g["scene_leaf"].dropna().astype(str).unique())[:5]),
                "n_objects": int(len(g)),
                "n_classes": int(g["true_label"].nunique()),
                **vals,
            }
        )
    diag = pd.DataFrame(diag_rows).sort_values(["coverage", "conflict_rate"], ascending=[True, False])
    diag.to_csv(out / "sun_category_diagnostics_v3.csv", index=False)
    write_sun_review(out / "sun_low_coverage_high_conflict_review.md", diag)
    write_json_safe(
        out / "sun_metadata_manifest_v3.json",
        {
            "generated_at": now_iso(),
            "source": str(ctx.root / "data" / "raw" / "xlsa17" / "data" / "SUN"),
            "official_sun_archive": str(ctx.root / "data" / "raw" / "sun" / "SUNAttributeDB.tar.gz"),
            "n_images": int(len(image_meta)),
            "n_official_attribute_matches": int(image_meta["official_attribute_match"].sum()),
            "n_unmatched_official_attribute_rows": int((~image_meta["official_attribute_match"]).sum()),
            "n_seen_prediction_rows": int(len(enhanced)),
            "category_diagnostic_rows": int(len(diag)),
        },
    )
    append_jsonl(runtime_log, {"dataset": "SUN", "phase": "v3_enhanced_seen_test", "seed": seed, "seconds": time.time() - t0, "status": "ok"})
    return [pred_path]


def write_sun_review(path: Path, diag: pd.DataFrame) -> None:
    lines = [
        "# SUN Low-Coverage and High-Conflict Review",
        "",
        "Scope: v3 groups existing SUN seen-test predictions by normalized SUN image hierarchy categories. This remains a portability stress test, not a competitive scene-recognition claim.",
        "",
    ]
    if diag.empty:
        lines.append("No category diagnostics were generated.")
    else:
        lines.append(f"Categories summarized: {len(diag)}.")
        lines.append(f"Mean category coverage: {diag['coverage'].mean():.4f}.")
        lines.append(f"Mean category covered fidelity to base: {diag['covered_fidelity_to_base'].mean():.4f}.")
        lines.extend(["", "## Lowest Coverage Categories", ""])
        for _, row in diag.sort_values(["coverage", "n_objects"], ascending=[True, False]).head(12).iterrows():
            lines.append(f"- {row['scene_category']} (n={int(row['n_objects'])}): coverage={row['coverage']:.4f}, conflict={row['conflict_rate']:.4f}")
        lines.extend(["", "## Highest Conflict Categories", ""])
        for _, row in diag.sort_values(["conflict_rate", "n_objects"], ascending=[False, False]).head(12).iterrows():
            lines.append(f"- {row['scene_category']} (n={int(row['n_objects'])}): conflict={row['conflict_rate']:.4f}, coverage={row['coverage']:.4f}")
        lines.extend(["", "These diagnostics should be inspected before strengthening any SUN portability claim."])
    write_markdown(path, lines)


def resolve_derm_image(base: Path, value: Any) -> Path:
    return base / "images" / str(value).replace("\\", "/")


def extract_derm_resnet_features(ctx: RunContext) -> Path:
    out = ensure_dir(ctx.out / "derm7pt")
    feature_path = out / "derm7pt_resnet50_imagenet1k_v2_features.parquet"
    manifest_path = out / "derm7pt_encoder_manifest.json"
    if feature_path.exists() and manifest_path.exists() and not ctx.force_rebuild:
        return feature_path
    base = ctx.root / "data" / "raw" / "Derm7pt"
    meta = pd.read_csv(base / "meta" / "meta.csv")
    try:
        import torch
        from torchvision import models
    except Exception as exc:
        raise RuntimeError(f"torch/torchvision are required for v3 Derm7pt encoder. Run scripts/semtra_revision.ps1 setup-vision. Import error: {exc}") from exc

    torch.manual_seed(42)
    if ctx.derm_device == "auto":
        device_name = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device_name = ctx.derm_device
    if device_name == "cuda" and not torch.cuda.is_available():
        ctx.warnings.append("CUDA requested for Derm7pt encoder but unavailable; using CPU.")
        device_name = "cpu"
    device = torch.device(device_name)
    weights = models.ResNet50_Weights.IMAGENET1K_V2
    model = models.resnet50(weights=weights)
    encoder = torch.nn.Sequential(*list(model.children())[:-1]).to(device).eval()
    transform = weights.transforms()

    features: list[np.ndarray] = []
    missing: list[int] = []
    batch_tensors = []
    batch_indices = []
    t0 = time.time()
    with torch.no_grad():
        for idx, row in meta.iterrows():
            image_path = resolve_derm_image(base, row["derm"])
            if not image_path.exists():
                missing.append(int(idx))
                features.append(np.zeros(2048, dtype=np.float32))
                continue
            with Image.open(image_path) as img:
                tensor = transform(img.convert("RGB"))
            batch_tensors.append(tensor)
            batch_indices.append(int(idx))
            if len(batch_tensors) >= ctx.derm_batch_size:
                batch = torch.stack(batch_tensors).to(device)
                out_batch = encoder(batch).flatten(1).cpu().numpy().astype(np.float32)
                for pos, feat in zip(batch_indices, out_batch):
                    while len(features) < pos:
                        features.append(np.zeros(2048, dtype=np.float32))
                    features.append(feat)
                batch_tensors = []
                batch_indices = []
        if batch_tensors:
            batch = torch.stack(batch_tensors).to(device)
            out_batch = encoder(batch).flatten(1).cpu().numpy().astype(np.float32)
            for pos, feat in zip(batch_indices, out_batch):
                while len(features) < pos:
                    features.append(np.zeros(2048, dtype=np.float32))
                features.append(feat)
    while len(features) < len(meta):
        features.append(np.zeros(2048, dtype=np.float32))
    mat = np.vstack(features).astype(np.float32)
    cols = [f"feature_{i:04d}" for i in range(mat.shape[1])]
    df = pd.DataFrame(mat, columns=cols)
    df.insert(0, "case_index", np.arange(len(df), dtype=int))
    df.to_parquet(feature_path, index=False)
    write_json_safe(
        out / "derm7pt_encoder_manifest.json",
        {
            "generated_at": now_iso(),
            "encoder": "torchvision.models.resnet50",
            "weights": "ResNet50_Weights.IMAGENET1K_V2",
            "image_column": "derm",
            "image_modality": "dermoscopic",
            "feature_dim": int(mat.shape[1]),
            "n_cases": int(mat.shape[0]),
            "missing_image_indices": missing,
            "device": device_name,
            "batch_size": int(ctx.derm_batch_size),
            "seconds": float(time.time() - t0),
            "torch_version": getattr(torch, "__version__", "unknown"),
            "torchvision_version": importlib_metadata.version("torchvision"),
            "feature_file": str(feature_path),
            "feature_sha256": sha256_file(feature_path),
            "clinical_scope": "retrospective technical validation only; ImageNet encoder is not a clinical dermatology model",
        },
    )
    return feature_path


def load_derm7pt_resnet_dataset(ctx: RunContext, feature_path: Path):
    from run_revision_v1 import SemanticDataset

    base = ctx.root / "data" / "raw" / "Derm7pt"
    meta = pd.read_csv(base / "meta" / "meta.csv")
    feat = pd.read_parquet(feature_path)
    feature_cols = [c for c in feat.columns if c.startswith("feature_")]
    A = feat[feature_cols].to_numpy(dtype=np.float32)
    concept_cols = [
        "pigment_network",
        "streaks",
        "pigmentation",
        "regression_structures",
        "dots_and_globules",
        "blue_whitish_veil",
        "vascular_structures",
    ]
    concept_data = []
    concept_maps: dict[str, dict[str, int]] = {}
    for col in concept_cols:
        s = meta[col].fillna("missing").astype(str)
        values = sorted(s.unique().tolist())
        mapping = {v: i for i, v in enumerate(values)}
        concept_maps[col] = mapping
        encoded = s.map(mapping).astype(float).to_numpy()
        denom = max(1.0, float(len(values) - 1))
        concept_data.append(encoded / denom)
    B_obj = np.vstack(concept_data).T.astype(float)
    grouped = meta["diagnosis"].map(group_derm_diagnosis)
    classes = sorted(grouped.unique().tolist())
    class_to_idx = {c: i for i, c in enumerate(classes)}
    y = grouped.map(class_to_idx).astype(int).to_numpy()
    locs = {}
    for split, fname in [("train", "train_indexes.csv"), ("val", "valid_indexes.csv"), ("test", "test_indexes.csv")]:
        locs[split] = pd.read_csv(base / "meta" / fname)["indexes"].to_numpy(dtype=int)
    manifest = {
        "source": str(base),
        "n_cases": int(len(meta)),
        "feature_source": "TorchVision ResNet50_Weights.IMAGENET1K_V2 on dermoscopic images",
        "feature_file": str(feature_path),
        "feature_dim": int(A.shape[1]),
        "image_column": "derm",
        "image_modality": "dermoscopic",
        "diagnosis_grouping": "melanoma variants collapsed to melanoma; nevus variants collapsed to nevus; infrequent diagnoses grouped as other unless named major category",
        "n_grouped_diagnosis_classes": int(len(classes)),
        "concept_columns": concept_cols,
        "concept_encoding": "categorical values encoded on full metadata and scaled to [0,1]; missing values encoded as an explicit category",
        "official_split_sizes": {k: int(len(v)) for k, v in locs.items()},
        "concept_maps": concept_maps,
        "claim_scope": "retrospective technical validation only",
    }
    return SemanticDataset("Derm7pt", A, y, None, B_obj, classes, concept_cols, manifest), locs, meta


def run_derm7pt_resnet(ctx: RunContext) -> list[Path]:
    out = ensure_dir(ctx.out / "derm7pt")
    runtime_log = ctx.out / "runtime" / "runtime.jsonl"
    t0 = time.time()
    feature_path = extract_derm_resnet_features(ctx)
    ds, locs, meta = load_derm7pt_resnet_dataset(ctx, feature_path)
    write_json_safe(out / "derm7pt_dataset_manifest_v3.json", {**ds.meta, "generated_at": now_iso()})
    train, val, test = locs["train"], locs["val"], locs["test"]
    tr = fit_transition(ds.A[train], ds.A[val], ds.A[test], ds.B_obj[train], ds.B_obj[val], ds.B_obj[test], n_components=min(64, ds.A.shape[1] - 1), seed=42)
    attrs = list(range(ds.B_obj.shape[1]))
    thresholds, threshold_df, _ = fit_discretizers(tr.Yhat_train, ds.y[train], attrs, alpha=0.65, max_depth=2, min_support=5)
    base_pred = classifier_predictions(tr.X_train, ds.y[train], tr.X_test)
    metrics, rules, pred = evaluate_rulebook(
        tr.Yhat_train,
        tr.Yhat_test,
        ds.y[train],
        ds.y[test],
        attrs,
        ds.attr_names,
        ds.class_names,
        thresholds,
        base_pred,
        min_confidence=0.60,
        min_support=5,
        fallback_max_distance=0.50,
        max_rules_per_class=4,
    )
    test_meta = meta.iloc[test].reset_index(drop=True)
    extra = pd.DataFrame(
        {
            "diagnosis": test_meta["diagnosis"].astype(str),
            "grouped_diagnosis": test_meta["diagnosis"].map(group_derm_diagnosis).astype(str),
            "derm_image": test_meta["derm"].astype(str),
            "clinic_image": test_meta["clinic"].astype(str),
            "seven_point_score": pd.to_numeric(test_meta["seven_point_score"], errors="coerce"),
        }
    )
    for col in ds.attr_names:
        extra[col] = test_meta[col].fillna("missing").astype(str).to_numpy()
    enhanced = enhanced_prediction_df(
        dataset="Derm7pt",
        seed=42,
        scope="resnet50_imagenet1k_v2_official_test_split",
        pred=pred,
        source_indices=test,
        true_labels=ds.y[test],
        class_names=ds.class_names,
        base_pred=base_pred,
        extra=extra,
    )
    pred_path = out / "derm7pt_rule_predictions_enhanced.csv"
    enhanced.to_csv(pred_path, index=False)
    rules.to_csv(out / "derm7pt_rulebook_v3.csv", index=False)
    if len(threshold_df):
        threshold_df.to_csv(out / "derm7pt_wedd_thresholds_v3.csv", index=False)
    row = {
        "dataset": "Derm7pt",
        "seed": 42,
        "scope": "resnet50_imagenet1k_v2_official_test_split",
        "test_mae": float(np.mean(np.abs(tr.Yhat_test - tr.Y_test))),
        "test_rmse": float(np.sqrt(np.mean((tr.Yhat_test - tr.Y_test) ** 2))),
        **metrics,
        "seconds": float(time.time() - t0),
    }
    write_csv(out / "derm7pt_rulebook_seedwise_v3.csv", [row])
    concept_rows = []
    for j, name in enumerate(ds.attr_names):
        concept_rows.append(
            {
                "concept": name,
                "n_encoded_categories": int(len(ds.meta["concept_maps"].get(name, {}))),
                "missing_value_category_present": bool("missing" in ds.meta["concept_maps"].get(name, {})),
                "test_mae": float(np.mean(np.abs(tr.Yhat_test[:, j] - tr.Y_test[:, j]))),
                "test_rmse": float(np.sqrt(np.mean((tr.Yhat_test[:, j] - tr.Y_test[:, j]) ** 2))),
            }
        )
    write_csv(out / "derm7pt_concept_transition_diagnostics_v3.csv", concept_rows)
    write_derm_diagnostics(ctx, enhanced)
    append_jsonl(runtime_log, {"dataset": "Derm7pt", "phase": "v3_resnet50_rulebook", "seed": 42, "seconds": time.time() - t0, "status": "ok"})
    return [pred_path]


def write_derm_diagnostics(ctx: RunContext, enhanced: pd.DataFrame) -> None:
    out = ensure_dir(ctx.out / "derm7pt")
    diag_rows = []
    for group, g in enhanced.groupby("grouped_diagnosis", dropna=False):
        diag_rows.append({"group": group, "n_cases": int(len(g)), **enhanced_metrics(g)})
    pd.DataFrame(diag_rows).sort_values("group").to_csv(out / "derm7pt_diagnosis_diagnostics_v3.csv", index=False)
    concept_rows = []
    concept_cols = [
        "pigment_network",
        "streaks",
        "pigmentation",
        "regression_structures",
        "dots_and_globules",
        "blue_whitish_veil",
        "vascular_structures",
    ]
    for concept in concept_cols:
        for value, g in enhanced.groupby(concept, dropna=False):
            concept_rows.append({"concept": concept, "concept_value": value, "group": f"{concept}={value}", "n_cases": int(len(g)), **enhanced_metrics(g)})
    pd.DataFrame(concept_rows).to_csv(out / "derm7pt_concept_diagnostics_v3.csv", index=False)
    lines = [
        "# Derm7pt v3 Limitations",
        "",
        "Derm7pt v3 replaces the handcrafted color/histogram baseline with a locked TorchVision ResNet-50 ImageNet-1K v2 encoder applied to dermoscopic images.",
        "",
        "The encoder is not dermatology-specific and is not a clinical diagnostic model. Results remain retrospective technical-validation outputs using the official case-level train/validation/test splits.",
        "",
        "Clinical validation, prospective evaluation, calibration, subgroup fairness, and reader-study comparisons remain out of scope.",
    ]
    write_markdown(out / "derm7pt_limitations_v3.md", lines)


def write_latex_tables(ctx: RunContext) -> None:
    table_dir = ensure_dir(ctx.out / "tables")
    intervals = pd.read_csv(ctx.out / "statistics" / "object_level_bootstrap_intervals.csv")
    keep = intervals[intervals["metric"].isin(["coverage", "covered_accuracy", "covered_fidelity_to_base"])].copy()
    rows = []
    for _, row in keep.iterrows():
        rows.append([row["dataset"], row["metric"].replace("_", " "), fmt_num(row["mean"]), f"[{fmt_num(row['ci_low'])}, {fmt_num(row['ci_high'])}]", int(row["n_objects"])])
    latex_table(table_dir / "table_v3_object_level_intervals.tex", "Revision v3 object-level bootstrap intervals from enhanced prediction exports.", "tab:v3_object_intervals", ["Dataset", "Metric", "Mean", "95\\% CI", "Objects"], rows, spec="llccr")

    sun_diag = pd.read_csv(ctx.out / "sun" / "sun_category_diagnostics_v3.csv")
    sun_rows = []
    for _, row in sun_diag.sort_values(["coverage", "n_objects"], ascending=[True, False]).head(6).iterrows():
        sun_rows.append([tex_escape(row["scene_category"]), int(row["n_objects"]), fmt_num(row["coverage"]), fmt_num(row["conflict_rate"]), fmt_num(row["covered_fidelity_to_base"])])
    latex_table(table_dir / "table_sun_v3_category_diagnostics.tex", "SUN v3 low-coverage category diagnostics.", "tab:sun_v3_category_diagnostics", ["Category", "Objects", "Coverage", "Conflict", "Covered fidelity"], sun_rows, spec="lrccc")

    derm = pd.read_csv(ctx.out / "derm7pt" / "derm7pt_rulebook_seedwise_v3.csv").iloc[0]
    derm_manifest = read_json(ctx.out / "derm7pt" / "derm7pt_encoder_manifest.json")
    derm_rows = [
        ["Encoder", "TorchVision ResNet-50 ImageNet-1K v2"],
        ["Feature dimension", int(derm_manifest["feature_dim"])],
        ["Test concept MAE", fmt_num(derm["test_mae"])],
        ["Coverage", fmt_num(derm["coverage"])],
        ["Covered accuracy", fmt_num(derm["covered_accuracy"])],
        ["Covered fidelity", fmt_num(derm["covered_fidelity_to_base"])],
    ]
    latex_table(table_dir / "table_derm7pt_v3_resnet_summary.tex", "Derm7pt v3 retrospective technical-validation summary with locked ResNet-50 features.", "tab:derm7pt_v3_resnet_summary", ["Metric", "Value"], derm_rows, spec="lc")


def write_statistical_assessment(ctx: RunContext) -> None:
    intervals = pd.read_csv(ctx.out / "statistics" / "object_level_bootstrap_intervals.csv")
    summary = pd.read_csv(ctx.out / "statistics" / "object_level_metric_summary.csv")
    lines = [
        "# Revision v3 Object-Level Statistical Assessment",
        "",
        "Revision v3 exports true labels and base-model predictions with every rule prediction, allowing object-level accuracy and fidelity intervals to be computed directly.",
        "",
        f"Enhanced prediction artifacts summarized: {len(summary)}.",
        f"Object-level bootstrap interval rows: {len(intervals)}.",
        "",
        "Intervals are nonparametric object-level bootstraps over the exported prediction rows. Covered accuracy and covered fidelity are computed only over non-abstained rows in each resample.",
        "",
        "The intervals quantify audit stability for the generated exports and do not convert Derm7pt into clinical validation or SUN into a competitive scene-recognition benchmark.",
    ]
    write_markdown(ctx.out / "statistics" / "object_level_statistical_assessment.md", lines)


def write_schemas(ctx: RunContext) -> None:
    schemas = {
        "enhanced_prediction.schema.json": {"format": "csv", "required_columns": REQUIRED_ENHANCED_COLUMNS},
        "object_level_bootstrap.schema.json": {"format": "csv", "required_columns": ["dataset", "artifact", "metric", "mean", "ci_low", "ci_high", "n_boot", "unit"]},
        "sun_metadata.schema.json": {"format": "csv", "required_columns": ["source_row_index", "normalized_image_path", "scene_category", "official_attribute_match"]},
        "derm_encoder_manifest.schema.json": {"format": "json", "required_keys": ["encoder", "weights", "feature_dim", "n_cases", "feature_sha256"]},
        "submission_bundle_manifest.schema.json": {"format": "json", "required_keys": ["generated_at", "bundle_root", "files", "raw_private_data_excluded"]},
    }
    for name, schema in schemas.items():
        write_json_safe(ctx.out / "schemas" / name, {"semtra_revision": V3_VERSION, **schema})


def validate_csv_columns(path: Path, required: list[str]) -> tuple[str, str]:
    if not path.exists():
        return "fail", "missing file"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    missing = [col for col in required if col not in header]
    return ("pass", "") if not missing else ("fail", ",".join(missing))


def validate_json_keys(path: Path, required: list[str]) -> tuple[str, str]:
    if not path.exists():
        return "fail", "missing file"
    obj = read_json(path)
    missing = [key for key in required if key not in obj]
    return ("pass", "") if not missing else ("fail", ",".join(missing))


def validate_v3_outputs(ctx: RunContext) -> list[dict[str, Any]]:
    rows = []
    checks = [
        (ctx.out / "awa2" / "awa2_rule_predictions_enhanced_seed42.csv", REQUIRED_ENHANCED_COLUMNS, "enhanced_prediction"),
        (ctx.out / "sun" / "sun_rule_predictions_enhanced.csv", REQUIRED_ENHANCED_COLUMNS, "enhanced_prediction"),
        (ctx.out / "derm7pt" / "derm7pt_rule_predictions_enhanced.csv", REQUIRED_ENHANCED_COLUMNS, "enhanced_prediction"),
        (ctx.out / "statistics" / "object_level_bootstrap_intervals.csv", ["dataset", "artifact", "metric", "mean", "ci_low", "ci_high"], "object_level_bootstrap"),
        (ctx.out / "statistics" / "object_level_metric_summary.csv", ["dataset", "artifact", "covered_accuracy", "covered_fidelity_to_base"], "object_level_metric_summary"),
        (ctx.out / "sun" / "sun_image_metadata.csv", ["source_row_index", "normalized_image_path", "scene_category", "official_attribute_match"], "sun_metadata"),
        (ctx.out / "sun" / "sun_category_diagnostics_v3.csv", ["scene_category", "n_objects", "coverage", "covered_fidelity_to_base"], "sun_category_diagnostics"),
        (ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics_v3.csv", ["group", "n_cases", "covered_accuracy", "covered_fidelity_to_base"], "derm_diagnosis_diagnostics"),
    ]
    for path, required, family in checks:
        status, detail = validate_csv_columns(path, required)
        rows.append({"family": family, "artifact": rel_to(path, ctx.root), "status": status, "detail": detail})
        if status != "pass":
            ctx.errors.append(f"V3 validation failed for {rel_to(path, ctx.root)}: {detail}")
    status, detail = validate_json_keys(ctx.out / "derm7pt" / "derm7pt_encoder_manifest.json", ["encoder", "weights", "feature_dim", "n_cases", "feature_sha256"])
    rows.append({"family": "derm_encoder_manifest", "artifact": "outputs/revision_v3/derm7pt/derm7pt_encoder_manifest.json", "status": status, "detail": detail})
    if status != "pass":
        ctx.errors.append(f"Derm7pt encoder manifest validation failed: {detail}")
    write_csv(ctx.out / "qc" / "schema_validation.csv", rows)
    return rows


def sync_latex_artifacts(ctx: RunContext) -> None:
    latex_dir = ensure_dir(ctx.out / "latex")
    records = []
    for stem in ["main", "supply"]:
        for ext in [".pdf", ".log", ".aux", ".bbl", ".blg", ".out", ".toc"]:
            src = ctx.manuscript / f"{stem}{ext}"
            fallback = ctx.v2 / "latex" / f"{stem}{ext}"
            chosen = src
            source = "manuscript_build"
            if (not chosen.exists()) or chosen.stat().st_size == 0:
                chosen = fallback
                source = "revision_v2_latex_archive"
            if chosen.exists():
                copy_if_exists(chosen, latex_dir / f"{stem}{ext}")
                records.append({"artifact": f"{stem}{ext}", "source": source, "source_path": str(chosen), "size": chosen.stat().st_size, "sha256": sha256_file(chosen)})
    write_json_safe(latex_dir / "latex_artifact_sources.json", {"generated_at": now_iso(), "records": records})


def write_submission_bundle(ctx: RunContext) -> None:
    bundle = ctx.out / "submission_bundle"
    if bundle.exists():
        shutil.rmtree(bundle)
    ensure_dir(bundle)
    files: list[dict[str, Any]] = []
    for name in ["main.tex", "supply.tex", "references.bib"]:
        copy_if_exists(ctx.manuscript / name, bundle / "manuscript" / name, files, "manuscript_source")
    for table in sorted((ctx.v1 / "tables").glob("*.tex")) if (ctx.v1 / "tables").exists() else []:
        copy_if_exists(table, bundle / "outputs" / "revision_v1" / "tables" / table.name, files, "generated_table_v1")
    for table in sorted((ctx.out / "tables").glob("*.tex")):
        copy_if_exists(table, bundle / "outputs" / "revision_v3" / "tables" / table.name, files, "generated_table_v3")
    for stem in ["main", "supply"]:
        for ext in [".pdf", ".log", ".bbl", ".blg"]:
            copy_if_exists(ctx.out / "latex" / f"{stem}{ext}", bundle / "latex" / f"{stem}{ext}", files, "latex_output")
    for rel in ["manifest_revision_v3.json", "artifact_index_revision_v3.csv"]:
        copy_if_exists(ctx.out / rel, bundle / "outputs" / "revision_v3" / rel, files, "v3_index")
    copy_referenced_figures(ctx, bundle, files)
    manifest = {
        "generated_at": now_iso(),
        "bundle_root": str(bundle),
        "raw_private_data_excluded": True,
        "downloaded_model_weights_excluded": True,
        "files": files,
        "required_present": {
            "main_tex": (bundle / "manuscript" / "main.tex").exists(),
            "supply_tex": (bundle / "manuscript" / "supply.tex").exists(),
            "references_bib": (bundle / "manuscript" / "references.bib").exists(),
            "main_pdf": (bundle / "latex" / "main.pdf").exists(),
            "supply_pdf": (bundle / "latex" / "supply.pdf").exists(),
            "v3_tables": len(list((bundle / "outputs" / "revision_v3" / "tables").glob("*.tex"))) if (bundle / "outputs" / "revision_v3" / "tables").exists() else 0,
        },
    }
    write_json_safe(bundle / "manifest.json", manifest)
    missing = [k for k, v in manifest["required_present"].items() if v in [False, 0]]
    if missing:
        ctx.errors.append(f"Submission bundle missing required entries: {', '.join(missing)}")


def write_qc(ctx: RunContext) -> None:
    tex_paths = [ctx.manuscript / "main.tex", ctx.manuscript / "supply.tex"]
    no_paragraph = [p.name for p in tex_paths if p.exists() and r"\paragraph{" in read_text(p)]
    dupes = duplicate_labels(tex_paths)
    missing_bib = missing_bib_keys(tex_paths, ctx.manuscript / "references.bib")
    log_issues = {stem: latex_log_issues(ctx.out / "latex" / f"{stem}.log") for stem in ["main", "supply"]}
    main_text = read_text(ctx.manuscript / "main.tex") if (ctx.manuscript / "main.tex").exists() else ""
    supply_text = read_text(ctx.manuscript / "supply.tex") if (ctx.manuscript / "supply.tex").exists() else ""
    claim_failures = []
    if "retrospective technical validation" not in (main_text + supply_text).lower():
        claim_failures.append("missing Derm7pt retrospective technical-validation wording")
    if "clinical deployment evidence" not in (main_text + supply_text).lower() and "clinical readiness evidence" not in (main_text + supply_text).lower():
        claim_failures.append("missing no-clinical-claim wording")
    for issue in no_paragraph:
        ctx.errors.append(f"Forbidden \\paragraph{{}} found in {issue}")
    if dupes:
        ctx.errors.append(f"Duplicate labels found: {', '.join(dupes)}")
    if missing_bib:
        ctx.errors.append(f"Missing BibTeX keys: {', '.join(missing_bib)}")
    for stem, issues in log_issues.items():
        if issues:
            ctx.errors.append(f"LaTeX log issues for {stem}: {', '.join(issues)}")
    for failure in claim_failures:
        ctx.errors.append(f"Claim discipline check failed: {failure}")
    checklist = [
        {"check": "no_paragraph", "status": "pass" if not no_paragraph else "fail", "detail": ",".join(no_paragraph)},
        {"check": "duplicate_labels", "status": "pass" if not dupes else "fail", "detail": ",".join(dupes)},
        {"check": "missing_bib_keys", "status": "pass" if not missing_bib else "fail", "detail": ",".join(missing_bib)},
        {"check": "latex_main_log", "status": "pass" if not log_issues["main"] else "fail", "detail": ",".join(log_issues["main"])},
        {"check": "latex_supply_log", "status": "pass" if not log_issues["supply"] else "fail", "detail": ",".join(log_issues["supply"])},
        {"check": "claim_discipline", "status": "pass" if not claim_failures else "fail", "detail": "; ".join(claim_failures)},
        {"check": "submission_bundle", "status": "pass" if (ctx.out / "submission_bundle" / "manifest.json").exists() else "fail", "detail": ""},
    ]
    write_csv(ctx.out / "qc" / "qc_checklist.csv", checklist)
    write_json_safe(ctx.out / "qc" / "qc_summary.json", {"generated_at": now_iso(), "status": "pass" if not ctx.errors else "fail", "errors": ctx.errors, "warnings": ctx.warnings, "latex_log_issues": log_issues})


def write_manifest(ctx: RunContext) -> None:
    artifacts = []
    for path in sorted(ctx.out.rglob("*")):
        if path.is_file() and path.name != "manifest_revision_v3.json":
            artifacts.append({"path": rel_to(path, ctx.root), "size": path.stat().st_size, "sha256": sha256_file(path)})
    manifest = {
        "generated_at": now_iso(),
        "semtra_revision": V3_VERSION,
        "status": "pass" if not ctx.errors else "fail",
        "v1_root": rel_to(ctx.v1, ctx.root),
        "v2_root": rel_to(ctx.v2, ctx.root),
        "v3_root": rel_to(ctx.out, ctx.root),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "package_versions": package_versions_v3(),
        "git_status": run_capture(["git", "status", "--short"], cwd=ctx.root),
        "errors": ctx.errors,
        "warnings": ctx.warnings,
        "claim_gating": {
            "derm7pt": "retrospective technical validation only; ResNet-50 ImageNet encoder is not clinical validation",
            "sun": "category diagnostics for portability stress testing",
            "prediction_exports": "true labels and base predictions included for object-level accuracy/fidelity intervals",
        },
    }
    write_json_safe(ctx.out / "manifest_revision_v3.json", manifest)
    write_csv(ctx.out / "artifact_index_revision_v3.csv", [{"path": a["path"], "size": a["size"], "sha256": a["sha256"]} for a in artifacts])


def write_report(ctx: RunContext) -> None:
    manifest = read_json(ctx.out / "manifest_revision_v3.json") if (ctx.out / "manifest_revision_v3.json").exists() else {}
    summary = pd.read_csv(ctx.out / "statistics" / "object_level_metric_summary.csv") if (ctx.out / "statistics" / "object_level_metric_summary.csv").exists() else pd.DataFrame()
    sun_diag = pd.read_csv(ctx.out / "sun" / "sun_category_diagnostics_v3.csv") if (ctx.out / "sun" / "sun_category_diagnostics_v3.csv").exists() else pd.DataFrame()
    derm_diag = pd.read_csv(ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics_v3.csv") if (ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics_v3.csv").exists() else pd.DataFrame()
    lines = [
        "# SEMTRA Revision v3 Report",
        "",
        f"Generated: {now_iso()}",
        "",
        "## Completed Work",
        "",
        "- Created `outputs/revision_v3/` without rewriting v1 or v2 artifacts.",
        "- Exported enhanced prediction CSVs with true labels, base predictions, rule predictions, correctness flags, and fidelity flags.",
        "- Generated object-level bootstrap intervals directly from enhanced prediction exports.",
        "- Added SUN image hierarchy/category metadata from xlsa17 image paths joined to the official SUN Attribute Database image list.",
        "- Replaced the Derm7pt handcrafted feature baseline with locked TorchVision ResNet-50 ImageNet-1K v2 dermoscopic-image features.",
        "- Created v3 schemas, QC outputs, tables, LaTeX archive sync, and a submission bundle.",
        "",
        "## Artifact Summary",
        "",
        f"- v3 artifact count: {manifest.get('artifact_count', 'unknown')}.",
        f"- Enhanced prediction summaries: {len(summary)}.",
        f"- SUN category diagnostic rows: {len(sun_diag)}.",
        f"- Derm7pt diagnosis diagnostic rows: {len(derm_diag)}.",
        "",
        "## QC Status",
        "",
        f"- Overall status: {manifest.get('status', 'unknown')}.",
        "- Errors: " + ("none recorded." if not ctx.errors else "; ".join(ctx.errors)),
        "- Warnings: " + ("none recorded." if not ctx.warnings else "; ".join(ctx.warnings)),
        "",
        "## Remaining Limitations",
        "",
        "- Derm7pt remains retrospective technical validation only; the ResNet-50 ImageNet encoder is locked and reproducible but not dermatology-specific clinical validation.",
        "- SUN category diagnostics expose hierarchy-dependent weakness and should be inspected before strengthening portability claims.",
        "- Object-level intervals depend on the generated prediction exports and do not replace external validation.",
        "",
        "## Recommendations",
        "",
        "- Keep enhanced prediction exports as the default format for future SEMTRA runs.",
        "- Add a documented dermoscopy-specific encoder only if its checkpoint, preprocessing, license, and provenance are fully traceable.",
        "- Use the SUN category diagnostics to guide targeted stress tests rather than broadening claims.",
    ]
    write_markdown(ctx.root / "revision_report_v3.md", lines)


def validate_existing(root: Path, out: Path) -> int:
    required = [
        "manifest_revision_v3.json",
        "artifact_index_revision_v3.csv",
        "awa2/awa2_rule_predictions_enhanced_seed42.csv",
        "sun/sun_rule_predictions_enhanced.csv",
        "derm7pt/derm7pt_rule_predictions_enhanced.csv",
        "derm7pt/derm7pt_resnet50_imagenet1k_v2_features.parquet",
        "derm7pt/derm7pt_encoder_manifest.json",
        "statistics/object_level_bootstrap_intervals.csv",
        "statistics/object_level_metric_summary.csv",
        "statistics/object_level_statistical_assessment.md",
        "sun/sun_image_metadata.csv",
        "sun/sun_category_metadata.csv",
        "sun/sun_category_diagnostics_v3.csv",
        "sun/sun_low_coverage_high_conflict_review.md",
        "derm7pt/derm7pt_diagnosis_diagnostics_v3.csv",
        "derm7pt/derm7pt_limitations_v3.md",
        "submission_bundle/manifest.json",
    ]
    failures = [rel for rel in required if not (out / rel).exists()]
    if (out / "manifest_revision_v3.json").exists():
        manifest = read_json(out / "manifest_revision_v3.json")
        if manifest.get("status") != "pass":
            failures.append("manifest status is not pass")
    payload = {"validated_at": now_iso(), "root": str(root), "v3": str(out), "status": "pass" if not failures else "fail", "failures": failures}
    print(json.dumps(payload, indent=2))
    return 0 if not failures else 1


def run_v3(ctx: RunContext) -> int:
    for sub in ["awa2", "sun", "derm7pt", "statistics", "runtime", "tables", "schemas", "qc", "latex", "submission_bundle"]:
        ensure_dir(ctx.out / sub)
    enhanced_paths = []
    enhanced_paths.extend(run_awa2_enhanced(ctx))
    enhanced_paths.extend(run_sun_enhanced(ctx))
    enhanced_paths.extend(run_derm7pt_resnet(ctx))
    generate_object_intervals(ctx, enhanced_paths)
    write_statistical_assessment(ctx)
    write_latex_tables(ctx)
    write_schemas(ctx)
    sync_latex_artifacts(ctx)
    write_submission_bundle(ctx)
    validate_v3_outputs(ctx)
    write_qc(ctx)
    write_manifest(ctx)
    write_report(ctx)
    status = "pass" if not ctx.errors else "fail"
    print(json.dumps({"status": status, "v3_root": str(ctx.out), "errors": ctx.errors, "warnings": ctx.warnings}, indent=2, default=json_default))
    return 0 if status == "pass" else 1


def package_existing_v3(ctx: RunContext) -> int:
    for sub in ["statistics", "tables", "schemas", "qc", "latex", "submission_bundle"]:
        ensure_dir(ctx.out / sub)
    write_latex_tables(ctx)
    write_schemas(ctx)
    sync_latex_artifacts(ctx)
    validate_v3_outputs(ctx)
    write_qc(ctx)
    write_manifest(ctx)
    write_submission_bundle(ctx)
    write_manifest(ctx)
    write_report(ctx)
    status = "pass" if not ctx.errors else "fail"
    print(json.dumps({"status": status, "v3_root": str(ctx.out), "package_only": True, "errors": ctx.errors, "warnings": ctx.warnings}, indent=2, default=json_default))
    return 0 if status == "pass" else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--v1", type=Path, default=None)
    parser.add_argument("--v2", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--force-rebuild", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--package-only", action="store_true", help="Refresh QC, manifest, report, LaTeX sync, and submission bundle without recomputing experiments.")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--n-boot", type=int, default=1000)
    parser.add_argument("--derm-batch-size", type=int, default=16)
    parser.add_argument("--derm-device", choices=["cpu", "cuda", "auto"], default="cpu")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    out = (args.out.resolve() if args.out else root / "outputs" / "revision_v3")
    if args.validate_only:
        return validate_existing(root, out)
    if args.force_rebuild:
        safe_reset_out_dir(out, root)
    ctx = RunContext(
        root=root,
        v1=args.v1.resolve() if args.v1 else root / "outputs" / "revision_v1",
        v2=args.v2.resolve() if args.v2 else root / "outputs" / "revision_v2",
        out=out,
        manuscript=root / "manuscript",
        rng=np.random.default_rng(DEFAULT_SEED),
        n_boot=args.n_boot,
        smoke=args.smoke,
        derm_batch_size=args.derm_batch_size,
        derm_device=args.derm_device,
        force_rebuild=args.force_rebuild,
        errors=[],
        warnings=[],
    )
    if args.package_only:
        return package_existing_v3(ctx)
    return run_v3(ctx)


if __name__ == "__main__":
    raise SystemExit(main())
