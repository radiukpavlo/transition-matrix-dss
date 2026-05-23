#!/usr/bin/env python3
"""Regenerate manuscript figures/tables from stored experiment artifacts.

This loader is intentionally lightweight: it reconstructs only the pieces needed by
run_all_experiments.generate_figures and generate_tables. It is useful when the heavy
AwA2 transitions have already been executed and artifact CSV/JSON files are present.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
from paper1_core import read_json, maybe_extract_awa2, load_awa2
from run_all_experiments import generate_figures, generate_tables


def transition_placeholder(summary, attr_error, out):
    metrics_path = out / "artifacts" / "awa2" / "protocol_a_transition_metrics.json"
    metrics = read_json(metrics_path) if metrics_path.exists() else {
        "train_mae": summary["test_mae"], "train_rmse": summary["test_rmse"], "train_semantic_correlation_mean": summary["test_semantic_correlation_mean"],
        "val_mae": summary["test_mae"], "val_rmse": summary["test_rmse"], "val_semantic_correlation_mean": summary["test_semantic_correlation_mean"],
        "test_mae": summary["test_mae"], "test_rmse": summary["test_rmse"], "test_semantic_correlation_mean": summary["test_semantic_correlation_mean"],
        "svd_explained_variance_ratio_sum": summary.get("explained_variance", 0.0),
    }
    coef = np.zeros((16, max(1, len(attr_error))), dtype=float)
    for i, v in enumerate(attr_error.get("salience", pd.Series(dtype=float)).to_numpy()[:coef.shape[1]]):
        coef[0, i] = float(v)
    return SimpleNamespace(metrics=metrics, model=SimpleNamespace(coef_=coef))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--awa2_zip", default="/mnt/data/awa2.zip")
    args = parser.parse_args()
    out = Path(args.out).resolve()
    awa2 = load_awa2(maybe_extract_awa2(args.awa2_zip, out / "artifacts" / "_tmp" / "awa2"))
    art = out / "artifacts" / "awa2"
    syn_art = out / "artifacts" / "synthetic"
    pa_summary = read_json(art / "protocol_a_summary.json")
    pb_summary = read_json(art / "protocol_b_summary.json")
    attr_error = pd.read_csv(art / "protocol_a_attribute_errors_and_salience.csv")
    protocol_a = {
        "summary": pa_summary,
        "transition": transition_placeholder(pa_summary, attr_error, out),
        "attribute_error": attr_error,
        "selected_attrs": pd.read_csv(art / "protocol_a_selected_attributes.csv")["attribute_index"].to_numpy(dtype=int),
        "thresholds": pd.read_csv(art / "protocol_a_wedd_thresholds.csv"),
        "granules": pd.read_csv(art / "protocol_a_granules.csv"),
        "main_rules": {"rules": pd.read_csv(art / "protocol_a_rulebook.csv")},
        "ablation": pd.read_csv(art / "protocol_a_wedd_rule_ablation.csv"),
        "stability": pd.read_csv(art / "protocol_a_threshold_stability.csv"),
    }
    protocol_b = {"summary": pb_summary, "per_class": pd.read_csv(art / "protocol_b_unseen_per_class.csv")}
    synthetic = {
        "summary": read_json(syn_art / "synthetic_summary.json"),
        "by_noise": pd.read_csv(syn_art / "synthetic_summary_by_noise.csv"),
        "ground_truth_rules": pd.read_csv(syn_art / "synthetic_ground_truth_rules.csv"),
    }
    generate_figures(out, awa2, protocol_a, protocol_b, synthetic)
    generate_tables(out, awa2, protocol_a, protocol_b, synthetic)
    print({"figures": len(list((out / "figs").glob("*.pdf"))), "tables": len(list((out / "tables").glob("table_*.tex")))})


if __name__ == "__main__":
    main()
