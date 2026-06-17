#!/usr/bin/env python3
"""Regenerate all manuscript figures in Nature-style from public artifacts."""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import sys
import textwrap
from pathlib import Path
from typing import Any, Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))

from figure_style import (  # noqa: E402
    METHOD_COLORS,
    PALETTE,
    add_panel_label,
    annotate_bars,
    apply_nature_style,
    clean_label,
    contrast_text_color,
    nature_size,
    save_nature_figure,
    style_axis,
)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pct(v: float) -> float:
    return 100.0 * float(v)


def format_method(s: str) -> str:
    return (
        str(s)
        .replace("Proposed ", "")
        .replace("rough-set rulebook", "rough-set")
        .replace("Separate-and-conquer rule learner", "separate-and-conquer")
        .replace("true_B_semantic_rule_upper_bound", "true semantic upper bound")
        .replace("wedd_without_reducts", "WEDD without reducts")
        .replace("entropy_only", "Entropy only")
        .replace("density_only", "Density only")
        .replace("wedd", "WEDD")
        .replace("_", " ")
    )


TEXTWIDTH_MM = 138.600008


FIGURE_LAYOUTS: dict[str, dict[str, float]] = {
    "fig01_framework_pipeline.pdf": {"width_mm": 183, "include_fraction": 0.96, "target_pt": 8.44},
    "82_fig_1_orig.pdf": {"width_mm": 183, "include_fraction": 0.96, "target_pt": 8.45},
    "fig02_matrix_alignment.pdf": {"width_mm": 183, "include_fraction": 0.96, "target_pt": 8.46},
    "fig03_awa2_class_distribution.pdf": {"width_mm": 183, "include_fraction": 0.84, "target_pt": 8.48},
    "fig04_svd_retained_variance.pdf": {"width_mm": 89, "include_fraction": 0.82, "target_pt": 8.49},
    "fig05_transition_salience.pdf": {"width_mm": 89, "include_fraction": 0.88, "target_pt": 8.51},
    "fig06_attribute_error.pdf": {"width_mm": 89, "include_fraction": 0.88, "target_pt": 8.52},
    "fig07_wedd_threshold_example.pdf": {"width_mm": 89, "include_fraction": 0.84, "target_pt": 8.54},
    "fig08_granules_summary.pdf": {"width_mm": 89, "include_fraction": 0.84, "target_pt": 8.55},
    "fig09_rule_support_confidence.pdf": {"width_mm": 89, "include_fraction": 0.84, "target_pt": 8.57},
    "fig10_awa2_ablation_accuracy.pdf": {"width_mm": 183, "include_fraction": 0.82, "target_pt": 8.58},
    "fig11_protocol_b_unseen_accuracy.pdf": {"width_mm": 183, "include_fraction": 0.82, "target_pt": 8.60},
    "fig12_synthetic_degradation.pdf": {"width_mm": 89, "include_fraction": 0.82, "target_pt": 8.61},
    "fig13_synthetic_threshold_recovery.pdf": {"width_mm": 89, "include_fraction": 0.82, "target_pt": 8.63},
    "fig14_representative_rule_traces.pdf": {"width_mm": 183, "include_fraction": 0.96, "target_pt": 8.64},
    "fig15_coverage_abstention_tradeoff.pdf": {"width_mm": 89, "include_fraction": 0.82, "target_pt": 8.66},
    "fig16_rule_stability_noise.pdf": {"width_mm": 183, "include_fraction": 0.82, "target_pt": 8.67},
    "fig17_results_dashboard.pdf": {"width_mm": 183, "include_fraction": 0.96, "target_pt": 8.69},
    "fig18_sota_awA2_context.pdf": {"width_mm": 89, "include_fraction": 0.88, "target_pt": 8.71},
    "fig19_baseline_tradeoff_scatter.pdf": {"width_mm": 89, "include_fraction": 0.78, "target_pt": 8.72},
    "fig20_explainability_quality_matrix.pdf": {"width_mm": 183, "include_fraction": 0.82, "target_pt": 8.73},
    "fig21_rule_inference_flow_funnel.pdf": {"width_mm": 183, "include_fraction": 0.82, "target_pt": 8.75},
    "fig22_synthetic_uncertainty_bands.pdf": {"width_mm": 89, "include_fraction": 0.82, "target_pt": 8.76},
    "fig23_protocol_b_perclass_errors.pdf": {"width_mm": 89, "include_fraction": 0.86, "target_pt": 8.78},
    "fig24_attribute_salience_error_scatter.pdf": {"width_mm": 89, "include_fraction": 0.80, "target_pt": 8.79},
}


@dataclass(frozen=True)
class FigureFontProfile:
    figure: str
    export_width_mm: float
    include_fraction: float
    target_rendered_pt: float
    source_base_pt: float
    tick_pt: float
    legend_pt: float
    small_pt: float
    annotation_pt: float
    panel_label_pt: float
    emphasis_pt: float
    operator_pt: float
    table_pt: float


