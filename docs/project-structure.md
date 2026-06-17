# Project Structure

This repository is organized to separate manuscript sources, reproducible code, public outputs, audit evidence, and local private data.

## Manuscript

`manuscript/` contains the TeX package:

- `manuscript.tex`
- `references.bib`
- `manuscript.pdf`
- `manuscript.bbl`
- `Definitions/`

The manuscript intentionally imports figures from `../figs/` and tables from `../tables/` so generated assets remain shared with the reproduction scripts.

## Reproduction Code

* `run_experiments.py` at the root acts as the unified command-line entry point.
* `scripts/` houses the codebase, categorized into the following subfolders:
  * `core/`: Common utility algorithms (`paper1_core.py`, `revision_common.py`, `figure_style.py`).
  * `experiments/`: Specific baseline, ablation, and diagnostic evaluation runners.
  * `generators/`: PDF figure, LaTeX table, and visual asset generators.
  * `runners/`: Global orchestration pipelines (including v1, v2, v3 scripts).
  * `utils/`: Auditing and data preparation tools.
  * `legacy/`: Historical proof-of-concept scripts.

## Public Outputs

`artifacts/`, `figs/`, `tables/`, and `audit/` hold the public result package:

- `artifacts/awa2/` - AwA2 metrics, rulebooks, thresholds, predictions, and baseline outputs.
- `artifacts/synthetic/` - synthetic benchmark summaries and ground-truth rules.
- `figs/` - manuscript-ready PDF figures.
- `tables/` - TeX tables and CSV summary files.
- `audit/` - logs, manifests, rendered manuscript pages, and quality checks.

## Private Data

`data/` is a local workspace. Raw archives, downloaded datasets, sensitive notes, and private derived files should remain in ignored subfolders such as `data/raw/` and `data/private/`.

## Revision Reports & Outputs

* `reports/` stores historical walkthrough response logs and design documentation locally.
* `outputs/` holds raw caches, intermediate log matrices, and compilation steps for revision cycles.
