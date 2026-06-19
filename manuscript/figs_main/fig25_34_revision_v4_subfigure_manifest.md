# Revision v4 Subfigure Manifest

All subfigures were generated with Python/matplotlib from existing revision artifacts and exported as PDF only.
Visible panel letters were intentionally omitted; subfigure letters are encoded only in filenames.

## fig25_a_revision_pipeline

- Archetype: schematic-led subfigure
- Core conclusion: v1-v3 revision artifacts form a cumulative evidence path.
- Source data: `outputs/revision_v1/revision_v1_run_summary.json; outputs/revision_v2/qc/claim_consistency_check.csv; outputs/revision_v3/manifest_revision_v3.json`
- PDF: `figs_main\fig25_a_revision_pipeline.pdf`

## fig25_b_artifact_counts

- Archetype: quantitative subfigure
- Core conclusion: The revision generated a multi-version artifact bundle.
- Source data: `outputs/revision_v1; outputs/revision_v2; outputs/revision_v3`
- PDF: `figs_main\fig25_b_artifact_counts.pdf`

## fig25_c_claim_gates

- Archetype: quantitative subfigure
- Core conclusion: SUN, Derm7pt, and QC gates are explicitly recorded.
- Source data: `outputs/revision_v1/revision_v1_run_summary.json; outputs/revision_v2/qc/qc_summary.json; outputs/revision_v3/manifest_revision_v3.json`
- PDF: `figs_main\fig25_c_claim_gates.pdf`

## fig25_d_validation_completeness

- Archetype: quantitative subfigure
- Core conclusion: Claim and QC validation completeness is machine-readable.
- Source data: `outputs/revision_v2/qc/claim_consistency_check.csv; outputs/revision_v3/qc/qc_checklist.csv`
- PDF: `figs_main\fig25_d_validation_completeness.pdf`

## fig26_a_object_level_audit_outcomes

- Archetype: quantitative subfigure
- Core conclusion: Enhanced prediction exports expose object-level coverage, accuracy, and fidelity.
- Source data: `outputs/revision_v3/statistics/object_level_metric_summary.csv; outputs/revision_v3/statistics/object_level_bootstrap_intervals.csv`
- PDF: `figs_main\fig26_a_object_level_audit_outcomes.pdf`

## fig26_b_conflict_abstention_limits

- Archetype: quantitative subfigure
- Core conclusion: Conflict and abstention reveal where symbolic auditing does not cover the base model.
- Source data: `outputs/revision_v3/statistics/object_level_metric_summary.csv`
- PDF: `figs_main\fig26_b_conflict_abstention_limits.pdf`

## fig26_c_object_level_bootstrap_intervals

- Archetype: quantitative subfigure
- Core conclusion: Object-level bootstrap intervals are computable from enhanced exports.
- Source data: `outputs/revision_v3/statistics/object_level_bootstrap_intervals.csv`
- PDF: `figs_main\fig26_c_object_level_bootstrap_intervals.pdf`

## fig27_a_coverage_by_discretizer

- Archetype: quantitative subfigure
- Core conclusion: Discretizer comparisons quantify WEDD without claiming universal superiority.
- Source data: `outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv`
- PDF: `figs_main\fig27_a_coverage_by_discretizer.pdf`

## fig27_b_accuracy_by_discretizer

- Archetype: quantitative subfigure
- Core conclusion: Discretizer comparisons quantify WEDD without claiming universal superiority.
- Source data: `outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv`
- PDF: `figs_main\fig27_b_accuracy_by_discretizer.pdf`

## fig27_c_fidelity_by_discretizer

- Archetype: quantitative subfigure
- Core conclusion: Discretizer comparisons quantify WEDD without claiming universal superiority.
- Source data: `outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv`
- PDF: `figs_main\fig27_c_fidelity_by_discretizer.pdf`

## fig27_d_conflict_by_discretizer

- Archetype: quantitative subfigure
- Core conclusion: Discretizer comparisons quantify WEDD without claiming universal superiority.
- Source data: `outputs/revision_v1/awa2/awa2_discretizer_comparison_summary.csv`
- PDF: `figs_main\fig27_d_conflict_by_discretizer.pdf`

## fig27_e_paired_wedd_mdlp_intervals

