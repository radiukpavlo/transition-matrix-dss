# SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-hoc Explainability

[![Preprint](https://img.shields.io/badge/Preprint-10.20944%2Fpreprints202606.0230.v1-blue)](https://www.preprints.org/manuscript/202606.0230)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository contains the official implementation, reproduction assets, computed result artifacts, figure and table generators, and quality gates auditing suite for the **SEMTRA** explainable AI (XAI) framework.

---

## 🔬 Core Scientific Contribution

SEMTRA introduces an explainable AI paradigm designed to bridge the semantic gap in deep neural representations through a post-hoc, concept-based symbolic translation pipeline. Instead of modifying core model weights (which often degrades performance) or relying solely on local attribution maps (which fail to define general policies), SEMTRA builds a global, auditable explanation layer.

### Technical Architecture
1. **Global Semantic Transition Matrix ($T$)**: Projects high-dimensional latent vectors ($X$) from standard vision backbones (e.g., ResNet-101/50) onto a continuous human-understandable concept space ($C = X \cdot T$), capturing global feature-attribute correlations.
2. **Vagueness Resolution via Rough-Set Approximations**: Concept projections are discretized using the Weighted Entropy-Density Discretization (WEDD) algorithm. Rough-Set Theory then defines upper ($\overline{B}X$) and lower ($\underline{B}X$) approximations of classes, separating sharp deterministic logical rules from highly vague boundary regions.
3. **Audit-Ready Rulebooks**: Induces noise-robust, traceable Boolean decision rules (e.g., `IF (swims AND flippers AND NOT fish) ⇒ Killer Whale`) that are equipped with explicit support, confidence, conflict, and abstention handling to support thorough post-hoc auditing.

### Figure 1: SEMTRA Framework Pipeline
The end-to-end flow from raw inputs and continuous representations to transition projection, discretization, rough-set approximations, and the final symbolic audit trail:
- [View Figure 1 PDF](./manuscript/figs_archived/fig01_semtra.pdf)
- Embedded diagram:
![SEMTRA Framework Pipeline](./manuscript/figs_archived/fig01_semtra.pdf)

### Figure 5: Conceptual Use-Case Mapping
Comparison between local single-case surrogates (which lack a reusable global policy) and the SEMTRA global semantic rulebook (which makes coverage and failure modes explicit):
- [View Figure 5 PDF](./manuscript/figs_archived/fig05_use-case.pdf)
- Embedded diagram:
![Surrogate vs. Global Rulebook](./manuscript/figs_archived/fig05_use-case.pdf)

---

## 📁 Repository Structure & Figure Archive Policy

- [scripts/core/](./scripts/core) — Core logic libraries (e.g., [figure_style.py](./scripts/core/figure_style.py)).
- [scripts/generators/](./scripts/generators) — Python figure and table generators.
- [manuscript/figs_archived/](./manuscript/figs_archived) — **Unified Figure Archive**. In accordance with submission policies, all generated publication figures are stored exclusively in this folder in PDF format only. SVGs and other image formats are disabled.
- [artifacts/](./artifacts) — Precomputed public experiment results (AwA2, SUN, Derm7pt, synthetic).
- [tables/](./tables) — Exported LaTeX table files and CSV matrices.
- [audit/](./audit) — Automated quality check logs and claim gate manifests.

---

## ⚙️ Reproducibility and Execution Guide

### Environment Setup
This codebase requires **Python 3.10** or higher. We recommend using a clean virtual environment:

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 1. Quick Asset Rebuild (From Existing Artifacts)
To regenerate all figures inside `manuscript/figs_archived/` using the audited public experiment results:

```bash
# Regenerates Figures 1-24
.venv/Scripts/python scripts/generators/generate_nature_figures.py

# Regenerates Figures 25-34 (Revision v4 details)
.venv/Scripts/python scripts/generators/generate_revision_v4_figures.py
```

### 2. Full Experiment Replication (From Raw Data)
To re-run all baseline comparisons, discretization sweeps, noise ablations, and rulebook inductions:

1. Place the raw benchmark archives into local directories:
   - `data/raw/awa2.zip` (Animals with Attributes 2)
   - `data/raw/xlsa17.zip` (Zero-shot learning benchmark package)
2. Run the unified experiments orchestrator:
   ```bash
   .venv/Scripts/python run_experiments.py --awa2_zip data/raw/awa2.zip --xlsa17_zip data/raw/xlsa17.zip --out . --seed 42
   ```

### 3. Package Verification & Quality Gates
To run the automated consistency audit and verify package integrity:
```bash
.venv/Scripts/python scripts/utils/audit_revision_package.py
```

---

## ✍️ Citation & Preprint

If you use this work or codebase in your research, please cite the following preprint:

```bibtex
@article{radiuk2026semtra,
  title     = {SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-hoc Explainability},
  author    = {Radiuk, Pavlo and Barmak, Oleksander and Krak, Iurii},
  journal   = {Preprints},
  year      = {2026},
  pages     = {202606.0230},
  doi       = {10.20944/preprints202606.0230.v1},
  url       = {https://www.preprints.org/manuscript/202606.0230}
}
```

Detailed document access is available via [Preprints.org Manuscript 202606.0230](https://www.preprints.org/manuscript/202606.0230).
