# Revision report: Paper 1 PoC XAI manuscript package

Generated: 2026-05-19T18:48:00.737194+00:00

## Scope

The revised package remains a non-medical proof-of-concept XAI manuscript. It focuses on Animals with Attributes 2 (AwA2) and a controlled synthetic benchmark. The legacy cardiac MRI/ECG placeholder title was not imported into the manuscript.

## Main implemented changes

### Comment 01: Preserve Paper 1 non-medical PoC boundary
- Status: `implemented`
- Action: Remove clinical placeholder and keep AwA2 plus synthetic only
- Files/artifacts: manuscript.tex; Sections 1-6
- Manuscript location: title, abstract, data availability
- Verification: No ECG/cardiac MRI claims in manuscript body.

### Comment 02: Run initial package audit
- Status: `implemented`
- Action: Create audit/revision_initial_audit.json and precompile log
- Files/artifacts: audit/revision_initial_audit.json; audit/revision_precompile.log; audit files
- Manuscript location: audit
- Verification: Initial audit and baseline compile logs are present.

### Comment 03: Use official xlsa17 split
- Status: `implemented`
- Action: Replace deterministic holdout with supplied official split
- Files/artifacts: scripts/run_official_xlsa_protocol.py; tables/table_protocol_b.tex; fig11
- Manuscript location: Results: Protocol B
- Verification: source_notes/awa2_split_note.md documents official xlsa17 usage.

### Comment 04: Track all reviewer comments
- Status: `implemented`
- Action: Create reviewer_response_matrix.csv with final statuses
- Files/artifacts: audit/reviewer_response_matrix.csv; revision_report.md
- Manuscript location: audit
- Verification: Thirty rows populated; no pending status.

### Comment 05: Add LIME baseline agreement
- Status: `implemented`
- Action: Implement local explanation agreement metrics
- Files/artifacts: scripts/run_local_xai_baselines.py; tables/table_local_xai_agreement.tex
- Manuscript location: Results: Agreement with local post-hoc explanations
- Verification: 1000 stratified objects evaluated.

### Comment 06: Add SHAP baseline agreement
- Status: `implemented`
- Action: Compute additive semantic-contribution agreement
- Files/artifacts: scripts/run_local_xai_baselines.py; tables/table_local_xai_agreement.tex
- Manuscript location: Results: Agreement with local post-hoc explanations
- Verification: SHAP-style agreement and CI reported.

### Comment 07: Document feature extractor
- Status: `implemented_with_limitation`
- Action: Add ResNet-101 feature extractor and preprocessing details
- Files/artifacts: manuscript.tex; README.md; tables/table_feature_extractor_hyperparameters.tex
- Manuscript location: Appendix A
- Verification: No raw-image augmentation was performed because supplied package uses released representation features.

### Comment 08: Train a base predictor
- Status: `implemented`
- Action: Train reproducible predictor on representation matrix
- Files/artifacts: scripts/train_base_predictor.py; tables/table_base_predictor_performance.tex
- Manuscript location: Results: Base predictor
- Verification: Predictions saved in artifacts/awa2/base_predictor_predictions.csv.

### Comment 09: Report Top-1, Top-5, F1, AUROC
- Status: `implemented`
- Action: Expand base predictor metrics
- Files/artifacts: scripts/train_base_predictor.py; tables/table_base_predictor_performance.tex
- Manuscript location: Results: Base predictor
- Verification: Top-1, Top-5, macro-F1, weighted-F1, AUROC, and ECE reported.

### Comment 10: Define fidelity metrics
- Status: `implemented`
- Action: Add covered and all-object fidelity definitions
- Files/artifacts: manuscript.tex; tables/table_explainability_metrics.tex
- Manuscript location: Methods: Evaluation metrics
- Verification: Fidelity added to rulebook, discretizer, and symbolic baseline tables.

