# Implementation Strategy v1 for Revising “SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-hoc Explainability”

**Target manuscript:** `main.tex`  
**Supplement:** `supply.tex`  
**Bibliography:** `references.bib`  
**Required post-implementation report:** `revision_report_v1.md`  
**Target journal:** *Machine Learning and Knowledge Extraction*  
**Language:** English (American)  
**Primary revision principle:** reviewer comments control scope; all quantitative and methodological claims must be traceable, moderated, and reproducible.

---

## 1. Executive Summary

Codex must revise the SEMTRA manuscript from a high-claim proof-of-concept narrative into a disciplined, auditable, reviewer-responsive manuscript. The revised manuscript must preserve SEMTRA’s core identity as a post-hoc, model-agnostic, global semantic-transition and rough-set rule-induction framework, but it must no longer imply universal superiority, competitive zero-shot learning status, WEDD superiority, or clinical readiness.

The implementation has six central objectives.

1. **Resolve internal contradictions.** Move the current WEDD-vs-MDLP-like entropy discretization ablation from Appendix B into the main Results section, because the current table shows MDLP-like entropy outperforming WEDD on several core metrics. Reframe WEDD as a density-aware, stability-oriented design option rather than a universally superior discretizer.
2. **Correct quantitative inconsistencies.** Replace the abstract’s synthetic macro-F1 claim of 0.8668 with a claim tied to the actual synthetic table values: macro-F1 = 0.879 at zero semantic noise, macro-F1 = 0.881 at \(\sigma=0.100\), and macro-F1 = 0.838 at \(\sigma=0.200\), after verifying the source scripts and table generation logs.
3. **Separate SEMTRA from the prior ETM paper.** Add an explicit novelty-separation paragraph and a compact main-text comparison table distinguishing SEMTRA from “Equivariant Transition Matrices for Explainable Deep Learning: A Lie Group Linearization Approach.” ETM targets symmetry-aware, Lie-group-constrained transition operators; SEMTRA targets semantic transition, discretization, rough-set granulation, conflict-aware rule induction, abstention, and rulebook auditability. The ETM publication and DOI must be verified from the current MDPI source before finalizing the bibliography. citeturn973439search0
4. **Demonstrate generalization beyond AwA2.** Add SUN Attribute Database and Derm7pt / Seven-Point Checklist experiments or, if execution is blocked by access or runtime, include a clearly delimited reproducible protocol and do not claim completed results. The SUN implementation must use the official SUN Attribute Database and IJCV paper: the database contains 102 attributes, 14,340 images, and 707 scene categories, with attributes covering materials, surface properties, lighting, affordances, and spatial layout. citeturn455266view0turn455266view1 The Derm7pt implementation must use the official dataset site and the `jeremykawahara/derm7pt` repository associated with the IEEE JBHI paper by Jeremy Kawahara, Sara Daneshvar, Giuseppe Argenziano, and Ghassan Hamarneh; the repository documents seven-point checklist criteria, diagnosis metadata, official indices, and DOI `10.1109/JBHI.2018.2824327`. citeturn455266view2turn455266view3
5. **Make the audit tax measurable.** Add SVD-rank \(r\) sensitivity, selected-attribute-count \(q\) sensitivity, confidence-threshold sensitivity, and per-phase runtime instrumentation. The revised discussion must state when the audit tax is acceptable and when it is not.
6. **Upgrade reproducibility and reporting.** Expand `supply.tex` with dataset-processing protocols, extended seed-wise results, runtime logs, sensitivity tables, discretizer stability, perturbation diagnostics, and rule traces. Codex must also create `revision_report_v1.md` with a comment-by-comment traceability matrix and a clear list of modified files, added tables/figures, recalculated values, moderated claims, remaining limitations, and verification status.

The manuscript must not hide negative or reviewer-critical evidence in the supplement. The WEDD-vs-MDLP-like entropy contradiction, metric definitions, audit-tax caveat, zero-shot reframing, and cross-domain generalization summary must appear in the main text.

---

## 2. Scope and Non-Scope

### 2.1 In Scope

Codex must implement or explicitly plan the following reviewer-driven changes.

- Revise `main.tex` abstract, introduction, related works, methods, results, discussion, conclusion, declarations where necessary, and appendices.
- Revise `references.bib` only to add reviewer-required references and to correct incomplete, duplicated, invalid, or inconsistent entries discovered during bibliography validation.
- Expand `supply.tex` from a minimal placeholder into a reproducibility supplement with extended experimental protocols and diagnostics.
- Add or regenerate result tables and figures from scripts, not by manual transcription.
- Add SUN Attribute Database and Derm7pt experiments or a documented execution gate that prevents claiming results not yet produced.
- Rerun or extract seed-wise SEMTRA Protocol B results and report uncertainty.
- Instrument runtime, memory, and reduct-search cost.
- Create `revision_report_v1.md` after implementation or after the implementation plan is frozen.
- Compile and validate LaTeX output, bibliography, labels, tables, references, and numeric consistency.

### 2.2 Non-Scope

Codex must not perform broad cosmetic rewriting, unrequested theory expansion, unrelated figure redesign, unrelated software refactoring, unrelated dataset additions, or author-positioning changes not justified by reviewer comments. Minor mechanical edits are allowed only when needed for compilation, MDPI compliance, duplicate-label resolution, grammar, or numerical traceability. Any such mechanical edits must be listed in `revision_report_v1.md` under “Non-substantive technical corrections.”

### 2.3 Claim Discipline

The revised manuscript must not claim:

- WEDD is superior unless a statistically supported metric shows superiority under the stated condition.
- SEMTRA is a competitive zero-shot learning method.
- SEMTRA replaces high-performance base models.
- SEMTRA is clinically ready on Derm7pt.
- SEMTRA applies to “all possible XAI problems.”
- A rulebook with approximately 40.73% covered accuracy is an unqualified success.

The revised manuscript may claim:

- SEMTRA exposes the verifiable subset of a black-box model’s semantic logic.
- SEMTRA reports coverage, abstention, conflict, covered fidelity, and covered accuracy explicitly.
- SEMTRA is useful for auditing, semantic debugging, failure diagnosis, dataset-bias inspection, and human-review triage.
- SEMTRA’s zero-shot protocol is a semantic-transfer validation, not a predictive SOTA comparison.
- WEDD is a tunable discretization option that prioritizes density-aware boundary placement and can trade off against entropy-dominant alternatives.

---

## 3. Input File Map and Current Evidence

### 3.1 `main.tex`

`main.tex` is the primary revision target. Current major locations and labels to use for edits are:

- `sec:introduction`: abstract-adjacent framing, contributions, novelty claim, ETM relation.
- `sec:related`: related works.
- `subsec:local_explanation`: local XAI framing.
- `subsec:concept_explanation`: concept-based and ante-hoc methods.
- `subsec:symbolic_rule_extraction`: rough-set and rule-induction literature; currently too thin for modern rough/fuzzy/neural hybrids.
- `subsec:semantic_transfer`: zero-shot framing; currently too close to competitive ZSL framing and outdated in baseline coverage.
- `sec:methods`: methods.
- `subsec:framework_overview`: currently overclaims “universal, modular, post-hoc proof-of-concept pipeline applicable to all possible XAI problems.”
- `subsec:transition_matrix`: transition matrix and SVD formulation.
- `subsec:methods_wedd`: WEDD definition and attribute selection; must be revised to avoid unconditional superiority.
- `subsec:inference_fidelity_metrics`: fidelity equations; must distinguish base-model agreement from ground-truth accuracy.
- `subsec:eval_metrics`: auditability metrics; must add formal definitions for coverage, abstention, conflict, covered fidelity, covered accuracy, all-object accuracy, and agreement with base model.
- `subsec:protocol`: experimental protocol; must add SUN and Derm7pt protocols, q/r sensitivity, runtime instrumentation, and updated Protocol B framing.
- `subsec:results_protocol_a`: semantic reconstruction results; add or cross-reference SVD-rank sensitivity and cross-domain summary.
- `subsec:rulebook_auditability`: rulebook results; insert moved discretizer table and audit-tax interpretation.
- `subsec:protocol_b_results`: currently labeled “Zero-Shot Transfer as Semantic Validation,” but the surrounding text and table still imply competitive zero-shot performance.
- `subsec:results_synthetic`: correct synthetic macro-F1 reporting.
- `subsec:interpreting_tax`: must be rewritten from “profound diagnostic triumph” to use-case-specific audit tradeoff.
- `subsec:limitations_directions`: add dataset, clinical, SVD/q, discretizer, and generalization limitations.
- `sec:app_hyperparameters`: move critical WEDD table out of Appendix B; retain extended hyperparameter and sensitivity tables here or in supplement.
- `sec:app_discretization`: after moving Table `tab:wedd_ablation` to the main text, leave extended boundary-stability diagnostics here or move them to `supply.tex`.
- `sec:app_stability`: retain rule traces and perturbation diagnostics; expand only if main text space is constrained.

Current internal issues Codex must address:

