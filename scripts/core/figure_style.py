"""Nature-style Matplotlib helpers for manuscript figures."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt


PALETTE = {
    "blue": "#0072B2",
    "sky": "#56B4E9",
    "teal": "#009E73",
    "orange": "#E69F00",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
    "yellow": "#F0E442",
    "black": "#1F1F1F",
    "dark": "#4D4D4D",
    "mid": "#8F8F8F",
    "light": "#D8D8D8",
    "pale_blue": "#DDECF7",
    "pale_teal": "#DDEFE8",
    "pale_orange": "#F8EAC7",
}

METHOD_COLORS = [
    PALETTE["blue"],
    PALETTE["teal"],
    PALETTE["orange"],
    PALETTE["purple"],
    PALETTE["sky"],
    PALETTE["vermillion"],
]


def apply_nature_style() -> None:
    """Apply compact Nature-family plotting defaults."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Liberation Sans", "sans-serif"],
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "font.size": 7.0,
        "axes.labelsize": 7.0,
        "axes.titlesize": 7.5,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "xtick.labelsize": 6.2,
        "ytick.labelsize": 6.2,
        "xtick.major.width": 0.55,
        "ytick.major.width": 0.55,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "legend.fontsize": 6.2,
        "legend.frameon": False,
        "figure.dpi": 180,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def apply_style() -> None:
    """Backward-compatible alias used by older scripts."""
    apply_nature_style()


def mm_to_in(mm: float) -> float:
    return mm / 25.4


def nature_size(width_mm: float = 89, height_mm: float = 60) -> tuple[float, float]:
    return mm_to_in(width_mm), mm_to_in(height_mm)


def style_axis(ax, grid_axis: str | None = None) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=2.5, width=0.55, pad=2)
    if grid_axis:
        ax.grid(True, axis=grid_axis, color="#D8D8D8", linewidth=0.35, alpha=0.65)
        ax.set_axisbelow(True)


def add_panel_label(ax, label: str, x: float = -0.08, y: float = 1.02, fontsize: float = 8) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=fontsize,
        fontweight="bold",
        color=PALETTE["black"],
    )


def luminance(hex_color: str) -> float:
    color = hex_color.lstrip("#")
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b


def contrast_text_color(hex_color: str) -> str:
    return "white" if luminance(hex_color) < 0.48 else PALETTE["black"]


def clean_label(value: object, max_len: int = 28) -> str:
    text = str(value).replace("_", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "..."


def annotate_bars(
    ax,
    bars: Iterable,
    values: Sequence[float],
    fmt: str = "{:.2f}",
    offset: float | None = None,
    fontsize: float = 6.0,
) -> None:
    vals = list(values)
    if not vals:
        return
    if offset is None:
        ymax = max(max(vals), 1e-9)
        offset = ymax * 0.025
    for bar, value in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + offset,
            fmt.format(value),
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color=PALETTE["black"],
        )


def save_nature_figure(
    fig,
    path: Path | str,
    formats: Sequence[str] = ("pdf", "svg"),
    dpi: int = 600,
    close: bool = True,
) -> list[str]:
    """Save one figure stem with editable vector text."""
    base = Path(path)
    if base.suffix:
        stem = base.with_suffix("")
    else:
        stem = base
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.7)
    saved: list[str] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        out = stem.with_suffix(f".{fmt}")
        kwargs = {"bbox_inches": "tight", "facecolor": "white"}
        if fmt in {"tif", "tiff"}:
            kwargs["dpi"] = dpi
            kwargs["pil_kwargs"] = {"compression": "tiff_lzw"}
        fig.savefig(out, **kwargs)
        saved.append(str(out))
    if close:
        plt.close(fig)
    return saved