### Comment 11: Add CBM baseline
- Status: `implemented`
- Action: Implement frozen-feature concept bottleneck
- Files/artifacts: scripts/run_cbm_tcav_baselines.py; tables/table_cbm_tcav_baselines.tex
- Manuscript location: Results: Concept baselines
- Verification: CBM reconstruction and class metrics reported.

### Comment 12: Add TCAV baseline
- Status: `implemented_with_limitation`
- Action: Implement concept-vector diagnostic at representation layer
- Files/artifacts: scripts/run_cbm_tcav_baselines.py; tables/table_cbm_tcav_baselines.tex
- Manuscript location: Results: Concept baselines
- Verification: TCAV is representation-layer only because raw activation stack is not supplied.

### Comment 13: Add CART baseline
- Status: `implemented`
- Action: Compare against decision tree rules
- Files/artifacts: scripts/run_symbolic_baselines.py; tables/table_symbolic_baselines.tex
- Manuscript location: Results: Symbolic baselines
- Verification: CART accuracy, fidelity, coverage, and rule count reported.

### Comment 14: Add RIPPER-like baseline
- Status: `implemented`
- Action: Compare against separate-and-conquer rules
- Files/artifacts: scripts/run_symbolic_baselines.py; tables/table_symbolic_baselines.tex
- Manuscript location: Results: Symbolic baselines
- Verification: RIPPER-like coverage, accuracy, fidelity, and conflict rate reported.

### Comment 15: Add WEDD ablation
- Status: `implemented`
- Action: Compare WEDD against MDLP/equal-frequency/equal-width
- Files/artifacts: scripts/run_discretizer_ablation.py; tables/table_wedd_ablation.tex
- Manuscript location: Results: Discretizer baselines
- Verification: Same reconstructed semantics and rule logic used.

### Comment 16: Add nonlinear transition ablation
- Status: `implemented`
- Action: Compare linear ridge, kernel ridge, and MLP
- Files/artifacts: scripts/run_transition_operator_ablation.py; tables/table_transition_operator_ablation.tex
- Manuscript location: Results: Transition-operator baselines
- Verification: Runtime, reconstruction, prototype, and rule metrics reported.

### Comment 17: Correct dimensionality bridge
- Status: `implemented`
- Action: Define compressed and full transition matrix dimensions
- Files/artifacts: manuscript.tex; Equations 1-2
- Manuscript location: Methods: Problem formulation
- Verification: SVD bridge dimensions explicitly stated.

### Comment 18: Define WEDD KDE density term
- Status: `implemented`
- Action: Add Gaussian KDE expression and stopping rules
- Files/artifacts: manuscript.tex; Algorithm 1
- Manuscript location: Methods: WEDD
- Verification: KDE formula, lambda, epsilon, min bin, and max depth stated.

### Comment 19: Formalize reduct objective
- Status: `implemented`
- Action: Add optimization constraint for support and confidence
- Files/artifacts: manuscript.tex; Equation 7
- Manuscript location: Methods: Rough-set granulation
- Verification: Greedy solver and tie-breaking described.

### Comment 20: Define selection score
- Status: `implemented`
- Action: Add salience/MAE score and alpha
- Files/artifacts: manuscript.tex; tables/table_selected_attributes.tex
- Manuscript location: Methods: Attribute selection
- Verification: Score formula and components reported.

### Comment 21: Define symbolic Hamming distance
- Status: `implemented`
- Action: Add formula used by Protocol B/fallback
- Files/artifacts: manuscript.tex; Equation 8
- Manuscript location: Methods: Rule inference
- Verification: Wildcard/non-wildcard denominator convention described.

### Comment 22: Add complexity analysis
- Status: `implemented`
- Action: Add Big-O complexity and memory discussion
- Files/artifacts: manuscript.tex; Methods subsection
- Manuscript location: Methods: Computational complexity
- Verification: SVD, ridge, WEDD, granules, reducts, and inference costs described.