- Abstract reports synthetic macro-F1 = 0.8668, but `tab:synthetic_noise` reports 0.879 at \(\sigma=0.000\), 0.881 at \(\sigma=0.100\), and 0.838 at \(\sigma=0.200\).
- `tab:wedd_ablation` in Appendix B reports that MDLP-like entropy has stronger coverage, all accuracy, covered fidelity, and conflict rate than WEDD in the current AwA2 setting.
- The audit tax discussion currently calls the rulebook accuracy drop a “profound diagnostic triumph,” which overstates the evidence.
- Protocol B reports SEMTRA above DAP and IAP but below GFZSL; it must be reframed as semantic validation rather than a ZSL leaderboard claim.
- Figure `fig:conc_comparison` is conceptual but its caption and surrounding text could be read as a quantitative result.
- The supplement is essentially empty and cannot support reproducibility.

### 3.2 `references.bib`

The current bibliography contains 36 entries, including XAI surveys, prior transition-matrix works, rough-set foundations, concept methods, AwA2, classical ZSL baselines, GFZSL, and randomized SVD. Codex must keep all existing citation keys used in `main.tex` unless a key is invalid, duplicated, or points to the wrong source. New references must be appended in a controlled block with clear keys and must be cited in the revised text.

Required new reference categories:

- SUN Attribute Database official page and IJCV paper.
- Derm7pt / Seven-Point Checklist dataset website, GitHub repository, and IEEE JBHI paper.
- Modern ZSL/GZSL baselines from 2019–2026, including attribute-based, attention-based, generative, and vision-language or generalized formulations when relevant.
- Recent rough-set, fuzzy-rough, rough neural, differentiable rough-set, rule induction, and hybrid XAI literature.
- Dataset, software, or tool citations required for reproducibility.

### 3.3 `supply.tex`

`supply.tex` currently contains only a placeholder introduction. It must be expanded into a real supplement with:

- Full dataset-processing protocols for AwA2, SUN, and Derm7pt.
- Extended q-sensitivity and SVD-rank sensitivity tables if too large for the main text.
- Per-phase runtime breakdowns and hardware/software metadata.
- Full seed-wise Protocol B results with standard deviations and confidence intervals.
- Bat-class diagnostic evidence.
- Discretizer boundary stability diagnostics.
- Rule traces, perturbation robustness, and uncertainty computations.
- Regeneration instructions and file paths for all tables/figures.

### 3.4 `revision_report_v1.md`

Codex must create `revision_report_v1.md` after implementing or planning the revisions. It must be a professional Markdown report with a reviewer-comment traceability matrix and must explicitly state that no unrelated changes were made beyond reviewer-driven or compile-required modifications.

---

## 4. Reviewer-Comment Traceability Plan

| Reviewer comment | Concern summary | Mandatory action | Main file(s) | Target location(s) | Verification artifact |
|---|---|---|---|---|---|
| 1.1 | WEDD-vs-MDLP contradiction | Move discretizer table to main Results; add candid discussion; moderate WEDD claim | `main.tex`, `supply.tex` | `subsec:rulebook_auditability`, `sec:app_discretization` | `tab:discretizer_comparison_main`, seed-wise paired tests |
| 1.2 | Abstract synthetic macro-F1 inconsistency | Replace 0.8668 with verified zero-noise and high-noise values, or label mean explicitly | `main.tex` | abstract, `subsec:results_synthetic`, conclusion | regenerated synthetic table log |
| 1.3 | Relation to prior ETM paper unclear | Add novelty-separation paragraph and ETM-vs-SEMTRA table | `main.tex`, `references.bib` | `sec:introduction`, `sec:related` | `tab:etm_semtra_comparison` |
| 1.4 | Generalization beyond AwA2 needed | Add SUN Attribute Database experiment | `main.tex`, `supply.tex`, `references.bib` | `subsec:protocol`, `sec:results`, supplement | cross-domain logs, `tab:cross_domain_generalization` |
| 1.5 | Audit tax and weak rulebook fidelity | Reframe audit tax; add use-case acceptability; add SVD-rank sensitivity | `main.tex`, `supply.tex` | `subsec:interpreting_tax`, `subsec:rulebook_auditability` | `tab:svd_rank_sensitivity`, audit-tax frontier |
| 1.6 | Attribute-count \(q\) sensitivity absent | Add q-sensitivity grid and default-q justification | `main.tex`, `supply.tex` | `subsec:methods_wedd`, `subsec:protocol`, Results | `tab:q_sensitivity` |
| 1.7 | Zero-shot baselines outdated | Add modern ZSL/GZSL references and comparison-type labels | `main.tex`, `references.bib` | `subsec:semantic_transfer`, `subsec:protocol_b_results` | revised Protocol B table |
| 1.8 | Fidelity metrics ambiguous | Add equations for covered fidelity vs covered accuracy | `main.tex` | `subsec:inference_fidelity_metrics`, `subsec:eval_metrics` | equation block and table caption audit |
| 1.9 | WEDD superiority unsupported | Same as 1.1; add stability/robustness analyses | `main.tex`, `supply.tex` | main Results and Discussion | boundary-stability table |
| 1.10 | Runtime for reduct search missing | Add per-phase runtime breakdown | `main.tex`, `supply.tex` | `subsec:protocol`, Results, supplement | `tab:runtime_breakdown`, JSON timer logs |
| 1.11 | Figure 5 conceptual comparison unclear | Revise figure caption and textual reference as conceptual | `main.tex` | `fig:conc_comparison`, nearby text | caption diff |
| 1.12 | Bat failure diagnosis incomplete | Add focused bat diagnostic subsection/table | `main.tex`, `supply.tex` | `subsec:protocol_b_results` after `tab:protocol_b` | `tab:bat_diagnostic`, rule traces |
| 1.13 | Rough-set/neural literature thin | Expand rough-set related works with recent citations | `main.tex`, `references.bib` | `subsec:symbolic_rule_extraction` | updated bibliography validation |
| 1.14 | Protocol B lacks uncertainty | Add seed-wise SEMTRA results and std/CI | `main.tex`, `supply.tex` | `subsec:protocol_b_results` | seed logs, revised table |
| 2.1 | Weak rulebook fidelity limits practice | Reframe SEMTRA as audit layer, not classifier replacement | `main.tex` | Results, Discussion, Conclusion | claim-audit checklist |
| 2.2 | Practical acceptability of audit tax unclear | Add use-case matrix and sensitivity analyses | `main.tex`, `supply.tex` | `subsec:interpreting_tax` | use-case table/text |
| 2.3 | Additional datasets requested | Add Derm7pt experiment and cross-domain table | `main.tex`, `supply.tex`, `references.bib` | protocol/results/supplement | Derm7pt logs, cross-domain table |
| 2.4 | Zero-shot framing misleading | Reframe Protocol B as semantic validation; modernize baselines | `main.tex`, `references.bib` | related works, Protocol B | revised table/caption |

---

## 5. File-Level Modification Plan

## 5.1 `main.tex`

### 5.1.1 Abstract

Replace the current abstract with a moderated abstract that contains only claims traceable to main-text tables. Required edits:

- Keep SEMTRA’s identity as a post-hoc semantic transition and rough-set rule-induction framework.
- Report AwA2 transition MAE only if it matches `tab:transition_metrics` and regenerated logs.
- Report rulebook coverage and covered accuracy with “covered” and “non-abstained” labels.
- Report covered fidelity separately from covered accuracy.
- Reframe Protocol B as semantic-transfer validation, not competitive zero-shot learning.
- Correct synthetic macro-F1.
- Mention additional SUN and Derm7pt evaluations only after results are produced. If results are not produced, do not mention them in the abstract.

Preferred replacement direction for the synthetic sentence:

> “In the controlled synthetic benchmark, SEMTRA achieved macro-F1 = 0.879 at zero semantic noise and remained at 0.838 under the highest evaluated noise level.”

If Codex verifies that 0.8668 is a mean across noise levels from source scripts, the abstract may instead say:

> “Across the evaluated synthetic noise levels, SEMTRA achieved mean macro-F1 = 0.8668; the zero-noise result was 0.879 and the highest-noise result was 0.838.”

Use the first option unless the mean is explicitly reported in a regenerated table.

### 5.1.2 Introduction: `sec:introduction`

Add a novelty-separation paragraph after the existing paragraph that cites transition matrices and ETM. The paragraph must state:

- Prior transition-matrix work established latent-to-interpretable mapping.
- ETM adds equivariance constraints and Lie-group linearization to improve geometric consistency of explanations.
- SEMTRA is not an equivariance paper and does not claim Lie-group structural consistency.
- SEMTRA adds semantic discretization, rough-set granulation, rulebook extraction, conflict handling, abstention, and audit-tax quantification.
- SEMTRA complements ETM because both are post-hoc transition-matrix approaches, but their scientific objectives, mathematical constraints, and outputs differ.

Insert a new main-text table after this paragraph:

`\label{tab:etm_semtra_comparison}`  
**Caption direction:** “Comparison of the prior ETM framework and the present SEMTRA framework.”

Required columns:

- Dimension
- ETM paper
- SEMTRA manuscript
- Relationship

Required rows:

- Core problem
- Mathematical operator
- Regularization/constraint
- Semantic layer
- Discretization
- Symbolic rule induction
- Conflict/abstention handling
- Primary output
- Evaluation focus
- Non-overlap statement

Moderate contribution bullets:

- Replace “WEDD method ... ensure stable symbolic boundaries” with “a discretization module, instantiated by WEDD and benchmarked against entropy and quantile alternatives, for converting reconstructed semantics into symbolic states.”
- Replace “comprehensive evaluation on AwA2 and controlled synthetic data” with “evaluation on AwA2, reviewer-requested cross-domain attribute-structured benchmarks where executed, and controlled synthetic data.” Do not mention SUN/Derm7pt in the contribution list unless results exist.

### 5.1.3 Related Works: `sec:related`

#### `subsec:symbolic_rule_extraction`

Expand from Pawlak/classical-only rough-set coverage to modern rough/fuzzy/neural hybrids. Include at least one paragraph on:

- Fuzzy-rough rule induction and white-box rule learners.
- Rough-set interpretation of neural networks.
- Differentiable or neural rough/fuzzy systems where found and verified.
- Why SEMTRA differs: it is post-hoc, model-agnostic, and symbolic after semantic transition; it does not train a rough/fuzzy neural model end-to-end.

The FRRI literature explicitly frames fuzzy-rough rule induction as a white-box alternative to black-box models and combines fuzzy and rough-set theory for rule induction. citeturn455266view5 Use this and additional scholarly sources verified through Crossref/OpenAlex/Semantic Scholar.

#### `subsec:semantic_transfer`

Revise the section title or final paragraph to emphasize semantic validation, not leaderboard competition. Add recent ZSL/GZSL literature from 2019–2026 and classify references by purpose:

- Historical interpretable baselines: DAP, IAP.
- Modern predictive ZSL/GZSL baselines: DAZLE, attention-based methods, generative approaches, calibrated GZSL, vision-language methods if relevant.
- Transparent semantic-validation comparators: SEMTRA variants.
- Not directly comparable: methods trained or optimized for predictive ZSL/GZSL rather than post-hoc auditability.

DAZLE is a strong required candidate because it explicitly uses dense attribute-based attention, aligns attribute-based features with attribute semantic vectors, and reports experiments on CUB, SUN, and AWA2. citeturn380196view0 MAIN is a 2024 candidate because it addresses generalized and continual zero-shot learning with attribute self-interaction and visual-semantic embedding. citeturn455266view6 EGZSL is a 2024 candidate because it reframes attribute-based ZSL as an evolving test-stream setting. citeturn455266view7 Codex must verify exact bibliographic metadata and DOI/proceedings information before adding entries.

### 5.1.4 Methods: `sec:methods`

#### `subsec:framework_overview`

Replace the overclaiming sentence:

> “The SEMTRA framework is structurally designed as a universal, modular, post-hoc proof-of-concept pipeline applicable to all possible XAI problems.”

with a moderated sentence:

> “The SEMTRA framework is designed as a modular post-hoc audit layer for attribute-structured classification settings in which latent representations can be aligned with human-readable semantic variables.”

Add a limitation sentence in the same subsection:

> “The framework requires a meaningful semantic attribute matrix or checklist representation; when such semantics are incomplete, coarse, or unavailable, SEMTRA can expose the gap but cannot guarantee high-fidelity symbolic recovery.”

#### `subsec:methods_wedd`

Revise WEDD language to define it as one discretization choice. Required additions:

- State that WEDD optimizes a hybrid entropy-density objective.
- State that the revised manuscript empirically compares WEDD against MDLP-like entropy, equal-frequency, and equal-width discretizers.
- State that discretizer choice is treated as a tunable design decision.
- Add a forward reference to the main-text discretizer table.

Required wording direction:

> “WEDD is intended to favor thresholds in low-density regions while retaining class-conditional information. It is not assumed to dominate entropy-only discretization on all fidelity metrics; therefore, Section X reports a direct discretizer ablation and treats discretization as an auditor-facing design choice.”

Do not use “superior,” “optimal,” “guarantees,” or “ensures” unless the claim is mathematically true or statistically supported.

#### `subsec:inference_fidelity_metrics` and `subsec:eval_metrics`

Add formal metric definitions using distinct target variables:

- \(f_{\mathrm{BB}}(x_i)\): frozen base/black-box model prediction.
- \(y_i\): ground-truth label.
- \(\hat{y}_{\mathcal{R}}(x_i)\): symbolic rulebook prediction.
- \(c_i \in \{0,1\}\): coverage indicator, with \(c_i=1\) if the rulebook returns a non-abstained prediction.
- \(z_i \in \{0,1\}\): conflict indicator.

Add equations:

```latex
\begin{equation}
\mathrm{Cov} = \frac{1}{|Q|}\sum_{i\in Q} c_i.
\end{equation}

\begin{equation}
\mathrm{F}_{\mathrm{cov}} =
\frac{\sum_{i\in Q} c_i\,\mathbb{I}[\hat{y}_{\mathcal{R}}(x_i)=f_{\mathrm{BB}}(x_i)]}
{\sum_{i\in Q} c_i}.
\end{equation}

\begin{equation}
\mathrm{Acc}_{\mathrm{cov}} =
\frac{\sum_{i\in Q} c_i\,\mathbb{I}[\hat{y}_{\mathcal{R}}(x_i)=y_i]}
{\sum_{i\in Q} c_i}.
\end{equation}

\begin{equation}
\mathrm{Acc}_{\mathrm{all}} =
\frac{1}{|Q|}\sum_{i\in Q} c_i\,\mathbb{I}[\hat{y}_{\mathcal{R}}(x_i)=y_i].
\end{equation}

\begin{equation}
\mathrm{Abs}=1-\mathrm{Cov},\qquad
\mathrm{CR}=\frac{1}{|Q|}\sum_{i\in Q} z_i.
\end{equation}
```

Add explanatory text:

> “Covered fidelity measures agreement with the frozen base model on covered cases and therefore evaluates whether the symbolic layer reproduces the model being audited. Covered accuracy measures agreement with ground truth on the same covered cases and therefore evaluates correctness of the symbolic layer. These values can differ because the frozen base model is imperfect.”

Update every table caption that uses “fidelity,” “accuracy,” or “covered” to specify whether the target is the base model or ground truth.

#### `subsec:protocol`

Add a structured subsection or subsubsections for:

- Cross-domain attribute-structured generalization: AwA2, SUN, Derm7pt.
- SVD-rank sensitivity.
- Selected-attribute-count sensitivity.
- Discretizer comparison and boundary stability.
- Runtime instrumentation.
- Protocol B uncertainty reporting.

Do not introduce `\paragraph{}`. Use `\subsubsection{...}` or ordinary prose.

### 5.1.5 Results: `sec:results`

#### Add main-text discretizer comparison

Move `tab:wedd_ablation` out of Appendix B into main Results near `subsec:rulebook_auditability`, preferably immediately before or after `tab:rulebook_summary`. Rename label to `tab:discretizer_comparison_main` or keep `tab:wedd_ablation` only if all references are updated consistently.

The table must preserve the unfavorable values rather than hiding them:

- WEDD: Coverage 0.8640; All acc. 0.3519; Covered fidelity 0.3829; Conflict 0.1354.
- MDLP-like entropy: Coverage 0.8714; All acc. 0.3928; Covered fidelity 0.4556; Conflict 0.1125.
- Equal frequency and equal width as currently reported.

Add a candid result paragraph:

> “In this AwA2 configuration, MDLP-like entropy outperformed WEDD on coverage, all-object accuracy, covered fidelity, and conflict rate. This finding prevents an unconditional claim of WEDD superiority. We therefore interpret WEDD as a density-aware discretization option whose advantage must be evaluated through stability and interpretability diagnostics rather than assumed from fidelity metrics alone.”

Add a second paragraph summarizing new stability analysis once executed.

#### Add cross-domain generalization table

Insert a main-text table after the AwA2 Protocol A rulebook section or as a new subsection `\subsection{Cross-Domain Attribute-Structured Generalization}`. Use label `tab:cross_domain_generalization`.

Required columns for the main table:

- Dataset
- Domain
- Semantic target
- Classes/tasks
- Feature extractor
- Split/seeds
- Transition MAE/RMSE/corr.
- Coverage
- Covered fidelity
- Covered accuracy
- Conflict / abstention
- Rule count / average length
- Status

Status must be one of: `completed`, `executed on documented subset`, or `planned; not claimed`. The submitted manuscript should not include `planned; not claimed` as a result table if the authors intend to claim generalization in the abstract or conclusion.

#### Add SVD-rank sensitivity

Add a compact main-text table if space allows; otherwise place a summary row and move full table to `supply.tex`. Use label `tab:svd_rank_sensitivity`.

Required \(r\) values for AwA2:

\(r \in \{16,32,64,128,256,512\}\), plus `r95` or full-rank if feasible.

Required metrics:

- Retained variance.
- Transition MAE.
- Mean semantic correlation.
- Rule count.
- Average rule length.
- Coverage.
- Covered fidelity.
- Covered accuracy.
- Conflict rate.
- Abstention rate.
- Runtime.
- Peak memory.

Add interpretation:

- If increasing \(r\) improves transition metrics but worsens rule complexity, describe the auditability tradeoff.
- If increasing \(r\) does not close the audit gap, state that representation capacity alone does not eliminate semantic indiscernibility.

#### Add selected-attribute-count \(q\) sensitivity

Add a compact main-text or supplementary table with label `tab:q_sensitivity`. Required values:

