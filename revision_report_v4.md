# Revision Report v4: SEMTRA Reviewer-Grilling Q&A

Generated: 2026-06-17

## Purpose

This report consolidates fifteen pressure-test questions and safe, reviewer-facing answers about the SEMTRA revision. The answers are written to directly address the reviewer issues captured in `implementation_strategy_v1.md`: claim moderation, covered fidelity versus accuracy, Protocol B framing, WEDD-vs-MDLP interpretation, SUN and Derm7pt scope, ETM comparison, reproducibility, and clinical-claim boundaries.

## 1. What is the precise central claim of SEMTRA after all v1--v3 revisions?

SEMTRA is a post-hoc semantic audit framework for frozen vision representations. It reconstructs concept-level transition structure, discretizes semantic evidence into rules, and reports where symbolic rules cover, agree with, or fail to track the base model. It is not a replacement classifier, not a clinical validation method, and not a competitive ZSL/GZSL model.

Reviewer issue addressed: moderates the main claim and prevents overstatement of predictive, clinical, or zero-shot competitiveness.

## 2. What exactly is SEMTRA's evidence unit: object-level predictions, class-level semantic prototypes, concept activations, or rules?

SEMTRA's evidence chain has multiple units, and the manuscript must keep them distinct. Object-level examples provide predictions, correctness, coverage, abstention, conflict, and fidelity outcomes. Concept-level semantic vectors define the interpretable attribute space. Class-level prototypes anchor semantic reconstruction. Induced rules summarize covered regions of the discretized concept space. Claims about fidelity and accuracy are object-level, while claims about semantic transition structure, compactness, salience, and rule length are rule/prototype-level.

Reviewer issue addressed: prevents mixing object-level performance evidence with rule/prototype-level interpretability evidence.

## 3. Why is covered fidelity to the base model not the same thing as covered accuracy against ground truth?

Covered accuracy asks whether SEMTRA's rule prediction matches the true label among covered objects. Covered fidelity asks whether SEMTRA's rule prediction matches the frozen base model among covered objects. Accuracy evaluates task correctness; fidelity evaluates whether the symbolic audit reproduces the model's observed behavior. A rule can be faithful but wrong if the base model is wrong, or accurate but unfaithful if it corrects a base-model error for reasons not captured by the base model.

Reviewer issue addressed: directly addresses the request to separate covered accuracy from covered fidelity.

## 4. If SEMTRA has low covered fidelity but moderate covered accuracy, what does that imply?

Low covered fidelity with moderate covered accuracy means the rulebook may be functioning as a partially useful semantic classifier but not as a faithful surrogate for the frozen base model. It can match ground truth while failing to reproduce the base model's observed decisions, so the rules should not be interpreted as explaining the model's behavior. For SEMTRA, this is evidence of audit decoupling: the semantic rule layer is informative about task structure but weak as a model-faithfulness account.

Reviewer issue addressed: avoids treating symbolic correctness as explanation truthfulness.

## 5. Why is Protocol B not a competitive zero-shot learning result?

Protocol B is not a competitive zero-shot learning result because it evaluates SEMTRA's semantic-transfer audit behavior under official unseen-class splits, not an end-to-end ZSL model optimized for recognition. The base features, semantic transition model, and rulebook are used to test whether concept-level structure can be transferred and audited. The result supports semantic-transfer validation, not leaderboard-style ZSL competitiveness.

Reviewer issue addressed: reframes Protocol B away from competitive ZSL/GZSL claims.

## 6. What would make Protocol B evidence stronger without turning the paper into a ZSL benchmark paper?

Protocol B would be strengthened by reporting concept-level reconstruction quality on unseen classes, not only final class accuracy. The key additions are unseen-class attribute MAE, semantic correlation, per-class failure audits, abstention/conflict rates, and soft-match distance distributions. The bat-class diagnostic is useful because it shows whether SEMTRA can localize semantic mismatch rather than merely reporting poor accuracy. This keeps Protocol B focused on auditability: can the semantic bridge transfer, can failures be diagnosed, and does the rule layer abstain or conflict when semantic evidence is weak?

Reviewer issue addressed: responds to requests for Protocol B uncertainty, failure diagnostics, and semantic-transfer evidence.

## 7. What is the single biggest threat to SEMTRA's validity as an audit method?

The biggest validity threat is semantic bottleneck error propagation. SEMTRA depends on predefined class-level attributes, a learned transition map, WEDD discretization, and rough-set rule induction. If the attribute dictionary misses intra-class variation or if early reconstruction errors distort the concept space, later rules may become artifacts of the audit pipeline rather than faithful summaries of the base model's behavior. Low fidelity can therefore mean either genuine model-semantic mismatch or SEMTRA pipeline decoupling, and the manuscript must distinguish those interpretations cautiously.

Reviewer issue addressed: acknowledges the main methodological limitation behind weak fidelity and audit reliability.

## 8. How do you distinguish "SEMTRA found a real model weakness" from "SEMTRA failed to approximate the model"?

The distinction requires triangulating evidence across pipeline stages. If continuous reconstruction is good, synthetic controls recover known logic, sensitivity analyses are stable, and failure cases concentrate in semantically ambiguous classes, then low fidelity is more plausibly a real model-semantic mismatch. If small changes in q, rank, thresholds, or feature source cause large swings, or if synthetic recovery fails, then low fidelity is more likely a SEMTRA approximation failure. The correct conclusion is probabilistic and diagnostic, not definitive.

Reviewer issue addressed: avoids unsupported causal claims about the base model's internal logic.

## 9. What evidence would falsify the claim that SEMTRA is a useful audit layer?