### Comment 23: Add explainability metrics table
- Status: `implemented`
- Action: Report sparsity, coverage, abstention, support, confidence
- Files/artifacts: scripts/generate_revision_tables.py; tables/table_explainability_metrics.tex
- Manuscript location: Results: Rulebook structure
- Verification: Metrics generated from artifacts.

### Comment 24: Add coverage-abstention tradeoff
- Status: `implemented`
- Action: Generate confidence-threshold plot
- Files/artifacts: scripts/generate_revision_figures.py; fig15_coverage_abstention_tradeoff.pdf
- Manuscript location: Results: Rule traces and tradeoff
- Verification: Raw CSV saved as coverage_abstention_tradeoff.csv.

### Comment 25: Add rule stability assessment
- Status: `implemented`
- Action: Perturb semantic representations and report consistency
- Files/artifacts: scripts/run_rule_stability.py; tables/table_rule_stability.tex; fig16
- Manuscript location: Results and Appendix C
- Verification: Sigma grid and consistency metrics reported.

### Comment 26: Improve figure aesthetics
- Status: `implemented_with_limitation`
- Action: Regenerate revision figures with consistent style
- Files/artifacts: scripts/figure_style.py; scripts/generate_revision_figures.py; fig14-fig16 plus retained figures
- Manuscript location: Figures
- Verification: Nature-figure skill not installed locally; equivalent local Matplotlib style used.

### Comment 27: Replace terminal-like rule trace
- Status: `implemented`
- Action: Use readable table-style representative trace
- Files/artifacts: scripts/generate_revision_figures.py; fig14_representative_rule_traces.pdf
- Manuscript location: Results: Rule traces
- Verification: Trace includes object, prediction, rule, support, confidence, source, antecedents.

### Comment 28: Expand references
- Status: `implemented`
- Action: Add 35-50 XAI, rough-set, discretization, and transition references
- Files/artifacts: references.bib; Bibliography
- Manuscript location: Related works
- Verification: 42 BibTeX entries; bibtex8 succeeds.

### Comment 29: Add abbreviations and variables
- Status: `implemented`
- Action: Include variables and abbreviations table
- Files/artifacts: scripts/generate_revision_tables.py; tables/table_abbreviations_variables.tex
- Manuscript location: After conflicts
- Verification: A, B, T, WEDD, CBM, TCAV, LIME, SHAP, CART, MDLP, KDE, fidelity, support included.

### Comment 30: Final package quality gate
- Status: `implemented`
- Action: Clean build, render, audit, and ZIP complete package
- Files/artifacts: scripts/audit_revision_package.py; audit/revision_final_audit.json
- Manuscript location: Final packaging
- Verification: pdflatex/bibtex sequence succeeds; PDF rendered to PNG for inspection.

## Key numerical results

- Base predictor test Top-1 accuracy: 0.7116; Top-5 accuracy: 0.9291; macro-F1: 0.5434.
- Primary transition bridge test MAE: 0.1295; RMSE: 0.1826; mean semantic correlation: 0.6828.
- Proposed rulebook: 54 rules; coverage: 0.8640; non-abstained accuracy: 0.4073; covered fidelity to base predictor: 0.3829.
- Official xlsa17 Protocol B: unseen nearest-prototype accuracy: 0.4644; symbolic-template accuracy: 0.3378.
- Synthetic benchmark: macro-F1: 0.8668; rule-recovery Jaccard: 0.7258; threshold recovery error: 0.0161; coverage: 0.9638.

## Documented limitations

- The package does not include original CNN logits or an end-to-end fine-tuned CNN; the revised base predictor is trained reproducibly on the supplied representation matrix.
- TCAV is implemented at the released representation layer because the full raw activation stack is not supplied.
- AwA2 attributes are class-level; object-level semantic annotations would permit stronger explanation validation.
- The requested nature-figure skill/repository was not available in the local skill directory; a local publication-style Matplotlib configuration was implemented instead.

## Build verification