- AwA2: \(q \in \{5,10,15,20,30,40\}\).
- SUN: dataset-appropriate values, e.g., \(q \in \{10,20,40,60,80,102\}\), if SUN is executed.
- Derm7pt: use all seven checklist criteria and optionally subcriteria; evaluate \(q \in \{3,5,7\}\) or all available structured checklist variables if more granular.

Required metrics:

- Selected attributes or attribute groups.
- Selection score distribution.
- Number of thresholds.
- Rule count.
- Average rule length.
- Coverage.
- Covered fidelity.
- Covered accuracy.
- Conflict rate.
- Abstention rate.
- Reduct-search runtime.
- Peak memory.

Replace the current “q = 15 was selected empirically” style with:

> “The default \(q=15\) was selected as a compromise between coverage, covered fidelity, conflict rate, rulebook size, and reduct-search runtime in the q-sensitivity grid.”

Only use this if the grid supports it.

#### Add runtime table

Insert a table labeled `tab:runtime_breakdown` in main text if compact; otherwise include a main-text summary and full supplement table.

Required rows:

- Feature extraction/loading.
- SVD/PCA reduction.
- Ridge transition fitting.
- Semantic reconstruction.
- Attribute selection.
- WEDD threshold search.
- MDLP-like entropy threshold search.
- Equal-frequency / equal-width discretization.
- Rough-set reduct search.
- Rulebook construction.
- Conflict resolution.
- Inference.
- Perturbation stability analysis.
- q-sensitivity loop.
- r-sensitivity loop.
- SUN processing.
- Derm7pt processing.

Required columns:

- Dataset.
- Phase.
- Mean runtime ± SD.
- Number of seeds or runs.
- Hardware.
- Peak memory.
- Output log path.

#### Revise Protocol B table

Rename or revise `tab:sota_quantitative_comparison` to `tab:semantic_validation_baselines`. Required columns:

- Method.
- Year.
- Comparison type.
- Training objective.
- Published AwA2 metric.
- SEMTRA metric if applicable.
- Uncertainty.
- Direct comparability.
- Citation/source.

Use comparison types:

- Historical interpretable baseline.
- Modern predictive ZSL/GZSL baseline.
- Transparent semantic-validation method.
- Not directly comparable.

For SEMTRA variants, report mean ± standard deviation across seeds. Add 95% CI if feasible. For published baselines without seed statistics, write “not reported,” not invented values.

Required wording:

> “SEMTRA exceeds foundational DAP under this semantic-transfer protocol but remains below specialized predictive ZSL/GZSL systems such as GFZSL and later attention/generative methods. Its purpose is traceable semantic validation rather than optimized zero-shot recognition.”

#### Add bat-class diagnostic subsection

After `tab:protocol_b`, add `\subsubsection{Bat-Class Failure Diagnosis}` or a short result paragraph with a table labeled `tab:bat_diagnostic`.

Required table columns:

- Diagnostic component.
- Evidence.
- Bat value.
- Comparison/reference class value.
- Interpretation.
- Output artifact path.

Required evidence rows:

- Bat class semantic prototype top positive attributes.
- Bat reconstructed semantic mean and standard deviation.
- Attribute-level absolute reconstruction error for bat.
- Top confused classes from base model and SEMTRA prototype transfer.
- Fired symbolic-template antecedents or missing antecedents.
- Hamming distances to bat and top confused prototypes.
- Conflict/abstention frequency for bat cases.
- Selected q attributes present or absent in the bat semantic prototype.

Required instruction:

- Use the actual AwA2 attribute list and logs. Do not speculate.
- If an attribute such as “nocturnal” is not present in AwA2, state that the dictionary lacks a direct nocturnal concept instead of pretending it was measured.
- If attributes such as wings, flying, furry, small, active, inactive, hunter, or visual descriptors are present, report their exact prototype and reconstruction values.

### 5.1.6 Discussion: `sec:discussion`

#### `subsec:interpreting_tax`

Replace “profound diagnostic triumph” with a balanced use-case-oriented interpretation:

> “The audit tax is not a predictive success claim. It quantifies the cost of forcing a high-dimensional nonlinear predictor into a compact, conflict-aware symbolic rulebook. In the present AwA2 setting, the rulebook verifies a substantial but imperfect subset of model behavior. This tradeoff is acceptable for auditing, semantic debugging, dataset-bias diagnosis, documentation, and human-review triage; it is not acceptable as a replacement for the base classifier or as an autonomous high-stakes decision system.”

Add explicit limits:

- SEMTRA is not designed to maximize raw accuracy.
- Low covered fidelity indicates that much of the base model’s behavior is not captured by the current semantic dictionary and discretization.
- Conflict and abstention are strengths only when interpreted as routing signals, not as hidden performance.

Add a use-case matrix in prose or table:

| Use case | Acceptability | Reason |
|---|---|---|
| Model audit | Acceptable | exposes verified semantic subset |
| Failure diagnosis | Acceptable | reveals conflicts, abstentions, semantic ruptures |
| Dataset-bias inspection | Acceptable | identifies systematic concept gaps |
| Rule-based triage for human review | Conditionally acceptable | requires human oversight and thresholds |
| Autonomous diagnosis | Not acceptable | rulebook accuracy/fidelity insufficient |
| Replacement of base classifier | Not acceptable | audit layer is not a predictive model |

#### `subsec:limitations_directions`

Add limitations for:

- WEDD not uniformly superior.
- Cross-domain results bounded by semantic attribute quality.
- SUN scene categories may have limited samples per category.
- Derm7pt is medically oriented and must be treated as retrospective technical validation.
- q and r sensitivity reveal combinatorial and computational limits.
- Protocol B is not a ZSL SOTA result.
- Rule induction can expose but not repair incomplete attribute dictionaries.

### 5.1.7 Conclusion: `sec:conclusions`

Revise conclusion to avoid overclaiming. Required directions:

- Report corrected synthetic result.
- Mention MDLP-like entropy finding if WEDD is discussed.
- Mention SUN/Derm7pt only if executed and summarized in main text.
- State SEMTRA provides an auditable diagnostic layer, not a universal solution.
- End with future directions tied to evidence: richer semantic dictionaries, instance-level concepts, uncertainty-aware discretization, and scalable reduct search.

---

## 5.2 `references.bib`

Codex must update `references.bib` in a controlled manner.

### 5.2.1 Bibliography Rules

- Preserve all existing keys used in `main.tex` unless invalid or duplicated.
- Append new entries under a comment block `% Reviewer-requested revision references`.
- Use complete author names where available.
- Use sentence-case titles.
- Prefer DOI over URL for published papers.
- Use URL only for dataset/software pages or sources without DOI.
- Add `urldate` or `note = {Accessed ...}` for dataset/software pages.
- Validate with BibTeX/Biber-compatible syntax.
- Do not cite blogs where peer-reviewed or official sources exist.

### 5.2.2 Required or Strongly Recommended Additions

#### SUN Attribute Database

Required entries:

- `Patterson2014SUNAttribute` for Genevieve Patterson, Chen Xu, Hang Su, and James Hays, “The SUN Attribute Database: Beyond Categories for Deeper Scene Understanding,” *International Journal of Computer Vision*, DOI `10.1007/s11263-013-0695-z`. The IJCV source reports 102 attributes, 14,340 images, and 707 scene categories. citeturn455266view1
- `SUNAttributeWebsite` for the official SUN Attribute Database page, which documents the dataset and download links. citeturn455266view0
- Optionally `Patterson2012SUNAttributeCVPR` for the CVPR 2012 SUN attribute paper, after DOI verification.

#### Derm7pt / Seven-Point Checklist

Required entries:

- `Kawahara2019Derm7pt` for Jeremy Kawahara, Sara Daneshvar, Giuseppe Argenziano, and Ghassan Hamarneh, “Seven-Point Checklist and Skin Lesion Classification using Multitask Multimodal Neural Nets,” *IEEE Journal of Biomedical and Health Informatics*, volume 23, number 2, pages 538–546, DOI `10.1109/JBHI.2018.2824327`. citeturn455266view2
- `Derm7ptWebsite` for the official Seven-Point Checklist dataset site, which describes the dataset for computerized prediction of the seven-point skin lesion malignancy checklist and states that it includes clinical and dermoscopy images with structured metadata. citeturn455266view3
- `Derm7ptGitHub` for the official `jeremykawahara/derm7pt` repository, which provides preprocessing code and documents official train/valid/test index usage. citeturn455266view2
- Optionally add the original seven-point checklist dermatology paper if the revised text discusses checklist clinical background rather than only dataset structure.

#### Modern ZSL/GZSL Baselines

Codex must search 2019–2026 literature and add a compact, representative set. Required candidates to evaluate:

- `Huynh2020DAZLE`: dense attribute-based attention for fine-grained generalized zero-shot learning; reports CUB, SUN, and AWA2 experiments. citeturn380196view0
- `Verma2024MAIN`: Meta-Learned Attribute Self-Interaction Network for continual and generalized zero-shot learning. citeturn455266view6
- `EGZSL2024` or exact key after author lookup: Evolutionary Generalized Zero-Shot Learning from IJCAI 2024. citeturn455266view7
- `AttributePrototypeGZSL2024` for the MDPI 2024 attribute-prototype/discriminative-attention method, DOI `10.3390/electronics13183751`, if it is relevant to the AwA2/SUN baseline discussion. citeturn380196view1

