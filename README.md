# SEMTRA: Semantic Transition Matrix and Rough-Set Rules for Explainable AI

<!-- <p align="center">
  <img src="figs/framework_animation.svg" alt="XAI Decision Support System Framework" width="100%">
</p> -->

## A Transition-Matrix and Rough-Set Rule Induction Framework for Explainable AI (XAI)

This repository contains the official reproduction package, computed result artifacts, figure and table generators, and auditing manifests for the research study:

> **SEMTRA: Semantic Transition Matrix and Rough-Set Rules for Explainable AI**
> 
> *An explainable AI paradigm that maps continuous deep latent representations onto human-understandable concept attributes, resolves vagueness using rough-set theory, and induces discrete, noise-robust decision rules.*

---

## 🔬 Core Scientific Contribution

Deep neural networks achieve high classification accuracy but suffer from a "semantic gap" due to their opaque latent representations. Concept Bottleneck Models (CBMs) attempt to map latents to semantic attributes, but often introduce significant vagueness and drop in prediction accuracy. 

Our framework addresses this by:
1. **Semantic Mapping via Transition Matrix ($T$)**: Linearly projecting high-dimensional latent vectors ($X$) onto a human-interpretable concept space ($C = X \cdot T$).
2. **Vagueness Resolution via Rough-Set Approximations**: Calculating lower bounds ($\underline{B}X$) and upper bounds ($\overline{B}X$) on concept activations to delineate sharp, deterministic logic from highly uncertain/noisy concepts.
3. **Symbolic Rule Induction**: Automatically generating traceable, Boolean decision rules directly from approximations (e.g., `IF (swims AND flippers AND NOT fish) ⇒ Killer Whale`). 
4. **Resilience to Noise**: Exhibiting high tolerance to attribute labeling noise and representation drift, as demonstrated on Animals with Attributes 2 (AwA2) and synthetic datasets.

---

## 📁 Repository Structure & Tracking Policy

This repository is designed to separate reproducible source code and auditable public outcomes from local private data and manuscript workspaces. Under our active **[Gitignore Configuration](.gitignore)**, directories are governed by a strict tracking policy:

### 🟢 Tracked in Version Control
These directories house the public-facing reproducibility package:
* [run_experiments.py](./run_experiments.py) — Unified root-level CLI wrapper to run experiments.
* [scripts/](./scripts) — Core codebase organized into subfolders (`core`, `experiments`, `generators`, `runners`, `utils`, `legacy`).
* [artifacts/](./artifacts) — Public computed result metrics, rulebooks, and thresholds.
* [figs/](./figs) — Publication-ready vector diagrams (PDF, SVG) and dynamic assets.
* [tables/](./tables) — Output LaTeX tables and raw CSV summaries.
* [audit/](./audit) — Comprehensive logs, manifests, PDF renders, and quality gate metrics.
* [docs/](./docs) — Detailed project structures and user manuals.
* [source_notes/](./source_notes) — Technical details regarding dataset boundaries and AwA2 split handling.

### 🔴 Ignored Local Workspace (Local Only)
These folders are configured in `.gitignore` and are **never** committed to version control:
* `manuscript/` — Contains MDPI TeX sources, templates, and LaTeX build byproducts (fully ignored).
* `data/` — Contains raw local datasets (`data/raw/` for downloaded archives like `awa2.zip`) and local notes (`data/private/`).
* `.venv/`, `__pycache__/`, `.pytest_cache/` — Virtual environments and compiler caches.
* Developer specific files (credentials, VS Code `.vscode/`, PyCharm `.idea/`, general backups `*.bak`).

---

## ⚙️ Quick Setup

This project requires **Python 3.10** or newer. Set up a virtual environment and install standard dependencies:

### On Unix/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### On Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 Running Experiments & Rebuilding Assets

### Option A: Quick Rebuild (Generates Figures & Tables from Artifacts)
If you wish to regenerate the enhanced figures and tables using the pre-computed public results (stored under `artifacts/`):
```bash
python scripts/generators/generate_enhanced_results.py --root .
```
This script reads the checked-in metrics and saves updated publication-ready figures to `figs/` and LaTeX tables to `tables/`.

### Option B: Full Experiment Replication
To rerun all baseline comparisons, ablations, stability benchmarks, and rule induction from scratch, place the raw dataset archives inside the local ignored folder:
* `data/raw/awa2.zip` (Animals with Attributes 2 dataset)
* `data/raw/xlsa17.zip` (Standard Zero-Shot learning benchmarks)

Then execute the orchestration pipeline using the root-level wrapper:
```bash
python run_experiments.py \
  --awa2_zip data/raw/awa2.zip \
  --xlsa17_zip data/raw/xlsa17.zip \
  --out . \
  --seed 42 \
  --local_sample_size 1000
```
*Note: This calls the base CNN feature extractors, concept projection models, rough-set boundary estimators, symbolic rule engines, and outputs updated files into `artifacts/`, `figs/`, `tables/`, and `audit/`.*

---

## 🔍 Reproducibility & Package Auditing

To maintain high scientific integrity, this package implements automated reproducibility quality gates under the [audit/](./audit) directory:

- [audit/revision_initial_audit.json](./audit/revision_initial_audit.json) — Records the exact state of result artifacts before revisions.
- [audit/reviewer_response_matrix.csv](./audit/reviewer_response_matrix.csv) — A structured CSV tracking the status of all revision additions.
- [audit/revision_final_audit.json](./audit/revision_final_audit.json) — Final execution quality gate metrics and file integrity checks.
- [audit/enhanced_pdf_renders/](./audit/enhanced_pdf_renders) — Contains high-resolution PNG snapshots of rendered manuscript sheets for visual quality assurance.

You can verify the package integrity at any time by running:
```bash
python scripts/utils/audit_revision_package.py
```