- `pdflatex -> bibtex8 -> pdflatex -> pdflatex` succeeds with status `0 0 0 0`.
- The compiled PDF was rendered into 22 PNG pages under `audit/pdf_renders/` and summarized in `audit/render_contact_sheet.png`.
- The final package ZIP contains the manuscript source, compiled PDF, bibliography, MDPI definitions, scripts, figures, tables, artifacts, audits, source notes, README, and this revision report.

## Enhancement pass: expanded Results and Discussion, figure/table restructuring, and SOTA context

This enhancement pass implements the user's additional requirements after the revised submission package was produced.

### Manuscript expansion

- Rewrote and significantly expanded `manuscript.tex` to 10,515 counted English words by the package word-count audit.
- Expanded the Results section into a more rigorous structure: overview and figure placement, base predictor and semantic reconstruction, contextual AwA2 state-of-the-art comparison, rulebook and symbolic baselines, local and concept-based explanation agreement, official xlsa17 Protocol B transfer, synthetic rule recovery, stability, traces, and an interpretation matrix.
- Expanded the Discussion section with a rigorous interpretation of the 0.4073 non-abstained rule accuracy, an auditability-performance tradeoff analysis, state-of-the-art comparison interpretation, limitations, future work, and reproducibility/claims-discipline discussion.

### New figures

Created `scripts/generate_enhanced_results.py`, which reads existing experiment artifacts and generates these new publication figures:

- `fig17_results_dashboard.pdf`: unified dashboard for predictive, semantic, symbolic, Protocol B, and synthetic findings.
- `fig18_sota_awA2_context.pdf`: contextual AwA2 proposed-split comparison with published zero-shot baselines.
- `fig19_baseline_tradeoff_scatter.pdf`: symbolic baseline coverage-versus-covered-accuracy tradeoff.
- `fig20_explainability_quality_matrix.pdf`: multi-metric symbolic baseline matrix.
- `fig21_rule_inference_flow_funnel.pdf`: rule-inference flow through coverage, exact matching, fallback, correctness, and abstention.
- `fig22_synthetic_uncertainty_bands.pdf`: synthetic macro-F1, rule Jaccard, and coverage with 95% confidence intervals.
- `fig23_protocol_b_perclass_errors.pdf`: Protocol B per-class prototype and symbolic-template comparison.
- `fig24_attribute_salience_error_scatter.pdf`: semantic attribute salience-versus-error diagnostic.

### New tables

Generated these new TeX and CSV tables:

- `table_main_quantitative_results.tex` / `main_quantitative_results.csv`.
- `table_sota_quantitative_comparison.tex` / `sota_quantitative_comparison.csv`.
- `table_enhanced_baseline_synthesis.tex` / `enhanced_baseline_synthesis.csv`.
- `table_results_interpretation_matrix.tex` / `results_interpretation_matrix.csv`.
- `table_figure_table_placement_map.tex` / `figure_table_placement_map.csv`.

### Appendix restructuring

The main manuscript now retains the most important results and moves the majority of diagnostic figures/tables to the Appendix. The main Results section explicitly references all moved diagnostic figures, and Appendix Table A1 provides a placement map for all figure locations.

### Quantitative SOTA comparison

Added a new Results table comparing the proposed Protocol B variants with published AwA2 proposed-split class-averaged zero-shot baselines. The table uses official benchmark values for DAP, IAP, CONSE, CMT, SSE, LATEM, ALE, DEVISE, SJE, ESZSL, SYNC, SAE, and GFZSL, and computes the proposed rows from `artifacts/awa2/protocol_b_unseen_per_class.csv`.

### Verification

- Recompiled the MDPI manuscript successfully with `pdflatex -> bibtex8 -> pdflatex -> pdflatex`.
- Rendered the final 42-page PDF to PNG files using the PDF render workflow.
- Stored the final render contact sheet at `audit/enhanced_render_contact_sheet.png`.
- Stored generation and compile logs in `audit/`.