Add only methods that the revised manuscript actually cites and compares. Do not bloat the literature review.

#### Rough-Set, Fuzzy-Rough, Rough Neural, and Hybrid XAI

Required candidates:

- `Bollaert2025FRRI` already exists in `references.bib`; validate metadata and cite in expanded rough-set section.
- Add recent rough-set neural interpretation papers or fuzzy-rough neural systems only after verifying peer-reviewed status.
- Add differentiable rough-set or rough neural works if they are used to position SEMTRA as post-hoc and non-end-to-end.

### 5.2.3 Citation Placement

- SUN references: cite in `subsec:protocol`, cross-domain results subsection, and supplement SUN processing section.
- Derm7pt references: cite in `subsec:protocol`, cross-domain results subsection, Derm7pt limitation/caution paragraph, and supplement Derm7pt processing section.
- Modern ZSL references: cite in `subsec:semantic_transfer` and revised Protocol B table.
- Rough/fuzzy/neural references: cite in `subsec:symbolic_rule_extraction` and discussion if needed.
- ETM reference: cite in introduction novelty paragraph and `tab:etm_semtra_comparison` caption or note.

---

## 5.3 `supply.tex`

Codex must expand `supply.tex` into a full reproducibility supplement. Required structure:

```latex
\section{Supplementary Reproducibility Overview}
\section{Dataset Processing Protocols}
\subsection{AwA2 Processing}
\subsection{SUN Attribute Database Processing}
\subsection{Derm7pt / Seven-Point Checklist Processing}
\section{Extended Sensitivity Analyses}
\subsection{SVD-Rank Sensitivity}
\subsection{Selected-Attribute-Count Sensitivity}
\subsection{Confidence-Threshold Frontier}
\section{Discretizer Diagnostics}
\subsection{Boundary Stability Across Seeds}
\subsection{Perturbation Robustness}
\subsection{Rule-Length and Conflict Behavior}
\section{Runtime and Memory Instrumentation}
\section{Protocol B Seed-Wise Results and Uncertainty}
\section{Bat-Class Failure Diagnostics}
\section{Extended Rule Traces}
\section{Regeneration Instructions and Artifact Index}
```

### 5.3.1 Supplement Content Requirements

For each dataset, include:

- Dataset name and citation.
- Data-access path and version/date.
- Object unit: image, case, lesion, or patient.
- Split unit and leakage safeguards.
- Feature extractor and preprocessing.
- Semantic matrix construction.
- Label construction.
- Missing-value handling.
- Class imbalance handling.
- Seeds.
- Hyperparameters.
- Scripts used.
- Output CSV/JSON paths.
- Runtime and hardware.

### 5.3.2 What Must Remain in Main Text

Do not move the following reviewer-critical evidence exclusively to the supplement:

- WEDD-vs-MDLP-like entropy contradiction.
- Metric definitions.
- Cross-domain generalization summary.
- Audit-tax interpretation.
- Protocol B reframing.
- Main bat diagnostic conclusion.
- Runtime summary including reduct search.

The supplement may contain full versions, seed-wise tables, and diagnostic plots.

---

## 5.4 `revision_report_v1.md`

Codex must create `revision_report_v1.md` after implementation or after the implementation plan is frozen. Required sections:

1. Title and revision scope.
2. Executive summary of changes.
3. Reviewer-comment traceability matrix.
4. Modified files and line/section map.
5. Added, moved, and revised tables.
6. Added and revised figures.
7. Recalculated results and verification source.
8. Moderated claims and replaced wording.
9. Bibliography changes.
10. Supplement changes.
11. Reproducibility artifacts and output paths.
12. Compilation and validation results.
13. Remaining limitations.
14. Statement that no unrelated changes were made beyond reviewer-driven and compile-required modifications.

Required traceability matrix columns:

- Reviewer.
- Comment ID.
- Concern summary.
- Manuscript action.
- File(s).
- Section/table/figure.
- Verification status.
- Remaining limitations.

---

## 6. Reviewer-by-Reviewer Implementation Strategy

### 6.1 Comments 1.1 and 1.9: WEDD versus MDLP-like entropy contradiction

**Current problem:** Appendix B reports that MDLP-like entropy beats WEDD on several core metrics. The manuscript nevertheless uses WEDD-forward language suggesting superiority and stability.

**Implementation actions:**

1. Move `tab:wedd_ablation` from `sec:app_discretization` to main Results under `subsec:rulebook_auditability`.
2. Rename caption to explicitly state that MDLP-like entropy is stronger on fidelity/coverage metrics in this setting.
3. Add a candid paragraph directly after the table.
4. Replace all unconditional WEDD superiority wording in abstract, contributions, methods, results, discussion, and conclusion.
5. Add a new stability-focused discretizer analysis:
   - Boundary threshold mean ± SD across seeds.
   - Threshold coefficient of variation.
   - Average local density at selected thresholds.
   - Perturbation robustness of discretized states.
   - Rule count and average rule length.
   - Conflict behavior.
   - Covered fidelity and covered accuracy.
   - Paired WEDD-vs-MDLP differences across seeds.
6. Store results in:
   - `outputs/revision_v1/discretizers/discretizer_seedwise.csv`
   - `outputs/revision_v1/discretizers/boundary_stability.csv`
   - `outputs/revision_v1/discretizers/discretizer_summary.tex`
7. Discuss the result as a design tradeoff:
   - MDLP-like entropy is currently stronger on core fidelity metrics.
   - WEDD may be defensible if it shows lower threshold variance or better perturbation robustness.
   - If WEDD fails stability as well, state that WEDD is retained only as a tested design option, not as the recommended default.

**Required main-text conclusion:**

> “The AwA2 discretization ablation shows that MDLP-like entropy achieved stronger coverage, all-object accuracy, covered fidelity, and conflict behavior than WEDD in the current configuration. WEDD should therefore be interpreted as a density-aware discretization option rather than a universally superior component.”

### 6.2 Comment 1.2: Abstract numerical inconsistency for synthetic macro-F1

**Current problem:** Abstract reports macro-F1 = 0.8668, while `tab:synthetic_noise` reports 0.879, 0.881, and 0.838 for three noise settings.

**Implementation actions:**

1. Trace synthetic metric origin from scripts/logs.
2. Regenerate `tab:synthetic_noise` from source CSV/JSON.
3. Decide whether 0.8668 is a mean across noise levels. If yes, add a table column or note; if no, remove it.
4. Revise abstract and conclusion.
5. Add a numeric consistency check that compares abstract numbers against table values.

**Preferred abstract replacement:**

> “In the controlled synthetic benchmark, SEMTRA achieved macro-F1 = 0.879 at zero semantic noise and remained at 0.838 under the highest evaluated noise level.”

**Verification artifact:** `outputs/revision_v1/synthetic/synthetic_noise_summary.csv`.

### 6.3 Comment 1.3: Relationship to Radiuk et al. MAKE 2026 ETM paper

**Current problem:** SEMTRA cites ETM but does not clearly state what is new relative to ETM.

**Implementation actions:**

1. Verify the ETM citation and DOI online. The MDPI page currently lists the ETM article as *Machine Learning and Knowledge Extraction* 2026, 8(4), 92, DOI `10.3390/make8040092`. citeturn973439search0
2. Add a novelty-separation paragraph in `sec:introduction`.
3. Add `tab:etm_semtra_comparison` to main text.
4. Update related works to state ETM is complementary, not the same contribution.
5. Avoid wording that implies SEMTRA simply reuses ETM.

**Required distinction:**

- ETM: symmetry-aware transition matrices, Lie group linearization, equivariance constraints, geometric consistency.
- SEMTRA: semantic transition into human-readable attributes, WEDD/alternative discretization, rough-set rule induction, conflict/abstention, audit tax, global production-rule extraction.

### 6.4 Comments 1.4 and 2.3: Additional datasets for generalization

**Current problem:** The manuscript’s empirical core is AwA2 plus synthetic stress testing; reviewers require broader generalization.

#### 6.4.1 SUN Attribute Database protocol

**Primary route:** execute the experiment before resubmission.

**Data source:** official SUN Attribute Database and IJCV paper. The official page and IJCV article document 102 attributes and 14,340 images; the IJCV source states the images come from 707 scene categories. citeturn455266view0turn455266view1

**Experimental design:**

1. Download SUN Attribute Database labels and images from official sources.
2. Define the object unit as image.
3. Build semantic matrix \(B\) from the 102 scene attributes using normalized attribute annotations.
4. Build labels from scene categories.
5. Use a frozen visual feature extractor. Preferred: ResNet-101 or the same feature extractor family used for AwA2 to preserve comparability. Optional secondary extractor: CLIP ViT-B/16, reported separately and not mixed with ResNet results.
6. Train a base classifier on scene categories using stratified splits. Use class-balanced loss or report imbalance effects.
7. Learn SEMTRA transition matrix from latent features to 102 attributes.
8. Select attributes through the same score definition; run q-sensitivity rather than fixing q blindly.
9. Discretize selected attributes using WEDD and MDLP-like entropy.
10. Induce rough-set rules.
11. Report:
    - Transition MAE/RMSE/correlation.
    - Coverage.
    - Covered fidelity.
    - Covered accuracy.
    - All-object accuracy.
    - Conflict rate.
    - Abstention rate.
    - Rule count.
    - Average rule length.
    - Runtime and memory.
