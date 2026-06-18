from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.text import Text


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7.8
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["legend.frameon"] = False
plt.rcParams["legend.fontsize"] = 6.8
plt.rcParams["xtick.major.width"] = 0.6
plt.rcParams["ytick.major.width"] = 0.6


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "figs_main"
TEXT_SCALE = 1.12

PALETTE = {
    "blue": "#0F4D92",
    "blue2": "#3775BA",
    "teal": "#42949E",
    "green": "#8BCF8B",
    "green_dark": "#2E9E44",
    "red": "#B64342",
    "red_soft": "#E9A6A1",
    "gold": "#C99A2E",
    "violet": "#9A4D8E",
    "neutral0": "#F4F4F4",
    "neutral1": "#D8D8D8",
    "neutral2": "#A8A8A8",
    "neutral3": "#606060",
    "black": "#272727",
}

FIGURES: list[dict[str, str]] = []


OLD_GENERATED_PATTERNS = [
    "fig25_revision_evidence_map.*",
    "fig26_object_level_metric_intervals.*",
    "fig27_wedd_mdlp_discretizer_evidence.*",
    "fig28_sensitivity_runtime_audit_tax.*",
    "fig29_protocol_b_semantic_transfer.*",
    "fig30_synthetic_noise_recovery.*",
    "fig31_cross_domain_portability_scope.*",
    "fig32_sun_category_failure_modes.*",
    "fig33_derm7pt_resnet50_diagnostics.*",
    "fig34_reproducibility_claim_gates.*",
    "fig25_34_revision_v4_figure_manifest.*",
    "fig25_34_revision_v4_subfigure_manifest.*",
    "fig2[5-9][a-z]_*.*",
    "fig3[0-4][a-z]_*.*",
    "fig2[5-9]_[a-z]_*.*",
    "fig3[0-4]_[a-z]_*.*",
]


def cleanup_previous_v4_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for pattern in OLD_GENERATED_PATTERNS:
        for file in OUT.glob(pattern):
            if file.is_file():
                file.unlink()


def p(rel: str) -> Path:
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(f"Required artifact is missing: {rel}")
    return path


def read_csv(rel: str) -> pd.DataFrame:
    return pd.read_csv(p(rel))


def read_json(rel: str) -> dict:
    return json.loads(p(rel).read_text(encoding="utf-8"))


def clean_label(text: object, width: int = 26) -> str:
    s = str(text).replace("_", " ")
    if len(s) <= width:
        return s
    parts = s.split("/")
    if len(parts) > 1 and len(parts[-1]) <= width:
        return parts[-1].replace("_", " ")
    return s[: width - 1] + "..."


def metric_title(metric: str) -> str:
    return {
        "coverage": "Coverage",
        "covered_accuracy": "Covered accuracy",
        "covered_fidelity_to_base": "Covered fidelity",
        "all_object_accuracy": "All-object accuracy",
        "all_object_fidelity_to_base": "All-object fidelity",
        "conflict_rate": "Conflict rate",
        "abstention_rate": "Abstention rate",
        "test_mae": "Transition MAE",
        "prototype_unseen_accuracy": "Prototype accuracy",
        "symbolic_template_unseen_accuracy": "Symbolic accuracy",
        "prototype_unseen_macro_f1": "Prototype macro-F1",
        "symbolic_template_unseen_macro_f1": "Symbolic macro-F1",
        "symbolic_template_mean_hamming": "Mean Hamming distance",
    }.get(metric, metric.replace("_", " ").title())


def fig_ax(
    width: float = 3.7,
    height: float = 2.75,
    left: float = 0.16,
    right: float = 0.96,
    bottom: float = 0.18,
    top: float = 0.86,
):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)
    return fig, ax


def style_axis(ax, xlabel: str | None = None, ylabel: str | None = None) -> None:
    if xlabel:
        ax.set_xlabel(xlabel, labelpad=4)
    if ylabel:
        ax.set_ylabel(ylabel, labelpad=4)
    ax.tick_params(axis="both", labelsize=6.8, length=2.5)


def set_title(ax, title: str) -> None:
    ax.set_title("")


def polish_figure(fig) -> None:
    for ax in fig.axes:
        ax.set_title("")
        for text in ax.findobj(Text):
            text.set_fontsize(text.get_fontsize() * TEXT_SCALE)
        legend = ax.get_legend()
        if legend is not None:
            legend.set_frame_on(False)


def save(fig, stem: str, conclusion: str, source_data: str, archetype: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    base = OUT / stem
    polish_figure(fig)
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)
    FIGURES.append(
        {
            "figure": stem,
            "pdf": str(base.with_suffix(".pdf").relative_to(ROOT)),
            "archetype": archetype,
            "core_conclusion": conclusion,
            "source_data": source_data,
        }
    )


def draw_status_dot(ax, x: float, y: float, ok: bool, label: str) -> None:
    color = PALETTE["green_dark"] if ok else PALETTE["red"]
    ax.scatter([x], [y], s=36, color=color, edgecolor="white", linewidth=0.6, zorder=3)
    ax.text(x + 0.05, y, label, va="center", ha="left", fontsize=7)


def aggregate_object_intervals() -> pd.DataFrame:
    boot = read_csv("outputs/revision_v3/statistics/object_level_bootstrap_intervals.csv")
    metrics = ["coverage", "covered_accuracy", "covered_fidelity_to_base", "conflict_rate", "abstention_rate"]
    datasets = ["AwA2", "SUN", "Derm7pt"]
    rows = []
    for dataset in datasets:
        for metric in metrics:
            sub = boot[(boot["dataset"] == dataset) & (boot["metric"] == metric)]
            if sub.empty:
                continue
            rows.append(
                {
                    "dataset": dataset,
                    "metric": metric,
                    "mean": sub["mean"].mean(),
                    "ci_low": sub["ci_low"].min(),
                    "ci_high": sub["ci_high"].max(),
                }
            )
    return pd.DataFrame(rows)


