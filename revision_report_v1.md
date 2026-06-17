# Revision Report v1: SEMTRA Reviewer-Driven Revision

Generated: 2026-06-17

## Executive Assessment

The v1 implementation plan has been substantially and successfully executed, and the current manuscript/artifact state corresponds closely to the reviewer comments encoded in `implementation_strategy_v1.md`. The core reviewer concerns were not handled only rhetorically: the project now contains traceable experiment artifacts, claim-gating checks, regenerated tables, LaTeX-ready inserts, moderated manuscript language, and follow-on v2/v3 hardening artifacts.

The strongest completed elements are the AwA2 seed-wise regeneration, the separation of covered accuracy from covered fidelity, the WEDD-vs-MDLP paired analysis, the added SUN and Derm7pt stress-test protocols, the Protocol B reframing, the ETM comparison, the runtime/sensitivity diagnostics, and the claim-audit discipline. The current results support SEMTRA as a post-hoc semantic audit layer for frozen representations, not as a universal classifier, clinical model, or competitive zero-shot learning method.

One project-level gap from the original v1 deliverables was found during this assessment: the root-level `revision_report_v1.md` requested by the plan was missing. This file closes that reporting gap and records the current reviewer-alignment status.

## Implementation Status

Completed:

- Added and executed the v1 orchestration path through `scripts/run_revision_v1.py`.
- Preserved prior dirty workspace state and generated artifacts under `outputs/revision_v1/`.
- Generated a full non-smoke v1 run over AwA2 seeds `42,43,44,45,46`.
- Completed SUN and Derm7pt claim gates for v1, with both marked claimable only under their stated scopes.
- Added follow-on v2/v3 reproducibility and diagnostic layers without replacing v1 outputs.
- Added v3 enhanced prediction exports with true labels, base predictions, rule predictions, coverage, correctness, and fidelity flags.
- Added v3 object-level bootstrap metric summaries and intervals.
- Replaced the v3 Derm7pt handcrafted baseline with a locked TorchVision `ResNet50_Weights.IMAGENET1K_V2` image encoder.
- Added SUN category/hierarchy diagnostics in v3.
- Compiled and packaged manuscript/supplement artifacts through the v3 LaTeX and submission-bundle flow.

Verified current outputs:

- `outputs/revision_v1/revision_v1_run_summary.json`: status `ok`; `sun_completed=true`; `derm7pt_completed=true`.
- `outputs/revision_v1/qc/qc_checklist.md`: non-smoke run, seeds `42--46`, SUN/Derm7pt/synthetic claimable.
- `outputs/revision_v2/qc/claim_consistency_check.csv`: all claim checks pass.
- `outputs/revision_v3/qc/qc_summary.json`: status `pass`, no errors or warnings.
- `outputs/revision_v3/latex/latex_status.json`: direct fallback LaTeX compilation passes for `main.tex` and `supply.tex`.

## Reviewer Traceability

Reviewer concern 1.1, WEDD evidence and apparent contradictions:

Addressed. The manuscript now includes a main-text discretizer comparison and the v1 artifacts include `outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv` and `outputs/revision_v1/awa2/awa2_wedd_vs_mdlp_paired_stats.csv`. The paired WEDD-minus-MDLP differences are small: coverage `+0.0146`, covered accuracy `+0.0061`, and covered fidelity `+0.0073`. The revised wording correctly treats WEDD as a tunable discretization option, not as a universally superior method.

Reviewer concern 1.2, synthetic macro-F1 wording:

Addressed. Synthetic macro-F1 is now described as mean macro-F1, not as a final single operating-point result. The v1 audit traces the synthetic values to generated artifacts: zero-noise macro-F1 `0.879`, high-noise macro-F1 `0.838`, and mean macro-F1 `0.8668`.

Reviewer concern 1.3, ETM comparison:

Addressed. The manuscript includes an ETM-vs-SEMTRA comparison with ETM cited through DOI `10.3390/make8040092`. The comparison is framed methodologically rather than as a direct benchmark, which is appropriate because ETM and SEMTRA answer different parts of the evidence-tracing problem.

Reviewer concern 1.4, SUN expansion:

Addressed with bounded claims. The v1 bundle includes SUN manifests, transition metrics, rulebooks, predictions, q sensitivity, runtime logs, and LaTeX tables under `outputs/revision_v1/sun/`. Cross-domain reporting states the xlsa17 SUN scope explicitly. The v3 pass adds `sun_image_metadata.csv`, `sun_category_metadata.csv`, `sun_category_diagnostics_v3.csv`, and `sun_low_coverage_high_conflict_review.md` for deeper portability diagnostics.