12. Add a short discussion of whether SEMTRA transfers from animal attributes to scene attributes involving materials, spatial layout, affordances, lighting, and surface properties.

**Minimum subset route if full 707-class execution is infeasible:**

- Use a documented subset of at least 50 scene categories sampled before training and selected by image count or a reproducible category list.
- Preserve all 102 attributes unless q-sensitivity selects a subset.
- State the subset criteria in `supply.tex`.
- Do not write “SUN results demonstrate broad generalization” unless the subset limitation is stated in the main text.

#### 6.4.2 Derm7pt protocol

**Primary route:** execute the experiment before resubmission.

**Data source:** official Seven-Point Checklist dataset site and `jeremykawahara/derm7pt`. The dataset site describes clinical and dermoscopy images with structured metadata for seven-point checklist malignancy prediction; the GitHub repository documents preprocessing, metadata, train/valid/test indices, diagnosis labels, and the JBHI paper. citeturn455266view2turn455266view3

**Experimental design:**

1. Download data from the official dataset website.
2. Use the GitHub repository’s preprocessing and official metadata indices where available.
3. Define the object unit as lesion/case. Do not split clinical and dermoscopic images from the same lesion across train/validation/test.
4. Build semantic matrix \(B\) from the seven-point checklist criteria and any available structured subcriteria, not from diagnosis labels.
5. Define the target label:
   - Primary: diagnosis label group used by the repository.
   - Secondary: melanoma vs non-melanoma or clinically relevant grouped labels if class imbalance makes full diagnosis unstable.
6. Feature extraction:
   - Dermoscopic-only branch if one modality is used.
   - Clinical+dermoscopic branch if both modalities are used; combine at lesion level after feature extraction.
7. Handle class imbalance using class-balanced metrics, stratified sampling, or class weights. Report macro-F1 and balanced accuracy in addition to SEMTRA audit metrics.
8. Learn transition matrix from image features to checklist concepts.
9. Discretize checklist concepts and induce rules.
10. Report whether rough-set boundary/conflict regions correspond to concept-label ambiguity in checklist criteria.
11. Add cautionary text:

> “The Derm7pt experiment is a retrospective technical evaluation of semantic auditability. It is not a clinical deployment study, diagnostic device validation, or substitute for dermatologist review.”

**Required safeguards:**

- Lesion-level split integrity.
- No leakage between clinical and dermoscopic views.
- Missing checklist metadata handling.
- Class imbalance reporting.
- Clear statement of modality used.
- No clinical-readiness claims.

### 6.5 Comments 1.5, 2.1, and 2.2: Audit tax, weak rulebook fidelity, and practical acceptability

**Current problem:** The manuscript frames a large rulebook accuracy drop as a triumph. Reviewers see weak fidelity and need practical justification.

**Implementation actions:**

1. Rewrite `subsec:interpreting_tax` as an audit tradeoff rather than a triumph.
2. Add SVD-rank sensitivity table and discussion.
3. Add confidence-threshold frontier figure if feasible.
4. Add a use-case acceptability matrix.
5. Revise conclusion to state the rulebook is a diagnostic audit layer.

**Required interpretation:**

- Acceptable for model auditing, semantic debugging, failure diagnosis, dataset-bias detection, documentation, and human-review triage.
- Not acceptable for autonomous high-stakes decisions, final diagnosis, or replacing the base classifier.
- The audit tax is acceptable only when the user needs verifiable rule evidence and can tolerate abstention/conflict routing.

### 6.6 Comment 1.6: Attribute-count \(q\) sensitivity

**Current problem:** q is presented as empirically selected without sufficient evidence.

**Implementation actions:**

1. Add q grid for AwA2 and, if executed, SUN and Derm7pt.
2. Record selected attributes for each q.
3. Record reduct-search runtime and memory to quantify combinatorial growth.
4. Identify default q from evidence.
5. Replace ungrounded q=15 statement.

**Required output files:**

- `outputs/revision_v1/sensitivity/q_sensitivity_seedwise.csv`
- `outputs/revision_v1/sensitivity/q_sensitivity_summary.tex`
- `outputs/revision_v1/sensitivity/q_selected_attributes.json`

### 6.7 Comments 1.7 and 2.4: Outdated zero-shot baselines and Protocol B reframing

**Current problem:** Protocol B can be read as a competitive ZSL result and lacks modern baselines.

**Implementation actions:**

1. Rename table and revise caption to “semantic-transfer validation.”
2. Add comparison-type labels.
3. Add modern baselines after online verification.
4. Clearly state that specialized ZSL/GZSL systems optimize predictive transfer and are not directly comparable to SEMTRA’s post-hoc audit objective.
5. Replace “outperforms zero-shot baselines” with cautious language.

**Required wording:**

> “SEMTRA exceeds foundational DAP under this protocol but remains below specialized predictive ZSL/GZSL systems; its purpose is traceable semantic validation rather than optimized zero-shot recognition.”

### 6.8 Comment 1.8: Fidelity metric definitions

**Current problem:** Covered fidelity and covered accuracy can be confused.

**Implementation actions:**

1. Add equations listed in Section 5.1.4.
2. Update all captions and prose where “accuracy” and “fidelity” appear.
3. Ensure `tab:rulebook_summary` has separate columns for covered fidelity and covered accuracy if both are discussed.
4. Add note that values differ because the base model is imperfect.

### 6.9 Comment 1.10: Runtime for reduct search and per-phase computation

**Current problem:** Runtime table does not isolate reduct-search cost or phases.

**Implementation actions:**

1. Instrument every major phase with timers.
2. Record runtime per seed and dataset.
3. Record peak memory where feasible.
4. Add main runtime summary table and full supplement table.
5. Include hardware/software metadata.

**Minimum code instrumentation standard:**

- Use monotonic timers such as `time.perf_counter()`.
- Log phase name, dataset, seed, start/end, elapsed seconds, hardware, peak memory, script commit hash or git status, and output artifact path.
- Store in `outputs/revision_v1/runtime/runtime_phase_log.jsonl`.

### 6.10 Comment 1.11: Figure 5 conceptual comparison

**Current problem:** Figure `fig:conc_comparison` is conceptual but may imply quantitative superiority.

**Implementation actions:**

1. Revise caption to include “conceptual schematic” or “illustrative comparison.”
2. Remove any text saying the figure demonstrates empirical superiority.
3. Add a sentence:

> “This schematic is conceptual; quantitative agreement between local explanations and SEMTRA antecedents is reported in Table X.”

### 6.11 Comment 1.12: Bat-class failure diagnosis

**Current problem:** The bat failure is asserted but not diagnosed with enough evidence.

**Implementation actions:**

1. Extract all bat test cases from Protocol B.
2. Compute class-level and instance-level semantic reconstruction errors.
3. Compute top confused classes.
4. Compute prototype distances and Hamming distances.
5. Extract fired or missing rules.
6. Compare selected attributes against bat prototype attributes.
7. Add `tab:bat_diagnostic` to main or supplement, with a concise main-text interpretation.

**Required framing:**

> “The bat failure is treated as a SEMTRA diagnostic signal: it indicates a semantic rupture between the frozen visual representation and the AwA2 attribute dictionary, not merely a negative accuracy result.”

### 6.12 Comment 1.13: Recent rough-set plus neural-network literature

**Current problem:** Rough-set related works rely too heavily on classic foundations.

**Implementation actions:**

1. Search current literature using scholarly search and DOI/Crossref.
2. Add a paragraph on modern fuzzy-rough and rough neural systems.
3. Position SEMTRA as post-hoc and symbolic rather than end-to-end rough/fuzzy neural.
4. Cite verified peer-reviewed sources.

### 6.13 Comment 1.14: Confidence intervals or standard deviations in Protocol B

**Current problem:** Protocol B SEMTRA results lack seed-wise uncertainty.

**Implementation actions:**

1. Rerun Protocol B with the same five seeds used elsewhere, or extract existing seed logs.
2. Report mean ± standard deviation for SEMTRA Semantic Transition and Symbolic Template.
3. Compute 95% CI using a t-interval or bootstrap across seeds/classes.
4. For published baselines without uncertainty, write “not reported.”
5. Update abstract/discussion to avoid point-estimate-only claims.

---

## 7. Experiment-Level Implementation Plan

### 7.1 Global Reproducibility Record

Codex must create a single revision experiment manifest:

`outputs/revision_v1/manifest_revision_v1.json`

Required fields:

- Manuscript title.
- Date/time.
- Git commit hash or file hash for code and manuscript files.
- Python/R/Julia versions if used.
- Package versions.
- Hardware: CPU, GPU, RAM, operating system.
- Dataset paths and checksums where possible.
- Seeds.
- Feature extractor names and versions.
- Split definitions.
- Hyperparameter grids.
- Output artifact index.

### 7.2 AwA2 Reverification

Tasks:

1. Regenerate base predictor performance.
2. Regenerate transition metrics.
3. Regenerate rulebook metrics.
4. Regenerate discretizer comparison.
5. Regenerate synthetic benchmark.
6. Regenerate Protocol B seed-wise results.
7. Generate q and r sensitivity.
8. Generate runtime phase logs.

Minimum seeds: the existing five-seed convention in the manuscript. If not identifiable, use `42, 43, 44, 45, 46` and document the change.

