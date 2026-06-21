#!/usr/bin/env python3
"""Core algorithms for Paper 1 PoC XAI experiments.

The functions in this module deliberately use generic XAI terminology. They implement
transition-matrix reconstruction, weighted entropy-density discretization (WEDD),
rough-set granulation, reduct minimization, rule induction, and conflict-aware inference.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from collections import Counter, defaultdict
import json
import math
import os
import zipfile

import numpy as np
import pandas as pd

from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.tree import DecisionTreeClassifier


EPS = 1e-12


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: str | Path, obj: Any) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def tex_escape(s: Any) -> str:
    text = str(s)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return text


def clean_name(s: Any) -> str:
    return str(s).replace("+", " ").replace("_", " ")


def entropy(labels: np.ndarray) -> float:
    if len(labels) == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    p = counts.astype(float) / counts.sum()
    return float(-(p * np.log2(p + EPS)).sum())


def macro_f1_safe(y_true: np.ndarray, y_pred: np.ndarray, labels: Optional[Sequence[int]] = None) -> float:
    if len(y_true) == 0:
        return float("nan")
    return float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0))


def accuracy_safe(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len(y_true) == 0:
        return float("nan")
    return float(accuracy_score(y_true, y_pred))


# -----------------------------------------------------------------------------
# AwA2 loading and preprocessing
# -----------------------------------------------------------------------------


def maybe_extract_awa2(awa2_zip: str | Path, work_dir: str | Path) -> Path:
    """Return a directory containing the AwA2 parquet files.

    If `awa2_zip` is already a directory, it is returned. Otherwise the archive is
    extracted into `work_dir` only if the expected files are not already present.
    """
    src = Path(awa2_zip)
    if src.is_dir():
        return src
    out = ensure_dir(work_dir)
    expected = out / "AwA2-features.parquet"
    if expected.exists():
        return out
    with zipfile.ZipFile(src, "r") as zf:
        zf.extractall(out)
    return out


@dataclass
class AwA2Data:
    A: np.ndarray
    y: np.ndarray
    B_obj_raw: np.ndarray
    B_class_raw: np.ndarray
    class_names: List[str]
    predicate_names: List[str]
    filenames: List[str]
    labels_raw: np.ndarray


def load_awa2(awa2_dir: str | Path) -> AwA2Data:
    p = Path(awa2_dir)
    A = pd.read_parquet(p / "AwA2-features.parquet").to_numpy(dtype=np.float32)
    labels_raw = pd.read_parquet(p / "AwA2-labels.parquet")["label"].to_numpy(dtype=int)
    classes = pd.read_parquet(p / "classes.parquet")
    predicates = pd.read_parquet(p / "predicates.parquet")
    B_class = pd.read_parquet(p / "predicate-matrix-continuous.parquet").to_numpy(dtype=float)
    filenames = pd.read_parquet(p / "AwA2-filenames.parquet")["filename"].astype(str).tolist()

    # AwA2 labels are one-based class identifiers aligned to the class table.
    y = labels_raw.astype(int) - 1
    class_names = [clean_name(x) for x in classes["class_name"].tolist()]
    predicate_names = [clean_name(x) for x in predicates["predicate_name"].tolist()]
    B_obj = B_class[y]
    return AwA2Data(A=A, y=y, B_obj_raw=B_obj, B_class_raw=B_class,
                    class_names=class_names, predicate_names=predicate_names,
                    filenames=filenames, labels_raw=labels_raw)


@dataclass
class TransitionResult:
    scaler_A: StandardScaler
    svd: TruncatedSVD
    scaler_B: MinMaxScaler
    ridge: Ridge
    alpha: float
    n_components: int
    explained_variance: float
    X_train: np.ndarray
    X_val: np.ndarray
    X_test: np.ndarray
    Y_train: np.ndarray
    Y_val: np.ndarray
    Y_test: np.ndarray
    Yhat_train: np.ndarray
    Yhat_val: np.ndarray
    Yhat_test: np.ndarray
    salience: np.ndarray
    metrics: Dict[str, Any]


def fit_transition(
    A_train: np.ndarray,
    A_val: np.ndarray,
    A_test: np.ndarray,
    B_train: np.ndarray,
    B_val: np.ndarray,
    B_test: np.ndarray,
    n_components: int = 256,
    ridge_grid: Sequence[float] = (0.01, 0.1, 1.0, 10.0, 100.0),
    seed: int = 42,
) -> TransitionResult:
    """Fit a compressed ridge transition layer Bhat = A T + intercept."""
    n_components = int(min(n_components, A_train.shape[1] - 1, A_train.shape[0] - 1))
    scaler_A = StandardScaler(with_mean=False)
    A_train_s = scaler_A.fit_transform(A_train).astype(np.float32)
    A_val_s = scaler_A.transform(A_val).astype(np.float32)
    A_test_s = scaler_A.transform(A_test).astype(np.float32)

    svd = TruncatedSVD(n_components=n_components, random_state=seed, n_iter=2)
    # Fit the compression basis on a deterministic subset when the representation
    # matrix is large. This keeps the experiment tractable while preserving an
    # SVD-based projection for every row.
    max_svd_rows = min(5000, A_train_s.shape[0])
    if A_train_s.shape[0] > max_svd_rows:
        rng = np.random.default_rng(seed)
        fit_rows = rng.choice(np.arange(A_train_s.shape[0]), size=max_svd_rows, replace=False)
        svd.fit(A_train_s[fit_rows])
        X_train = svd.transform(A_train_s).astype(np.float32)
    else:
        X_train = svd.fit_transform(A_train_s).astype(np.float32)
    X_val = svd.transform(A_val_s).astype(np.float32)
    X_test = svd.transform(A_test_s).astype(np.float32)
    explained = float(np.sum(svd.explained_variance_ratio_))

    scaler_B = MinMaxScaler()
    Y_train = scaler_B.fit_transform(B_train)
    Y_val = scaler_B.transform(B_val)
    Y_test = scaler_B.transform(B_test)
    Y_train = np.clip(Y_train, 0.0, 1.0)
    Y_val = np.clip(Y_val, 0.0, 1.0)
    Y_test = np.clip(Y_test, 0.0, 1.0)

    best = None
    candidates = []
    for alpha in ridge_grid:
        model = Ridge(alpha=float(alpha), fit_intercept=True, random_state=seed)
        model.fit(X_train, Y_train)
        pred_val = np.clip(model.predict(X_val), 0.0, 1.0)
        mae = float(np.mean(np.abs(pred_val - Y_val)))
        rmse = float(np.sqrt(np.mean((pred_val - Y_val) ** 2)))
        candidates.append({"ridge_alpha": float(alpha), "val_mae": mae, "val_rmse": rmse})
        if best is None or mae < best[0]:
            best = (mae, rmse, float(alpha), model)
    assert best is not None
    _, _, alpha, ridge = best
    Yhat_train = np.clip(ridge.predict(X_train), 0.0, 1.0)
    Yhat_val = np.clip(ridge.predict(X_val), 0.0, 1.0)
    Yhat_test = np.clip(ridge.predict(X_test), 0.0, 1.0)

    def aggregate(Y, Yhat, split):
        err = Yhat - Y
        corrs = []
        for j in range(Y.shape[1]):
            if np.std(Y[:, j]) < EPS or np.std(Yhat[:, j]) < EPS:
                continue
            corrs.append(np.corrcoef(Y[:, j], Yhat[:, j])[0, 1])
        return {
            f"{split}_mae": float(np.mean(np.abs(err))),
            f"{split}_rmse": float(np.sqrt(np.mean(err ** 2))),
            f"{split}_semantic_correlation_mean": float(np.nanmean(corrs)) if corrs else float("nan"),
        }
    metrics = {
        "n_components": n_components,
        "explained_variance_ratio_sum": explained,
        "selected_ridge_alpha": alpha,
        "ridge_grid": candidates,
    }
    metrics.update(aggregate(Y_train, Yhat_train, "train"))
    metrics.update(aggregate(Y_val, Yhat_val, "val"))
    metrics.update(aggregate(Y_test, Yhat_test, "test"))
    salience = np.linalg.norm(ridge.coef_.T, axis=0)  # coef_: targets x features -> T = coef_.T
    return TransitionResult(scaler_A, svd, scaler_B, ridge, alpha, n_components, explained,
                            X_train, X_val, X_test, Y_train, Y_val, Y_test,
                            Yhat_train, Yhat_val, Yhat_test, salience, metrics)


def nearest_prototype_predict(Yhat: np.ndarray, class_prototypes: np.ndarray, class_labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    # squared Euclidean distances, vectorized in chunks to control memory.
    preds = []
    dmins = []
    for start in range(0, len(Yhat), 4096):
        chunk = Yhat[start:start + 4096]
        d = ((chunk[:, None, :] - class_prototypes[None, :, :]) ** 2).sum(axis=2)
        idx = np.argmin(d, axis=1)
        preds.append(class_labels[idx])
        dmins.append(np.sqrt(d[np.arange(len(chunk)), idx]))
    return np.concatenate(preds), np.concatenate(dmins)


# -----------------------------------------------------------------------------
# WEDD discretization
# -----------------------------------------------------------------------------


def candidate_thresholds(x: np.ndarray, max_candidates: int = 96) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return np.array([], dtype=float)
    uniq = np.unique(x)
    if len(uniq) <= max_candidates + 1:
        return (uniq[:-1] + uniq[1:]) / 2.0
    qs = np.linspace(1.0, 99.0, max_candidates)
    vals = np.unique(np.quantile(x, qs / 100.0))
    vals = vals[(vals > np.min(x)) & (vals < np.max(x))]
    return vals.astype(float)


def local_density(values_sorted: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    if len(values_sorted) < 2 or len(candidates) == 0:
        return np.zeros_like(candidates, dtype=float)
    iqr = np.subtract(*np.percentile(values_sorted, [75, 25]))
    sd = np.std(values_sorted)
    h = 0.9 * min(sd if sd > EPS else 1.0, iqr / 1.34 if iqr > EPS else sd if sd > EPS else 1.0) * (len(values_sorted) ** (-1 / 5))
    if not np.isfinite(h) or h <= EPS:
        h = max(np.ptp(values_sorted) / 20.0, 1e-3)
    left = np.searchsorted(values_sorted, candidates - h, side="left")
    right = np.searchsorted(values_sorted, candidates + h, side="right")
    dens = (right - left) / max(1, len(values_sorted)) / (2.0 * h)
    return dens.astype(float)


def threshold_objective(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.65,
    min_support: int = 30,
    max_candidates: int = 96,
) -> pd.DataFrame:
    """Fast WEDD objective table for one split node.

    This implementation sorts once and computes class entropies from cumulative
    label counts rather than rescanning the label vector for every candidate.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    finite = np.isfinite(x)
    x = x[finite]
    y = y[finite]
    if len(x) < 2 * min_support or len(np.unique(x)) < 2:
        return pd.DataFrame()
    cands = candidate_thresholds(x, max_candidates=max_candidates)
    if len(cands) == 0:
        return pd.DataFrame()

    order = np.argsort(x)
    xs = x[order]
    _, yi = np.unique(y[order], return_inverse=True)
    n_classes = int(yi.max()) + 1
    n = len(xs)
    # cumulative counts after each sorted position
    cum = np.zeros((n, n_classes), dtype=np.int32)
    cum[np.arange(n), yi] = 1
    cum = np.cumsum(cum, axis=0)
    total = cum[-1].astype(float)

    pos = np.searchsorted(xs, cands, side="right")
    valid = (pos >= min_support) & (pos <= n - min_support)
    cands = cands[valid]
    pos = pos[valid]
    if len(cands) == 0:
        return pd.DataFrame()

    left_counts = cum[pos - 1].astype(float)
    right_counts = total[None, :] - left_counts
    n_l = left_counts.sum(axis=1)
    n_r = right_counts.sum(axis=1)

    def counts_entropy(counts: np.ndarray) -> np.ndarray:
        denom = counts.sum(axis=1, keepdims=True)
        p = counts / np.maximum(denom, EPS)
        return -(p * np.log2(p + EPS)).sum(axis=1)

    H_left = counts_entropy(left_counts)
    H_right = counts_entropy(right_counts)
    E = (n_l / n) * H_left + (n_r / n) * H_right
    parent_counts = total[None, :]
    parent_H = float(counts_entropy(parent_counts)[0])
    dens = local_density(xs, cands)
    df = pd.DataFrame({
        "threshold": cands.astype(float),
        "entropy": E.astype(float),
        "density": dens.astype(float),
        "gain": (parent_H - E).astype(float),
        "n_left": n_l.astype(int),
        "n_right": n_r.astype(int),
    })
    for col in ["entropy", "density"]:
        lo = float(df[col].min())
        hi = float(df[col].max())
        if abs(hi - lo) < EPS:
            df[col + "_norm"] = 0.0
        else:
            df[col + "_norm"] = (df[col] - lo) / (hi - lo)
    df["objective"] = alpha * df["entropy_norm"] + (1 - alpha) * df["density_norm"]
    return df.sort_values("objective", ascending=True).reset_index(drop=True)