def fig25_subfigures() -> None:
    v1 = read_json("outputs/revision_v1/revision_v1_run_summary.json")
    v2 = read_json("outputs/revision_v2/qc/qc_summary.json")
    v3 = read_json("outputs/revision_v3/manifest_revision_v3.json")
    claim = read_csv("outputs/revision_v2/qc/claim_consistency_check.csv")
    qc = read_csv("outputs/revision_v3/qc/qc_checklist.csv")

    fig, ax = fig_ax(6.2, 2.3, left=0.03, right=0.98, bottom=0.12, top=0.84)
    ax.set_axis_off()
    set_title(ax, "Cumulative revision evidence path")
    stages = [
        ("v1 reviewer revision", "AwA2 seeds\nSUN + Derm7pt\nclaim gates", PALETTE["blue"]),
        ("v2 hardening", "schemas\nclaim checks\nbootstrap CIs", PALETTE["teal"]),
        ("v3 traceability", "object exports\nSUN metadata\nResNet-50 Derm7pt", PALETTE["violet"]),
    ]
    xs = [0.15, 0.50, 0.85]
    for i, (title, body, color) in enumerate(stages):
        box = FancyBboxPatch(
            (xs[i] - 0.13, 0.34),
            0.26,
            0.42,
            boxstyle="round,pad=0.018,rounding_size=0.025",
            facecolor=color,
            edgecolor=PALETTE["black"],
            linewidth=0.8,
            alpha=0.94,
            transform=ax.transAxes,
        )
        ax.add_patch(box)
        ax.text(xs[i], 0.63, title, transform=ax.transAxes, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(xs[i], 0.44, body, transform=ax.transAxes, ha="center", va="center", color="white", fontsize=6.7)
        if i < 2:
            ax.add_patch(
                FancyArrowPatch(
                    (xs[i] + 0.15, 0.55),
                    (xs[i + 1] - 0.15, 0.55),
                    arrowstyle="-|>",
                    mutation_scale=11,
                    color=PALETTE["neutral3"],
                    linewidth=1.2,
                    transform=ax.transAxes,
                )
            )
    ax.text(0.5, 0.13, "v2/v3 validate and extend v1 artifacts; they do not replace the v1 evidence bundle.", ha="center", fontsize=7, transform=ax.transAxes)
    save(fig, "fig25_a_revision_pipeline", "v1-v3 revision artifacts form a cumulative evidence path.", "outputs/revision_v1/revision_v1_run_summary.json; outputs/revision_v2/qc/claim_consistency_check.csv; outputs/revision_v3/manifest_revision_v3.json", "schematic-led subfigure")

    counts = [len([x for x in (ROOT / "outputs" / rev).rglob("*") if x.is_file()]) for rev in ["revision_v1", "revision_v2", "revision_v3"]]
    fig, ax = fig_ax(3.2, 2.8)
    ax.bar(["v1", "v2", "v3"], counts, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["violet"]], edgecolor=PALETTE["black"], linewidth=0.6)
    for i, val in enumerate(counts):
        ax.text(i, val + max(counts) * 0.025, str(val), ha="center", va="bottom", fontsize=6.5)
    set_title(ax, "Generated artifact files")
    style_axis(ax, ylabel="Files")
    save(fig, "fig25_b_artifact_counts", "The revision generated a multi-version artifact bundle.", "outputs/revision_v1; outputs/revision_v2; outputs/revision_v3", "quantitative subfigure")

    fig, ax = fig_ax(3.7, 2.85, left=0.04, right=0.98, bottom=0.08, top=0.86)
    ax.set_axis_off()
    set_title(ax, "Revision claim gates")
    gates = [
        (v1.get("status") == "ok", "v1 runner status"),
        (bool(v1.get("sun_completed")), "SUN gate complete"),
        (bool(v1.get("derm7pt_completed")), "Derm7pt gate complete"),
        (v2.get("status") == "pass", "v2 QC pass"),
        (v3.get("status") == "pass", "v3 manifest pass"),
    ]
    for i, (ok, label) in enumerate(gates):
        draw_status_dot(ax, 0.10, 0.78 - i * 0.16, ok, label)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(fig, "fig25_c_claim_gates", "SUN, Derm7pt, and QC gates are explicitly recorded.", "outputs/revision_v1/revision_v1_run_summary.json; outputs/revision_v2/qc/qc_summary.json; outputs/revision_v3/manifest_revision_v3.json", "quantitative subfigure")

    checks = [
        ("claim checks", (claim["status"] == "pass").mean()),
        ("v3 QC checks", (qc["status"] == "pass").mean()),
        ("artifact hash list", 1.0 if v3.get("artifact_count", 0) > 0 else 0.0),
    ]
    fig, ax = fig_ax(3.6, 2.8, left=0.30)
    ax.barh([c[0] for c in checks], [c[1] for c in checks], color=PALETTE["green"], edgecolor=PALETTE["black"], linewidth=0.6)
    ax.set_xlim(0, 1.05)
    set_title(ax, "Validation completeness")
    style_axis(ax, xlabel="Pass fraction")
    save(fig, "fig25_d_validation_completeness", "Claim and QC validation completeness is machine-readable.", "outputs/revision_v2/qc/claim_consistency_check.csv; outputs/revision_v3/qc/qc_checklist.csv", "quantitative subfigure")