- Archetype: quantitative subfigure
- Core conclusion: Paired intervals show modest WEDD effects and preserve cautious framing.
- Source data: `outputs/revision_v2/statistics/paired_discretizer_intervals.csv`
- PDF: `figs_main\fig27_e_paired_wedd_mdlp_intervals.pdf`

## fig28_a_q_sensitivity

- Archetype: quantitative subfigure
- Core conclusion: q sensitivity makes the granularity tradeoff inspectable.
- Source data: `outputs/revision_v1/sensitivity/awa2_q_sensitivity.csv`
- PDF: `figs_main\fig28_a_q_sensitivity.pdf`

## fig28_b_svd_rank_sensitivity

- Archetype: quantitative subfigure
- Core conclusion: SVD rank changes both reconstruction and rule coverage.
- Source data: `outputs/revision_v1/sensitivity/awa2_svd_rank_sensitivity.csv`
- PDF: `figs_main\fig28_b_svd_rank_sensitivity.pdf`

## fig28_c_confidence_threshold_frontier

- Archetype: quantitative subfigure
- Core conclusion: Confidence thresholds expose coverage, accuracy, and fidelity tradeoffs.
- Source data: `outputs/revision_v1/sensitivity/awa2_confidence_threshold_frontier.csv`
- PDF: `figs_main\fig28_c_confidence_threshold_frontier.pdf`

## fig28_d_runtime_summary

- Archetype: quantitative subfigure
- Core conclusion: Runtime logs quantify the practical audit-tax components.
- Source data: `outputs/revision_v1/runtime/runtime_summary.csv`
- PDF: `figs_main\fig28_d_runtime_summary.pdf`

## fig29_a_protocol_b_seed_metrics

- Archetype: quantitative subfigure
- Core conclusion: Protocol B is reported as semantic-transfer validation, not ZSL competition.
- Source data: `outputs/revision_v1/awa2/awa2_protocol_b_seedwise.csv`
- PDF: `figs_main\fig29_a_protocol_b_seed_metrics.pdf`

## fig29_b_transfer_accuracy_vs_mae

- Archetype: quantitative subfigure
- Core conclusion: Unseen transfer metrics support auditability rather than recognition competitiveness.
- Source data: `outputs/revision_v1/awa2/awa2_protocol_b_seedwise.csv`
- PDF: `figs_main\fig29_b_transfer_accuracy_vs_mae.pdf`

## fig29_c_per_class_protocol_b_failures

- Archetype: quantitative subfigure
- Core conclusion: Per-class diagnostics localize semantic-transfer failures such as bat.
- Source data: `outputs/revision_v1/awa2/awa2_protocol_b_per_class_seed42.csv; outputs/revision_v1/awa2/awa2_bat_diagnostic.csv`
- PDF: `figs_main\fig29_c_per_class_protocol_b_failures.pdf`

## fig30_a_synthetic_macro_f1

- Archetype: quantitative subfigure
- Core conclusion: Synthetic controls show recoverability and noise degradation within a bounded setting.
- Source data: `outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv`
- PDF: `figs_main\fig30_a_synthetic_macro_f1.pdf`

## fig30_b_synthetic_rule_recovery

- Archetype: quantitative subfigure
- Core conclusion: Synthetic controls show recoverability and noise degradation within a bounded setting.
- Source data: `outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv`
- PDF: `figs_main\fig30_b_synthetic_rule_recovery.pdf`

## fig30_c_synthetic_coverage

- Archetype: quantitative subfigure
- Core conclusion: Synthetic controls show recoverability and noise degradation within a bounded setting.
- Source data: `outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv`
- PDF: `figs_main\fig30_c_synthetic_coverage.pdf`

## fig30_d_synthetic_threshold_error

- Archetype: quantitative subfigure
- Core conclusion: Synthetic controls show recoverability and noise degradation within a bounded setting.
- Source data: `outputs/revision_v1/synthetic/synthetic_summary_by_noise.csv`
- PDF: `figs_main\fig30_d_synthetic_threshold_error.pdf`

## fig31_a_portability_coverage_fidelity

- Archetype: quantitative subfigure
- Core conclusion: Cross-domain portability must be gated by coverage and fidelity.
- Source data: `outputs/revision_v1/statistics/cross_domain_generalization.csv`
- PDF: `figs_main\fig31_a_portability_coverage_fidelity.pdf`