def wedd_thresholds(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.65,
    max_depth: int = 2,
    min_support: int = 30,
    min_gain: float = 0.002,
    max_candidates: int = 96,
) -> Tuple[List[float], List[Dict[str, Any]]]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y)
    thresholds: List[float] = []
    provenance: List[Dict[str, Any]] = []

    def rec(indices: np.ndarray, depth: int) -> None:
        if depth >= max_depth or len(indices) < 2 * min_support:
            return
        xi = x[indices]
        yi = y[indices]
        df = threshold_objective(xi, yi, alpha=alpha, min_support=min_support, max_candidates=max_candidates)
        if df.empty:
            return
        row = df.iloc[0].to_dict()
        if alpha > 0 and row["gain"] < min_gain:
            return
        t = float(row["threshold"])
        thresholds.append(t)
        row.update({"depth": int(depth), "n": int(len(indices)), "alpha": float(alpha)})
        provenance.append(row)
        left_idx = indices[xi <= t]
        right_idx = indices[xi > t]
        rec(left_idx, depth + 1)
        rec(right_idx, depth + 1)

    rec(np.arange(len(x)), 0)
    thresholds = sorted(set([round(float(t), 10) for t in thresholds]))
    return thresholds, provenance


def fit_discretizers(Yhat_train: np.ndarray, y_train: np.ndarray, attr_indices: Sequence[int], alpha: float, max_depth: int = 2,
                     min_support: int = 30) -> Tuple[Dict[int, List[float]], pd.DataFrame, Dict[int, pd.DataFrame]]:
    thresholds: Dict[int, List[float]] = {}
    prov_rows = []
    objective_examples = {}
    for j in attr_indices:
        thrs, prov = wedd_thresholds(Yhat_train[:, j], y_train, alpha=alpha, max_depth=max_depth, min_support=min_support)
        thresholds[int(j)] = thrs
        for p in prov:
            row = dict(p)
            row["attribute_index"] = int(j)
            prov_rows.append(row)
        # Store full objective at root for figure examples.
        objective_examples[int(j)] = threshold_objective(Yhat_train[:, j], y_train, alpha=alpha, min_support=min_support)
    return thresholds, pd.DataFrame(prov_rows), objective_examples