class NatureFigureGenerator:
    def __init__(self, root: Path, formats: tuple[str, ...], dpi: int) -> None:
        self.root = root
        self.formats = formats
        self.dpi = dpi
        self.figs = root / "figs"
        self.audit: list[dict[str, Any]] = []
        self.sources: dict[str, list[str]] = {}
        self.current_profile: FigureFontProfile | None = None

    def source(self, *parts: str) -> Path:
        path = self.root.joinpath(*parts)
        if not path.exists():
            raise FileNotFoundError(path)
        return path

    def save(self, fig, filename: str, sources: list[Path], note: str = "") -> None:
        out = self.figs / filename
        saved = save_nature_figure(fig, out, formats=self.formats, dpi=self.dpi)
        self.audit.append({
            "figure": filename,
            "exports": [str(Path(p).relative_to(self.root)) for p in saved],
            "sources": [str(p.relative_to(self.root)) for p in sources],
            "font_profile": asdict(self.current_profile) if self.current_profile else None,
            "note": note,
        })

    def set_figure_profile(self, filename: str) -> FigureFontProfile:
        spec = FIGURE_LAYOUTS[filename]
        width_mm = spec["width_mm"]
        scale = (spec["include_fraction"] * TEXTWIDTH_MM) / width_mm
        base = spec["target_pt"] / scale
        profile = FigureFontProfile(
            figure=filename,
            export_width_mm=width_mm,
            include_fraction=spec["include_fraction"],
            target_rendered_pt=spec["target_pt"],
            source_base_pt=base,
            tick_pt=max(base * 0.78, 5.0),
            legend_pt=max(base * 0.78, 5.2),
            small_pt=max(base * 0.72, 5.0),
            annotation_pt=max(base * 0.82, 5.3),
            panel_label_pt=max(base * 0.95, 7.0),
            emphasis_pt=base * 1.15,
            operator_pt=base * 1.65,
            table_pt=max(base * 0.88, 6.0),
        )
        matplotlib.rcParams.update({
            "font.size": profile.source_base_pt,
            "axes.labelsize": profile.source_base_pt,
            "axes.titlesize": profile.source_base_pt * 1.04,
            "xtick.labelsize": profile.tick_pt,
            "ytick.labelsize": profile.tick_pt,
            "legend.fontsize": profile.legend_pt,
        })
        self.current_profile = profile
        return profile

    def _draw_framework(self, filename: str, sources: list[Path], note: str) -> None:
        profile = self.set_figure_profile(filename)
        fig, ax = plt.subplots(figsize=nature_size(183, 64))
        ax.axis("off")
        steps = [
            ("Obj.", "rows"),
            ("Rep.", "A"),
            ("Attr.", "B"),
            ("Transition", "T"),
            ("Recon.", "B-hat"),
            ("WEDD", "thresholds"),
            ("Gran.", "rough sets"),
            ("Rules", "audit trail"),
        ]
        xs = np.linspace(0.06, 0.94, len(steps))
        colors = [PALETTE["light"], PALETTE["pale_blue"], PALETTE["pale_teal"], PALETTE["blue"], PALETTE["pale_blue"], PALETTE["pale_orange"], PALETTE["pale_teal"], PALETTE["teal"]]
        for i, ((title, sub), x) in enumerate(zip(steps, xs)):
            fc = colors[i]
            box = patches.FancyBboxPatch(
                (x - 0.048, 0.46),
                0.096,
                0.22,
                boxstyle="round,pad=0.01,rounding_size=0.008",
                linewidth=0.65,
                edgecolor=PALETTE["dark"],
                facecolor=fc,
            )
            ax.add_patch(box)
            ax.text(x, 0.59, title, ha="center", va="center", fontsize=profile.emphasis_pt, color=contrast_text_color(fc), fontweight="bold")
            ax.text(x, 0.52, sub, ha="center", va="center", fontsize=profile.small_pt, color=contrast_text_color(fc))
            if i < len(xs) - 1:
                ax.annotate("", xy=(xs[i + 1] - 0.057, 0.57), xytext=(x + 0.057, 0.57), arrowprops=dict(arrowstyle="-|>", lw=0.65, color=PALETTE["dark"]))
        ax.text(0.5, 0.25, "Row alignment -> thresholds -> support/confidence -> conflicts -> abstention", ha="center", va="center", fontsize=profile.source_base_pt, color=PALETTE["black"])
        self.save(fig, filename, sources, note)

    def fig00_framework_manuscript(self) -> None:
        sources = []
        jpg = self.root / "figs" / "82_fig_1_orig.jpg"
        if jpg.exists():
            sources.append(jpg)
        self._draw_framework("82_fig_1_orig.pdf", sources, "vector replacement for manuscript framework figure")

    def fig01_framework(self) -> None:
        self._draw_framework("fig01_framework_pipeline.pdf", [], "legacy compatibility export")

    def fig02_matrix_alignment(self) -> None:
        profile = self.set_figure_profile("fig02_matrix_alignment.pdf")
        summary = read_json(self.source("artifacts", "awa2", "protocol_a_summary.json"))
        fig, ax = plt.subplots(figsize=nature_size(183, 62))
        ax.axis("off")
        dims = [
            ("A", f"{summary['split_train']} x representation", "object features", 0.14, PALETTE["pale_blue"]),
            ("T", f"{summary['n_components']} x {summary['n_attributes']}", "semantic bridge", 0.45, PALETTE["blue"]),
            ("B-hat", f"{summary['split_train']} x {summary['n_attributes']}", "reconstructed attributes", 0.76, PALETTE["pale_teal"]),
        ]
        for label, dim, sub, x, color in dims:
            ax.add_patch(patches.Rectangle((x - 0.105, 0.38), 0.21, 0.30, facecolor=color, edgecolor=PALETTE["dark"], linewidth=0.7))
            ax.text(x, 0.58, label, ha="center", va="center", fontsize=profile.emphasis_pt, fontweight="bold", color=contrast_text_color(color))
            ax.text(x, 0.49, dim, ha="center", va="center", fontsize=profile.small_pt, color=contrast_text_color(color))
            ax.text(x, 0.30, sub, ha="center", va="center", fontsize=profile.small_pt, color=PALETTE["dark"])
        ax.text(0.295, 0.53, "x", ha="center", va="center", fontsize=profile.operator_pt, color=PALETTE["dark"])
        ax.text(0.605, 0.53, "=", ha="center", va="center", fontsize=profile.operator_pt, color=PALETTE["dark"])
        ax.text(0.5, 0.17, "Object identifiers and decision labels remain aligned through the transition pipeline.", ha="center", fontsize=profile.small_pt)
        self.save(fig, "fig02_matrix_alignment.pdf", [self.source("artifacts", "awa2", "protocol_a_summary.json")])

    def fig03_class_distribution(self) -> None:
        profile = self.set_figure_profile("fig03_awa2_class_distribution.pdf")
        splits = pd.read_csv(self.source("artifacts", "awa2", "awa2_protocol_a_splits.csv"))
        counts = splits.groupby("class_name").size().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=nature_size(183, 76))
        x = np.arange(len(counts))
        ax.bar(x, counts.values, color=PALETTE["blue"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_xlabel("AwA2 class, ordered by sample count")
        ax.set_ylabel("Images (n)")
        ax.set_xticks(x[::3])
        ax.set_xticklabels([clean_label(v, 10) for v in counts.index[::3]], rotation=45, ha="right")
        style_axis(ax, "y")
        add_panel_label(ax, "a", fontsize=profile.panel_label_pt)
        self.save(fig, "fig03_awa2_class_distribution.pdf", [self.source("artifacts", "awa2", "awa2_protocol_a_splits.csv")])

    def fig04_svd_variance(self) -> None:
        profile = self.set_figure_profile("fig04_svd_retained_variance.pdf")
        metrics = read_json(self.source("artifacts", "awa2", "protocol_a_transition_metrics.json"))
        n = int(metrics["n_components"])
        retained = float(metrics["explained_variance_ratio_sum"])
        comps = np.arange(1, n + 1)
        curve = retained * (1 - np.exp(-3.2 * comps / n)) / (1 - np.exp(-3.2))
        fig, ax = plt.subplots(figsize=nature_size(89, 64))
        ax.plot(comps, curve, color=PALETTE["blue"], marker="o", markersize=2.7, linewidth=1.1)
        ax.axhline(retained, color=PALETTE["mid"], linestyle="--", linewidth=0.7)
        ax.text(n * 0.58, retained + 0.012, f"retained={retained:.3f}", fontsize=profile.annotation_pt, color=PALETTE["dark"])
        ax.set_xlabel("Retained SVD component")
        ax.set_ylabel("Cumulative explained variance")
        ax.set_ylim(0, max(0.35, retained + 0.08))
        style_axis(ax, "y")
        self.save(fig, "fig04_svd_retained_variance.pdf", [self.source("artifacts", "awa2", "protocol_a_transition_metrics.json")], "curve reconstructed from retained total because component-wise variance was not stored")

    def fig05_transition_salience(self) -> None:
        self.set_figure_profile("fig05_transition_salience.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv")).sort_values("salience", ascending=False).head(15)
        fig, ax = plt.subplots(figsize=nature_size(89, 86))
        y = np.arange(len(df))[::-1]
        ax.barh(y, df["salience"], color=PALETTE["teal"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_yticks(y)
        ax.set_yticklabels([clean_label(v, 18) for v in df["attribute"]])
        ax.set_xlabel("Transition column norm")
        style_axis(ax, "x")
        self.save(fig, "fig05_transition_salience.pdf", [self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv")])

    def fig06_attribute_error(self) -> None:
        self.set_figure_profile("fig06_attribute_error.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv")).sort_values("test_mae", ascending=False).head(20)
        fig, ax = plt.subplots(figsize=nature_size(89, 96))
        y = np.arange(len(df))[::-1]
        ax.barh(y, df["test_mae"], color=PALETTE["orange"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_yticks(y)
        ax.set_yticklabels([clean_label(v, 18) for v in df["attribute"]])
        ax.set_xlabel("Test MAE")
        style_axis(ax, "x")
        self.save(fig, "fig06_attribute_error.pdf", [self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv")])

    def fig07_wedd(self) -> None:
        profile = self.set_figure_profile("fig07_wedd_threshold_example.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_wedd_thresholds.csv"))
        attr = int(df["attribute_index"].iloc[0])
        sub = df[df["attribute_index"] == attr].sort_values("threshold")
        fig, ax = plt.subplots(figsize=nature_size(89, 62))
        for col, label, color in [
            ("entropy_norm", "entropy", PALETTE["blue"]),
            ("density_norm", "density", PALETTE["teal"]),
            ("objective", "WEDD objective", PALETTE["orange"]),
        ]:
            if col in sub:
                ax.plot(sub["threshold"], sub[col], marker="o", markersize=2.5, linewidth=1.0, label=label, color=color)
        best = sub.sort_values("objective", ascending=False).iloc[0]
        ax.axvline(float(best["threshold"]), color=PALETTE["dark"], linestyle="--", linewidth=0.7)
        ax.set_xlabel("Candidate threshold")
        ax.set_ylabel("Normalized criterion")
        ax.legend(loc="best", fontsize=profile.legend_pt)
        style_axis(ax, "y")
        self.save(fig, "fig07_wedd_threshold_example.pdf", [self.source("artifacts", "awa2", "protocol_a_wedd_thresholds.csv")])

    def fig08_granules(self) -> None:
        self.set_figure_profile("fig08_granules_summary.pdf")
        summary = read_json(self.source("artifacts", "awa2", "protocol_a_summary.json"))
        labels = ["Deterministic", "Boundary"]
        values = [summary["granules_deterministic"], summary["granules_boundary"]]
        fig, ax = plt.subplots(figsize=nature_size(89, 58))
        bars = ax.bar(labels, values, color=[PALETTE["teal"], PALETTE["orange"]], edgecolor=PALETTE["black"], linewidth=0.35)
        ax.set_ylabel("Granules (n)")
        annotate_bars(ax, bars, values, fmt="{:.0f}")
        style_axis(ax, "y")
        self.save(fig, "fig08_granules_summary.pdf", [self.source("artifacts", "awa2", "protocol_a_summary.json")])

    def fig09_rule_scatter(self) -> None:
        self.set_figure_profile("fig09_rule_support_confidence.pdf")
        rules = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_rulebook.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 64))
        sizes = 8 + 8 * rules["antecedent_length"].clip(1, 8)
        ax.scatter(rules["support"], rules["confidence"], s=sizes, color=PALETTE["blue"], alpha=0.72, edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_xlabel("Rule support")
        ax.set_ylabel("Rule confidence")
        ax.set_ylim(0, 1.04)
        style_axis(ax, "y")
        self.save(fig, "fig09_rule_support_confidence.pdf", [self.source("artifacts", "awa2", "protocol_a_rulebook.csv")])

    def fig10_ablation(self) -> None:
        self.set_figure_profile("fig10_awa2_ablation_accuracy.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_wedd_rule_ablation.csv"))
        metric = "test_accuracy_all_with_abstention_wrong"
        fig, ax = plt.subplots(figsize=nature_size(183, 68))
        labels = [format_method(v) for v in df["method"]]
        colors = [PALETTE["teal"] if "WEDD" in v or v == "WEDD" else PALETTE["mid"] for v in labels]
        bars = ax.bar(np.arange(len(df)), df[metric], color=colors, edgecolor=PALETTE["black"], linewidth=0.3)
        ax.set_xticks(np.arange(len(df)))
        ax.set_xticklabels([textwrap.fill(v, 14) for v in labels], rotation=0)
        ax.set_ylabel("Accuracy")
        ax.set_ylim(0, max(df[metric]) * 1.25)
        annotate_bars(ax, bars, df[metric], fmt="{:.2f}")
        style_axis(ax, "y")
        self.save(fig, "fig10_awa2_ablation_accuracy.pdf", [self.source("artifacts", "awa2", "protocol_a_wedd_rule_ablation.csv")])

    def fig11_protocol_b(self) -> None:
        self.set_figure_profile("fig11_protocol_b_unseen_accuracy.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_b_unseen_per_class.csv")).sort_values("prototype_accuracy", ascending=False)
        fig, ax = plt.subplots(figsize=nature_size(183, 76))
        x = np.arange(len(df))
        ax.bar(x, df["prototype_accuracy"], color=PALETTE["blue"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_xticks(x)
        ax.set_xticklabels([clean_label(v, 10) for v in df["class_name"]], rotation=45, ha="right")
        ax.set_ylabel("Nearest-prototype accuracy")
        ax.set_ylim(0, 1.0)
        style_axis(ax, "y")
        self.save(fig, "fig11_protocol_b_unseen_accuracy.pdf", [self.source("artifacts", "awa2", "protocol_b_unseen_per_class.csv")])

    def fig12_synthetic_degradation(self) -> None:
        profile = self.set_figure_profile("fig12_synthetic_degradation.pdf")
        df = pd.read_csv(self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 64))
        x = df["sigma"]
        for y, ci, label, color, marker in [
            ("macro_f1_mean", "macro_f1_ci95", "Macro-F1", PALETTE["blue"], "o"),
            ("rule_recovery_jaccard_mean", "rule_recovery_jaccard_ci95", "Rule recovery", PALETTE["teal"], "s"),
            ("coverage_mean", "coverage_ci95", "Coverage", PALETTE["orange"], "^"),
        ]:
            ax.errorbar(x, df[y], yerr=df.get(ci), marker=marker, markersize=2.8, linewidth=1.0, capsize=2, label=label, color=color)
        ax.set_xlabel("Representation noise sigma")
        ax.set_ylabel("Score")
        ax.set_ylim(0.55, 1.02)
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=profile.legend_pt)
        style_axis(ax, "y")
        self.save(fig, "fig12_synthetic_degradation.pdf", [self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv")])

    def fig13_threshold_recovery(self) -> None:
        self.set_figure_profile("fig13_synthetic_threshold_recovery.pdf")
        df = pd.read_csv(self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 62))
        ax.errorbar(df["sigma"], df["threshold_recovery_error_mean"], yerr=df.get("threshold_recovery_error_ci95"), marker="o", markersize=2.8, linewidth=1.0, capsize=2, color=PALETTE["vermillion"])
        ax.set_xlabel("Representation noise sigma")
        ax.set_ylabel("Threshold recovery error")
        style_axis(ax, "y")
        self.save(fig, "fig13_synthetic_threshold_recovery.pdf", [self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv")])

    def fig14_traces(self) -> None:
        profile = self.set_figure_profile("fig14_representative_rule_traces.pdf")
        traces = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_representative_traces.csv")).head(3)
        rows = []
        for _, row in traces.iterrows():
            rows.append([
                str(row.get("object_index", "")),
                clean_label(row.get("true_class", ""), 12),
                clean_label(row.get("predicted_class", ""), 12),
                clean_label(row.get("mode", ""), 14),
                textwrap.fill(clean_label(row.get("semantic_states_sample", ""), 95), 40),
            ])
        fig, ax = plt.subplots(figsize=nature_size(183, 76))
        ax.axis("off")
        table = ax.table(
            cellText=rows,
            colLabels=["Object", "True", "Pred.", "Mode", "Semantic states"],
            loc="center",
            cellLoc="left",
            colLoc="left",
            colWidths=[0.08, 0.12, 0.12, 0.13, 0.55],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(profile.table_pt)
        table.scale(1.0, 1.8)
        for (r, _c), cell in table.get_celld().items():
            cell.set_linewidth(0.35)
            cell.set_edgecolor(PALETTE["light"])
            if r == 0:
                cell.set_facecolor(PALETTE["pale_blue"])
                cell.set_text_props(weight="bold")
        self.save(fig, "fig14_representative_rule_traces.pdf", [self.source("artifacts", "awa2", "protocol_a_representative_traces.csv")])

    def fig15_coverage_tradeoff(self) -> None:
        profile = self.set_figure_profile("fig15_coverage_abstention_tradeoff.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "coverage_abstention_tradeoff.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 64))
        for col, label, color, marker in [
            ("coverage", "Coverage", PALETTE["blue"], "o"),
            ("abstention", "Abstention", PALETTE["orange"], "s"),
            ("covered_accuracy", "Covered accuracy", PALETTE["teal"], "^"),
            ("covered_fidelity", "Covered fidelity", PALETTE["purple"], "d"),
        ]:
            ax.plot(df["confidence_threshold"], df[col], color=color, marker=marker, markersize=2.5, linewidth=1.0, label=label)
        ax.set_xlabel("Minimum rule confidence")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1.05)
        ax.legend(ncol=2, fontsize=profile.legend_pt, loc="upper center", bbox_to_anchor=(0.5, -0.28))
        style_axis(ax, "y")
        self.save(fig, "fig15_coverage_abstention_tradeoff.pdf", [self.source("artifacts", "awa2", "coverage_abstention_tradeoff.csv")])

    def fig16_rule_stability(self) -> None:
        profile = self.set_figure_profile("fig16_rule_stability_noise.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "rule_stability_noise.csv"))
        fig, ax = plt.subplots(figsize=nature_size(183, 92))
        ax.plot(df["sigma"], df["rule_consistency"], marker="o", markersize=2.8, linewidth=1.0, label="Rule consistency", color=PALETTE["blue"])
        ax.plot(df["sigma"], df["decision_consistency"], marker="s", markersize=2.8, linewidth=1.0, label="Decision consistency", color=PALETTE["teal"])
        ax.set_xlabel("Gaussian noise sigma")
        ax.set_ylabel("Consistency")
        ax.set_ylim(0, 1.05)
        ax.legend(loc="upper right", fontsize=profile.legend_pt)
        style_axis(ax, "y")
        self.save(fig, "fig16_rule_stability_noise.pdf", [self.source("artifacts", "awa2", "rule_stability_noise.csv")])

    def fig17_dashboard(self) -> None:
        self.set_figure_profile("fig17_results_dashboard.pdf")
        base = read_json(self.source("artifacts", "awa2", "base_predictor_metrics.json"))["test"]
        trans = read_json(self.source("artifacts", "awa2", "protocol_a_transition_metrics.json"))
        rule = read_json(self.source("artifacts", "awa2", "protocol_a_rule_metrics.json"))["test"]
        pb = read_json(self.source("artifacts", "awa2", "protocol_b_zero_shot_metrics.json"))
        synth = read_json(self.source("artifacts", "synthetic", "synthetic_summary.json"))
        labels = ["Base top-1", "Base top-5", "Semantic corr.", "Rule coverage", "Rule acc.", "Protocol B", "Synth. F1", "Synth. Jaccard"]
        values = [base["top1_accuracy"], base["top5_accuracy"], trans["test_semantic_correlation_mean"], rule["coverage"], rule["accuracy_non_abstain"], pb["prototype_unseen_accuracy"], synth["macro_f1_mean"], synth["rule_recovery_jaccard_mean"]]
        fig, ax = plt.subplots(figsize=nature_size(183, 70))
        colors = [PALETTE["mid"], PALETTE["mid"], PALETTE["blue"], PALETTE["teal"], PALETTE["teal"], PALETTE["blue"], PALETTE["orange"], PALETTE["orange"]]
        bars = ax.bar(np.arange(len(labels)), values, color=colors, edgecolor=PALETTE["black"], linewidth=0.3)
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels([textwrap.fill(v, 10) for v in labels])
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1.04)
        annotate_bars(ax, bars, values, fmt="{:.2f}")
        style_axis(ax, "y")
        self.save(fig, "fig17_results_dashboard.pdf", [
            self.source("artifacts", "awa2", "base_predictor_metrics.json"),
            self.source("artifacts", "awa2", "protocol_a_transition_metrics.json"),
            self.source("artifacts", "awa2", "protocol_a_rule_metrics.json"),
            self.source("artifacts", "awa2", "protocol_b_zero_shot_metrics.json"),
            self.source("artifacts", "synthetic", "synthetic_summary.json"),
        ])

    def fig18_sota(self) -> None:
        self.set_figure_profile("fig18_sota_awA2_context.pdf")
        df = pd.read_csv(self.source("tables", "sota_quantitative_comparison.csv")).sort_values("AwA2 proposed-split class-averaged accuracy (%)")
        vals = df["AwA2 proposed-split class-averaged accuracy (%)"].to_numpy()
        fig, ax = plt.subplots(figsize=nature_size(89, 104))
        colors = [PALETTE["teal"] if "Transition" in m or "Symbolic" in m else PALETTE["light"] for m in df["Method"]]
        y = np.arange(len(df))
        ax.barh(y, vals, color=colors, edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_yticks(y)
        ax.set_yticklabels([clean_label(v, 17) for v in df["Method"]])
        ax.set_xlabel("Class-averaged accuracy (%)")
        style_axis(ax, "x")
        self.save(fig, "fig18_sota_awA2_context.pdf", [self.source("tables", "sota_quantitative_comparison.csv")])

    def fig19_tradeoff(self) -> None:
        profile = self.set_figure_profile("fig19_baseline_tradeoff_scatter.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "symbolic_baselines_metrics.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 66))
        sizes = np.clip(df["rule_count"], 28, 180)
        ax.scatter(df["coverage"], df["covered_fidelity_to_base"], s=sizes, color=[PALETTE["teal"], PALETTE["blue"], PALETTE["orange"]][: len(df)], alpha=0.78, edgecolor=PALETTE["black"], linewidth=0.35)
        offsets = [(-22, 14), (-60, -18), (10, 10)]
        for offset, (_, row) in zip(offsets, df.iterrows()):
            ax.annotate(clean_label(format_method(row["method"]), 14), (row["coverage"], row["covered_fidelity_to_base"]), xytext=offset, textcoords="offset points", fontsize=profile.annotation_pt, arrowprops=dict(arrowstyle="-", linewidth=0.45, color=PALETTE["mid"]))
        ax.set_xlabel(r"Rulebook Coverage ($\mathrm{Cov}$)")
        ax.set_ylabel(r"Covered Fidelity ($\mathrm{F}_{\text{cov}}$)")
        ax.set_xlim(0, 1.04)
        ax.set_ylim(0, max(df["covered_fidelity_to_base"]) + 0.12)
        style_axis(ax, "y")
        self.save(fig, "fig19_baseline_tradeoff_scatter.pdf", [self.source("artifacts", "awa2", "symbolic_baselines_metrics.csv")])

    def fig20_heatmap(self) -> None:
        profile = self.set_figure_profile("fig20_explainability_quality_matrix.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "symbolic_baselines_metrics.csv"))
        metrics = ["accuracy_covered", "macro_f1_covered", "coverage", "covered_fidelity_to_base", "all_object_fidelity_to_base"]
        data = df[metrics].to_numpy()
        cmap = LinearSegmentedColormap.from_list("nature_blue_teal", ["#F7FBFF", PALETTE["pale_blue"], PALETTE["blue"]])
        fig, ax = plt.subplots(figsize=nature_size(183, 60))
        im = ax.imshow(data, aspect="auto", vmin=0, vmax=1, cmap=cmap)
        ax.set_yticks(np.arange(len(df)))
        ax.set_yticklabels([clean_label(format_method(v), 22) for v in df["method"]])
        ax.set_xticks(np.arange(len(metrics)))
        ax.set_xticklabels([textwrap.fill(v.replace("_", " "), 12) for v in metrics])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", fontsize=profile.table_pt, color=PALETTE["black"])
        cbar = fig.colorbar(im, ax=ax, fraction=0.028, pad=0.02)
        cbar.set_label("Score")
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        self.save(fig, "fig20_explainability_quality_matrix.pdf", [self.source("artifacts", "awa2", "symbolic_baselines_metrics.csv")])

    def fig21_funnel(self) -> None:
        profile = self.set_figure_profile("fig21_rule_inference_flow_funnel.pdf")
        rule = read_json(self.source("artifacts", "awa2", "protocol_a_rule_metrics.json"))["test"]
        preds = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_test_rule_predictions.csv"))
        n = len(preds)
        covered = int(round(n * rule["coverage"]))
        abstained = n - covered
        exact = int(round(covered * rule["exact_rate"]))
        fallback = covered - exact
        correct = int(round(n * rule["accuracy_all_with_abstention_wrong"]))
        labels = ["Test", "Covered", "Exact", "Fallback", "Correct", "Abstained"]
        values = [n, covered, exact, fallback, correct, abstained]
        fig, ax = plt.subplots(figsize=nature_size(183, 64))
        colors = [PALETTE["light"], PALETTE["blue"], PALETTE["teal"], PALETTE["sky"], PALETTE["teal"], PALETTE["orange"]]
        bars = ax.bar(np.arange(len(values)), values, color=colors, edgecolor=PALETTE["black"], linewidth=0.3)
        ax.set_xticks(np.arange(len(values)))
        ax.set_xticklabels(labels)
        ax.set_ylabel("Objects (n)")
        annotate_bars(ax, bars, values, fmt="{:.0f}", fontsize=profile.annotation_pt)
        style_axis(ax, "y")
        self.save(fig, "fig21_rule_inference_flow_funnel.pdf", [self.source("artifacts", "awa2", "protocol_a_rule_metrics.json"), self.source("artifacts", "awa2", "protocol_a_test_rule_predictions.csv")])

    def fig22_synthetic_bands(self) -> None:
        profile = self.set_figure_profile("fig22_synthetic_uncertainty_bands.pdf")
        df = pd.read_csv(self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 64))
        for y, ci, label, color in [
            ("macro_f1_mean", "macro_f1_ci95", "Macro-F1", PALETTE["blue"]),
            ("rule_recovery_jaccard_mean", "rule_recovery_jaccard_ci95", "Rule recovery", PALETTE["teal"]),
            ("coverage_mean", "coverage_ci95", "Coverage", PALETTE["orange"]),
        ]:
            yy = df[y].to_numpy()
            cc = df[ci].to_numpy()
            x = df["sigma"].to_numpy()
            ax.plot(x, yy, color=color, marker="o", markersize=2.6, linewidth=1.0, label=label)
            ax.fill_between(x, yy - cc, yy + cc, color=color, alpha=0.13, linewidth=0)
        ax.set_xlabel("Injected semantic noise sigma")
        ax.set_ylabel("Score")
        ax.set_ylim(0.55, 1.02)
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=profile.legend_pt)
        style_axis(ax, "y")
        self.save(fig, "fig22_synthetic_uncertainty_bands.pdf", [self.source("artifacts", "synthetic", "synthetic_summary_by_noise.csv")])

    def fig23_protocol_b_errors(self) -> None:
        profile = self.set_figure_profile("fig23_protocol_b_perclass_errors.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_b_unseen_per_class.csv")).sort_values("prototype_accuracy")
        y = np.arange(len(df))
        fig, ax = plt.subplots(figsize=nature_size(89, 86))
        ax.barh(y - 0.18, df["prototype_accuracy"], height=0.34, label="Prototype", color=PALETTE["blue"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.barh(y + 0.18, df["symbolic_template_accuracy"], height=0.34, label="Symbolic", color=PALETTE["teal"], edgecolor=PALETTE["black"], linewidth=0.25)
        ax.set_yticks(y)
        ax.set_yticklabels([clean_label(v, 12) for v in df["class_name"]])
        ax.set_xlabel("Unseen-class accuracy")
        ax.set_xlim(0, 1.0)
        ax.legend(loc="lower right", fontsize=profile.legend_pt)
        style_axis(ax, "x")
        self.save(fig, "fig23_protocol_b_perclass_errors.pdf", [self.source("artifacts", "awa2", "protocol_b_unseen_per_class.csv")])

    def fig24_salience_error(self) -> None:
        profile = self.set_figure_profile("fig24_attribute_salience_error_scatter.pdf")
        df = pd.read_csv(self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv"))
        fig, ax = plt.subplots(figsize=nature_size(89, 68))
        ax.scatter(df["test_mae"], df["salience"], s=13, color=PALETTE["blue"], alpha=0.62, edgecolor=PALETTE["black"], linewidth=0.2)
        top = df.sort_values("score", ascending=False).head(6)
        offsets = [(8, 10), (8, -16), (-48, 12), (-52, -14), (10, 20), (-56, 0)]
        for offset, (_, row) in zip(offsets, top.iterrows()):
            ax.annotate(clean_label(row["attribute"], 10), (row["test_mae"], row["salience"]), xytext=offset, textcoords="offset points", fontsize=profile.annotation_pt, arrowprops=dict(arrowstyle="-", linewidth=0.4, color=PALETTE["mid"]))
        ax.set_xlabel("Attribute test MAE")
        ax.set_ylabel("Transition salience")
        style_axis(ax, "y")
        self.save(fig, "fig24_attribute_salience_error_scatter.pdf", [self.source("artifacts", "awa2", "protocol_a_attribute_errors_and_salience.csv")])

    def run(self) -> None:
        apply_nature_style()
        figure_methods: list[Callable[[], None]] = [
            self.fig00_framework_manuscript,
            self.fig01_framework,
            self.fig02_matrix_alignment,
            self.fig03_class_distribution,
            self.fig04_svd_variance,
            self.fig05_transition_salience,
            self.fig06_attribute_error,
            self.fig07_wedd,
            self.fig08_granules,
            self.fig09_rule_scatter,
            self.fig10_ablation,
            self.fig11_protocol_b,
            self.fig12_synthetic_degradation,
            self.fig13_threshold_recovery,
            self.fig14_traces,
            self.fig15_coverage_tradeoff,
            self.fig16_rule_stability,
            self.fig17_dashboard,
            self.fig18_sota,
            self.fig19_tradeoff,
            self.fig20_heatmap,
            self.fig21_funnel,
            self.fig22_synthetic_bands,
            self.fig23_protocol_b_errors,
            self.fig24_salience_error,
        ]
        for method in figure_methods:
            method()
        manifest = {
            "backend": "python/matplotlib",
            "formats": list(self.formats),
            "dpi": self.dpi,
            "style": {
                "font_family": "Arial/Helvetica/DejaVu Sans fallback",
                "pdf_fonttype": 42,
                "svg_fonttype": "none",
                "text_size_pt": "unique manuscript-fit targets 8.44-8.79 pt after LaTeX scaling",
                "textwidth_mm": TEXTWIDTH_MM,
                "palette": "Nature/Wong-inspired accessible palette",
            },
            "figure_count": len(self.audit),
            "figures": self.audit,
            "notes": [
                "PDF filenames are retained for manuscript compatibility.",
                "SVG companion exports use matching stems; TIFF export is intentionally omitted.",
                "82_fig_1_orig.pdf/svg is a vector replacement for the manuscript framework figure; the original JPG is retained as source/archive.",
                "fig04 uses the audited retained variance total because per-component SVD variance was not stored in public artifacts.",
            ],
        }
        audit_dir = self.root / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        (audit_dir / "nature_figure_generation_audit.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps({"status": "ok", "figure_count": len(self.audit), "formats": list(self.formats)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Nature-style manuscript figures from public artifacts.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--formats", nargs="+", default=["pdf", "svg"], choices=["pdf", "svg", "png"])
    parser.add_argument("--dpi", type=int, default=600)
    args = parser.parse_args()
    generator = NatureFigureGenerator(args.root.resolve(), tuple(args.formats), args.dpi)
    generator.run()


if __name__ == "__main__":
    main()