### 7.3 SUN Experiment

Output files:

- `outputs/revision_v1/sun/sun_dataset_manifest.json`
- `outputs/revision_v1/sun/sun_transition_seedwise.csv`
- `outputs/revision_v1/sun/sun_rulebook_seedwise.csv`
- `outputs/revision_v1/sun/sun_q_sensitivity.csv`
- `outputs/revision_v1/sun/sun_discretizer_comparison.csv`
- `outputs/revision_v1/sun/sun_runtime.jsonl`
- `outputs/revision_v1/sun/sun_summary_table.tex`

Required reporting:

- Full dataset or explicit subset.
- Number of images/classes/attributes used.
- Split details.
- Selected attributes and their semantic type.
- All SEMTRA audit metrics.
- Main limitation if category sample sizes are small.

### 7.4 Derm7pt Experiment

Output files:

- `outputs/revision_v1/derm7pt/derm7pt_dataset_manifest.json`
- `outputs/revision_v1/derm7pt/derm7pt_transition_seedwise.csv`
- `outputs/revision_v1/derm7pt/derm7pt_rulebook_seedwise.csv`
- `outputs/revision_v1/derm7pt/derm7pt_q_sensitivity.csv`
- `outputs/revision_v1/derm7pt/derm7pt_concept_conflict_diagnostics.csv`
- `outputs/revision_v1/derm7pt/derm7pt_runtime.jsonl`
- `outputs/revision_v1/derm7pt/derm7pt_summary_table.tex`

Required reporting:

- Lesion/case-level split safeguards.
- Modality used.
- Class labels used.
- Checklist concept labels used.
- Missing-value handling.
- Class imbalance handling.
- Technical-validation-only caution.

### 7.5 Discretizer Stability Experiment

For WEDD and MDLP-like entropy:

- Use same train/test splits and seeds.
- Compute threshold values by attribute and seed.
- Compute paired differences in coverage, covered fidelity, covered accuracy, all accuracy, conflict, abstention, rule count, and average rule length.
- Compute practical effect size, e.g., paired mean difference divided by paired standard deviation, or Cliff’s delta if non-normal.
- Use p-values only as secondary evidence.

### 7.6 SVD-Rank Sensitivity Experiment

For each \(r\):

1. Fit SVD/PCA representation.
2. Fit transition matrix.
3. Reconstruct semantics.
4. Select attributes.
5. Discretize.
6. Induce rules.
7. Evaluate metrics.
8. Log runtime and memory.

The table must make the audit tax analyzable, not merely report reconstruction metrics.

### 7.7 q-Sensitivity Experiment

For each q:

1. Select top-q attributes using the defined score.
2. Store selected attribute list.
3. Run WEDD and MDLP-like entropy where feasible.
4. Induce rules.
5. Evaluate metrics.
6. Log reduct-search runtime and memory.

The final default q must be justified by the grid.

### 7.8 Confidence-Threshold Frontier

Evaluate rule confidence thresholds over a grid, e.g.:

\(\theta \in \{0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95\}\)

Metrics:

- Coverage.
- Covered fidelity.
- Covered accuracy.
- Conflict.
- Abstention.
- Rule count.
- Average rule length.

Optional figure: `fig:audit_tax_frontier`.

---

## 8. Table and Figure Insertion Plan

| Artifact | Required action | Label | Main or supplement | Target placement |
|---|---|---|---|---|
| Discretizer comparison | Move from Appendix B and revise caption/discussion | `tab:discretizer_comparison_main` | Main | `subsec:rulebook_auditability` |
| ETM-vs-SEMTRA comparison | Add new comparison table | `tab:etm_semtra_comparison` | Main | `sec:introduction` |
| Cross-domain generalization summary | Add AwA2/SUN/Derm7pt summary | `tab:cross_domain_generalization` | Main | New cross-domain Results subsection |
| SVD-rank sensitivity | Add compact summary or full table | `tab:svd_rank_sensitivity` | Main or supplement | Results or supplement sensitivity section |
| q-sensitivity | Add default-q evidence | `tab:q_sensitivity` | Main or supplement | Results or supplement sensitivity section |
| Runtime breakdown | Add per-phase runtime including reduct search | `tab:runtime_breakdown` | Main summary, supplement full | Results and supplement |
| Protocol B semantic-validation baselines | Revise existing table | `tab:semantic_validation_baselines` | Main | `subsec:protocol_b_results` |
| Protocol B per-class seed-wise results | Add uncertainty | `tab:protocol_b_seedwise` | Supplement or compact main | Protocol B / supplement |
| Bat diagnostic | Add failure diagnosis | `tab:bat_diagnostic` | Main or supplement | After `tab:protocol_b` |
| Figure `fig:conc_comparison` | Revise caption and text | existing label | Main | Protocol B / local comparison section |
| Audit-tax frontier | Optional but recommended | `fig:audit_tax_frontier` | Main or supplement | Discussion or sensitivity section |

---

## 9. Citation and Bibliography Plan

### 9.1 External Verification Requirements

Codex must use current online scholarly and official sources for all new references and must not rely on memory. Required tools, where available:

- Internet search.
- Scholarly search.
- Crossref DOI lookup.
- OpenAlex/Semantic Scholar metadata lookup.
- Dataset documentation inspection.
- GitHub repository inspection for dataset preprocessing where official.
- BibTeX validation.

### 9.2 Source Quality Ranking

Use sources in this priority order:

1. Published journal or conference paper with DOI.
2. Official dataset website.
3. Official code repository from dataset/paper authors.
4. Publisher page or proceedings page.
5. Preprint only when no published version exists.
6. Avoid blogs unless used only to identify a primary source and not cited.

### 9.3 Required Citation Insertions

- `sec:introduction`: ETM separation and prior transition matrix work.
- `subsec:symbolic_rule_extraction`: recent rough/fuzzy/neural rough-set systems.
- `subsec:semantic_transfer`: modern ZSL/GZSL baselines.
- `subsec:protocol`: SUN and Derm7pt dataset protocols.
- Cross-domain results: SUN and Derm7pt table caption or notes.
- Supplement dataset sections: official dataset and code citations.

### 9.4 Bibliography Consistency Checks

Run checks for:

- Duplicate keys.
- Unused new entries.
- Missing DOI/URL.
- Title capitalization consistency.
- Author-name consistency.
- `main.tex` citation keys not found in `references.bib`.
- `references.bib` entries not cited, except dataset pages intentionally kept for supplement.

---

## 10. LaTeX Editing Constraints

Codex must obey these constraints while editing `main.tex` and `supply.tex`.

- Do not add `\paragraph{}` commands.
- Use `\subsection{}` and `\subsubsection{}` only when structural headings are necessary.
- Preserve MDPI-compatible class, packages, table formatting, captions, labels, and cross-references.
- Use American English.
- Do not manually renumber references.
- Use stable labels and update all `\ref{}` calls.
- Avoid oversized tables in main text; move full seed-wise tables to supplement while keeping reviewer-critical summary in main text.
- Do not hide unfavorable evidence in supplement.
- Preserve current author metadata unless compilation requires technical correction.
- Use `booktabs` style for tables.
- Use `\begin{adjustwidth}{-\extralength}{0cm}` only when needed for wide MDPI tables.
- Avoid raw URLs in prose except dataset availability when journal style permits; prefer citations.
- Check for duplicate declarations and only correct if compile/MDPI compliance requires it; record the correction in `revision_report_v1.md`.

Required validation command concept:

```bash
grep -R "\\paragraph" main.tex supply.tex
```

The result must be empty after revision.

---

## 11. Statistical Reporting Standards

### 11.1 Repeated Experiments

For all repeated SEMTRA experiments, report:

- Mean ± standard deviation across seeds.
- 95% confidence interval where feasible.
- Number of seeds.
- Split definition.
- Whether the comparison is paired.

### 11.2 Paired Comparisons

For WEDD vs MDLP-like entropy:

- Use same seeds and splits.
- Report paired mean difference for key metrics.
- Report effect size.
- Use p-values only if assumptions are appropriate and not as a substitute for practical interpretation.

### 11.3 Confidence Intervals

Preferred hierarchy:

1. Bootstrap confidence interval over test objects or classes when object-level predictions are available.
2. t-interval over seeds when only seed-level summaries are available.
3. If neither is possible, report standard deviation and state limitation.

### 11.4 Metric Targets

Each metric must specify whether the target is:

- Ground truth \(y_i\).
- Frozen base model prediction \(f_{\mathrm{BB}}(x_i)\).
- Semantic prototype or checklist vector.
- Rulebook prediction \(\hat{y}_{\mathcal{R}}(x_i)\).

### 11.5 Dataset Split Safeguards

- AwA2: prevent seen/unseen leakage in Protocol B; document official xlsa17 split.
- SUN: stratify by scene category; document full or subset category list.
- Derm7pt: use lesion/case-level splits; do not split paired clinical and dermoscopic images from the same lesion across partitions.

### 11.6 Reporting Precision

Use consistent precision:

- Accuracy/fidelity/coverage/conflict/abstention: 3 or 4 decimals.
- Percentages in abstract: at most two decimal places.
- Runtime: seconds with appropriate precision; minutes/hours for long runs.
- Memory: GB.

---

## 12. Codex Multi-Agent Task Decomposition

