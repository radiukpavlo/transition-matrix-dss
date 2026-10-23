# AI4I experiment: results digest for writing

Source of truth: `E:\GitHub\semtra-ai4i\RESULTS.md` (results memo, every number traced to `outputs/`), the frozen
`PROTOCOL.md` (frozen 2026-10-23, checksums in `outputs/protocol_freeze.sha256`), tables in `outputs/tables/` (T1-T4 as
CSV and Markdown) and data plots in `outputs/figures/` (F2-F4 as PDF and SVG). Test stage, 5 seeds, mean ± SD.

## 1. What the paper can now claim

1. **Physics recovery with faithful concepts.** The class-reduct rulebook fitted on the true concept values uses exactly the
   documented concept sets for HDF {ΔT, speed}, PWF {power} and OSF {strain, product type} in 5/5 seeds, with no distractor;
   cuts at ΔT 8.600 K, speed 1379.4 rpm, power 9005 W, strain 11045 minNm; macro-F1 0.710 ± 0.020 with 5.2 rules, on par
   with the MLP (0.705 ± 0.044).
2. **The transition is the bottleneck for narrow regions.** Transition R² 0.974-0.992 for every physical concept (noise
   sensor −0.017), yet on predicted concepts the concept set is recovered for HDF in 1/5 seeds, PWF 4/5, OSF 2/5;
   macro-F1 0.457 ± 0.061.
3. **The rulebook as published in MAKE collapses at 97:3 imbalance**: macro-F1 0.280 ± 0.054 (predicted), 0.266 ± 0.034
   (true). This motivates the class-reduct rulebook, the paper's method contribution (decision 32).
4. **Rule disagreement complements the MLP's confidence.** AUROC 0.938 (max-probability) vs 0.782 (class-reduct
   disagreement); hybrid 0.944 ± 0.008, above max-probability in 5/5 seeds. At an equal review budget (54 flagged
   decisions, 2.7%) rule flags catch 23.2 errors vs 19.8, and 8.0 per seed only the rules catch. 58% of the MLP's errors are
   confident (max-probability ≥ 0.90); the rules flag 10.2 of 22.4.
5. **TWF is unrecoverable by design** (random generation); no method finds a TWF rule.

Not claimable: rules beating the MLP on predicted concepts, safety guarantees, plant validity (AI4I is synthetic),
statistical significance (5 seeds; test sets hold about 21 HDF, 16 PWF, 16 OSF, 8 TWF rows).

## 2. Data facts now verified from the CSV

L/M/H 6000/2997/1003; Machine failure 339; TWF 46, HDF 115, PWF 95, OSF 98, RNF 19; 24 multi-mode rows. HDF, PWF and OSF
labels match the documented rules on every row; TWF: 43 of 790 rows in the 200-240 min window are labelled. PWF: 31
low-power, 64 high-power. OSF: L 87, M 9, H 2. Kept 9,958 rows (none 9652, HDF 106, PWF 80, OSF 78, TWF 42).
These replace the conflicting UCI-page counts in `04_mdpi_overlap.md` §8.

## 3. Mapping to the 12-page outline (decision 19)

| Section | Content from the experiment |
|---------|-----------------------------|
| 3 Method | Transition, WEDD and MAKE rulebook cited to MAKE; new: class-specific reducts with pair lookahead, default-class inference, rule-disagreement score, budget-matched triage (`PROTOCOL.md` §3-4) |
| 4 Setup | `PROTOCOL.md` §1-3: data, labels, concepts, splits, MLP, settings, selection on validation, frozen protocol |
| 5.1 Transition fidelity | T1, F4 |
| 5.2 Physics recovery | T2a, T2b, F2, representative rules (`RESULTS.md` §4) |
| 5.3 Method comparison | T3 |
| 5.4 Triage | T4, F3 |
| 6 Discussion | `RESULTS.md` §9-10: what is and is not supported, limitations, the MAKE text vs code settings |

F1 is drawn by the authors from the component list in `RESULTS.md` §8. Captions and alt text are written by the authors
from the facts in `RESULTS.md` §7 (CEUR GenAI policy, decisions 20 and 23).

## 4. Code facts for the Method and the GenAI declaration

- Vendored MAKE module `src/semtra_core.py` (unchanged copy of `scripts/core/paper1_core.py`); new code in `ai4i_data.py`,
  `pipeline.py`, `run_experiment.py`, `make_report.py`, `figure_style.py`, `check_data.py`, `explore_validation.py`.
- The analysis and plotting code was written by Claude (Anthropic) under the author's direction; declare it in plain words.
- s_min = 11 on AI4I (n_train 5,974); transition 63 SVD components; selected on validation: MLP L2 alpha 1e-3 (seed 42) or
  1e-2 (43-46), CART depth 6/7/5/5/5.
- Done 2026-10-23: the MAKE commit hash in the header of `src/semtra_core.py` is masked; `CHANGES_AFTER_FREEZE.md` records
  the change (comment only, code digest unchanged). For the camera-ready version restore the original hash
  263c3225d6b8e5e1ae962a51b2ab14d7a1d23a3d (this repository's commit 263c322).
- Private GitHub repo https://github.com/radiukpavlo/semtra-ai4i (first commit 00c6c49, 2026-10-23); `.gitattributes`
  keeps files byte for byte so the frozen checksums hold. Anonymous mirror https://anonymous.4open.science/r/semtra-ai4i-CD9B (created 2026-10-23
  from commit 00c6c49, auto-update off, removed after 31 Jan 2027; nine redaction terms: GitHub username, author
  surnames and first name, Klymenko, khmnu, transition-matrix-dss, the old hash). Checked without login: all 64 files
  served byte-identical to the commit, no identifying term present. The GitHub App "Anonymous GitHub Read-only" has
  read access to this one repository; remove it in GitHub Settings > Applications after the review.