SEMTRA's audit-layer claim would be weakened or falsified if several diagnostics failed together: poor semantic reconstruction with high rule accuracy, low or unstable fidelity under small threshold/rank/q changes, failure on zero-noise synthetic rules, inconsistent rule extraction across seeds, and failure cases that do not correspond to interpretable semantic ambiguity. That pattern would show the rules are dataset-fitting artifacts rather than stable summaries of the base model's observed behavior.

Reviewer issue addressed: clarifies what kind of evidence would undermine SEMTRA rather than treating the method as unfalsifiable.

## 10. What is the strongest argument a reviewer could make against using Derm7pt in this paper at all?

The strongest objection is that Derm7pt may be too domain-shifted for a generic ImageNet-pretrained encoder. A locked ResNet-50 ImageNet1K V2 feature extractor is not trained to represent dermoscopic checklist concepts such as pigment network, streaks, or vascular structures. If SEMTRA performs weakly, the result may reflect an unsuitable encoder rather than a limitation of the audit method. If strong performance required dermatology-specific fine-tuning, that would weaken the paper's post-hoc frozen-representation portability claim. Therefore Derm7pt must be framed as retrospective technical stress testing, not clinical validation or proof of domain generality.

Reviewer issue addressed: limits Derm7pt claims and keeps the medical-image result outside clinical validation.

## 11. What is the strongest argument a reviewer could make against the SUN portability claim?

The strongest objection is that SUN's scene categories are far more numerous, overlapping, and semantically continuous than AwA2 animal classes. The global rough-set rulebook has to operate over 102 non-exclusive attributes and many fine-grained scene classes, so discretization can create large boundary regions, high conflict, and high abstention. The current SUN results support that concern: coverage is very low and conflict/abstention are high. Therefore SUN should be presented as a portability stress test that exposes current limitations, not as evidence that SEMTRA generalizes cleanly to scene recognition.

Reviewer issue addressed: constrains cross-domain portability claims and acknowledges SUN failure modes.

## 12. What exactly does the WEDD-vs-MDLP result prove, and what does it not prove?

The WEDD-vs-MDLP comparison shows that WEDD is a viable discretization choice with small empirical gains in coverage, covered accuracy, and covered fidelity on the current AwA2 seed set. It supports using density-aware thresholds as a tunable way to place semantic cutpoints, but the paired effects are modest. It does not prove universal superiority, guaranteed robustness, or optimal predictive performance. WEDD should be framed as an empirically useful discretizer in this setting, not as a generally dominant method.

Reviewer issue addressed: resolves WEDD overclaiming and presents the paired analysis conservatively.

## 13. Is the ETM comparison fair? What exactly can SEMTRA claim relative to ETM, and what would be unfair to claim?

The comparison is fair only as a methodological contrast. ETM emphasizes continuous transition structure and equivariance/geometric constraints; SEMTRA targets post-hoc symbolic auditability by adding discretization, rough-set rules, conflict reporting, abstention, and covered fidelity/accuracy metrics. SEMTRA can claim it adds a rule-level audit interface that ETM does not provide. It cannot claim superior geometric robustness, adversarial stability, or direct predictive dominance over ETM unless those properties are explicitly benchmarked.

Reviewer issue addressed: adds ETM context while avoiding unfair performance claims.

## 14. If a skeptical reviewer says, "Your artifact bundle is impressive, but I do not trust that the manuscript numbers were copied from it," what is the strongest answer?

The strongest answer is that the project now has layered traceability. Generated tables are emitted as LaTeX-ready `.tex` files from machine-readable CSV/JSON artifacts under `outputs/revision_v1/`, and v2 adds automated claim checking in `outputs/revision_v2/qc/claim_consistency_check.csv`. The v2 validation run passes with all checked manuscript claims matched, including AwA2 MAE, coverage/accuracy/fidelity, Protocol B uncertainty, synthetic macro-F1, Derm7pt claim gating, WEDD caution, and non-competitive ZSL framing. v3 further exports object-level prediction CSVs with true labels, base predictions, rule predictions, correctness, and fidelity flags, so intervals and summaries can be recomputed directly. The right claim is traceable and checked, not that nothing was manually copied.

Reviewer issue addressed: establishes reproducibility and claim traceability without overstating automation.

## 15. Where is the exact boundary between "decision support" and "clinical decision support" in this manuscript?

The boundary is evidentiary. SEMTRA can be described as a decision-support audit method in the general sense: it provides traceability, coverage, conflict, abstention, and fidelity diagnostics for model behavior. It cannot be described as clinical decision support because the paper does not provide prospective validation, clinician-reader studies, calibration for patient outcomes, regulatory analysis, deployment monitoring, or dermatology-specific clinical model validation. Derm7pt is included only as retrospective technical stress testing of the audit pipeline on medical-image metadata and images. Any clinical decision-support use is future work requiring separate validation.

Reviewer issue addressed: prevents unsupported clinical-readiness claims and protects the Derm7pt interpretation.

## Final Two-Sentence Defense

SEMTRA contributes a post-hoc semantic audit framework that maps frozen visual representations into concept-level transition estimates, discretizes those estimates with WEDD, and induces rough-set rules that expose coverage, conflict, abstention, covered accuracy, and covered fidelity. The revision shows, across AwA2, controlled synthetic tests, SUN, and Derm7pt stress tests, that SEMTRA can produce traceable audit artifacts and diagnose where semantic rule reconstructions align with or decouple from a base model, while preserving clear limits on portability, clinical interpretation, and zero-shot competitiveness.

## Summary

The safe reviewer-facing position is that SEMTRA is useful as an audit layer when its claims are tied to generated artifacts and when fidelity, accuracy, coverage, and semantic reconstruction are kept distinct. The revised manuscript should continue to avoid broad generalization, clinical-validation language, competitive ZSL framing, and WEDD superiority claims beyond the measured paired evidence.