Reviewer concern 1.5, audit tax and SVD compression:

Addressed. The v1 bundle includes `outputs/revision_v1/sensitivity/awa2_svd_rank_sensitivity.csv`, runtime summaries, and manuscript discussion of the cost/coverage tradeoff. The artifact name is prefixed with `awa2_`, but it covers the intended SVD-rank sensitivity requirement.

Reviewer concern 1.6, q sensitivity:

Addressed. The v1 bundle includes `outputs/revision_v1/sensitivity/awa2_q_sensitivity.csv` with q values `8,12,18,24,32`. As with SVD sensitivity, the generated filename is dataset-prefixed rather than the shorter nominal path in the strategy.

Reviewer concern 1.7, modern ZSL context:

Addressed. The bibliography and manuscript now cite modern context references only where the revised text discusses broad ZSL/GZSL categories. The manuscript avoids competitive ZSL framing for Protocol B.

Reviewer concern 1.8, covered fidelity versus covered accuracy:

Addressed. The manuscript and artifacts separate coverage, covered accuracy, and covered fidelity to the base predictor. v1 cross-domain summary reports AwA2 coverage `0.8480`, covered fidelity `0.4048`, and covered accuracy `0.3973`; v3 adds object-level interval-ready prediction exports.

Reviewer concern 1.9, WEDD superiority overclaim:

Addressed. The current manuscript says WEDD is not unconditionally superior and uses the paired analysis to support a cautious, empirical statement.

Reviewer concern 1.10, runtime:

Addressed. The v1 bundle includes `outputs/revision_v1/runtime/runtime_summary.csv` and runtime JSONL logs for the experimental components.

Reviewer concern 1.11, conceptual figure:

Addressed at the manuscript level by treating the comparison figure/text as conceptual rather than as an empirical performance claim.

Reviewer concern 1.12, bat-class anomaly:

Addressed. The v1 bundle includes `outputs/revision_v1/awa2/awa2_bat_diagnostic.csv`, which records the bat-class diagnostic failure mode rather than leaving it as anecdotal text.

Reviewer concern 1.13, rough-set/neural-symbolic literature:

Addressed. `outputs/revision_v1/literature/added_references.md` records the verified additions, and the BibTeX validation log reports no missing cited keys or duplicate BibTeX entries.

Reviewer concern 1.14, Protocol B uncertainty:

Addressed. Protocol B is now framed as semantic-transfer validation only, with seed-wise uncertainty. v1 reports Protocol B accuracy `44.02% +/- 1.22%` and avoids competitive ZSL language.

Reviewer concern 2.1, weak fidelity:

Addressed by reframing. The manuscript no longer presents weak covered fidelity as predictive success. It treats low fidelity as audit evidence about where symbolic reconstruction does or does not track the frozen base predictor.

Reviewer concern 2.2, practical acceptability of audit tax:

Addressed. The q sensitivity, SVD sensitivity, confidence-threshold frontier, and runtime logs make the practical tradeoff inspectable.

Reviewer concern 2.3, additional datasets:

Addressed with scope limits. SUN and Derm7pt are included as cross-domain stress tests. SUN remains a portability stress test with low coverage/low fidelity. Derm7pt remains retrospective technical validation only.

Reviewer concern 2.4, zero-shot framing:

Addressed. Protocol B is described as semantic-transfer validation and not as a competitive zero-shot learning result.

## Key Generated Evidence

AwA2:

- Protocol A test MAE: `0.1029 +/- 0.0005`.
- Rulebook coverage: `84.80%`.
- Covered accuracy: `39.73%`.
- Covered fidelity to base predictor: `40.48%`.
- Protocol B accuracy: `44.02% +/- 1.22%`, semantic-transfer only.

Synthetic benchmark:

- Zero-noise mean macro-F1: `0.879`.
- High-noise mean macro-F1: `0.838`.
- Overall synthetic mean macro-F1: `0.8668`.

SUN:

- v1 scope: xlsa17 SUN unseen transfer and seen-test audit.
- Objects: `1440`.
- Attributes: `102`.
- Transition MAE: `0.0683`.
- Coverage: `0.0760`.
- Covered fidelity: `0.0918`.
- Covered accuracy: `0.0714`.
- Interpretation: completed, but evidence supports stress-test/portability wording only.

Derm7pt:

- v1 scope: official test split, retrospective technical validation.
- Objects: `395`.
- Concepts: `7`.
- Transition MAE: `0.2433`.
- Coverage: `0.9241`.
- Covered fidelity: `0.5288`.
- Covered accuracy: `0.4219`.
- v3 replacement encoder: TorchVision ResNet-50 ImageNet1K V2, official case-level splits, deterministic no-gradient feature extraction.
- Interpretation: technical validation only, not clinical validation.

v3 object-level diagnostics:

- AwA2 seed-wise enhanced prediction exports include true labels, base predictions, rule predictions, correctness flags, and fidelity flags.
- SUN object-level coverage is `0.0760`, with low covered accuracy and low covered fidelity.
- Derm7pt ResNet-50 object-level coverage is `0.9899`, covered accuracy is `0.5729`, and covered fidelity is `0.7417`.

## Manuscript And Supplement Revisions

Completed manuscript changes include:

- Moderated abstract and conclusion claims.
- Corrected synthetic macro-F1 wording.
- Moved discretizer evidence into the Results section.
- Added ETM-vs-SEMTRA comparison.
- Separated covered fidelity from covered accuracy.
- Reframed Protocol B as semantic-transfer validation.
- Added cross-domain summaries only for completed runs.
- Removed or softened unsupported overclaims.
- Replaced simple Derm7pt feature wording with locked ResNet-50 encoder wording in the v3 update.
- Added SUN category-diagnostic caveats.
- Clarified that SEMTRA is a post-hoc diagnostic audit layer, not a classifier replacement.

Completed supplement changes include:

- Dataset protocol details.
- Seed-wise tables.
- Runtime logs and sensitivity grids.
- Rule traces and perturbation diagnostics.
- Artifact index and reproducibility notes.
- v3 enhanced prediction export documentation.
- v3 object-level interval and diagnostic table inserts.

## Reproducibility And QC

The current project has substantially stronger reproducibility than the starting v1 state:

- v1 artifacts are preserved under `outputs/revision_v1/`.
- v2 validation artifacts, schemas, claim checks, and submission bundle are preserved under `outputs/revision_v2/`.
- v3 enhanced predictions, object-level intervals, SUN metadata diagnostics, Derm7pt ResNet-50 artifacts, and submission bundle are preserved under `outputs/revision_v3/`.
- `scripts/semtra_revision.ps1` provides local entrypoints for setup, v1/v2/v3 execution, LaTeX compilation, QC, and packaging.
- LaTeX fallback compilation currently passes for both manuscript and supplement.
- Duplicate-label and missing-citation checks pass.
- No `\paragraph{}` commands were found in `manuscript/main.tex` or `manuscript/supply.tex`.

Remaining minor QC note:

- The BibTeX validation log records three unused BibTeX entries, but no missing cited keys and no duplicate BibTeX keys. This is not a blocking reviewer-response issue.

## Remaining Limitations

SUN:

- The SUN symbolic audit has very low coverage and low covered fidelity. The current evidence supports reporting SUN as a difficult portability stress test, not as proof of robust cross-domain generalization.
- v3 category diagnostics should be inspected before strengthening any portability claims.

Derm7pt:

- The v3 ResNet-50 encoder improves feature traceability, but it is ImageNet-pretrained and not a dermatology-specific clinical model.
- Derm7pt must remain retrospective technical validation only.
- No clinical-readiness, diagnostic-device, or patient-care claims are supported.

AwA2 and WEDD:

- WEDD shows small paired improvements over the MDLP-like entropy discretizer, but the effect sizes are modest. The manuscript should keep the current cautious framing.

Protocol B:

- Protocol B supports semantic-transfer validation only. It should not be framed as a competitive GZSL/ZSL benchmark result.

General:

- SEMTRA remains dependent on predefined semantic attributes. It can miss visual variation that is not represented in the concept dictionary.
- Rule extraction and reduct search can become expensive with larger concept dictionaries.

## Final Assessment

The current results do correspond successfully to the reviewer comments in `implementation_strategy_v1.md`. The revision is especially strong on traceability: most major claims now point to generated CSV/JSON/TeX artifacts, and the manuscript language is gated by those artifacts. The project also goes beyond the v1 requirements through v2/v3 claim checking, schema validation, enhanced prediction exports, object-level intervals, SUN category diagnostics, and a locked Derm7pt ResNet-50 encoder.

The work should not be described as proving broad clinical readiness, universal interpretability, universal WEDD superiority, or competitive zero-shot learning performance. With those boundaries maintained, the revised manuscript and artifacts form a materially stronger, reviewer-responsive SEMTRA revision package.