def fig26_subfigures() -> None:
    agg = aggregate_object_intervals()
    datasets = ["AwA2", "SUN", "Derm7pt"]

    fig, ax = fig_ax(4.6, 3.1, left=0.13, right=0.77, bottom=0.17, top=0.82)
    x = np.arange(len(datasets))
    width = 0.24
    for j, (metric, color) in enumerate([("coverage", PALETTE["blue"]), ("covered_accuracy", PALETTE["green_dark"]), ("covered_fidelity_to_base", PALETTE["teal"])]):
        vals = [agg[(agg.dataset == d) & (agg.metric == metric)]["mean"].iloc[0] for d in datasets]
        ax.bar(x + (j - 1) * width, vals, width=width, label=metric_title(metric), color=color, edgecolor=PALETTE["black"], linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylim(0, 1.22)
    ax.legend(fontsize=6, loc="upper center", ncol=1)
    set_title(ax, "Object-level audit outcomes")
    style_axis(ax, ylabel="Rate")
    save(fig, "fig26_a_object_level_audit_outcomes", "Enhanced prediction exports expose object-level coverage, accuracy, and fidelity.", "outputs/revision_v3/statistics/object_level_metric_summary.csv; outputs/revision_v3/statistics/object_level_bootstrap_intervals.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.2, 3.0, left=0.13, right=0.78, bottom=0.17, top=0.83)
    for j, (metric, color) in enumerate([("conflict_rate", PALETTE["red_soft"]), ("abstention_rate", PALETTE["neutral2"])]):
        vals = [agg[(agg.dataset == d) & (agg.metric == metric)]["mean"].iloc[0] for d in datasets]
        ax.bar(x + (j - 0.5) * 0.32, vals, width=0.30, label=metric_title(metric), color=color, edgecolor=PALETTE["black"], linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylim(0, 1.22)
    ax.legend(fontsize=6, loc="upper center", ncol=2)
    set_title(ax, "Conflict and abstention expose audit limits")
    style_axis(ax, ylabel="Rate")
    save(fig, "fig26_b_conflict_abstention_limits", "Conflict and abstention reveal where symbolic auditing does not cover the base model.", "outputs/revision_v3/statistics/object_level_metric_summary.csv", "quantitative subfigure")

    forest = agg[agg["metric"].isin(["coverage", "covered_accuracy", "covered_fidelity_to_base"])].copy()
    forest["label"] = forest["dataset"] + " | " + forest["metric"].map(metric_title)
    forest = forest.sort_values(["dataset", "metric"])
    fig, ax = fig_ax(5.2, 3.6, left=0.38, right=0.96, bottom=0.15, top=0.87)
    y = np.arange(len(forest))[::-1]
    for yi, (_, row) in zip(y, forest.iterrows()):
        color = {"AwA2": PALETTE["blue"], "SUN": PALETTE["teal"], "Derm7pt": PALETTE["violet"]}[row["dataset"]]
        ax.plot([row["ci_low"], row["ci_high"]], [yi, yi], color=color, lw=1.4)
        ax.plot(row["mean"], yi, "o", color=color, ms=4.2)
    ax.set_yticks(y)
    ax.set_yticklabels(forest["label"], fontsize=5.8)
    ax.set_xlim(0, 1.02)
    set_title(ax, "Object-level bootstrap intervals")
    style_axis(ax, xlabel="Rate")
    save(fig, "fig26_c_object_level_bootstrap_intervals", "Object-level bootstrap intervals are computable from enhanced exports.", "outputs/revision_v3/statistics/object_level_bootstrap_intervals.csv", "quantitative subfigure")


def fig27_subfigures() -> None:
    summary = read_csv("outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv")
    paired = read_csv("outputs/revision_v2/statistics/paired_discretizer_intervals.csv")
    method_colors = {"WEDD": PALETTE["blue"], "MDLP-like entropy": PALETTE["teal"], "Equal frequency": PALETTE["neutral2"], "Equal width": PALETTE["neutral1"]}
    specs = [
        ("fig27_a_coverage_by_discretizer", "coverage_mean", "Coverage by discretizer", "Rate"),
        ("fig27_b_accuracy_by_discretizer", "covered_accuracy_mean", "Covered accuracy by discretizer", "Rate"),
        ("fig27_c_fidelity_by_discretizer", "covered_fidelity_to_base_mean", "Covered fidelity by discretizer", "Rate"),
        ("fig27_d_conflict_by_discretizer", "conflict_rate_mean", "Conflict rate by discretizer", "Rate"),
    ]
    labels = [m.replace("MDLP-like entropy", "MDLP-like").replace("Equal ", "Eq. ") for m in summary["method"]]
    for stem, col, title, ylabel in specs:
        fig, ax = fig_ax(4.1, 3.1, left=0.15, right=0.95, bottom=0.25, top=0.84)
        vals = summary[col].values
        ax.bar(range(len(vals)), vals, color=[method_colors.get(m, PALETTE["neutral2"]) for m in summary["method"]], edgecolor=PALETTE["black"], linewidth=0.5)
        ax.set_xticks(range(len(vals)))
        ax.set_xticklabels(labels, rotation=28, ha="right", fontsize=6)
        if "conflict" in col:
            ax.set_ylim(0, min(0.50, max(vals) * 1.25))
        else:
            ax.set_ylim(max(0, vals.min() - 0.08), min(1.0, vals.max() + 0.08))
        set_title(ax, title)
        style_axis(ax, ylabel=ylabel)
        save(fig, stem, "Discretizer comparisons quantify WEDD without claiming universal superiority.", "outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv", "quantitative subfigure")

    keep = paired[paired["metric"].isin(["coverage", "covered_accuracy", "covered_fidelity_to_base", "all_object_accuracy", "conflict_rate", "abstention_rate"])].copy()
    keep["label"] = keep["metric"].map(metric_title)
    keep = keep.sort_values("mean_difference_wedd_minus_mdlp")
    fig, ax = fig_ax(4.8, 3.3, left=0.36, right=0.96, bottom=0.16, top=0.86)
    y = np.arange(len(keep))[::-1]
    for yi, (_, row) in zip(y, keep.iterrows()):
        color = PALETTE["green_dark"] if row["mean_difference_wedd_minus_mdlp"] >= 0 else PALETTE["red"]
        ax.plot([row["ci_low"], row["ci_high"]], [yi, yi], color=color, lw=1.5)
        ax.plot(row["mean_difference_wedd_minus_mdlp"], yi, "o", color=color, ms=4.2)
    ax.axvline(0, color=PALETTE["neutral3"], lw=0.8, ls="--")
    ax.set_yticks(y)
    ax.set_yticklabels(keep["label"], fontsize=6)
    set_title(ax, "Paired WEDD minus MDLP-like intervals")
    style_axis(ax, xlabel="Rate difference")
    save(fig, "fig27_e_paired_wedd_mdlp_intervals", "Paired intervals show modest WEDD effects and preserve cautious framing.", "outputs/revision_v2/statistics/paired_discretizer_intervals.csv", "quantitative subfigure")


def fig28_subfigures() -> None:
    q = read_csv("outputs/revision_v1/sensitivity/awa2_q_sensitivity.csv")
    rank = read_csv("outputs/revision_v1/sensitivity/awa2_svd_rank_sensitivity.csv")
    conf = read_csv("outputs/revision_v1/sensitivity/awa2_confidence_threshold_frontier.csv")
    runtime = read_csv("outputs/revision_v1/runtime/runtime_summary.csv")

    fig, ax = fig_ax(4.4, 3.0, left=0.14, right=0.78, bottom=0.16, top=0.84)
    for metric, color in [("coverage", PALETTE["blue"]), ("covered_fidelity_to_base", PALETTE["teal"]), ("conflict_rate", PALETTE["red_soft"])]:
        ax.plot(q["q"], q[metric], marker="o", lw=1.5, color=color, label=metric_title(metric))
    ax.set_ylim(0, 1.12)
    ax.legend(fontsize=6, loc="upper center", ncol=1)
    set_title(ax, "Quantile granularity sensitivity")
    style_axis(ax, xlabel="q", ylabel="Rate")
    save(fig, "fig28_a_q_sensitivity", "q sensitivity makes the granularity tradeoff inspectable.", "outputs/revision_v1/sensitivity/awa2_q_sensitivity.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.5, 3.1, left=0.14, right=0.86, bottom=0.16, top=0.84)
    ax.plot(rank["n_components"], rank["test_mae"], marker="o", lw=1.5, color=PALETTE["blue"], label="MAE")
    ax2 = ax.twinx()
    ax2.plot(rank["n_components"], rank["coverage"], marker="s", lw=1.2, color=PALETTE["teal"], label="Coverage")
    set_title(ax, "SVD rank affects bridge and coverage")
    style_axis(ax, xlabel="SVD rank", ylabel="Transition MAE")
    ax2.set_ylabel("Coverage", fontsize=7, labelpad=4)
    ax2.tick_params(axis="y", labelsize=6, length=2.5)
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles + handles2, labels + labels2, loc="upper center", fontsize=6, ncol=2)
    save(fig, "fig28_b_svd_rank_sensitivity", "SVD rank changes both reconstruction and rule coverage.", "outputs/revision_v1/sensitivity/awa2_svd_rank_sensitivity.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.5, 3.0, left=0.14, right=0.78, bottom=0.16, top=0.84)
    for metric, color in [("coverage", PALETTE["blue"]), ("covered_accuracy", PALETTE["green_dark"]), ("covered_fidelity_to_base", PALETTE["teal"])]:
        ax.plot(conf["confidence_threshold"], conf[metric], marker="o", lw=1.4, color=color, label=metric_title(metric))
    ax.set_ylim(0, 1.12)
    ax.legend(fontsize=6, loc="upper center", ncol=1)
    set_title(ax, "Confidence threshold frontier")
    style_axis(ax, xlabel="Rule confidence threshold", ylabel="Rate")
    save(fig, "fig28_c_confidence_threshold_frontier", "Confidence thresholds expose coverage, accuracy, and fidelity tradeoffs.", "outputs/revision_v1/sensitivity/awa2_confidence_threshold_frontier.csv", "quantitative subfigure")

    rt = runtime.copy()
    rt["label"] = rt["dataset"] + ": " + rt["phase"].str.replace("protocol_a_", "", regex=False).str.replace("_", " ")
    rt = rt.sort_values("sum", ascending=True).tail(8)
    fig, ax = fig_ax(4.6, 3.4, left=0.40, right=0.95, bottom=0.15, top=0.86)
    ax.barh(range(len(rt)), rt["sum"], color=PALETTE["neutral2"], edgecolor=PALETTE["black"], linewidth=0.5)
    ax.set_yticks(range(len(rt)))
    ax.set_yticklabels([clean_label(x, 30) for x in rt["label"]], fontsize=5.7)
    set_title(ax, "Runtime summary")
    style_axis(ax, xlabel="Total seconds")
    save(fig, "fig28_d_runtime_summary", "Runtime logs quantify the practical audit-tax components.", "outputs/revision_v1/runtime/runtime_summary.csv", "quantitative subfigure")


def fig29_subfigures() -> None:
    seed = read_csv("outputs/revision_v1/awa2/awa2_protocol_b_seedwise.csv")
    per_class = read_csv("outputs/revision_v1/awa2/awa2_protocol_b_per_class_seed42.csv")
    bat = read_csv("outputs/revision_v1/awa2/awa2_bat_diagnostic.csv")

    metrics = ["prototype_unseen_accuracy", "symbolic_template_unseen_accuracy", "prototype_unseen_macro_f1", "symbolic_template_unseen_macro_f1"]
    labels = ["Prototype acc.", "Symbolic acc.", "Prototype F1", "Symbolic F1"]
    fig, ax = fig_ax(4.2, 3.1, left=0.14, right=0.95, bottom=0.25, top=0.84)
    means, sds = seed[metrics].mean(), seed[metrics].std()
    ax.bar(range(len(metrics)), means, yerr=sds, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["blue2"], PALETTE["green"]], edgecolor=PALETTE["black"], linewidth=0.5, capsize=2)
    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=6)
    ax.set_ylim(0, 0.55)
    set_title(ax, "Protocol B semantic-transfer metrics")
    style_axis(ax, ylabel="Mean across seeds")
    save(fig, "fig29_a_protocol_b_seed_metrics", "Protocol B is reported as semantic-transfer validation, not ZSL competition.", "outputs/revision_v1/awa2/awa2_protocol_b_seedwise.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.0, 3.0, left=0.15, right=0.95, bottom=0.17, top=0.84)
    ax.scatter(seed["mae_unseen"], seed["prototype_unseen_accuracy"], s=36, color=PALETTE["blue"], edgecolor="white", linewidth=0.5, label="Prototype")
    ax.scatter(seed["mae_unseen"], seed["symbolic_template_unseen_accuracy"], s=36, color=PALETTE["teal"], edgecolor="white", linewidth=0.5, label="Symbolic")
    for _, row in seed.iterrows():
        ax.plot([row["mae_unseen"], row["mae_unseen"]], [row["symbolic_template_unseen_accuracy"], row["prototype_unseen_accuracy"]], color=PALETTE["neutral2"], lw=0.7, zorder=0)
    ax.legend(fontsize=6, loc="upper right")
    set_title(ax, "Transfer accuracy remains audit-scoped")
    style_axis(ax, xlabel="Unseen-class MAE", ylabel="Accuracy")
    save(fig, "fig29_b_transfer_accuracy_vs_mae", "Unseen transfer metrics support auditability rather than recognition competitiveness.", "outputs/revision_v1/awa2/awa2_protocol_b_seedwise.csv", "quantitative subfigure")

    pc = per_class.sort_values("prototype_accuracy")
    y = np.arange(len(pc))
    fig, ax = fig_ax(5.0, 3.7, left=0.25, right=0.96, bottom=0.15, top=0.86)
    ax.barh(y - 0.17, pc["prototype_accuracy"], height=0.32, color=PALETTE["blue"], label="Prototype", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.barh(y + 0.17, pc["symbolic_template_accuracy"], height=0.32, color=PALETTE["teal"], label="Symbolic template", edgecolor=PALETTE["black"], linewidth=0.4)
    bat_name = bat["class_name"].iloc[0]
    for yi, name in enumerate(pc["class_name"]):
        if name == bat_name:
            ax.add_patch(Rectangle((0, yi - 0.45), 1.02, 0.9, facecolor="#F6CFCB", alpha=0.35, edgecolor="none", zorder=-1))
            ax.text(0.78, yi, "bat rupture", fontsize=6, va="center", color=PALETTE["red"])
    ax.set_yticks(y)
    ax.set_yticklabels(pc["class_name"], fontsize=6)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(-0.6, len(pc) + 0.9)
    ax.legend(fontsize=6, loc="upper right")
    set_title(ax, "Per-class semantic-transfer rupture")
    style_axis(ax, xlabel="Accuracy")
    save(fig, "fig29_c_per_class_protocol_b_failures", "Per-class diagnostics localize semantic-transfer failures such as bat.", "outputs/revision_v1/awa2/awa2_protocol_b_per_class_seed42.csv; outputs/revision_v1/awa2/awa2_bat_diagnostic.csv", "quantitative subfigure")


def fig30_subfigures() -> None:
    syn = read_csv("outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv")
    specs = [
        ("fig30_a_synthetic_macro_f1", "macro_f1_mean", "macro_f1_ci95", "Synthetic macro-F1 under noise", PALETTE["blue"]),
        ("fig30_b_synthetic_rule_recovery", "rule_recovery_jaccard_mean", "rule_recovery_jaccard_ci95", "Rule recovery under noise", PALETTE["teal"]),
        ("fig30_c_synthetic_coverage", "coverage_mean", "coverage_ci95", "Synthetic coverage under noise", PALETTE["green_dark"]),
        ("fig30_d_synthetic_threshold_error", "threshold_recovery_error_mean", "threshold_recovery_error_ci95", "Threshold recovery error", PALETTE["red"]),
    ]
    for stem, mean_col, ci_col, title, color in specs:
        fig, ax = fig_ax(3.8, 2.9, left=0.15, right=0.96, bottom=0.17, top=0.84)
        x, y, ci = syn["sigma"].values, syn[mean_col].values, syn[ci_col].values
        ax.plot(x, y, marker="o", lw=1.6, color=color)
        ax.fill_between(x, y - ci, y + ci, color=color, alpha=0.16, linewidth=0)
        if mean_col != "threshold_recovery_error_mean":
            ax.set_ylim(max(0, min(y - ci) - 0.05), min(1.05, max(y + ci) + 0.05))
        set_title(ax, title)
        style_axis(ax, xlabel="Synthetic noise sigma", ylabel="Value")
        save(fig, stem, "Synthetic controls show recoverability and noise degradation within a bounded setting.", "outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv", "quantitative subfigure")


def fig31_subfigures() -> None:
    cross = read_csv("outputs/revision_v1/statistics/cross_domain_generalization.csv")
    cross["plot_dataset"] = cross["dataset"].replace({"AwA2 Protocol B": "AwA2 B"})
    metric = read_csv("outputs/revision_v3/statistics/object_level_metric_summary.csv")
    colors = {"AwA2": PALETTE["blue"], "SUN": PALETTE["teal"], "Derm7pt": PALETTE["violet"]}

    cm = cross.dropna(subset=["coverage"]).copy()
    fig, ax = fig_ax(4.0, 3.1, left=0.15, right=0.95, bottom=0.16, top=0.84)
    for _, row in cm.iterrows():
        ax.scatter(row["coverage"], row["covered_fidelity"], s=30 + row["attributes"] * 0.9, color=colors.get(row["dataset"], PALETTE["neutral2"]), alpha=0.85, edgecolor="white", linewidth=0.6)
        ax.text(row["coverage"] + 0.015, row["covered_fidelity"], row["dataset"], fontsize=6.4, va="center")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 0.82)
    set_title(ax, "Coverage-fidelity portability map")
    style_axis(ax, xlabel="Coverage", ylabel="Covered fidelity")
    save(fig, "fig31_a_portability_coverage_fidelity", "Cross-domain portability must be gated by coverage and fidelity.", "outputs/revision_v1/statistics/cross_domain_generalization.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.0, 3.1, left=0.15, right=0.95, bottom=0.24, top=0.84)
    x_cross = np.arange(len(cross))
    ax.bar(x_cross, cross["transition_mae"], color=[colors.get(d, PALETTE["neutral2"]) for d in cross["dataset"]], edgecolor=PALETTE["black"], linewidth=0.5)
    ax.set_xticks(x_cross)
    ax.set_xticklabels(cross["plot_dataset"], rotation=25, ha="right", fontsize=6)
    set_title(ax, "Transition reconstruction by scope")
    style_axis(ax, ylabel="MAE")
    save(fig, "fig31_b_transition_mae_by_scope", "Transition reconstruction differs by dataset and validation scope.", "outputs/revision_v1/statistics/cross_domain_generalization.csv", "quantitative subfigure")

    m = metric.copy()
    m["label"] = m["dataset"]
    m.loc[m["dataset"] == "AwA2", "label"] = "AwA2 seeds"
    grouped = m.groupby("label")[["coverage", "covered_accuracy", "covered_fidelity_to_base", "conflict_rate"]].mean().reset_index()
    labels = list(grouped["label"])
    x = np.arange(len(labels))
    fig, ax = fig_ax(4.8, 3.1, left=0.13, right=0.75, bottom=0.17, top=0.84)
    width = 0.18
    for i, (col, color) in enumerate([("coverage", PALETTE["blue"]), ("covered_accuracy", PALETTE["green_dark"]), ("covered_fidelity_to_base", PALETTE["teal"]), ("conflict_rate", PALETTE["red_soft"])]):
        ax.bar(x + (i - 1.5) * width, grouped[col], width=width, color=color, edgecolor=PALETTE["black"], linewidth=0.4, label=metric_title(col))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.25)
    ax.legend(fontsize=5.8, loc="upper center", ncol=2)
    set_title(ax, "v3 cross-domain object metrics")
    style_axis(ax, ylabel="Rate")
    save(fig, "fig31_c_cross_domain_object_metrics", "v3 stress tests preserve scoped interpretation across AwA2, SUN, and Derm7pt.", "outputs/revision_v3/statistics/object_level_metric_summary.csv", "quantitative subfigure")


def fig32_subfigures() -> None:
    sun = read_csv("outputs/revision_v3/sun/sun_category_diagnostics_v3.csv")
    sun["covered_fidelity_to_base"] = sun["covered_fidelity_to_base"].fillna(0.0)

    fig, ax = fig_ax(4.0, 3.0, left=0.15, right=0.95, bottom=0.16, top=0.84)
    bins = np.linspace(0, 1, 11)
    ax.hist(sun["coverage"], bins=bins, color=PALETTE["teal"], edgecolor="white", linewidth=0.5, alpha=0.92, label="Coverage")
    ax.hist(sun["conflict_rate"], bins=bins, color=PALETTE["red_soft"], edgecolor="white", linewidth=0.5, alpha=0.65, label="Conflict")
    ax.set_ylim(0, ax.get_ylim()[1] * 1.18)
    ax.legend(fontsize=6, loc="upper right", ncol=1)
    set_title(ax, "SUN category coverage and conflict")
    style_axis(ax, xlabel="Rate", ylabel="Number of categories")
    save(fig, "fig32_a_sun_category_histograms", "SUN category diagnostics are dominated by abstention and conflict.", "outputs/revision_v3/sun/sun_category_diagnostics_v3.csv", "quantitative subfigure")

    fig, ax = fig_ax(4.0, 3.1, left=0.15, right=0.95, bottom=0.16, top=0.84)
    ax.scatter(sun["coverage"], sun["conflict_rate"], s=np.clip(sun["n_objects"] * 3, 10, 60), color=PALETTE["neutral3"], alpha=0.35, edgecolor="none")
    ax.axvline(sun["coverage"].mean(), color=PALETTE["blue"], lw=1.0, ls="--", label="mean coverage")
    ax.axhline(sun["conflict_rate"].mean(), color=PALETTE["red"], lw=1.0, ls="--", label="mean conflict")
    ax.text(0.04, 0.90, f"zero coverage: {(sun.coverage == 0).mean():.1%}", fontsize=6.3, color=PALETTE["black"])
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.legend(fontsize=5.7, loc="upper right")
    set_title(ax, "SUN coverage-conflict map")
    style_axis(ax, xlabel="Coverage", ylabel="Conflict rate")
    save(fig, "fig32_b_sun_coverage_conflict_map", "SUN categories show high-conflict, low-coverage portability failure modes.", "outputs/revision_v3/sun/sun_category_diagnostics_v3.csv", "quantitative subfigure")

    top = sun.sort_values(["coverage", "covered_fidelity_to_base"], ascending=False).head(12).iloc[::-1]
    y = np.arange(len(top))
    fig, ax = fig_ax(5.2, 3.8, left=0.38, right=0.96, bottom=0.14, top=0.86)
    ax.barh(y - 0.17, top["coverage"], height=0.32, color=PALETTE["teal"], label="Coverage", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.barh(y + 0.17, top["covered_fidelity_to_base"], height=0.32, color=PALETTE["blue"], label="Covered fidelity", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([clean_label(x, 34) for x in top["scene_category"]], fontsize=5.5)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(-0.6, len(top) + 0.9)
    ax.legend(fontsize=6, loc="upper right")
    set_title(ax, "Best-covered SUN categories")
    style_axis(ax, xlabel="Rate")
    save(fig, "fig32_c_sun_best_covered_categories", "Best-covered SUN categories are narrow exceptions, not broad portability proof.", "outputs/revision_v3/sun/sun_category_diagnostics_v3.csv", "quantitative subfigure")


def fig33_subfigures() -> None:
    diag = read_csv("outputs/revision_v3/derm7pt/derm7pt_diagnosis_diagnostics_v3.csv")
    concept = read_csv("outputs/revision_v3/derm7pt/derm7pt_concept_diagnostics_v3.csv")
    enc = read_json("outputs/revision_v3/derm7pt/derm7pt_encoder_manifest.json")

    d = diag.sort_values("covered_accuracy")
    y = np.arange(len(d))
    fig, ax = fig_ax(5.0, 3.6, left=0.34, right=0.96, bottom=0.14, top=0.86)
    ax.barh(y - 0.15, d["covered_accuracy"], height=0.28, color=PALETTE["green_dark"], label="Covered accuracy", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.barh(y + 0.15, d["covered_fidelity_to_base"], height=0.28, color=PALETTE["violet"], label="Covered fidelity", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([clean_label(x, 29) for x in d["group"]], fontsize=5.6)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(-0.6, len(d) + 0.9)
    ax.legend(fontsize=5.8, loc="upper right")
    set_title(ax, "Derm7pt diagnosis-level diagnostics")
    style_axis(ax, xlabel="Rate")
    save(fig, "fig33_a_derm7pt_diagnosis_diagnostics", "Derm7pt diagnosis strata vary under technical validation only.", "outputs/revision_v3/derm7pt/derm7pt_diagnosis_diagnostics_v3.csv", "quantitative subfigure")

    fig, ax = fig_ax(3.8, 3.0, left=0.06, right=0.97, bottom=0.08, top=0.86)
    ax.set_axis_off()
    set_title(ax, "Locked dermoscopic encoder")
    info = [
        ("Encoder", "ResNet-50"),
        ("Weights", "ImageNet1K V2"),
        ("Feature dim.", str(enc.get("feature_dim"))),
        ("Cases", str(enc.get("n_cases"))),
        ("Device", str(enc.get("device"))),
        ("Scope", "technical only"),
    ]
    ax.add_patch(FancyBboxPatch((0.03, 0.08), 0.92, 0.76, boxstyle="round,pad=0.02,rounding_size=0.025", facecolor=PALETTE["neutral0"], edgecolor=PALETTE["neutral2"], linewidth=0.7))
    for i, (k, v) in enumerate(info):
        y0 = 0.73 - i * 0.105
        ax.text(0.12, y0, k, fontsize=6.8, color=PALETTE["neutral3"], ha="left", va="center")
        ax.text(0.49, y0, v, fontsize=6.8, color=PALETTE["black"], ha="left", va="center")
    save(fig, "fig33_b_derm7pt_encoder_manifest", "Derm7pt v3 uses a locked ImageNet ResNet-50 encoder, not a clinical model.", "outputs/revision_v3/derm7pt/derm7pt_encoder_manifest.json", "schematic subfigure")

    c = concept[concept["n_cases"] >= 10].copy()
    c["label"] = c["concept"].str.replace("_", " ", regex=False) + "=" + c["concept_value"].astype(str).str.replace("_", " ", regex=False)
    c = c.sort_values("covered_fidelity_to_base", ascending=False).head(14).iloc[::-1]
    y = np.arange(len(c))
    fig, ax = fig_ax(5.5, 4.0, left=0.40, right=0.96, bottom=0.13, top=0.86)
    ax.barh(y - 0.15, c["covered_accuracy"], height=0.28, color=PALETTE["green_dark"], label="Covered accuracy", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.barh(y + 0.15, c["covered_fidelity_to_base"], height=0.28, color=PALETTE["violet"], label="Covered fidelity", edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels([clean_label(x, 38) for x in c["label"]], fontsize=5.4)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(-0.6, len(c) + 0.9)
    ax.legend(fontsize=5.8, loc="upper right")
    set_title(ax, "Derm7pt checklist-concept strata")
    style_axis(ax, xlabel="Rate")
    save(fig, "fig33_c_derm7pt_concept_diagnostics", "Checklist-concept diagnostics support retrospective technical interpretation only.", "outputs/revision_v3/derm7pt/derm7pt_concept_diagnostics_v3.csv", "quantitative subfigure")


def fig34_subfigures() -> None:
    artifact_index = read_csv("outputs/revision_v3/artifact_index_revision_v3.csv")
    claim = read_csv("outputs/revision_v2/qc/claim_consistency_check.csv")
    qc = read_csv("outputs/revision_v3/qc/qc_checklist.csv")
    bundle = read_json("outputs/revision_v3/submission_bundle/manifest.json")
    manifest = read_json("outputs/revision_v3/manifest_revision_v3.json")

    ai = artifact_index.copy()
    ai["family"] = ai["path"].str.split("/").str[:3].str.join("/")
    fam = ai["family"].value_counts().head(10).sort_values()
    fig, ax = fig_ax(4.7, 3.5, left=0.42, right=0.95, bottom=0.14, top=0.86)
    ax.barh(range(len(fam)), fam.values, color=PALETTE["blue2"], edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(range(len(fam)))
    ax.set_yticklabels([clean_label(x, 30) for x in fam.index], fontsize=5.4)
    set_title(ax, "Hash-indexed v3 artifact families")
    style_axis(ax, xlabel="Files")
    save(fig, "fig34_a_artifact_hash_families", "The v3 artifact index records hash-addressed artifact families.", "outputs/revision_v3/artifact_index_revision_v3.csv", "quantitative subfigure")

    claim_status = claim.assign(value=(claim["status"] == "pass").astype(int))
    fig, ax = fig_ax(4.6, 3.4, left=0.43, right=0.95, bottom=0.14, top=0.86)
    ax.barh(range(len(claim_status)), claim_status["value"], color=PALETTE["green"], edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(range(len(claim_status)))
    ax.set_yticklabels([clean_label(x, 32) for x in claim_status["claim_id"]], fontsize=5.3)
    ax.set_xlim(0, 1.05)
    set_title(ax, "Manuscript claim checks")
    style_axis(ax, xlabel="Pass")
    save(fig, "fig34_b_manuscript_claim_checks", "Automated claim checks tie manuscript claims to generated artifacts.", "outputs/revision_v2/qc/claim_consistency_check.csv", "quantitative subfigure")

    qc_status = qc.assign(value=(qc["status"] == "pass").astype(int))
    fig, ax = fig_ax(4.3, 3.2, left=0.37, right=0.95, bottom=0.14, top=0.86)
    ax.barh(range(len(qc_status)), qc_status["value"], color=PALETTE["teal"], edgecolor=PALETTE["black"], linewidth=0.4)
    ax.set_yticks(range(len(qc_status)))
    ax.set_yticklabels([clean_label(x, 30) for x in qc_status["check"]], fontsize=5.4)
    ax.set_xlim(0, 1.05)
    set_title(ax, "v3 QC checklist")
    style_axis(ax, xlabel="Pass")
    save(fig, "fig34_c_v3_qc_checklist", "The v3 QC checklist passes required manuscript and artifact checks.", "outputs/revision_v3/qc/qc_checklist.csv", "quantitative subfigure")

    required = bundle.get("required_present", {})
    fig, ax = fig_ax(4.1, 3.0, left=0.06, right=0.97, bottom=0.08, top=0.86)
    ax.set_axis_off()
    set_title(ax, "Submission bundle gates")
    y = 0.75
    for key, val in required.items():
        ok = bool(val)
        ax.scatter([0.09], [y], s=36, color=PALETTE["green_dark"] if ok else PALETTE["red"], edgecolor="white", linewidth=0.5)
        ax.text(0.16, y, key.replace("_", " "), fontsize=6.8, ha="left", va="center")
        y -= 0.105
    ax.text(0.07, 0.08, f"v3 status: {manifest.get('status')} | artifacts: {manifest.get('artifact_count')}", fontsize=6.5, color=PALETTE["neutral3"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(fig, "fig34_d_submission_bundle_gates", "The shareable submission bundle records required files and excludes raw private data.", "outputs/revision_v3/submission_bundle/manifest.json; outputs/revision_v3/manifest_revision_v3.json", "schematic subfigure")


def write_manifest() -> None:
    manifest = pd.DataFrame(FIGURES)
    manifest.to_csv(OUT / "fig25_34_revision_v4_subfigure_manifest.csv", index=False)
    lines = [
        "# Revision v4 Subfigure Manifest",
        "",
        "All subfigures were generated with Python/matplotlib from existing revision artifacts and exported as PDF only.",
        "Visible panel letters were intentionally omitted; subfigure letters are encoded only in filenames.",
        "",
    ]
    for row in FIGURES:
        lines.extend(
            [
                f"## {row['figure']}",
                "",
                f"- Archetype: {row['archetype']}",
                f"- Core conclusion: {row['core_conclusion']}",
                f"- Source data: `{row['source_data']}`",
                f"- PDF: `{row['pdf']}`",
                "",
            ]
        )
    (OUT / "fig25_34_revision_v4_subfigure_manifest.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cleanup_previous_v4_outputs()
    fig25_subfigures()
    fig26_subfigures()
    fig27_subfigures()
    fig28_subfigures()
    fig29_subfigures()
    fig30_subfigures()
    fig31_subfigures()
    fig32_subfigures()
    fig33_subfigures()
    fig34_subfigures()
    write_manifest()
    print(json.dumps({"status": "ok", "subfigures": len(FIGURES), "figures": [r["figure"] for r in FIGURES]}, indent=2))


if __name__ == "__main__":
    main()
