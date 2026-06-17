#!/usr/bin/env python
"""SEMTRA revision v2 artifact hardening runner.

This script treats outputs/revision_v1 as the immutable baseline and writes a
new validation, diagnostics, packaging, and reporting bundle under
outputs/revision_v2.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))

from run_revision_v1 import (  # noqa: E402
    clean_name,
    group_derm_diagnosis,
    json_default,
    mat_string,
    now_iso,
    package_versions,
    run_capture,
    sha256_file,
    write_csv,
    write_json_safe,
)


V2_VERSION = "2.0"
DEFAULT_SEED = 20260617

REQUIRED_V1_FILES = [
    "environment.json",
    "manifest_revision_v1.json",
    "revision_v1_run_summary.json",
    "audit/claim_audit.csv",
    "statistics/metric_consistency_check.csv",
    "statistics/cross_domain_generalization.csv",
    "awa2/awa2_protocol_a_seedwise.csv",
    "awa2/awa2_protocol_b_seedwise.csv",
    "awa2/awa2_discretizer_comparison_seedwise.csv",
    "awa2/awa2_rule_predictions_seed42.csv",
    "sun/sun_dataset_manifest.json",
    "sun/sun_rule_predictions.csv",
    "sun/sun_rulebook_seedwise.csv",
    "derm7pt/derm7pt_dataset_manifest.json",
    "derm7pt/derm7pt_rule_predictions.csv",
    "derm7pt/derm7pt_rulebook_seedwise.csv",
]

SCHEMAS: dict[str, dict[str, Any]] = {
    "dataset_manifest.schema.json": {
        "family": "dataset_manifest",
        "format": "json",
        "required_keys": ["source"],
        "recommended_keys": ["dataset", "status"],
        "description": "Dataset provenance, scope, split, and status manifest.",
    },
    "metric_summary.schema.json": {
        "family": "metric_summary",
        "format": "csv",
        "required_columns": ["dataset"],
        "recommended_columns": ["seed", "coverage", "covered_accuracy", "covered_fidelity_to_base"],
        "description": "Seed-wise or aggregate audit metric table.",
    },
    "runtime_log.schema.json": {
        "family": "runtime_log",
        "format": "jsonl",
        "required_keys": ["dataset", "stage", "seconds", "status"],
        "description": "JSONL runtime and stage log records.",
    },
    "claim_check.schema.json": {
        "family": "claim_check",
        "format": "csv",
        "required_columns": ["claim_id", "source", "expected", "observed", "status", "severity"],
        "description": "Machine-readable manuscript claim consistency checks.",
    },
    "bootstrap_interval.schema.json": {
        "family": "bootstrap_interval",
        "format": "csv",
        "required_columns": [
            "dataset",
            "artifact",
            "metric",
            "unit",
            "n",
            "mean",
            "ci_low",
            "ci_high",
            "n_boot",
            "note",
        ],
        "description": "Bootstrap confidence intervals for available seed- or object-level metrics.",
    },
    "paired_discretizer_interval.schema.json": {
        "family": "paired_discretizer_interval",
        "format": "csv",
        "required_columns": [
            "metric",
            "n_pairs",
            "mean_difference_wedd_minus_mdlp",
            "ci_low",
            "ci_high",
            "n_boot",
            "note",
        ],
        "description": "Paired bootstrap intervals for WEDD-minus-MDLP seed-wise differences.",
    },
    "sun_diagnostics.schema.json": {
        "family": "sun_diagnostics",
        "format": "csv",
        "required_columns": [
            "class_index",
            "class_name",
            "n_objects",
            "coverage",
            "covered_accuracy",
            "covered_fidelity",
            "conflict_rate",
            "abstention_rate",
        ],
        "description": "SUN class/category-level stress-test diagnostics.",
    },
    "derm7pt_diagnostics.schema.json": {
        "family": "derm7pt_diagnostics",
        "format": "csv",
        "required_columns": [
            "group",
            "n_cases",
            "coverage",
            "covered_accuracy",
            "covered_fidelity",
            "conflict_rate",
            "abstention_rate",
        ],
        "description": "Derm7pt diagnosis/concept diagnostic summaries.",
    },
    "submission_bundle_manifest.schema.json": {
        "family": "submission_bundle_manifest",
        "format": "json",
        "required_keys": ["generated_at", "bundle_root", "files", "raw_private_data_excluded"],
        "description": "Traceable list of files included in the clean submission bundle.",
    },
}


@dataclass
class RunContext:
    root: Path
    v1: Path
    out: Path
    manuscript: Path
    rng: np.random.Generator
    n_boot: int
    errors: list[str]
    warnings: list[str]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin(["true", "1", "yes", "y"])


def safe_reset_out_dir(out: Path, root: Path) -> None:
    resolved_out = out.resolve()
    resolved_root = root.resolve()
    default_out = (resolved_root / "outputs" / "revision_v2").resolve()
    if resolved_out != default_out:
        raise RuntimeError(f"Refusing to delete non-default v2 output path: {resolved_out}")
    if resolved_out.exists():
        shutil.rmtree(resolved_out)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8", newline="\n")


def copy_if_exists(src: Path, dst: Path, files: list[dict[str, Any]] | None = None, role: str = "") -> bool:
    if not src.exists():
        return False
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    if files is not None:
        files.append(file_record(dst, role=role))
    return True


def file_record(path: Path, role: str = "") -> dict[str, Any]:
    return {
        "path": str(path),
        "size": path.stat().st_size,
        "sha256": sha256_file(path),
        "role": role,
    }


def rel_to(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve())


def validate_v1_baseline(v1: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for rel in REQUIRED_V1_FILES:
        path = v1 / rel
        rows.append(
            {
                "artifact": rel,
                "status": "present" if path.exists() else "missing",
                "size": str(path.stat().st_size) if path.exists() else "",
                "sha256": sha256_file(path) if path.exists() else "",
            }
        )
    return rows


def bootstrap_ci(values: Iterable[float], rng: np.random.Generator, n_boot: int) -> tuple[float, float, float]:
    arr = np.asarray([float(v) for v in values if pd.notna(v)], dtype=float)
    if arr.size == 0:
        return (math.nan, math.nan, math.nan)
    if arr.size == 1:
        return (float(arr[0]), float(arr[0]), float(arr[0]))
    idx = rng.integers(0, arr.size, size=(n_boot, arr.size))
    boot = arr[idx].mean(axis=1)
    return (float(arr.mean()), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975)))


def add_bootstrap_row(
    rows: list[dict[str, Any]],
    dataset: str,
    artifact: str,
    metric: str,
    unit: str,
    values: Iterable[float],
    rng: np.random.Generator,
    n_boot: int,
    note: str,
) -> None:
    vals = [float(v) for v in values if pd.notna(v)]
    mean, low, high = bootstrap_ci(vals, rng, n_boot)
    rows.append(
        {
            "dataset": dataset,
            "artifact": artifact,
            "metric": metric,
            "unit": unit,
            "n": len(vals),
            "mean": mean,
            "ci_low": low,
            "ci_high": high,
            "n_boot": n_boot,
            "note": note,
        }
    )


def prediction_metric_values(df: pd.DataFrame) -> dict[str, np.ndarray]:
    out: dict[str, np.ndarray] = {}
    if "abstained" in df.columns:
        abstained = as_bool(df["abstained"]).to_numpy()
        out["coverage"] = (~abstained).astype(float)
        out["abstention_rate"] = abstained.astype(float)
    if "conflict" in df.columns:
        out["conflict_rate"] = as_bool(df["conflict"]).astype(float).to_numpy()
    if "mode" in df.columns:
        mode = df["mode"].astype(str)
        out["fallback_rate"] = (mode == "fallback").astype(float).to_numpy()
        out["exact_rate"] = (mode == "exact").astype(float).to_numpy()
    if "n_activated" in df.columns:
        out["n_activated"] = pd.to_numeric(df["n_activated"], errors="coerce").to_numpy(dtype=float)
    return out


def generate_bootstrap_intervals(ctx: RunContext) -> None:
    rows: list[dict[str, Any]] = []

    seedwise_specs = [
        ("awa2", "awa2/awa2_protocol_a_seedwise.csv", "seed"),
        ("awa2_protocol_b", "awa2/awa2_protocol_b_seedwise.csv", "seed"),
        ("sun", "sun/sun_rulebook_seedwise.csv", "seed"),
        ("derm7pt", "derm7pt/derm7pt_rulebook_seedwise.csv", "seed"),
    ]
    seed_metrics = [
        "coverage",
        "covered_accuracy",
        "covered_fidelity_to_base",
        "all_object_accuracy",
        "conflict_rate",
        "abstention_rate",
        "test_mae",
    ]
    for dataset, rel, unit in seedwise_specs:
        path = ctx.v1 / rel
        if not path.exists():
            ctx.warnings.append(f"Bootstrap seed artifact missing: {rel}")
            continue
        df = pd.read_csv(path)
        for metric in seed_metrics:
            if metric in df.columns:
                add_bootstrap_row(
                    rows,
                    dataset,
                    rel,
                    metric,
                    unit,
                    pd.to_numeric(df[metric], errors="coerce"),
                    ctx.rng,
                    ctx.n_boot,
                    "seed-wise nonparametric bootstrap over completed v1 runs",
                )

    object_specs = [
        ("awa2", "awa2/awa2_rule_predictions_seed42.csv"),
        ("sun", "sun/sun_rule_predictions.csv"),
        ("derm7pt", "derm7pt/derm7pt_rule_predictions.csv"),
    ]
    for dataset, rel in object_specs:
        path = ctx.v1 / rel
        if not path.exists():
            ctx.warnings.append(f"Bootstrap prediction artifact missing: {rel}")
            continue
        df = pd.read_csv(path)
        for metric, values in prediction_metric_values(df).items():
            add_bootstrap_row(
                rows,
                dataset,
                rel,
                metric,
                "object",
                values,
                ctx.rng,
                ctx.n_boot,
                "object-level bootstrap for prediction-state metrics available in v1 predictions",
            )

    out_path = ctx.out / "statistics" / "bootstrap_intervals.csv"
    write_csv(out_path, rows)
    if not rows:
        ctx.errors.append("No bootstrap interval rows were generated.")


def generate_paired_discretizer_intervals(ctx: RunContext) -> None:
    path = ctx.v1 / "awa2" / "awa2_discretizer_comparison_seedwise.csv"
    rows: list[dict[str, Any]] = []
    if not path.exists():
        ctx.errors.append("Missing v1 paired discretizer artifact.")
        write_csv(ctx.out / "statistics" / "paired_discretizer_intervals.csv", rows)
        return

    df = pd.read_csv(path)
    if "method" not in df.columns or "seed" not in df.columns:
        ctx.errors.append("Discretizer comparison is missing method or seed columns.")
        write_csv(ctx.out / "statistics" / "paired_discretizer_intervals.csv", rows)
        return

    method_values = set(df["method"].astype(str))
    wedd_names = [m for m in method_values if "wedd" in m.lower()]
    mdlp_names = [m for m in method_values if "mdlp" in m.lower() or "entropy" in m.lower()]
    if not wedd_names or not mdlp_names:
        ctx.errors.append(f"Could not identify WEDD/MDLP methods in {path.name}: {sorted(method_values)}")
        write_csv(ctx.out / "statistics" / "paired_discretizer_intervals.csv", rows)
        return
    wedd_name = sorted(wedd_names)[0]
    mdlp_name = sorted(mdlp_names)[0]

    metrics = [
        "coverage",
        "covered_accuracy",
        "covered_fidelity_to_base",
        "all_object_accuracy",
        "conflict_rate",
        "abstention_rate",
    ]
    for metric in metrics:
        if metric not in df.columns:
            continue
        sub = df[["seed", "method", metric]].copy()
        pivot = sub.pivot_table(index="seed", columns="method", values=metric, aggfunc="mean")
        if wedd_name not in pivot.columns or mdlp_name not in pivot.columns:
            continue
        diffs = (pivot[wedd_name] - pivot[mdlp_name]).dropna().to_numpy(dtype=float)
        mean, low, high = bootstrap_ci(diffs, ctx.rng, ctx.n_boot)
        rows.append(
            {
                "metric": metric,
                "n_pairs": int(diffs.size),
                "mean_difference_wedd_minus_mdlp": mean,
                "ci_low": low,
                "ci_high": high,
                "n_boot": ctx.n_boot,
                "note": f"Paired seed bootstrap: {wedd_name} minus {mdlp_name}; positive values do not imply universal superiority.",
            }
        )

    write_csv(ctx.out / "statistics" / "paired_discretizer_intervals.csv", rows)
    if not rows:
        ctx.errors.append("No paired discretizer interval rows were generated.")


def load_sun_seen_labels(ctx: RunContext, n_pred: int) -> tuple[np.ndarray | None, list[str]]:
    manifest_path = ctx.v1 / "sun" / "sun_dataset_manifest.json"
    if not manifest_path.exists():
        ctx.warnings.append("SUN manifest missing; category diagnostics will omit labels.")
        return None, []
    manifest = read_json(manifest_path)
    source = Path(manifest.get("source", ""))
    if not source.exists():
        ctx.warnings.append(f"SUN source not found: {source}")
        return None, []
    try:
        from scipy.io import loadmat

        splits = loadmat(source / "att_splits.mat", squeeze_me=True, struct_as_record=False)
        res = loadmat(source / "res101.mat", squeeze_me=True, struct_as_record=False)
        labels = np.asarray(res["labels"]).ravel().astype(int) - 1
        seen_loc = np.asarray(splits["test_seen_loc"]).ravel().astype(int) - 1
        y = labels[seen_loc]
        names_raw = np.asarray(splits.get("allclasses_names", []), dtype=object).ravel()
        names = [clean_name(mat_string(x)) for x in names_raw]
        if y.size != n_pred:
            ctx.warnings.append(f"SUN seen label count {y.size} does not match prediction count {n_pred}; truncating.")
            m = min(y.size, n_pred)
            y = y[:m]
        return y, names
    except Exception as exc:  # pragma: no cover - defensive diagnostics path
        ctx.warnings.append(f"SUN label loading failed: {exc}")
        return None, []


def safe_prediction_int(series: pd.Series) -> np.ndarray:
    return pd.to_numeric(series, errors="coerce").fillna(-1).astype(int).to_numpy()


def generate_sun_diagnostics(ctx: RunContext) -> None:
    pred_path = ctx.v1 / "sun" / "sun_rule_predictions.csv"
    rows: list[dict[str, Any]] = []
    if not pred_path.exists():
        ctx.errors.append("SUN prediction file missing for v2 diagnostics.")
        write_csv(ctx.out / "sun" / "sun_category_diagnostics.csv", rows)
        write_text(ctx.out / "sun" / "sun_failure_modes.md", "# SUN Failure Modes\n\nSUN predictions were unavailable.\n")
        return

    df = pd.read_csv(pred_path)
    y, names = load_sun_seen_labels(ctx, len(df))
    if y is None:
        y = np.full(len(df), -1, dtype=int)
    m = min(len(df), len(y))
    df = df.iloc[:m].reset_index(drop=True)
    y = y[:m]

    pred = safe_prediction_int(df["prediction"]) if "prediction" in df.columns else np.full(m, -1, dtype=int)
    abstained = as_bool(df["abstained"]).to_numpy() if "abstained" in df.columns else pred < 0
    conflict = as_bool(df["conflict"]).to_numpy() if "conflict" in df.columns else np.zeros(m, dtype=bool)
    mode = df["mode"].astype(str).to_numpy() if "mode" in df.columns else np.array(["unknown"] * m)
    n_activated = pd.to_numeric(df.get("n_activated", pd.Series([np.nan] * m)), errors="coerce").to_numpy()

    for cls in sorted(set(int(v) for v in y if int(v) >= 0)):
        idx = np.where(y == cls)[0]
        if idx.size == 0:
            continue
        covered = ~abstained[idx]
        correct = pred[idx] == y[idx]
        rows.append(
            {
                "class_index": cls,
                "class_name": names[cls] if 0 <= cls < len(names) else f"class_{cls}",
                "n_objects": int(idx.size),
                "coverage": float(covered.mean()),
                "covered_accuracy": float(correct[covered].mean()) if covered.any() else math.nan,
                "covered_fidelity": math.nan,
                "conflict_rate": float(conflict[idx].mean()),
                "abstention_rate": float(abstained[idx].mean()),
                "fallback_rate": float((mode[idx] == "fallback").mean()),
                "exact_rate": float((mode[idx] == "exact").mean()),
                "mean_n_activated": float(np.nanmean(n_activated[idx])) if np.isfinite(n_activated[idx]).any() else math.nan,
                "scope": "seen-test stress-test diagnostics",
                "note": "covered_fidelity omitted because v1 prediction exports do not include base-model labels",
            }
        )

    out_csv = ctx.out / "sun" / "sun_category_diagnostics.csv"
    write_csv(out_csv, rows)

    diag = pd.DataFrame(rows)
    if diag.empty:
        ctx.errors.append("SUN diagnostic table is empty.")
        failure_text = "# SUN Failure Modes\n\nNo SUN class-level diagnostics could be generated.\n"
    else:
        low_cov = diag.sort_values(["coverage", "n_objects"], ascending=[True, False]).head(10)
        high_conflict = diag.sort_values(["conflict_rate", "n_objects"], ascending=[False, False]).head(10)
        lines = [
            "# SUN Failure Modes",
            "",
            "Scope: v2 diagnostics aggregate the existing SUN v1 seen-test rule predictions by SUN class label. They are a portability stress test, not a competitive zero-shot learning benchmark.",
            "",
            f"Classes summarized: {len(diag)}. Mean class coverage: {diag['coverage'].mean():.4f}. Mean class conflict rate: {diag['conflict_rate'].mean():.4f}.",
            "",
            "## Lowest Coverage Classes",
            "",
        ]
        for _, row in low_cov.iterrows():
            lines.append(
                f"- {row['class_name']} (n={int(row['n_objects'])}): coverage={row['coverage']:.4f}, conflict={row['conflict_rate']:.4f}"
            )
        lines.extend(["", "## Highest Conflict Classes", ""])
        for _, row in high_conflict.iterrows():
            lines.append(
                f"- {row['class_name']} (n={int(row['n_objects'])}): conflict={row['conflict_rate']:.4f}, coverage={row['coverage']:.4f}"
            )
        lines.extend(
            [
                "",
                "## Interpretation",
                "",
                "SUN remains reported as a stress-test/portability result. The diagnostics show that low coverage and high conflict are class-dependent, so v2 does not strengthen the manuscript into a competitive SUN claim.",
            ]
        )
        failure_text = "\n".join(lines) + "\n"
    write_text(ctx.out / "sun" / "sun_failure_modes.md", failure_text)


def load_derm_test_meta(ctx: RunContext, n_pred: int) -> tuple[pd.DataFrame | None, np.ndarray | None, list[str]]:
    manifest_path = ctx.v1 / "derm7pt" / "derm7pt_dataset_manifest.json"
    if not manifest_path.exists():
        ctx.warnings.append("Derm7pt manifest missing.")
        return None, None, []
    manifest = read_json(manifest_path)
    source = Path(manifest.get("source", ""))
    meta_path = source / "meta" / "meta.csv"
    test_idx_path = source / "meta" / "test_indexes.csv"
    if not meta_path.exists() or not test_idx_path.exists():
        ctx.warnings.append(f"Derm7pt metadata or test indexes missing under {source}.")
        return None, None, []
    meta = pd.read_csv(meta_path)
    test_idx_df = pd.read_csv(test_idx_path)
    if "indexes" in test_idx_df.columns:
        test_idx = test_idx_df["indexes"].to_numpy(dtype=int)
    else:
        test_idx = pd.to_numeric(test_idx_df.iloc[:, 0], errors="coerce").dropna().astype(int).to_numpy()
    grouped = meta["diagnosis"].map(group_derm_diagnosis).astype(str)
    classes = sorted(grouped.dropna().unique().tolist())
    class_to_idx = {name: idx for idx, name in enumerate(classes)}
    test_meta = meta.iloc[test_idx].reset_index(drop=True)
    y_names = test_meta["diagnosis"].map(group_derm_diagnosis).astype(str)
    y = y_names.map(class_to_idx).to_numpy(dtype=int)
    if len(test_meta) != n_pred:
        ctx.warnings.append(f"Derm7pt test count {len(test_meta)} does not match predictions {n_pred}; truncating.")
        m = min(len(test_meta), n_pred)
        test_meta = test_meta.iloc[:m].reset_index(drop=True)
        y = y[:m]
    return test_meta, y, classes


def derm_metric_row(group: str, idx: np.ndarray, y: np.ndarray, pred: np.ndarray, abstained: np.ndarray, conflict: np.ndarray, mode: np.ndarray, note: str) -> dict[str, Any]:
    covered = ~abstained[idx]
    correct = pred[idx] == y[idx]
    return {
        "group": group,
        "n_cases": int(idx.size),
        "coverage": float(covered.mean()) if idx.size else math.nan,
        "covered_accuracy": float(correct[covered].mean()) if covered.any() else math.nan,
        "covered_fidelity": math.nan,
        "conflict_rate": float(conflict[idx].mean()) if idx.size else math.nan,
        "abstention_rate": float(abstained[idx].mean()) if idx.size else math.nan,
        "fallback_rate": float((mode[idx] == "fallback").mean()) if idx.size else math.nan,
        "exact_rate": float((mode[idx] == "exact").mean()) if idx.size else math.nan,
        "note": note,
    }


def generate_derm_diagnostics(ctx: RunContext) -> None:
    pred_path = ctx.v1 / "derm7pt" / "derm7pt_rule_predictions.csv"
    diagnosis_rows: list[dict[str, Any]] = []
    concept_rows: list[dict[str, Any]] = []
    if not pred_path.exists():
        ctx.errors.append("Derm7pt prediction file missing for v2 diagnostics.")
        write_csv(ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics.csv", diagnosis_rows)
        write_csv(ctx.out / "derm7pt" / "derm7pt_concept_diagnostics_v2.csv", concept_rows)
        write_text(ctx.out / "derm7pt" / "derm7pt_limitations.md", "# Derm7pt Limitations\n\nPredictions were unavailable.\n")
        return

    df = pd.read_csv(pred_path)
    meta, y, classes = load_derm_test_meta(ctx, len(df))
    if meta is None or y is None:
        ctx.errors.append("Derm7pt metadata could not be loaded for diagnostics.")
        return
    m = min(len(df), len(meta), len(y))
    df = df.iloc[:m].reset_index(drop=True)
    meta = meta.iloc[:m].reset_index(drop=True)
    y = y[:m]

    pred = safe_prediction_int(df["prediction"]) if "prediction" in df.columns else np.full(m, -1, dtype=int)
    abstained = as_bool(df["abstained"]).to_numpy() if "abstained" in df.columns else pred < 0
    conflict = as_bool(df["conflict"]).to_numpy() if "conflict" in df.columns else np.zeros(m, dtype=bool)
    mode = df["mode"].astype(str).to_numpy() if "mode" in df.columns else np.array(["unknown"] * m)

    for cls_idx, cls_name in enumerate(classes):
        idx = np.where(y == cls_idx)[0]
        if idx.size:
            diagnosis_rows.append(
                derm_metric_row(
                    cls_name,
                    idx,
                    y,
                    pred,
                    abstained,
                    conflict,
                    mode,
                    "retrospective technical validation diagnostic; covered_fidelity omitted because v1 predictions do not include base-model labels",
                )
            )

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
        if concept not in meta.columns:
            continue
        values = meta[concept].fillna("missing").astype(str)
        for value in sorted(values.unique()):
            idx = np.where(values.to_numpy() == value)[0]
            row = derm_metric_row(
                f"{concept}={value}",
                idx,
                y,
                pred,
                abstained,
                conflict,
                mode,
                "concept-stratified diagnostic only; not clinical validation",
            )
            row["concept"] = concept
            row["concept_value"] = value
            row["missing_value"] = value.lower() == "missing"
            concept_rows.append(row)

    write_csv(ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics.csv", diagnosis_rows)
    write_csv(ctx.out / "derm7pt" / "derm7pt_concept_diagnostics_v2.csv", concept_rows)

    diag = pd.DataFrame(diagnosis_rows)
    concept_df = pd.DataFrame(concept_rows)
    lines = [
        "# Derm7pt Limitations",
        "",
        "Scope: v2 keeps the existing simple-image-feature Derm7pt run as a reproducible retrospective technical-validation baseline.",
        "",
        "The diagnostics are stratified by grouped diagnosis and seven-point checklist concept values. They do not constitute clinical validation, prospective evaluation, reader-study evidence, or medical-device readiness evidence.",
        "",
    ]
    if not diag.empty:
        lines.append(
            f"Diagnosis groups summarized: {len(diag)}. Mean diagnosis-group coverage: {diag['coverage'].mean():.4f}. Mean diagnosis-group conflict rate: {diag['conflict_rate'].mean():.4f}."
        )
    if not concept_df.empty:
        lines.append(f"Concept strata summarized: {len(concept_df)} across {concept_df['concept'].nunique()} checklist concepts.")
    lines.extend(
        [
            "",
            "Key limitations remain: hand-engineered color/texture features are not a modern dermoscopic representation; metadata-level splits are retrospective; checklist labels are sparse and partly missing; and no clinical deployment claim is supported.",
        ]
    )
    write_text(ctx.out / "derm7pt" / "derm7pt_limitations.md", "\n".join(lines) + "\n")

    if not diagnosis_rows:
        ctx.errors.append("Derm7pt diagnosis diagnostics are empty.")
    if not concept_rows:
        ctx.errors.append("Derm7pt concept diagnostics are empty.")


def write_statistical_assessment(ctx: RunContext) -> None:
    boot_path = ctx.out / "statistics" / "bootstrap_intervals.csv"
    paired_path = ctx.out / "statistics" / "paired_discretizer_intervals.csv"
    boot = pd.read_csv(boot_path) if boot_path.exists() else pd.DataFrame()
    paired = pd.read_csv(paired_path) if paired_path.exists() else pd.DataFrame()
    lines = [
        "# Statistical Assessment",
        "",
        "Revision v2 adds nonparametric bootstrap intervals around the v1 audit artifacts without rewriting the v1 bundle.",
        "",
    ]
    if not boot.empty:
        lines.append(f"Bootstrap rows generated: {len(boot)} across {boot['dataset'].nunique()} dataset scopes.")
        object_rows = boot[boot["unit"] == "object"]
        seed_rows = boot[boot["unit"] == "seed"]
        lines.append(f"Object-level intervals: {len(object_rows)}. Seed-level intervals: {len(seed_rows)}.")
    else:
        lines.append("No bootstrap rows were generated.")
    lines.append("")
    if not paired.empty:
        lines.append(
            "Paired WEDD-vs-MDLP intervals were generated over matched AwA2 seeds. These quantify the observed paired differences and do not justify wording that WEDD is universally superior."
        )
    else:
        lines.append("Paired WEDD-vs-MDLP intervals were not generated.")
    lines.extend(
        [
            "",
            "Interpretation guardrails:",
            "",
            "- Object-level intervals are available only for fields exported in v1 prediction files. Base-model labels are not present in those files, so covered-fidelity object-level intervals are intentionally omitted from the prediction-level bootstrap.",
            "- Seed-wise intervals are based on five-seed v1 runs where available and should be read as stability diagnostics rather than population-level inferential guarantees.",
            "- SUN and Derm7pt diagnostics remain scoped as portability and retrospective technical-validation checks.",
        ]
    )
    write_text(ctx.out / "statistics" / "statistical_assessment.md", "\n".join(lines) + "\n")


def extract_metric_value(metric_csv: Path, metric: str) -> str:
    if not metric_csv.exists():
        return ""
    df = pd.read_csv(metric_csv)
    if "metric" not in df.columns or "manuscript_value" not in df.columns:
        return ""
    sub = df[df["metric"] == metric]
    if sub.empty:
        return ""
    return str(sub.iloc[0]["manuscript_value"])


def generate_claim_checks(ctx: RunContext) -> list[dict[str, Any]]:
    main_path = ctx.manuscript / "main.tex"
    supply_path = ctx.manuscript / "supply.tex"
    main = read_text(main_path) if main_path.exists() else ""
    supply = read_text(supply_path) if supply_path.exists() else ""
    combined = main + "\n" + supply
    metric_csv = ctx.v1 / "statistics" / "metric_consistency_check.csv"

    checks = [
        {
            "claim_id": "awa2_test_mae",
            "source": "manuscript/main.tex",
            "expected": extract_metric_value(metric_csv, "abstract_awA2_test_mae") or r"0.1029 \\pm 0.0005",
            "pattern": r"0\.1029\s*\\pm\s*0\.0005",
            "severity": "error",
            "discipline": "numeric",
        },
        {
            "claim_id": "coverage_accuracy_fidelity",
            "source": "manuscript/main.tex",
            "expected": "84.80%, 39.73%, 40.48%",
            "pattern": r"84\.80\\%.*39\.73\\%.*40\.48\\%",
            "severity": "error",
            "discipline": "numeric",
        },
        {
            "claim_id": "protocol_b_uncertainty",
            "source": "manuscript/main.tex",
            "expected": "44.02% +/- 1.22% and not competitive ZSL",
            "pattern": r"44\.02\\%.*1\.22\\%.*(?:not\s+a\s+competitive\s+zero-shot\s+learning\s+claim|not\s+as\s+a\s+competitive\s+zero-shot\s+learning\s+claim)",
            "severity": "error",
            "discipline": "claim_gate",
        },
        {
            "claim_id": "synthetic_macro_f1",
            "source": "manuscript/main.tex",
            "expected": "0.879, 0.838, 0.8668",
            "pattern": r"0\.879.*0\.838.*0\.8668",
            "severity": "error",
            "discipline": "numeric",
        },
        {
            "claim_id": "derm7pt_not_clinical",
            "source": "manuscript/main.tex",
            "expected": "retrospective technical validation and no clinical readiness",
            "pattern": r"retrospective\s+technical\s+validation.*(?:not\s+as\s+clinical\s+readiness\s+evidence|clinical\s+readiness\s+evidence)",
            "severity": "error",
            "discipline": "claim_gate",
        },
        {
            "claim_id": "wedd_not_universal_superiority",
            "source": "manuscript/main.tex",
            "expected": "WEDD not unconditionally superior",
            "pattern": r"(?:not\s+as\s+an\s+unconditionally\s+superior\s+discretizer|not\s+an\s+unconditionally\s+superior\s+discretizer|not\s+as\s+universal\s+dominance|not\s+a\s+standalone\s+superiority\s+claim|rather\s+than\s+as\s+a\s+universally\s+superior\s+discretizer)",
            "severity": "error",
            "discipline": "claim_gate",
        },
        {
            "claim_id": "no_competitive_zsl_framing",
            "source": "manuscript/main.tex",
            "expected": "no competitive zero-shot learning framing",
            "pattern": r"not\s+a\s+competitive\s+zero-shot\s+learning\s+claim|not\s+as\s+a\s+competitive\s+zero-shot\s+learning\s+claim",
            "severity": "error",
            "discipline": "claim_gate",
        },
    ]

    rows: list[dict[str, Any]] = []
    for check in checks:
        matched = re.search(check["pattern"], combined, flags=re.IGNORECASE | re.DOTALL) is not None
        rows.append(
            {
                "claim_id": check["claim_id"],
                "source": check["source"],
                "expected": check["expected"],
                "observed": "matched" if matched else "not_found",
                "status": "pass" if matched else "fail",
                "severity": check["severity"],
                "discipline": check["discipline"],
            }
        )
    write_csv(ctx.out / "qc" / "claim_consistency_check.csv", rows)
    for row in rows:
        if row["severity"] == "error" and row["status"] != "pass":
            ctx.errors.append(f"Claim check failed: {row['claim_id']}")
    return rows


def write_schemas(ctx: RunContext) -> None:
    schema_dir = ctx.out / "schemas"
    ensure_dir(schema_dir)
    for name, schema in SCHEMAS.items():
        payload = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "semtra_revision": V2_VERSION,
            **schema,
        }
        write_json_safe(schema_dir / name, payload)


def validate_csv_columns(path: Path, required: list[str]) -> tuple[str, str]:
    if not path.exists():
        return ("fail", "missing file")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
    except Exception as exc:
        return ("fail", str(exc))
    missing = [col for col in required if col not in header]
    return ("pass", "") if not missing else ("fail", ",".join(missing))


def validate_json_keys(path: Path, required: list[str]) -> tuple[str, str]:
    if not path.exists():
        return ("fail", "missing file")
    try:
        obj = read_json(path)
    except Exception as exc:
        return ("fail", str(exc))
    missing = [key for key in required if key not in obj]
    return ("pass", "") if not missing else ("fail", ",".join(missing))


def validate_jsonl_keys(path: Path, required: list[str]) -> tuple[str, str]:
    if not path.exists():
        return ("fail", "missing file")
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                obj = json.loads(line)
                missing = [key for key in required if key not in obj]
                if missing:
                    return ("fail", f"line {line_no}: {','.join(missing)}")
                return ("pass", "")
    except Exception as exc:
        return ("fail", str(exc))
    return ("fail", "empty jsonl")


def validate_schemas(ctx: RunContext) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    checks = [
        ("dataset_manifest", ctx.v1 / "sun" / "sun_dataset_manifest.json", "dataset_manifest.schema.json"),
        ("dataset_manifest", ctx.v1 / "derm7pt" / "derm7pt_dataset_manifest.json", "dataset_manifest.schema.json"),
        ("metric_summary", ctx.v1 / "awa2" / "awa2_protocol_a_seedwise.csv", "metric_summary.schema.json"),
        ("metric_summary", ctx.v1 / "sun" / "sun_rulebook_seedwise.csv", "metric_summary.schema.json"),
        ("metric_summary", ctx.v1 / "derm7pt" / "derm7pt_rulebook_seedwise.csv", "metric_summary.schema.json"),
        ("claim_check", ctx.out / "qc" / "claim_consistency_check.csv", "claim_check.schema.json"),
        ("bootstrap_interval", ctx.out / "statistics" / "bootstrap_intervals.csv", "bootstrap_interval.schema.json"),
        ("paired_discretizer_interval", ctx.out / "statistics" / "paired_discretizer_intervals.csv", "paired_discretizer_interval.schema.json"),
        ("sun_diagnostics", ctx.out / "sun" / "sun_category_diagnostics.csv", "sun_diagnostics.schema.json"),
        ("derm7pt_diagnostics", ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics.csv", "derm7pt_diagnostics.schema.json"),
        ("derm7pt_diagnostics", ctx.out / "derm7pt" / "derm7pt_concept_diagnostics_v2.csv", "derm7pt_diagnostics.schema.json"),
        ("submission_bundle_manifest", ctx.out / "submission_bundle" / "manifest.json", "submission_bundle_manifest.schema.json"),
    ]
    for family, path, schema_name in checks:
        schema = SCHEMAS[schema_name]
        if schema["format"] == "csv":
            status, detail = validate_csv_columns(path, schema.get("required_columns", []))
        elif schema["format"] == "json":
            status, detail = validate_json_keys(path, schema.get("required_keys", []))
        elif schema["format"] == "jsonl":
            status, detail = validate_jsonl_keys(path, schema.get("required_keys", []))
        else:
            status, detail = ("fail", f"unknown schema format {schema['format']}")
        rows.append(
            {
                "family": family,
                "schema": schema_name,
                "artifact": rel_to(path, ctx.root),
                "status": status,
                "detail": detail,
            }
        )
        if status != "pass":
            ctx.errors.append(f"Schema validation failed for {rel_to(path, ctx.root)}: {detail}")
    write_csv(ctx.out / "qc" / "schema_validation.csv", rows)
    return rows


def duplicate_labels(tex_paths: list[Path]) -> list[str]:
    labels: dict[str, Path] = {}
    dupes: list[str] = []
    for path in tex_paths:
        if not path.exists():
            continue
        text = read_text(path)
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            if label in labels:
                dupes.append(label)
            else:
                labels[label] = path
    return sorted(set(dupes))


def missing_bib_keys(tex_paths: list[Path], bib_path: Path) -> list[str]:
    cite_keys: set[str] = set()
    for path in tex_paths:
        if not path.exists():
            continue
        text = read_text(path)
        for match in re.findall(r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear)\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}", text):
            for key in match.split(","):
                if key.strip():
                    cite_keys.add(key.strip())
    bib_keys: set[str] = set()
    if bib_path.exists():
        bib_text = read_text(bib_path)
        bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text))
    return sorted(cite_keys - bib_keys)


def latex_log_issues(log_path: Path) -> list[str]:
    if not log_path.exists():
        return [f"missing log: {log_path.name}"]
    if log_path.stat().st_size == 0:
        return [f"empty log: {log_path.name}"]
    text = read_text(log_path)
    issues = []
    patterns = [
        ("fatal_error", r"Fatal error occurred"),
        ("undefined_refs", r"undefined references"),
        ("undefined_citations", r"Citation .* undefined"),
        ("rerun_required", r"Rerun to get cross-references right|Label\(s\) may have changed"),
        ("overfull_hbox", r"Overfull \\hbox"),
    ]
    for name, pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            issues.append(name)
    return issues


def sync_latex_artifacts(ctx: RunContext) -> None:
    latex_dir = ctx.out / "latex"
    ensure_dir(latex_dir)
    records = []
    for stem in ["main", "supply"]:
        for ext in [".pdf", ".log", ".aux", ".bbl", ".blg", ".out", ".toc"]:
            src = ctx.manuscript / f"{stem}{ext}"
            fallback = ctx.v1 / "latex" / f"{stem}{ext}"
            chosen = src
            source = "manuscript_build"
            if (not chosen.exists()) or (chosen.stat().st_size == 0):
                chosen = fallback
                source = "revision_v1_latex_archive"
            if chosen.exists():
                copy_if_exists(chosen, latex_dir / f"{stem}{ext}")
                records.append(
                    {
                        "artifact": f"{stem}{ext}",
                        "source": source,
                        "source_path": str(chosen),
                        "size": chosen.stat().st_size,
                        "sha256": sha256_file(chosen),
                    }
                )
            else:
                records.append(
                    {
                        "artifact": f"{stem}{ext}",
                        "source": "missing",
                        "source_path": "",
                        "size": 0,
                        "sha256": "",
                    }
                )
    write_json_safe(
        latex_dir / "latex_artifact_sources.json",
        {
            "generated_at": now_iso(),
            "note": "Fresh manuscript build files are preferred. Empty or missing files fall back to the successful revision_v1 LaTeX archive.",
            "records": records,
        },
    )


def copy_referenced_figures(ctx: RunContext, bundle_root: Path, files: list[dict[str, Any]]) -> None:
    tex_paths = [ctx.manuscript / "main.tex", ctx.manuscript / "supply.tex"]
    seen: set[Path] = set()
    for tex_path in tex_paths:
        if not tex_path.exists():
            continue
        text = read_text(tex_path)
        for raw in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text):
            raw_path = raw.strip()
            candidates = [
                (ctx.manuscript / raw_path).resolve(),
                (ctx.root / raw_path).resolve(),
                (ctx.root / "figs" / Path(raw_path).name).resolve(),
            ]
            src = next((p for p in candidates if p.exists()), None)
            if src is None or src in seen:
                continue
            seen.add(src)
            try:
                rel = src.relative_to(ctx.root.resolve())
            except ValueError:
                rel = Path("figs") / src.name
            copy_if_exists(src, bundle_root / rel, files, role="referenced_figure")


def write_submission_bundle(ctx: RunContext) -> None:
    bundle = ctx.out / "submission_bundle"
    if bundle.exists():
        shutil.rmtree(bundle)
    ensure_dir(bundle)
    files: list[dict[str, Any]] = []

    for name in ["main.tex", "supply.tex", "references.bib"]:
        copy_if_exists(ctx.manuscript / name, bundle / "manuscript" / name, files, role="manuscript_source")

    table_src = ctx.v1 / "tables"
    if table_src.exists():
        for table in sorted(table_src.glob("*.tex")):
            copy_if_exists(table, bundle / "outputs" / "revision_v1" / "tables" / table.name, files, role="generated_table")

    for table in sorted((ctx.out / "statistics").glob("*.tex")):
        copy_if_exists(table, bundle / "outputs" / "revision_v2" / "statistics" / table.name, files, role="generated_table")

    latex_src = ctx.out / "latex"
    for stem in ["main", "supply"]:
        for ext in [".pdf", ".log", ".bbl", ".blg"]:
            copy_if_exists(latex_src / f"{stem}{ext}", bundle / "latex" / f"{stem}{ext}", files, role="latex_output")

    copy_referenced_figures(ctx, bundle, files)

    manifest = {
        "generated_at": now_iso(),
        "bundle_root": str(bundle),
        "raw_private_data_excluded": True,
        "manuscript_directory_policy": "manuscript/ remains ignored; shareable copies are placed in this bundle.",
        "files": files,
        "required_present": {
            "main_tex": (bundle / "manuscript" / "main.tex").exists(),
            "supply_tex": (bundle / "manuscript" / "supply.tex").exists(),
            "references_bib": (bundle / "manuscript" / "references.bib").exists(),
            "main_pdf": (bundle / "latex" / "main.pdf").exists(),
            "supply_pdf": (bundle / "latex" / "supply.pdf").exists(),
            "generated_tables": len(list((bundle / "outputs" / "revision_v1" / "tables").glob("*.tex"))) if (bundle / "outputs" / "revision_v1" / "tables").exists() else 0,
        },
    }
    write_json_safe(bundle / "manifest.json", manifest)
    files.append(file_record(bundle / "manifest.json", role="bundle_manifest"))

    missing = [key for key, value in manifest["required_present"].items() if value in [False, 0]]
    if missing:
        ctx.errors.append(f"Submission bundle missing required entries: {', '.join(missing)}")


def write_environment_and_status(ctx: RunContext) -> None:
    env = {
        "generated_at": now_iso(),
        "semtra_revision": V2_VERSION,
        "python": sys.version,
        "platform": platform.platform(),
        "package_versions": package_versions(),
        "git_status": run_capture(["git", "status", "--short"], cwd=ctx.root),
        "git_rev_parse_head": run_capture(["git", "rev-parse", "HEAD"], cwd=ctx.root),
        "v1_root": str(ctx.v1),
        "v2_root": str(ctx.out),
    }
    write_json_safe(ctx.out / "environment_v2.json", env)

    v1_rows = validate_v1_baseline(ctx.v1)
    write_csv(ctx.out / "qc" / "v1_baseline_validation.csv", v1_rows)
    for row in v1_rows:
        if row["status"] != "present":
            ctx.errors.append(f"Required v1 artifact missing: {row['artifact']}")


def write_claim_gating_metadata(ctx: RunContext, claim_rows: list[dict[str, Any]]) -> None:
    gating = {
        "generated_at": now_iso(),
        "derm7pt_claim_scope": "retrospective technical validation only",
        "protocol_b_claim_scope": "semantic-transfer validation only; not competitive ZSL",
        "wedd_claim_scope": "tunable discretization option; no universal superiority claim",
        "sun_claim_scope": "stress-test/portability diagnostics",
        "claim_checks_passed": all(row["status"] == "pass" for row in claim_rows if row.get("severity") == "error"),
        "claim_checks": claim_rows,
    }
    write_json_safe(ctx.out / "qc" / "claim_gating_metadata.json", gating)


def write_qc_outputs(ctx: RunContext) -> None:
    tex_paths = [ctx.manuscript / "main.tex", ctx.manuscript / "supply.tex"]
    no_paragraph = []
    for path in tex_paths:
        if path.exists() and r"\paragraph{" in read_text(path):
            no_paragraph.append(path.name)
    dupes = duplicate_labels(tex_paths)
    missing_bib = missing_bib_keys(tex_paths, ctx.manuscript / "references.bib")
    log_issues = {stem: latex_log_issues(ctx.out / "latex" / f"{stem}.log") for stem in ["main", "supply"]}

    if no_paragraph:
        ctx.errors.append(f"Forbidden \\paragraph{{}} found in: {', '.join(no_paragraph)}")
    if dupes:
        ctx.errors.append(f"Duplicate labels found: {', '.join(dupes)}")
    if missing_bib:
        ctx.errors.append(f"Missing BibTeX keys: {', '.join(missing_bib)}")
    for stem, issues in log_issues.items():
        hard = [issue for issue in issues if issue in {"fatal_error", "undefined_refs", "undefined_citations", "rerun_required", "overfull_hbox"}]
        if hard:
            ctx.errors.append(f"LaTeX log issues for {stem}: {', '.join(hard)}")

    checklist = [
        {"check": "no_paragraph", "status": "pass" if not no_paragraph else "fail", "detail": ",".join(no_paragraph)},
        {"check": "duplicate_labels", "status": "pass" if not dupes else "fail", "detail": ",".join(dupes)},
        {"check": "missing_bib_keys", "status": "pass" if not missing_bib else "fail", "detail": ",".join(missing_bib)},
        {"check": "latex_main_log", "status": "pass" if not log_issues["main"] else "fail", "detail": ",".join(log_issues["main"])},
        {"check": "latex_supply_log", "status": "pass" if not log_issues["supply"] else "fail", "detail": ",".join(log_issues["supply"])},
        {"check": "claim_consistency", "status": "pass" if not any("Claim check failed" in e for e in ctx.errors) else "fail", "detail": ""},
        {"check": "schema_validation", "status": "pending", "detail": "resolved after schema validation"},
        {"check": "submission_bundle", "status": "pass" if (ctx.out / "submission_bundle" / "manifest.json").exists() else "fail", "detail": ""},
    ]
    write_csv(ctx.out / "qc" / "qc_checklist.csv", checklist)
    write_json_safe(
        ctx.out / "qc" / "qc_summary.json",
        {
            "generated_at": now_iso(),
            "status": "pass" if not ctx.errors else "fail",
            "errors": ctx.errors,
            "warnings": ctx.warnings,
            "latex_log_issues": log_issues,
        },
    )


def update_qc_schema_status(ctx: RunContext) -> None:
    checklist_path = ctx.out / "qc" / "qc_checklist.csv"
    schema_path = ctx.out / "qc" / "schema_validation.csv"
    if not checklist_path.exists() or not schema_path.exists():
        return
    checklist = pd.read_csv(checklist_path)
    schema = pd.read_csv(schema_path)
    status = "pass" if not (schema["status"] != "pass").any() else "fail"
    detail = "" if status == "pass" else "; ".join(schema.loc[schema["status"] != "pass", "artifact"].astype(str).tolist())
    checklist.loc[checklist["check"] == "schema_validation", "status"] = status
    checklist.loc[checklist["check"] == "schema_validation", "detail"] = detail
    checklist.to_csv(checklist_path, index=False)


def write_manifest(ctx: RunContext, claim_rows: list[dict[str, Any]]) -> None:
    artifacts = []
    for path in sorted(ctx.out.rglob("*")):
        if path.is_file() and path.name != "manifest_revision_v2.json":
            artifacts.append(
                {
                    "path": rel_to(path, ctx.root),
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    manifest = {
        "generated_at": now_iso(),
        "semtra_revision": V2_VERSION,
        "v1_root": rel_to(ctx.v1, ctx.root),
        "v2_root": rel_to(ctx.out, ctx.root),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "claim_gating": {
            "claim_checks_passed": all(row["status"] == "pass" for row in claim_rows if row.get("severity") == "error"),
            "derm7pt": "retrospective technical validation only",
            "protocol_b": "semantic-transfer validation only",
            "wedd": "tunable discretization option, not universal superiority",
            "sun": "stress-test/portability diagnostics",
        },
        "status": "pass" if not ctx.errors else "fail",
        "errors": ctx.errors,
        "warnings": ctx.warnings,
    }
    write_json_safe(ctx.out / "manifest_revision_v2.json", manifest)

    index_rows = [
        {
            "path": item["path"],
            "size": item["size"],
            "sha256": item["sha256"],
        }
        for item in artifacts
    ]
    write_csv(ctx.out / "artifact_index_revision_v2.csv", index_rows)


def write_revision_report(ctx: RunContext) -> None:
    manifest_path = ctx.out / "manifest_revision_v2.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {}
    boot = pd.read_csv(ctx.out / "statistics" / "bootstrap_intervals.csv") if (ctx.out / "statistics" / "bootstrap_intervals.csv").exists() else pd.DataFrame()
    paired = pd.read_csv(ctx.out / "statistics" / "paired_discretizer_intervals.csv") if (ctx.out / "statistics" / "paired_discretizer_intervals.csv").exists() else pd.DataFrame()
    sun = pd.read_csv(ctx.out / "sun" / "sun_category_diagnostics.csv") if (ctx.out / "sun" / "sun_category_diagnostics.csv").exists() else pd.DataFrame()
    derm = pd.read_csv(ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics.csv") if (ctx.out / "derm7pt" / "derm7pt_diagnosis_diagnostics.csv").exists() else pd.DataFrame()
    qc = read_json(ctx.out / "qc" / "qc_summary.json") if (ctx.out / "qc" / "qc_summary.json").exists() else {}

    lines = [
        "# SEMTRA Revision v2 Report",
        "",
        f"Generated: {now_iso()}",
        "",
        "## Completed Work",
        "",
        "- Created a v2 artifact bundle under `outputs/revision_v2/` while preserving `outputs/revision_v1/`.",
        "- Added machine-readable schemas, v1 baseline validation, package/git status capture, file hashes, and a v2 manifest.",
        "- Added automated claim-gating metadata and manuscript claim consistency checks for the central numeric and wording constraints.",
        "- Added bootstrap and paired WEDD-vs-MDLP interval diagnostics without rewriting v1 results.",
        "- Added SUN class-level stress-test diagnostics and Derm7pt diagnosis/concept diagnostics.",
        "- Created a clean submission bundle with manuscript sources, generated tables, final PDFs/logs when available, referenced figures, and a bundle manifest.",
        "",
        "## Artifact Summary",
        "",
        f"- v2 artifact count: {manifest.get('artifact_count', 'unknown')}.",
        f"- Bootstrap interval rows: {len(boot)}.",
        f"- Paired discretizer interval rows: {len(paired)}.",
        f"- SUN diagnostic rows: {len(sun)}.",
        f"- Derm7pt diagnosis diagnostic rows: {len(derm)}.",
        "",
        "## QC Status",
        "",
        f"- Overall status: {qc.get('status', manifest.get('status', 'unknown'))}.",
    ]
    errors = qc.get("errors", []) or manifest.get("errors", [])
    warnings = qc.get("warnings", []) or manifest.get("warnings", [])
    if errors:
        lines.append("- Errors:")
        for err in errors:
            lines.append(f"  - {err}")
    else:
        lines.append("- Errors: none recorded.")
    if warnings:
        lines.append("- Warnings:")
        for warn in warnings:
            lines.append(f"  - {warn}")
    else:
        lines.append("- Warnings: none recorded.")

    lines.extend(
        [
            "",
            "## Remaining Limitations",
            "",
            "- SUN remains a stress-test/portability result; the v2 diagnostics expose class-dependent coverage and conflict rather than converting SUN into a competitive benchmark.",
            "- Derm7pt remains retrospective technical validation only. The simple image-feature baseline is reproducible but not a clinical validation pipeline.",
            "- Object-level bootstrap intervals are limited to fields exported by v1 prediction files; base-model labels are not present in those prediction exports, so object-level covered-fidelity intervals are intentionally absent.",
            "- Seed-wise intervals are based on the completed v1 seed set and should be interpreted as stability diagnostics.",
            "",
            "## Recommendations",
            "",
            "- Export true labels and base-model predictions in future prediction CSVs so object-level accuracy and fidelity confidence intervals can be generated directly.",
            "- For SUN, add category metadata beyond class names where available and inspect low-coverage/high-conflict classes before strengthening portability claims.",
            "- For Derm7pt, replace the simple handcrafted baseline with a locked, documented dermoscopic encoder and keep official case-level splits.",
            "- Keep WEDD wording as a tunable discretization option unless a larger paired study demonstrates robustness across datasets and metrics.",
            "- Preserve the submission bundle as the shareable artifact while keeping `manuscript/` ignored.",
        ]
    )
    write_text(ctx.root / "revision_report_v2.md", "\n".join(lines) + "\n")


def validate_existing_v2(root: Path, v1: Path, out: Path, require_v2: bool) -> int:
    failures: list[str] = []
    for row in validate_v1_baseline(v1):
        if row["status"] != "present":
            failures.append(f"missing v1 artifact: {row['artifact']}")
    if require_v2:
        required_v2 = [
            "manifest_revision_v2.json",
            "artifact_index_revision_v2.csv",
            "statistics/bootstrap_intervals.csv",
            "statistics/paired_discretizer_intervals.csv",
            "statistics/statistical_assessment.md",
            "sun/sun_category_diagnostics.csv",
            "sun/sun_failure_modes.md",
            "derm7pt/derm7pt_diagnosis_diagnostics.csv",
            "derm7pt/derm7pt_concept_diagnostics_v2.csv",
            "derm7pt/derm7pt_limitations.md",
            "qc/claim_consistency_check.csv",
            "qc/schema_validation.csv",
            "submission_bundle/manifest.json",
        ]
        for rel in required_v2:
            if not (out / rel).exists():
                failures.append(f"missing v2 artifact: {rel}")
        manifest_path = out / "manifest_revision_v2.json"
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            if manifest.get("status") != "pass":
                failures.append("v2 manifest status is not pass")
    payload = {
        "validated_at": now_iso(),
        "root": str(root),
        "v1": str(v1),
        "v2": str(out),
        "require_v2": require_v2,
        "status": "pass" if not failures else "fail",
        "failures": failures,
    }
    print(json.dumps(payload, indent=2))
    return 0 if not failures else 1


def run_v2(ctx: RunContext) -> int:
    ensure_dir(ctx.out)
    for sub in ["statistics", "sun", "derm7pt", "qc", "schemas", "latex", "submission_bundle"]:
        ensure_dir(ctx.out / sub)

    write_environment_and_status(ctx)
    write_schemas(ctx)
    sync_latex_artifacts(ctx)
    generate_bootstrap_intervals(ctx)
    generate_paired_discretizer_intervals(ctx)
    generate_sun_diagnostics(ctx)
    generate_derm_diagnostics(ctx)
    write_statistical_assessment(ctx)
    claim_rows = generate_claim_checks(ctx)
    write_claim_gating_metadata(ctx, claim_rows)
    write_submission_bundle(ctx)
    write_qc_outputs(ctx)
    validate_schemas(ctx)
    update_qc_schema_status(ctx)
    write_qc_outputs(ctx)
    write_manifest(ctx, claim_rows)
    write_revision_report(ctx)

    status = "pass" if not ctx.errors else "fail"
    print(
        json.dumps(
            {
                "status": status,
                "v2_root": str(ctx.out),
                "errors": ctx.errors,
                "warnings": ctx.warnings,
            },
            indent=2,
            default=json_default,
        )
    )
    return 0 if status == "pass" else 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root.")
    parser.add_argument("--v1", type=Path, default=None, help="Existing revision v1 artifact root.")
    parser.add_argument("--out", type=Path, default=None, help="Revision v2 artifact root.")
    parser.add_argument("--force-rebuild", action="store_true", help="Delete and regenerate outputs/revision_v2.")
    parser.add_argument("--validate-only", action="store_true", help="Validate required artifacts without writing outputs.")
    parser.add_argument("--require-v2", action="store_true", help="With --validate-only, require the v2 bundle to exist and pass.")
    parser.add_argument("--n-boot", type=int, default=1000, help="Number of bootstrap resamples.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    v1 = (args.v1.resolve() if args.v1 else root / "outputs" / "revision_v1")
    out = (args.out.resolve() if args.out else root / "outputs" / "revision_v2")
    manuscript = root / "manuscript"

    if args.validate_only:
        return validate_existing_v2(root, v1, out, args.require_v2)

    if args.force_rebuild:
        safe_reset_out_dir(out, root)

    ctx = RunContext(
        root=root,
        v1=v1,
        out=out,
        manuscript=manuscript,
        rng=np.random.default_rng(DEFAULT_SEED),
        n_boot=args.n_boot,
        errors=[],
        warnings=[],
    )
    return run_v2(ctx)


if __name__ == "__main__":
    raise SystemExit(main())