def quantize(Yhat: np.ndarray, attr_indices: Sequence[int], thresholds: Dict[int, List[float]]) -> np.ndarray:
    Z = np.zeros((Yhat.shape[0], len(attr_indices)), dtype=np.int16)
    for p, j in enumerate(attr_indices):
        Z[:, p] = np.digitize(Yhat[:, j], thresholds.get(int(j), []), right=False).astype(np.int16)
    return Z


# -----------------------------------------------------------------------------
# Rough-set granules, reducts, rules, and inference
# -----------------------------------------------------------------------------


def granule_table(Z: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    groups = defaultdict(list)
    for i, row in enumerate(Z):
        groups[tuple(int(v) for v in row)].append(i)
    rows = []
    for sig, idx in groups.items():
        labels, counts = np.unique(y[idx], return_counts=True)
        order = np.argsort(counts)[::-1]
        labels = labels[order]
        counts = counts[order]
        support = int(counts.sum())
        purity = float(counts[0] / support)
        rows.append({
            "signature": sig,
            "support": support,
            "majority_label": int(labels[0]),
            "majority_count": int(counts[0]),
            "purity": purity,
            "n_labels": int(len(labels)),
            "is_deterministic": bool(len(labels) == 1),
            "label_counts": {int(a): int(b) for a, b in zip(labels, counts)},
        })
    return pd.DataFrame(rows).sort_values(["support", "purity"], ascending=[False, False]).reset_index(drop=True)


def rule_stats(antecedent: Dict[int, int], consequent: int, Z: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    if not antecedent:
        mask = np.ones(Z.shape[0], dtype=bool)
    else:
        mask = np.ones(Z.shape[0], dtype=bool)
        for a, state in antecedent.items():
            mask &= Z[:, int(a)] == int(state)
    support = int(mask.sum())
    if support == 0:
        return {"support": 0, "confidence": 0.0, "coverage": 0.0, "conflict_count": 0, "covered_indices": []}
    covered_y = y[mask]
    good = int(np.sum(covered_y == consequent))
    conflict = int(support - good)
    return {
        "support": support,
        "confidence": float(good / support),
        "coverage": float(support / len(y)),
        "conflict_count": conflict,
        "covered_indices": np.where(mask)[0].astype(int).tolist(),
    }


def reduce_antecedent(
    antecedent: Dict[int, int],
    consequent: int,
    Z: np.ndarray,
    y: np.ndarray,
    min_confidence: float,
    min_support: int,
    attr_priority: Optional[Sequence[int]] = None,
) -> Tuple[Dict[int, int], Dict[str, Any], int]:
    current = dict(antecedent)
    original_len = len(current)
    if attr_priority is None:
        removal_order = list(current.keys())
    else:
        # Remove lower-priority attributes first. attr_priority is high-to-low; reverse it.
        rank = {int(a): r for r, a in enumerate(attr_priority)}
        removal_order = sorted(current.keys(), key=lambda a: rank.get(int(a), 10_000), reverse=True)
    improved = True
    while improved and len(current) > 1:
        improved = False
        for a in list(removal_order):
            if a not in current or len(current) <= 1:
                continue
            cand = dict(current)
            cand.pop(a)
            st = rule_stats(cand, consequent, Z, y)
            if st["support"] >= min_support and st["confidence"] >= min_confidence:
                current = cand
                improved = True
    final_stats = rule_stats(current, consequent, Z, y)
    return current, final_stats, original_len


def class_mode_signatures(Z: np.ndarray, y: np.ndarray, labels: Sequence[int]) -> Dict[int, np.ndarray]:
    modes = {}
    for label in labels:
        rows = Z[y == label]
        if len(rows) == 0:
            continue
        m = []
        for j in range(Z.shape[1]):
            counts = np.bincount(rows[:, j].astype(int), minlength=int(rows[:, j].max()) + 1)
            m.append(int(np.argmax(counts)))
        modes[int(label)] = np.array(m, dtype=np.int16)
    return modes


def induce_rules(
    Z: np.ndarray,
    y: np.ndarray,
    attr_names: Sequence[str],
    class_names: Sequence[str],
    min_confidence: float = 0.90,
    min_support: int = 20,
    max_rules_per_class: int = 5,
    attr_scores: Optional[np.ndarray] = None,
    allow_prototypes: bool = True,
    reduce: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    labels = sorted(np.unique(y).astype(int).tolist())
    granules = granule_table(Z, y)
    if attr_scores is None:
        attr_priority = list(range(Z.shape[1]))
    else:
        attr_priority = list(np.argsort(attr_scores)[::-1].astype(int))
    rules: List[Dict[str, Any]] = []
    rule_id = 1

    # Rules from high-purity granules (rough-set lower approximation for purity=1,
    # support-aware boundary rules for purity >= min_confidence). A cap avoids
    # pathological ablation settings where many near-identical granules generate
    # redundant reduction calls.
    eligible_granules = granules[(granules["support"] >= min_support) & (granules["purity"] >= min_confidence)].head(500)
    for _, g in eligible_granules.iterrows():
        antecedent = {i: int(v) for i, v in enumerate(g["signature"])}
        consequent = int(g["majority_label"])
        if reduce:
            red, st, original_len = reduce_antecedent(antecedent, consequent, Z, y, min_confidence, min_support, attr_priority)
        else:
            red = antecedent
            st = rule_stats(red, consequent, Z, y)
            original_len = len(antecedent)
        if st["support"] < min_support or st["confidence"] < min_confidence:
            continue
        source = "strict_lower" if bool(g["is_deterministic"]) else "boundary_high_confidence"
        rules.append(_make_rule_row(rule_id, red, consequent, st, original_len, source, attr_names, class_names))
        rule_id += 1

    # Deduplicate by consequent and antecedent; keep best support/confidence.
    rules = _dedupe_rules(rules)

    # Ensure each class can be represented by at least one class-template rule when
    # strict granules are too sparse.
    if allow_prototypes:
        existing = {int(r["consequent"]): 0 for r in rules}
        modes = class_mode_signatures(Z, y, labels)
        for label in labels:
            if label in existing:
                continue
            rows = Z[y == label]
            if len(rows) < min_support:
                continue
            # Attribute states ranked by one-vs-rest precision for this class.
            candidates = []
            for a in range(Z.shape[1]):
                state = int(modes[label][a])
                mask = Z[:, a] == state
                support = int(mask.sum())
                conf = float(np.mean(y[mask] == label)) if support > 0 else 0.0
                class_cov = float(np.mean(rows[:, a] == state))
                score = conf * 0.7 + class_cov * 0.3
                if attr_scores is not None:
                    score += 0.05 * float(attr_scores[a] / (np.max(attr_scores) + EPS))
                candidates.append((score, a, state))
            candidates.sort(reverse=True)
            antecedent = {}
            best = None
            for _, a, state in candidates[: min(8, len(candidates))]:
                antecedent[int(a)] = int(state)
                st = rule_stats(antecedent, int(label), Z, y)
                if st["support"] >= min_support and st["confidence"] >= max(0.55, min_confidence - 0.20):
                    best = (dict(antecedent), st)
                    break
            if best is None:
                antecedent = {int(a): int(state) for _, a, state in candidates[:4]}
                st = rule_stats(antecedent, int(label), Z, y)
                best = (antecedent, st)
            ant, st = best
            if reduce and st["support"] >= min_support:
                ant, st, original_len = reduce_antecedent(ant, int(label), Z, y, max(0.55, min_confidence - 0.20), min_support, attr_priority)
            else:
                original_len = len(ant)
            rules.append(_make_rule_row(rule_id, ant, int(label), st, original_len, "semantic_prototype", attr_names, class_names))
            rule_id += 1
        rules = _dedupe_rules(rules)

    df = pd.DataFrame(rules)
    if not df.empty:
        df = df.sort_values(["confidence", "support", "antecedent_length"], ascending=[False, False, True]).reset_index(drop=True)
        # Limit per class for readability and inference speed.
        df = df.groupby("consequent", group_keys=False).head(max_rules_per_class).reset_index(drop=True)
        df["rule_id"] = [f"R{i+1:04d}" for i in range(len(df))]
    return df, granules


def _make_rule_row(rule_id: int, antecedent: Dict[int, int], consequent: int, st: Dict[str, Any], original_len: int,
                   source: str, attr_names: Sequence[str], class_names: Sequence[str]) -> Dict[str, Any]:
    ant_parts = [f"{attr_names[a]}=s{state}" for a, state in sorted(antecedent.items())]
    return {
        "rule_id": f"R{rule_id:04d}",
        "antecedent": {str(int(a)): int(s) for a, s in sorted(antecedent.items())},
        "antecedent_text": " AND ".join(ant_parts),
        "consequent": int(consequent),
        "consequent_name": class_names[int(consequent)] if int(consequent) < len(class_names) else str(consequent),
        "support": int(st["support"]),
        "confidence": float(st["confidence"]),
        "coverage": float(st["coverage"]),
        "conflict_count": int(st["conflict_count"]),
        "antecedent_length": int(len(antecedent)),
        "original_antecedent_length": int(original_len),
        "source": source,
        "covered_indices_sample": st.get("covered_indices", [])[:20],
    }


def _dedupe_rules(rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best: Dict[Tuple[int, Tuple[Tuple[str, int], ...]], Dict[str, Any]] = {}
    for r in rules:
        key = (int(r["consequent"]), tuple(sorted((str(k), int(v)) for k, v in r["antecedent"].items())))
        if key not in best:
            best[key] = r
        else:
            old = best[key]
            if (r["confidence"], r["support"], -r["antecedent_length"]) > (old["confidence"], old["support"], -old["antecedent_length"]):
                best[key] = r
    return list(best.values())


def parse_antecedent(rule_row: pd.Series | Dict[str, Any]) -> Dict[int, int]:
    ant = rule_row["antecedent"]
    if isinstance(ant, str):
        ant = json.loads(ant.replace("'", '"'))
    return {int(k): int(v) for k, v in ant.items()}


def match_rule(z: np.ndarray, antecedent: Dict[int, int]) -> bool:
    for a, state in antecedent.items():
        if int(z[int(a)]) != int(state):
            return False
    return True


def infer_rules(
    Z: np.ndarray,
    rules_df: pd.DataFrame,
    class_prototypes_Z: Optional[Dict[int, np.ndarray]] = None,
    fallback_max_distance: float = 0.45,
    conflict_margin: float = 0.05,
) -> pd.DataFrame:
    rows = []
    rules = []
    for _, r in rules_df.iterrows():
        rr = r.to_dict()
        rr["antecedent_parsed"] = parse_antecedent(rr)
        rules.append(rr)
    proto_labels = []
    proto_mat = []
    if class_prototypes_Z:
        for lab, sig in class_prototypes_Z.items():
            proto_labels.append(int(lab))
            proto_mat.append(np.asarray(sig, dtype=int))
        proto_mat = np.vstack(proto_mat) if proto_mat else None
    else:
        proto_mat = None

    for i, z in enumerate(Z):
        activated = []
        votes = defaultdict(float)
        for r in rules:
            if match_rule(z, r["antecedent_parsed"]):
                strength = float(r["confidence"]) * math.log1p(float(r["support"])) / max(1, int(r["antecedent_length"]))
                votes[int(r["consequent"])] += strength
                activated.append(r["rule_id"])
        mode = "exact" if activated else "fallback"
        abstained = False
        pred = None
        conflict = False
        if votes:
            ranked = sorted(votes.items(), key=lambda kv: kv[1], reverse=True)
            pred = int(ranked[0][0])
            if len(ranked) > 1 and ranked[0][1] - ranked[1][1] < conflict_margin * max(1.0, ranked[0][1]):
                conflict = True
                abstained = True
                pred = -1
        else:
            if proto_mat is None:
                abstained = True
                pred = -1
            else:
                d = np.mean(proto_mat != z[None, :], axis=1)
                j = int(np.argmin(d))
                if float(d[j]) <= fallback_max_distance:
                    pred = int(proto_labels[j])
                else:
                    abstained = True
                    pred = -1
        rows.append({
            "row_index": int(i),
            "prediction": int(pred),
            "mode": mode,
            "abstained": bool(abstained),
            "conflict": bool(conflict),
            "activated_rules": ";".join(activated[:10]),
            "n_activated": int(len(activated)),
        })
    return pd.DataFrame(rows)


def prediction_metrics(y_true: np.ndarray, pred_df: pd.DataFrame, labels: Optional[Sequence[int]] = None) -> Dict[str, Any]:
    pred = pred_df["prediction"].to_numpy(dtype=int)
    non_abstain = pred >= 0
    metrics = {
        "coverage": float(np.mean(non_abstain)),
        "abstention_rate": float(1.0 - np.mean(non_abstain)),
        "conflict_rate": float(pred_df["conflict"].mean()),
        "fallback_rate": float(np.mean(pred_df["mode"].to_numpy() == "fallback")),
        "exact_rate": float(np.mean(pred_df["mode"].to_numpy() == "exact")),
        "accuracy_non_abstain": accuracy_safe(y_true[non_abstain], pred[non_abstain]) if non_abstain.any() else float("nan"),
        "macro_f1_non_abstain": macro_f1_safe(y_true[non_abstain], pred[non_abstain], labels=labels) if non_abstain.any() else float("nan"),
    }
    # Count abstention as wrong for all-row accuracy.
    pred_all = pred.copy()
    # Map abstentions to an impossible class so sklearn counts them as incorrect.
    metrics["accuracy_all_with_abstention_wrong"] = float(np.mean(pred_all == y_true))
    return metrics


# -----------------------------------------------------------------------------
# Synthetic benchmark
# -----------------------------------------------------------------------------


def generate_synthetic(seed: int, sigma: float, m: int = 10_000, l: int = 10, k: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[Dict[str, Any]]]:
    rng = np.random.default_rng(seed)
    # Balanced labels: 0 is background, 1-4 are rule classes.
    labels = np.repeat(np.arange(5), m // 5)
    if len(labels) < m:
        labels = np.concatenate([labels, rng.choice(np.arange(5), size=m - len(labels))])
    rng.shuffle(labels)
    B = rng.beta(2.0, 2.0, size=(m, l))

    def set_low(idx, attr): B[idx, attr] = rng.normal(0.18, 0.06, size=len(idx))
    def set_med(idx, attr): B[idx, attr] = rng.normal(0.50, 0.06, size=len(idx))
    def set_high(idx, attr): B[idx, attr] = rng.normal(0.82, 0.06, size=len(idx))

    for c in range(1, 5):
        idx = np.where(labels == c)[0]
        if c == 1:
            set_high(idx, 0); set_low(idx, 2)
        elif c == 2:
            set_med(idx, 1); set_high(idx, 4)
        elif c == 3:
            set_low(idx, 3); set_high(idx, 5); set_med(idx, 7)
        elif c == 4:
            set_high(idx, 6); set_low(idx, 8)
    # Background: discourage accidental rule activation.
    idx0 = np.where(labels == 0)[0]
    B[idx0, :] = rng.beta(2.0, 2.0, size=(len(idx0), l))
    accidental = synthetic_rule_labels(B) > 0
    # Resample accidental background rows a few times.
    for _ in range(4):
        bad = idx0[accidental[idx0]]
        if len(bad) == 0:
            break
        B[bad, :] = rng.beta(2.0, 2.0, size=(len(bad), l))
        accidental = synthetic_rule_labels(B) > 0
    B = np.clip(B, 0.0, 1.0)
    # Recompute labels from intended classes but preserve background generated above.
    y = labels.astype(int)

    W = rng.normal(size=(l, k))
    # Normalize rows to avoid ill-conditioning and add irrelevant dimensions.
    W = W / (np.linalg.norm(W, axis=1, keepdims=True) + EPS)
    Bz = (B - B.mean(axis=0, keepdims=True)) / (B.std(axis=0, keepdims=True) + EPS)
    A = Bz @ W + rng.normal(0.0, sigma, size=(m, k))
    rules = synthetic_ground_truth_rules()
    return A.astype(np.float32), B.astype(float), y.astype(int), rules


def synthetic_ground_truth_rules() -> List[Dict[str, Any]]:
    return [
        {"class": 1, "text": "if b1 is high and b3 is low", "antecedent": {0: "high", 2: "low"}, "thresholds": {"b1_high": 0.70, "b3_low": 0.35}},
        {"class": 2, "text": "if b2 is medium and b5 is high", "antecedent": {1: "medium", 4: "high"}, "thresholds": {"b2_low": 0.35, "b2_high": 0.65, "b5_high": 0.70}},
        {"class": 3, "text": "if b4 is low and b6 is high and b8 is medium", "antecedent": {3: "low", 5: "high", 7: "medium"}, "thresholds": {"b4_low": 0.35, "b6_high": 0.70, "b8_low": 0.35, "b8_high": 0.65}},
        {"class": 4, "text": "if b7 is high and b9 is low", "antecedent": {6: "high", 8: "low"}, "thresholds": {"b7_high": 0.70, "b9_low": 0.35}},
    ]


def synthetic_rule_labels(B: np.ndarray) -> np.ndarray:
    y = np.zeros(B.shape[0], dtype=int)
    r1 = (B[:, 0] > 0.70) & (B[:, 2] < 0.35)
    r2 = (B[:, 1] >= 0.35) & (B[:, 1] <= 0.65) & (B[:, 4] > 0.70)
    r3 = (B[:, 3] < 0.35) & (B[:, 5] > 0.70) & (B[:, 7] >= 0.35) & (B[:, 7] <= 0.65)
    r4 = (B[:, 6] > 0.70) & (B[:, 8] < 0.35)
    y[r1] = 1
    y[r2] = 2
    y[r3] = 3
    y[r4] = 4
    return y


def threshold_recovery_error(thresholds: Dict[int, List[float]]) -> float:
    truth = {0: [0.70], 2: [0.35], 1: [0.35, 0.65], 4: [0.70], 3: [0.35], 5: [0.70], 7: [0.35, 0.65], 6: [0.70], 8: [0.35]}
    errs = []
    for a, ts in truth.items():
        got = thresholds.get(a, [])
        if not got:
            errs.extend([1.0 for _ in ts])
        else:
            for t in ts:
                errs.append(min(abs(float(g) - t) for g in got))
    return float(np.mean(errs)) if errs else float("nan")


def rule_recovery_jaccard(rules_df: pd.DataFrame) -> float:
    truth = {r["class"]: set(r["antecedent"].keys()) for r in synthetic_ground_truth_rules()}
    scores = []
    for cls, gt_attrs in truth.items():
        sub = rules_df[rules_df["consequent"] == cls]
        best = 0.0
        for _, r in sub.iterrows():
            ant = set(parse_antecedent(r).keys())
            if not ant and not gt_attrs:
                score = 1.0
            else:
                score = len(ant & gt_attrs) / max(1, len(ant | gt_attrs))
            best = max(best, score)
        scores.append(best)
    return float(np.mean(scores)) if scores else float("nan")