## fig31_b_transition_mae_by_scope

- Archetype: quantitative subfigure
- Core conclusion: Transition reconstruction differs by dataset and validation scope.
- Source data: `outputs/revision_v1/statistics/cross_domain_generalization.csv`
- PDF: `figs_main\fig31_b_transition_mae_by_scope.pdf`

## fig31_c_cross_domain_object_metrics

- Archetype: quantitative subfigure
- Core conclusion: v3 stress tests preserve scoped interpretation across AwA2, SUN, and Derm7pt.
- Source data: `outputs/revision_v3/statistics/object_level_metric_summary.csv`
- PDF: `figs_main\fig31_c_cross_domain_object_metrics.pdf`

## fig32_a_sun_category_histograms

- Archetype: quantitative subfigure
- Core conclusion: SUN category diagnostics are dominated by abstention and conflict.
- Source data: `outputs/revision_v3/sun/sun_category_diagnostics_v3.csv`
- PDF: `figs_main\fig32_a_sun_category_histograms.pdf`

## fig32_b_sun_coverage_conflict_map

- Archetype: quantitative subfigure
- Core conclusion: SUN categories show high-conflict, low-coverage portability failure modes.
- Source data: `outputs/revision_v3/sun/sun_category_diagnostics_v3.csv`
- PDF: `figs_main\fig32_b_sun_coverage_conflict_map.pdf`

## fig32_c_sun_best_covered_categories

- Archetype: quantitative subfigure
- Core conclusion: Best-covered SUN categories are narrow exceptions, not broad portability proof.
- Source data: `outputs/revision_v3/sun/sun_category_diagnostics_v3.csv`
- PDF: `figs_main\fig32_c_sun_best_covered_categories.pdf`

## fig33_a_derm7pt_diagnosis_diagnostics

- Archetype: quantitative subfigure
- Core conclusion: Derm7pt diagnosis strata vary under technical validation only.
- Source data: `outputs/revision_v3/derm7pt/derm7pt_diagnosis_diagnostics_v3.csv`
- PDF: `figs_main\fig33_a_derm7pt_diagnosis_diagnostics.pdf`

## fig33_b_derm7pt_encoder_manifest

- Archetype: schematic subfigure
- Core conclusion: Derm7pt v3 uses a locked ImageNet ResNet-50 encoder, not a clinical model.
- Source data: `outputs/revision_v3/derm7pt/derm7pt_encoder_manifest.json`
- PDF: `figs_main\fig33_b_derm7pt_encoder_manifest.pdf`

## fig33_c_derm7pt_concept_diagnostics

- Archetype: quantitative subfigure
- Core conclusion: Checklist-concept diagnostics support retrospective technical interpretation only.
- Source data: `outputs/revision_v3/derm7pt/derm7pt_concept_diagnostics_v3.csv`
- PDF: `figs_main\fig33_c_derm7pt_concept_diagnostics.pdf`

## fig34_a_artifact_hash_families

- Archetype: quantitative subfigure
- Core conclusion: The v3 artifact index records hash-addressed artifact families.
- Source data: `outputs/revision_v3/artifact_index_revision_v3.csv`
- PDF: `figs_main\fig34_a_artifact_hash_families.pdf`

## fig34_b_manuscript_claim_checks

- Archetype: quantitative subfigure
- Core conclusion: Automated claim checks tie manuscript claims to generated artifacts.
- Source data: `outputs/revision_v2/qc/claim_consistency_check.csv`
- PDF: `figs_main\fig34_b_manuscript_claim_checks.pdf`

## fig34_c_v3_qc_checklist

- Archetype: quantitative subfigure
- Core conclusion: The v3 QC checklist passes required manuscript and artifact checks.
- Source data: `outputs/revision_v3/qc/qc_checklist.csv`
- PDF: `figs_main\fig34_c_v3_qc_checklist.pdf`

## fig34_d_submission_bundle_gates

- Archetype: schematic subfigure
- Core conclusion: The shareable submission bundle records required files and excludes raw private data.
- Source data: `outputs/revision_v3/submission_bundle/manifest.json; outputs/revision_v3/manifest_revision_v3.json`
- PDF: `figs_main\fig34_d_submission_bundle_gates.pdf`
