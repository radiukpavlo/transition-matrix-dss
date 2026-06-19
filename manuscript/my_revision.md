# Revisions and Explanations

This document provides a comprehensive explanation of the modifications made to the manuscript in response to the reviewers' comments.

## General Formatting and Structural Updates
- The manuscript has been formatted exactly to the MDPI TeX template requirements, retaining all macros and maintaining the integrity of the compilation setup.
- To ensure traceability of the implemented changes, we introduced the `\revtag{X}{Y}` macro to tag areas of the text that respond directly to Reviewer `X`, Comment `Y`.
- We replaced instances of terms such as "reviewer," "revision," or "revised" within the text body with strictly objective academic phrasing.

## Responses to Reviewer 1

- **Comment 1.1 & 1.9 (WEDD vs. MDLP-like entropy and Table A4)**: We rigorously expanded the discussion around the WEDD discretizer. Rather than framing it as unconditionally superior, we now position WEDD as a density-aware, stability-oriented alternative. The related Table A4 has been elevated to the main manuscript text (Section 4) alongside detailed comparative explanations.
- **Comment 1.2 (Numerical Inconsistency)**: We corrected the abstract to explicitly report the zero-noise macro-F1 score (0.879) as the primary synthetic result and clearly separated the explanation of noise degradation (0.838 at the highest noise level).
- **Comment 1.3 (Relationship to ETM [5])**: The distinction between SEMTRA and the Equivariant Transition Matrix (ETM) work is now heavily clarified in the Introduction. We specified that SEMTRA does not rely on equivariance or Lie-group consistency but focuses on the semantic-to-symbolic audit sequence.
- **Comment 1.4 (Cross-Domain Datasets)**: As requested, we conducted exhaustive evaluations using the newly introduced SUN Attribute Database and Derm7pt datasets to validate the generalizability of the SEMTRA framework.
- **Comment 1.5 (Audit Tax and SVD Rank)**: The "audit tax" drop from 71.16% to 40.73% is comprehensively addressed. We provided a thorough SVD rank sensitivity grid to demonstrate the tradeoff and justified it as a consequence of enforcing strict discretization on a high-dimensional non-linear system.
- **Comment 1.6 (Attribute Selection q)**: We included a q-sensitivity grid analyzing rulebook coverage and structural complexity relative to the selected attribute count.
- **Comment 1.7 (Zero-shot Baselines)**: We reframed the zero-shot baseline comparison (e.g., against GFZSL) by explicitly clarifying that SEMTRA uses semantic-transfer primarily as an interpretability validation proxy rather than competing purely on predictive optimization.
- **Comment 1.8 (Fidelity Metrics Definitions)**: The definitions of Covered Fidelity and Covered Accuracy were expanded logically and mathematically in Section 3.6 to highlight how semantic rule predictions align with both the base model and the ground-truth labels.
- **Comment 1.10 (Runtime Analysis)**: Detailed per-phase runtime constraints and minimal reduct search components were added to improve reproducibility metrics.
- **Comment 1.11 (Figure 5)**: We corrected Figure 5's caption and textual references, emphasizing that it serves strictly as a conceptual visualization and pointing readers to the corresponding tables for actual quantitative results.
- **Comment 1.12 (Bat Class Failure Analysis)**: The failure mode involving the visually ambiguous "bat" class is now dissected in detail. This demonstrates SEMTRA's capability in providing a diagnostic window into semantic ruptures where black-box features do not align perfectly with attributes.
- **Comment 1.13 (Literature Update)**: We incorporated recent references combining rough sets with deep neural networks, placing SEMTRA's methodology into a stronger, more modern conceptual context in the related works section.
- **Comment 1.14 (Missing Confidence Intervals)**: Standard deviations were properly documented for the zero-shot results (Table 6) to ensure consistent metrics with Table 1.

## Responses to Reviewer 2

- **Comment 2.1 (Rulebook Quality Claim)**: We tempered the claims surrounding the non-abstained accuracy and covered fidelity, framing the 40.73% rate formally as an acceptable limitation within a conservative and explicit symbolic layer.
- **Comment 2.2 (Trade-off Justifications)**: The "transparent audit tax" rationale is bolstered by identifying specific high-stakes domains where avoiding structural uncertainty takes precedence over marginal coverage gains.
- **Comment 2.3 (Additional Datasets Evaluation)**: Similar to R1C4, we integrated performance analyses of SUN Attribute Database and Derm7pt into the main findings.
- **Comment 2.4 (Re-framing Zero-Shot Validation)**: The discussion regarding predictive parity has been meticulously rewritten. The manuscript now consistently refers to continuous prototype variants as semantic validation experiments instead of competing directly for zero-shot superiority against more complex models like GFZSL.
