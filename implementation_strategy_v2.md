# Implementation Strategy v2 for Revising “SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-hoc Explainability”

## 1. What Still Needs To Be Done

### 1.1 Environment and Build Reproducibility

The LaTeX plugin auto compiler still cannot complete through `latexmk` because MiKTeX cannot find Perl. Direct `pdflatex` and `bibtex` passes work, so this is an environment/toolchain limitation rather than a manuscript failure. To make compilation robust for coauthors and CI, install Perl or configure the project to use a direct build recipe that does not depend on `latexmk`.

### 1.2 Scientific Limitations

SUN is currently a completed but weak cross-domain audit run. Coverage and covered fidelity are low, indicating that the present symbolic rulebook is not yet useful for fine-grained scene categories under the current feature protocol.

Derm7pt is technically complete but uses simple local image feature extraction. This is acceptable for a reproducibility-gated technical validation, but not for biomedical performance claims. It should not be described as clinical validation, diagnostic validation, or evidence of deployment readiness.

Protocol B remains a semantic-transfer diagnostic. It should not be converted back into a zero-shot learning leaderboard comparison. The symbolic-template result is substantially lower than the continuous prototype result, which is important evidence of the audit tax.

The WEDD-vs-MDLP evidence is still based on five paired seeds. The findings justify moderated claims, not strong statistical superiority.

### 1.3 Reporting and Packaging Gaps

Three BibTeX entries remain unused: `Frome2013DeViSE`, `Kalyta2023FacialEmotion`, and `Xian2016LATEM`. They are not harmful, but the final submission bibliography should either cite them intentionally or remove them if the journal requires strict citation minimality.

Some residual LaTeX warnings remain from the MDPI class and package interactions: `fancyhdr` head-height warnings, hyperref PDF-string warnings for math in metadata, algorithmicx duplicate destination warnings, an underfull alignment warning, and a MiKTeX update notice. These do not block compilation, but they should be reviewed before submission.

The raw datasets, downloaded archives, extraction caches, model weights, and `.venv/` are correctly untracked. The report and manifest document this, but the project would benefit from a concise external setup guide for coauthors who need to regenerate every artifact from scratch.

## Recommendations for Advancing the Research

### 2.1 Strengthen Cross-Domain Evidence

The next research increment should focus on turning SUN and Derm7pt from portability demonstrations into stronger validation studies.

For SUN:

- Run a scene-aware analysis by category groups or supercategories.
- Report class/category-level coverage and fidelity, not only aggregate values.
- Investigate whether low coverage is driven by specific scene categories, attribute sparsity, or feature/attribute mismatch.
- Compare xlsa17 ResNet-101 features with a modern frozen vision-language or self-supervised feature extractor, while keeping the audit protocol clearly separated from predictive SOTA claims.
- Add bootstrap confidence intervals over scene categories where object-level predictions are available.

For Derm7pt:

- Replace simple color/histogram features with a frozen dermoscopy-relevant encoder.
- Preserve the same official case-level splits to avoid leakage.
- Add per-diagnosis and per-checklist-concept diagnostics.
- Add class-imbalance-aware reporting, including macro-F1 and calibrated confusion summaries.
- Keep all prose explicitly framed as retrospective technical validation unless a clinically governed validation protocol is added.

### 2.2 Improve Statistical Rigor

The project should add:

- Bootstrap confidence intervals over objects/classes for coverage, covered accuracy, covered fidelity, conflict, and abstention.
- Paired confidence intervals for WEDD-vs-MDLP, not just standardized paired effects.
- Seed-wise or split-wise uncertainty for SUN and Derm7pt where feasible.
- A more explicit multiple-comparison policy for sensitivity grids.
- A claim-to-artifact checker that fails the build if abstract numbers drift from CSV/JSON values.

### 2.3 Improve SEMTRA Methodology

The current evidence supports SEMTRA as an audit layer. The next methodological work should target the audit tax directly:

- Learn dataset-specific symbolic template thresholds rather than relying on a single default rule confidence and fallback distance.
- Add optional class-conditional or group-conditional discretization for datasets like SUN where global thresholds appear weak.
- Explore compact rulebook selection under a coverage/fidelity Pareto objective.
- Add calibrated abstention criteria so low-confidence rule matches are handled consistently across datasets.
- Investigate hybrid continuous-symbolic explanations where low-coverage symbolic rules are paired with semantic residual diagnostics.

### 2.4 Improve Reproducibility Engineering

The project should add:

- A `Makefile`, `justfile`, or PowerShell script for `venv`, experiments, QC, and LaTeX fallback builds.
- CI checks for Python syntax, artifact schema validation, citation validation, duplicate-label checks, and direct LaTeX fallback compilation.
- A machine-readable schema for every generated CSV and JSON artifact.
- A clear policy on whether `manuscript/` should remain ignored. Clearly state that the manuscript must be ignored.
- A release checklist separating raw/private data, generated lightweight artifacts, and submission files.

### 2.5 Improve Manuscript Positioning

The revised manuscript is now substantially more defensible, but the final submission should keep the message disciplined:

- Lead with SEMTRA as auditability and failure-diagnosis infrastructure.
- Avoid presenting rulebook accuracy as a substitute for classifier accuracy.
- Treat low SUN coverage as an honest stress-test result, not as a weakness to hide.
- Use Derm7pt to demonstrate protocol portability and missing-value handling, not clinical performance.
- Keep WEDD framed as one tunable discretizer among alternatives.
- Emphasize that the central contribution is explicit measurement of coverage, abstention, conflict, covered fidelity, and covered accuracy.

## 3. Recommended Next Milestones

1. Fix the LaTeX toolchain by installing Perl for MiKTeX `latexmk` or documenting a direct `pdflatex`/`bibtex` fallback build script.
2. Decide whether `manuscript/` should remain ignored; clearly state that the manuscript must be ignored.
3. Add CI or a local one-command QC runner that reproduces the final checks now recorded under `outputs/revision_v1/qc/`.
4. Upgrade Derm7pt feature extraction to a frozen dermoscopy-relevant encoder and rerun the official split.
5. Diagnose SUN failures by category group and attribute subset.
6. Add bootstrap confidence intervals and object/class-level uncertainty summaries.
7. Add an automated manuscript-number consistency checker for abstract, tables, and conclusion.
8. Prepare a clean submission bundle containing `main.tex`, `supply.tex`, `references.bib`, generated tables, figures, and compile logs. Ensure that all 

