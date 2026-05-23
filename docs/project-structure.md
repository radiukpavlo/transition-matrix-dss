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

`scripts/` contains all experiment, figure-generation, table-generation, and audit scripts. Most scripts accept `--out .` so outputs are written to the repository-level artifact folders.

## Public Outputs

`artifacts/`, `figs/`, `tables/`, and `audit/` hold the public result package:

- `artifacts/awa2/` - AwA2 metrics, rulebooks, thresholds, predictions, and baseline outputs.
- `artifacts/synthetic/` - synthetic benchmark summaries and ground-truth rules.
- `figs/` - manuscript-ready PDF figures.
- `tables/` - TeX tables and CSV summary files.
- `audit/` - logs, manifests, rendered manuscript pages, and quality checks.

## Private Data

`data/` is a local workspace. Raw archives, downloaded datasets, sensitive notes, and private derived files should remain in ignored subfolders such as `data/raw/` and `data/private/`.
