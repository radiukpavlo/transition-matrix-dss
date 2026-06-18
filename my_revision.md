# SEMTRA Revision v3 Modification Summary

This file summarizes the manuscript, supplement, and bibliography changes made to satisfy `implementation_strategy_v3.md`.

## Reviewer 1

- R1-C1: Moved the WEDD-vs-MDLP-like entropy comparison into the main Results discussion, reported paired WEDD-minus-MDLP differences, and moderated the WEDD claim to a density-aware design option rather than universal superiority.
- R1-C2: Corrected the synthetic benchmark framing in the abstract and Results by reporting macro-F1 0.879 at zero noise and 0.838 at the highest tested noise level, without presenting the 0.8668 mean as the headline result.
- R1-C3: Added an explicit ETM-vs-SEMTRA distinction table and prose explaining that SEMTRA contributes semantic-to-symbolic auditing, rough-set rules, conflict handling, abstention, and audit-tax reporting rather than Lie-group equivariance.
- R1-C4: Integrated SUN and Derm7pt as additional technical-validation domains and scoped their interpretation in the main manuscript and supplement.
- R1-C5: Added SVD-rank sensitivity interpretation and reframed the audit tax as a tunable coverage-fidelity-runtime design decision rather than a rhetorical success claim.
- R1-C6: Added q-sensitivity discussion explaining how the selected attribute count affects rulebook granularity, coverage, fidelity, and combinatorial search.
- R1-C7: Expanded the zero-shot baseline context beyond DAP/IAP/GFZSL and reframed Protocol B as semantic-transfer validation, not leaderboard competition.
- R1-C8: Added formulas and prose distinguishing covered fidelity from covered accuracy, including why the two differ when the base predictor is imperfect.
- R1-C9: Kept the discretizer comparison in the main Results section and discussed the tradeoff candidly.
- R1-C10: Added runtime and reduct-search discussion in the appendix and expanded supplement, with generated runtime summary evidence.
- R1-C11: Clarified that the local-surrogate comparison figure is conceptual and not a quantitative result.
- R1-C12: Added bat-class failure diagnosis as a semantic rupture involving missing visual/contextual cues in the selected AwA2 attribute subset.
- R1-C13: Expanded rough-set related work to discuss modern fuzzy, differentiable, and hybrid rough-neural approaches.
- R1-C14: Added Protocol B seed-wise dispersion language and retained the generated seed-wise table for SEMTRA variants.

## Reviewer 2

- R2-C1: Moderated the central claim around the modest covered fidelity and covered accuracy, presenting SEMTRA as an audit layer rather than a classifier replacement.
- R2-C2: Added use-case-oriented interpretation for when a large audit tax can still be acceptable: diagnostics, dataset triage, model documentation, and explicit abstention.
- R2-C3: Added SUN and Derm7pt evidence with careful portability and clinical-scope limitations.
- R2-C4: Reframed the zero-shot section as semantic-transfer validation and broadened the baseline context so the predictive comparison is not overstated.

## Files Updated

- `manuscript/main.tex`: Added required `\revtag`, `\Rone`, `\Rtwo`, and `\Rthree` macros; inserted visible response tags for all review comments; updated figure paths to `figs_main`; corrected abstract and Results framing; expanded zero-shot, WEDD, sensitivity, runtime, and dataset-scope discussions.
- `manuscript/supply.tex`: Rebuilt the supplement as a 5000+ word reproducibility and evidence appendix with exactly ten post-revision figures from `figs_main`.
- `manuscript/references.bib`: Normalized SUN and Derm7pt web references and retained the broader zero-shot, rough-set, ETM, SUN, and Derm7pt citation set.

## Validation Targets

The intended validation sequence is:

```powershell
rtk powershell -NoProfile -ExecutionPolicy Bypass -File scripts\runners\semtra_revision.ps1 latex-v3
python C:\Users\radiu\.codex\plugins\cache\openai-bundled\latex\0.2.2\scripts\compile_latex.py D:\GitHub\transition-matrix-dss\manuscript\main.tex --json
python C:\Users\radiu\.codex\plugins\cache\openai-bundled\latex\0.2.2\scripts\compile_latex.py D:\GitHub\transition-matrix-dss\manuscript\supply.tex --json
rtk .\.venv\Scripts\python.exe scripts\runners\run_revision_v3.py --package-only
rtk .\.venv\Scripts\python.exe scripts\runners\run_revision_v3.py --validate-only
```