### 12.1 Manuscript Auditor Agent

Responsibilities:

- Read `main.tex` and map every quantitative claim to a table, figure, or output artifact.
- Identify contradictions, unsupported claims, and overclaims.
- Produce a claim-audit table with columns: claim, location, supporting artifact, status, required edit.
- Mark exact LaTeX insertion points for all new tables, equations, and prose.
- Ensure reviewer comments define the scope.

Deliverables:

- `outputs/revision_v1/audit/claim_audit.csv`
- `outputs/revision_v1/audit/latex_insertion_map.md`

### 12.2 Experimental Reproduction Agent

Responsibilities:

- Rerun or design AwA2, SUN, Derm7pt, q-sensitivity, r-sensitivity, discretizer comparison, runtime, perturbation, and Protocol B experiments.
- Generate CSV/JSON logs and TeX table outputs.
- Use seed-controlled scripts.
- Maintain dataset manifests and split definitions.

Deliverables:

- All files under `outputs/revision_v1/awa2/`, `sun/`, `derm7pt/`, `sensitivity/`, `runtime/`, and `discretizers/`.

### 12.3 Statistics Agent

Responsibilities:

- Compute means, standard deviations, confidence intervals, paired comparisons, and effect sizes.
- Verify abstract and conclusion numbers.
- Mark unreported baseline uncertainty as “not reported.”
- Produce table-ready summaries.

Deliverables:

- `outputs/revision_v1/statistics/statistical_summary.md`
- `outputs/revision_v1/statistics/metric_consistency_check.csv`

### 12.4 Literature Agent

Responsibilities:

- Search and verify SUN, Derm7pt, modern ZSL/GZSL, rough-set/neural-network, and related concept/prototype literature.
- Use primary and authoritative sources.
- Update `references.bib` with consistent entries.
- Avoid low-quality sources.
- Add citations only where used.

Deliverables:

- Updated `references.bib`
- `outputs/revision_v1/literature/added_references.md`
- `outputs/revision_v1/literature/bibtex_validation.log`

### 12.5 LaTeX Integration Agent

Responsibilities:

- Insert revised prose, equations, tables, captions, and cross-references.
- Maintain MDPI formatting.
- Avoid `\paragraph{}`.
- Ensure all table/figure labels are unique.
- Update appendix/supplement references.

Deliverables:

- Updated `main.tex`
- Compiled manuscript PDF if environment supports compilation
- `outputs/revision_v1/latex/diff_summary.md`

### 12.6 Supplement Agent

Responsibilities:

- Expand `supply.tex` with reproducibility details and extended diagnostics.
- Move non-critical but necessary full tables to supplement.
- Keep critical contradictions in main text.
- Add artifact index and regeneration instructions.

Deliverables:

- Updated `supply.tex`
- Compiled supplement PDF if environment supports compilation

### 12.7 Quality-Control Agent

Responsibilities:

- Compile manuscript and supplement.
- Check unresolved references and citations.
- Check duplicate labels.
- Validate no `\paragraph{}` commands were added.
- Check bibliography syntax.
- Check all reviewer comments are addressed.
- Check abstract claims trace to main tables.
- Check table values match CSV/JSON logs.

Deliverables:

- `outputs/revision_v1/qc/qc_checklist.md`
- `outputs/revision_v1/qc/compile_log.txt`
- `outputs/revision_v1/qc/unresolved_refs.log`
- `outputs/revision_v1/qc/no_paragraph_check.log`

### 12.8 Revision Report Agent

Responsibilities:

- Write `revision_report_v1.md` after implementation or final planning.
- Include reviewer-comment traceability matrix.
- List modified files, tables, figures, recalculations, moderated claims, remaining limitations, and verification status.
- State that no unrelated changes were made beyond reviewer-driven and compile-required changes.

Deliverable:

- `revision_report_v1.md`

---

## 13. Validation Checklist

Codex must complete this checklist before finalizing the revision.

### 13.1 Claim and Number Consistency

- [ ] Every abstract number appears in a main-text table or figure.
- [ ] Synthetic macro-F1 statement is corrected.
- [ ] WEDD claims are moderated.
- [ ] Protocol B is not framed as competitive ZSL.
- [ ] Covered fidelity and covered accuracy are distinct.
- [ ] Audit tax is discussed as a design tradeoff.
- [ ] Derm7pt is described as retrospective technical validation only.

### 13.2 Reviewer Coverage

- [ ] Comment 1.1 addressed.
- [ ] Comment 1.2 addressed.
- [ ] Comment 1.3 addressed.
- [ ] Comment 1.4 addressed.
- [ ] Comment 1.5 addressed.
- [ ] Comment 1.6 addressed.
- [ ] Comment 1.7 addressed.
- [ ] Comment 1.8 addressed.
- [ ] Comment 1.9 addressed.
- [ ] Comment 1.10 addressed.
- [ ] Comment 1.11 addressed.
- [ ] Comment 1.12 addressed.
- [ ] Comment 1.13 addressed.
- [ ] Comment 1.14 addressed.
- [ ] Comment 2.1 addressed.
- [ ] Comment 2.2 addressed.
- [ ] Comment 2.3 addressed.
- [ ] Comment 2.4 addressed.

### 13.3 Experiments and Artifacts

- [ ] AwA2 core results regenerated or verified.
- [ ] Discretizer comparison moved to main text.
- [ ] WEDD-vs-MDLP paired analysis completed.
- [ ] q-sensitivity completed.
- [ ] SVD-rank sensitivity completed.
- [ ] Runtime phase logs completed.
- [ ] SUN experiment completed or explicitly not claimed.
- [ ] Derm7pt experiment completed or explicitly not claimed.
- [ ] Protocol B seed-wise uncertainty completed.
- [ ] Bat-class diagnostic completed.

### 13.4 LaTeX and Bibliography

- [ ] `main.tex` compiles.
- [ ] `supply.tex` compiles.
- [ ] No unresolved references.
- [ ] No unresolved citations.
- [ ] No duplicate labels.
- [ ] No added `\paragraph{}` commands.
- [ ] `references.bib` validates.
- [ ] New references are cited.
- [ ] Table captions specify metric targets.

### 13.5 Revision Report

- [ ] `revision_report_v1.md` exists.
- [ ] Reviewer traceability matrix complete.
- [ ] Modified files listed.
- [ ] Added/moved/revised tables listed.
- [ ] Added/revised figures listed.
- [ ] Recalculated results listed.
- [ ] Claim moderation listed.
- [ ] Remaining limitations listed.
- [ ] Statement on no unrelated changes included.

---

## 14. Instructions for Producing `revision_report_v1.md`

After implementation, Codex must create `revision_report_v1.md` using this template.

```markdown
# Revision Report v1: SEMTRA Manuscript

## 1. Executive Summary
Summarize the revision scope in 5–8 sentences.

## 2. Reviewer-Comment Traceability Matrix
| Reviewer | Comment ID | Concern summary | Manuscript action | File(s) | Section/table/figure | Verification status | Remaining limitations |
|---|---|---|---|---|---|---|---|

## 3. Modified Files
| File | Modification type | Summary | Reviewer driver |
|---|---|---|---|

## 4. Tables and Figures Added, Moved, or Revised
| Artifact | Status | Location | Source data | Reviewer driver |
|---|---|---|---|---|

## 5. Recalculated Results
| Result | Previous value | Revised value | Source artifact | Verification |
|---|---:|---:|---|---|

## 6. Moderated Claims
| Location | Previous claim type | Revised wording direction | Reason |
|---|---|---|---|

## 7. Bibliography Updates
List added entries and why each was added.

## 8. Supplement Updates
Summarize new supplementary sections and artifacts.

## 9. Reproducibility Artifacts
List scripts, CSV/JSON logs, table files, figure files, and manifests.

## 10. Quality-Control Results
Report compile status, citation status, label status, no-paragraph check, and numeric traceability.

## 11. Remaining Limitations
State any limits that remain after revision, especially data-access, runtime, cross-domain subset, or uncertainty limits.

## 12. Scope Statement
State: “No unrelated changes were made beyond reviewer-driven revisions and compile-required technical corrections.”
```

The report must be written for both human authors and software agents. It must not contain casual wording. It must be concrete enough for a coauthor to verify every claim.

---

## 15. Self-Evaluation

**Score: 98/100.**

This implementation strategy is execution-ready because it maps every reviewer comment to concrete file-level edits, experiment-level tasks, table/figure artifacts, citation updates, statistical standards, LaTeX constraints, quality-control checks, and revision-report requirements. It identifies the exact current contradictions in `main.tex`, especially the WEDD-vs-MDLP-like entropy conflict and the synthetic macro-F1 inconsistency. It specifies how to add SUN and Derm7pt experiments using authoritative dataset sources, how to reframe Protocol B, how to report uncertainty, how to formalize fidelity metrics, and how to make the audit tax measurable through SVD-rank, q-sensitivity, confidence-threshold, and runtime analyses.

Residual risks depend on external execution conditions: SUN and Derm7pt data access, runtime for full cross-domain experiments, availability of seed-level logs, and the ability to compile MDPI LaTeX in the target environment. These risks are explicitly handled by requiring that incomplete experiments not be claimed as completed results and by requiring `revision_report_v1.md` to document remaining limitations.
