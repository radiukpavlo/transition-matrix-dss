# 02 — Project inventory beyond the conference manuscript

This file lists what the SEMTRA repository holds beyond what went into the ICyberPhyS-2026 paper (see `01_conference_manuscript.md`). It records exact numbers, where each one lives, whether the conference paper used it, and whether it likely appears in the MDPI MAKE paper (2026, 8(7), 181). It also covers how to regenerate figures and tables, the environment they need, where the numbers do not match, and (last section) which code to reuse for the AI4I 2020 experiment of the AIT&AIS'2026 companion paper. Everything here comes from local files and local git history only; facts about the *published* MAKE article come from `04_mdpi_overlap.md`.

> Context (author, 2026-10-22): the new manuscript must be submitted in CMT **before 28 October 2026** (target 26 Oct, hard limit 27 Oct); the AIT&AIS'2026 talk is **online, given by Pavlo Radiuk alone**, as agreed with the organising committee. AwA2 results appear in the new paper only through citations to MAKE (decision 14).

## 0. Provenance: three result generations, in different places

| Gen | What | Where | Configuration | Used by |
|---|---|---|---|---|
| **G1** "Paper-1 PoC" package (May 2026) | Single-run AwA2 Protocol A/B, baselines, ablations, synthetic | **Working tree**: `artifacts/awa2/`, `artifacts/synthetic/`, `tables/*.csv/.tex`, `manuscript/figs_archived/fig01–fig24` | seed 42; Protocol A SVD r = **16** (explained variance 0.2952); auxiliary 64-coordinate cache for baselines; q = 18; WEDD α(λ_H) = 0.65; τ = 0.84; s_min = 18 | Conference Figs 2–4, Tables 3–5; Table 2 baseline columns |
| **G2** revision v1–v3 (2026-06-16/17) | 5-seed AwA2, discretizer comparison, q/SVD/confidence sensitivity, Protocol B seedwise, SUN, Derm7pt, runtime, object-level bootstrap | **Only in git history**: branch `origin/dev` (HEAD d190136, 2026-06-27) under `outputs/revision_v1/`, `revision_v2/`, `revision_v3/` (248 files, plus `outputs/README.md` = 249 under `outputs/`; commit bbd4007, 2026-06-18, deleted 51 LaTeX build files from `revision_v1/latex/` and `revision_v2/latex/`; `revision_v3/latex/` (44 files), `revision_v3/submission_bundle/` and all data CSVs remain). **Not on `main`** | seeds 42–46; r = **64** (explained variance ≈0.53); q = 18; Python 3.13.6, Windows 11 | Conference Tables 1–2 ("ours" column); MDPI main text |
| **G3** MDPI manuscript sources | `manuscript/main.tex` (1,281 lines, ≈14k words, 118 KB), `supply.tex`, `references.bib` (45 entries), `my_revision.md` (MDPI reviewer responses), a compiled `main.pdf` (31 pages, built 2026-06-20, commit 51ffb17, one day before the last `main.tex` edit), and `odt/85_Paper_v0.3_ceur_formatted.odt` with `build_ceur_odt.py` (an early CEUR conversion) | **Only in git history**: `origin/dev` (last `main.tex` edit f843e5e, 2026-06-21) | MDPI template; revision tags `\revtag{X}{Y}` | Basis for "likely in MDPI" judgements below |

The audit trail shows the earlier package history. `audit/compile_audit.json` (2026-05-18) records an 18-page build. `audit/enhanced_final_audit.json` (2026-05-19) records 42 pages, an estimated 10,515 words, 24 figures and 24 tables. `audit/revision_final_audit.json` (2026-05-28) records 29 pages, 36 references, 27 tables and 30 internal reviewer items (27 implemented, 3 "implemented_with_limitation"). The README cites the preprint *Preprints* 202606.0230.v1 (DOI 10.20944/preprints202606.0230.v1).

How to read G2/G3 locally without changing the working tree: `git show origin/dev:outputs/revision_v1/awa2/awa2_protocol_a_summary.csv`, `git show origin/dev:manuscript/main.tex`, and so on.

**Caveat:** G3 is the 2026-06-21 dev draft, not the published PDF. "Likely in MDPI" below means "present in that draft", backed by `revision_report.md`, `audit/reviewer_response_matrix.csv` and `manuscript/figs_archived` names. The online check recorded in `04_mdpi_overlap.md` §1 confirms the main-text tables of the published MAKE 8(7):181 (33 pages). It reports the published Supplementary File S1 as Tables S1–S3 plus one Figure S1 (object-level audit outcomes and bootstrap intervals), so the dev-draft supplement figures 27–33 cited below are **(unverified)** as published.

## 1. Datasets

| Dataset | Size / split | Representation | Source of numbers | In conf.? | In MDPI draft? |
|---|---|---|---|---|---|
| **AwA2 Protocol A** (closed world) | 37,322 images, 50 classes, 85 attributes; split 22,393 / 7,464 / 7,465 | ResNet-101 features, 2048-d (ILSVRC-pretrained, no augmentation): G1 reads `AwA2-features.parquet` from `awa2.zip` ("released with AwA2"), G2 reads the xlsa17 `res101` export `data/raw/awa2/Features/xlsa17/xlsa17_res101_features.parquet`; SVD to r = 16 (G1) or r = 64 (G2). **Semantics are class-level**: every object of a class gets the same 85-d attribute vector (`B_obj = B_class[y]`) | `tables/dataset_summary.csv`, `tables/feature_extractor_hyperparameters.csv`, `artifacts/awa2/protocol_a_summary.json` | Partly: 50/85 only; no sizes, no ResNet/SVD in text | Yes (main, Appendix hyperparameters) |
| **AwA2 Protocol B** (official xlsa17 proposed split) | 40 seen / 10 unseen; trainval 23,527 (train 16,187 + val 7,340); test unseen 7,913, test seen 5,882. Unseen: sheep, dolphin, bat, seal, blue whale, rat, horse, walrus, giraffe, bobcat | same features; G1 r = 32, ridge α = 100; G2 r = 64 | `artifacts/awa2/protocol_b_summary.json`; `source_notes/awa2_split_note.md` (MATLAB 1-based indices converted to 0-based) | **No** | Yes (main §4.3) |
| **SUN** (xlsa17 release) | 14,340 images, 717 classes, 102 attributes; train 9,280 / val 1,040 / test seen 2,580 / test unseen 1,440 (72 unseen classes) | xlsa17 features | `origin/dev:outputs/revision_v1/sun/*` | **No** | Yes (main cross-domain table + supplement) |
| **Derm7pt** | 1,011 cases; official test split 395; 7 checklist concepts (pigment_network, streaks, pigmentation, regression_structures, dots_and_globules, blue_whitish_veil, vascular_structures) | v1/v2: "simple-image-feature" run (the MDPI caption says "clinical metadata features"); v3: locked torchvision ResNet-50 IMAGENET1K_V2, 2048-d, CPU | `origin/dev:outputs/revision_v1/derm7pt/*`, `revision_v3/derm7pt/derm7pt_encoder_manifest.json` | **No** | Yes, framed as "retrospective technical validation only" |
| **Synthetic** | 10,000 objects per run, 5 classes, 10 attributes, 60/20/20 split; σ ∈ {0, 0.02, 0.05, 0.10, 0.15, 0.20} × 5 seeds = 30 runs; 4 ground-truth rules (class 1: b1 high ∧ b3 low; class 2: b2 medium ∧ b5 high; class 3: b4 low ∧ b6 high ∧ b8 medium; class 4: b7 high ∧ b9 low; thresholds 0.35 / 0.65 / 0.70) | ground-truth semantics + noise | `artifacts/synthetic/*`, `tables/synthetic_noise_summary.csv` | Partly: only σ = 0, 0.1, 0.2; generator not described | Yes (main, incl. GT rule table, Fig. 22 bands, Fig. 13) |

Raw archives are expected at `data/raw/awa2.zip` and `data/raw/xlsa17.zip` (the two named in `data/README.md`); the G2 runner additionally expects extracted files under `data/raw/awa2/Features/xlsa17/`, `data/raw/xlsa17/data/SUN/` and `data/raw/Derm7pt/` (`meta/meta.csv`, `images/`). **None is present** (`data/` holds only a README; `.gitignore` excludes `data/raw/` and `data/**/*.zip`). Only the G1 artifacts can be used offline.

## 2. Pipeline configuration (from `tables/feature_extractor_hyperparameters.csv` and code)

- **Base predictor (two different ones):** G1 = `RidgeClassifier(alpha=1.0)` on the 64 variance-screened cache coordinates, softmax-normalised decision scores, seed 42 (`scripts/experiments/train_base_predictor.py`; test Top-1 0.7116). G2 = `RidgeClassifier(alpha=1.0)` on each seed's 64 SVD coordinates, hard labels (`run_revision_v1.py::classifier_predictions`); test accuracy 0.802–0.810 (mean 0.806, computed from the v3 enhanced prediction exports). Conference Table 2 fidelity (0.4048) is measured against the G2 predictor.
- **Semantic bridge:** `scripts/core/paper1_core.py::fit_transition`: `StandardScaler(with_mean=False)` on A (no centring), `TruncatedSVD(n_components=r, n_iter=2)` whose basis is fit on a random subset of at most 5,000 training rows, targets `MinMaxScaler` fit on train and clipped to [0, 1], then `Ridge(fit_intercept=True)` with α from {0.01, 0.1, 1, 10, 100} chosen by validation MAE; predictions clipped to [0, 1]. α = 0.01 was selected in G1 and G2, but validation MAE differs by less than 2·10⁻⁶ across the whole grid, so α is effectively irrelevant there (G1 Protocol B, r = 32, picked α = 100). This is not centred PCA, despite the MDPI centring equation.
- **WEDD:**
  - objective α·entropy_norm + (1 − α)·density_norm, minimised, with α = 0.65, max_depth = 2 (≤ 3 thresholds, 4 states s0–s3), min_gain = 0.002 bits; min bin size 30 in G1 (`max(30, s_min)`), 18 in the G2 AwA2 runs (`max(10, s_min)`), 5 for Derm7pt;
  - entropy = count-weighted child class entropy (log2); both terms are min-max normalised over the candidates of the node;
  - density = box-kernel count with Silverman-type bandwidth h = 0.9·min(sd, IQR/1.34)·n^(−1/5) (`local_density`);
  - candidates: midpoints of unique values if there are ≤ 97 of them, else up to 96 quantiles between the 1st and 99th percentile (`candidate_thresholds`);
  - states assigned with `np.digitize(..., right=False)`: s0 < t1 ≤ s1 < t2 ≤ s2 < t3 ≤ s3 (during fitting a value equal to t goes left, so ties are treated inconsistently; harmless for continuous Ŷ).
- **Attribute selection (q = 18 of 85), two different rules:**
  - G1 (`scripts/legacy/run_all_experiments.py::select_attributes`): eight hand-forced attributes first (`FORCED_AWA2_ATTRS` = stripes, hooves, swims, paws, longneck, hunter, ocean, quadrapedal), then the top attributes by salience / (val MAE + 0.02). Selected: stripes, hooves, swims, paws, longneck, hunter, ocean, quadrapedal, water, flippers, hands, plankton, skimmer, small, jungle, yellow, furry, toughskin.
  - G2 (`run_revision_v1.py::select_attributes`): score = 0.5·minmax(salience) + 0.5·(1 − minmax(val MAE)); no σ_j normalisation, so it differs from the MDPI `attr_score` equation (e_j/(σ_j+ε)). Seed-42 selection: stripes, hooves, stalker, ocean, grazer, paws, flippers, hairless, yellow, claws, hops, jungle, water, hands, vegetation, bipedal, tree, hunter.
  - Salience = L2 norm of each target's ridge weights in SVD-score space (`np.linalg.norm(ridge.coef_.T, axis=0)`), not a column norm of T itself.
- **Rules (`induce_rules`):** granules with support ≥ s_min and purity ≥ τ (τ = 0.84, s_min = 18; at most 500 granules, largest first) are reduced greedily, lowest-priority attribute first, while support ≥ s_min and confidence ≥ τ hold. Pure granules give `strict_lower` rules, impure ones with purity ≥ τ give `boundary_high_confidence` rules. Every class still without a rule gets one class-mode `semantic_prototype` rule, built from up to 8 candidate states and accepted at confidence ≥ max(0.55, τ − 0.20) = 0.64; if none qualifies, the top-4 candidate states are used **whatever their confidence** (hence AwA2 prototype rules with confidence 0.04). At most 4 rules per class are kept (5 in the G1 discretizer ablation).
- **Inference (`infer_rules`):**
  - vote strength = conf × log1p(support) / antecedent length;
  - conflict = top-two vote margin < 0.05·max(1, top vote) → abstain;
  - no rule fired → nearest class-mode signature by mean Hamming distance if ≤ the fallback threshold, else abstain. Threshold 0.50 in the G1 main pipeline, rule stability, the Fig. 4 sweep, SUN and Derm7pt; 0.45 in the G2 AwA2 runs and the G1 discretizer and operator ablations; the MDPI draft's hyperparameter table states τ_H = 0.25, which no script uses;
  - coverage = share of objects not abstained, **which includes fallbacks**.
- **Hardware note in the MDPI draft:** NVIDIA RTX 3090 and Intel Core i9-10900K.

## 3. Experiments and key numbers

### 3.1 Base predictor (G1, `artifacts/awa2/base_predictor_metrics.json`) — NOT in conf.; MDPI: yes (appendix table)

| Split | Top-1 | Top-5 | Macro-F1 | Weighted-F1 | AUROC (OvR) | ECE (10-bin) |
|---|---|---|---|---|---|---|
| Validation | 0.7093 | 0.9306 | 0.5399 | 0.6639 | 0.9832 | 0.6622 |
| Test | **0.7116** | 0.9291 | 0.5434 | 0.6681 | 0.9836 | **0.6645** |

ECE 0.66 means the softmax-of-ridge scores are badly calibrated; flag this if the table is reused. The "audit tax" that MDPI reviewers discussed is 71.16% → 40.73% (G1). For the G2 numbers printed in conference Table 2 the base predictor reaches about 80.6% test accuracy (§2), so the gap there is about 0.81 → 0.40.

### 3.2 Transition reconstruction

| Run | Test MAE | Test RMSE | Mean corr. | Note |
|---|---|---|---|---|
| G1 r = 16 (`protocol_a_transition_metrics.json`) | 0.1295 | 0.1826 | 0.6828 | train 0.1292 / val 0.1299 |
| G1 r = 64 cache (`revision_transition_cache_meta.json`; top-64-variance raw coordinates, standardised, not SVD) | 0.1076 | 0.1573 | 0.7759 | used by the base predictor, CART / separate-and-conquer, MDLP/EF/EW discretizers, CBM/TCAV, local-XAI agreement, operator ablation, rule stability, control knobs and the Fig. 4 sweep |
| **G2 5-seed r = 64** (`revision_v1/awa2/awa2_protocol_a_summary.csv`) | **0.1029 ± 0.0005** | 0.1484 ± 0.0007 | 0.8070 | = conference Table 1 |
| G2 SVD-rank sensitivity (seed 42): r = 16 / 32 / 64 / 128 | 0.1295 / 0.1150 / 0.1031 / 0.0942 | 0.1826 / 0.1638 / 0.1487 / 0.1378 | 0.6828 / 0.7556 / 0.8060 / 0.8374 | explained variance 0.295 / 0.407 / 0.530 / 0.655 |

SVD-rank sensitivity, rulebook side (cov / covered acc / covered fid / rules): r16 0.9037 / 0.3913 / 0.3875 / 56; r32 0.9023 / 0.3695 / 0.3668 / 57; r64 0.8469 / 0.4054 / 0.4109 / 57; r128 0.7893 / 0.4801 / 0.4898 / 59. — NOT in conf.; MDPI: yes (main table + supplement Fig. 28b).

### 3.3 Rulebook properties (G1 seed 42 r = 16; `tables/rulebook_summary.csv`, `explainability_metrics.csv`, `protocol_a_rulebook.csv`) — NOT in conf. in this form

- 54 rules. Granules 14,130 (12,730 deterministic, 1,400 boundary).
- Test coverage 0.8640, abstention 0.1360, conflict 0.1354, exact-match rate 0.8681, fallback rate 0.1319.
- Covered accuracy 0.4073, covered macro-F1 0.3203, accuracy on all objects 0.3519.
- Covered fidelity 0.3829, all-object fidelity 0.3309.
- Mean/median antecedent length 4.037 / 4. Sparsity 0.7757. Mean support 1,237.1. Mean confidence 0.3912.
- **Rule sources:** 7 `strict_lower` (conf 0.846–0.896), 3 `boundary_high_confidence` (0.865–0.873), **44 `semantic_prototype` (conf 0.041–0.767, median 0.17)**. All 50 classes are covered.
- G2 5-seed (WEDD): rules 57 / 61 / 56 / 59 / 62 (59.0 ± 2.55). Coverage 0.8469 / 0.8257 / 0.8926 / 0.9027 / 0.7721. Fallback 0.093 / 0.111 / 0.104 / 0.104 / 0.075. Mean rule confidence 0.42–0.46.
- G2 object-level bootstrap (v3, 1,000 resamples, seed 42): coverage 0.8469 [0.8394, 0.8547], covered acc 0.4054 [0.3937, 0.4170], covered fid 0.4109 [0.3990, 0.4228], conflict 0.1378 [0.1309, 0.1449]. — MDPI: supplement (Fig. 26).

### 3.4 Symbolic baselines (G1, `artifacts/awa2/symbolic_baselines_metrics.csv`) — partly in conf. (Table 2, Fig. 2); MDPI: yes

| Method | Cov | Covered acc | Covered macro-F1 | **Covered fid** | All-obj acc | All-obj fid | Rules | Avg len | Conflict |
|---|---|---|---|---|---|---|---|---|---|
| Proposed rough-set rulebook | 0.8640 | 0.4073 | 0.3203 | 0.3829 | 0.3519 | 0.3309 | 54 | 4.04 | 0.1354 |
| CART (depth 7, min leaf 60) | 1.0000 | 0.4129 | 0.2830 | **0.4421** | 0.4129 | 0.4421 | 53 | 7.0 | 0 |
| Separate-and-conquer (RIPPER-like: min_sup 18, min_conf 0.60, max_len 4, ≤ 4 rules/class) | 0.2620 | 0.6334 | 0.5176 | **0.5915** | 0.1660 | 0.1550 | 197 | 3.26 | 0.2301 |

The conference Table 2 prints "-" for the two bold fidelity values. Not like-for-like: the "Proposed" row is the r = 16 SVD rulebook, while CART and separate-and-conquer are fit on the 64-coordinate cache semantics (better reconstruction, MAE 0.1076 vs 0.1295). CART "Rules" = leaves and "Avg len" 7.0 = tree depth; separate-and-conquer "Conflict" = share of objects matched by more than one rule (`run_symbolic_baselines.py`). A second tree baseline exists (`protocol_a_decision_tree_baseline.json`: depth 7, 40 leaves, test acc 0.3578, macro-F1 0.2185), as does a transition-only nearest-prototype classifier (`protocol_a_transition_only_nearest_prototype.json`: test acc 0.4355, macro-F1 0.3399).

### 3.5 Concept baselines: CBM / TCAV (G1; `cbm_metrics.json`, `tcav_*.{json,csv}`, `tables/cbm_tcav_baselines.csv`) — NOT in conf.; MDPI: yes

- **Frozen-feature CBM:** semantic MAE 0.1076, RMSE 0.1573, concept corr 0.7759, Top-1 **0.7232**, Top-5 0.9361, macro-F1 0.5508, AUROC 0.9852. It beats the base predictor (0.7116).
- **TCAV** at the released representation layer, 7 concepts (furry, swims, paws, hunter, water, quadrapedal, longneck): positive-sensitivity scores 0.42–0.58 (mean 0.4850), mean directional sensitivity about 0 (|·| < 0.007, mean −0.0021), overlap with transition-selected attributes 1.0. In effect this is uninformative. Limitation: representation layer only, because the raw activation stack was unavailable.

### 3.6 Local XAI agreement: LIME-style / SHAP-style (G1; `local_xai_agreement.json`, raw CSV of 1,000 rule-covered test objects, stratified over 50 classes) — NOT in conf.; MDPI: yes

| Method | Top-k antecedent agreement [95% CI] | Signed direction agreement [CI] | Spearman (rule salience) [CI] |
|---|---|---|---|
| LIME-style (local Gaussian perturbations in semantic space) | 0.2610 [0.2468, 0.2745] | 0.5907 [0.5770, 0.6046] | 0.0222 [0.0023, 0.0417] |
| SHAP-style (additive semantic contributions) | 0.3213 [0.3050, 0.3386] | 0.6071 [0.5914, 0.6233] | 0.1271 [0.1089, 0.1459] |

Mean rule length is 3.938. Both methods are re-implementations; the `lime` and `shap` packages are not used. This measures *agreement*, not superiority, so it cannot support the conference's "easily outperforms LIME and SHAP". The SHAP-style row matches the MDPI draft, but the draft's LIME row (0.2845 / 0.5412 / 0.1044) matches no repo artifact, and per `04_mdpi_overlap.md` the published Table 12 prints LIME 0.5412; the origin of the LIME numbers is (unverified).

### 3.7 Discretizer ablation

G1 seed 42 (`discretizer_ablation_metrics.csv`, `tables/wedd_ablation.csv`) — MDLP-like wins here, **but the comparison is confounded**: the WEDD row re-scores the r = 16 SVD rulebook, while the MDLP-like, equal-frequency and equal-width rows are induced on the 64-coordinate cache semantics (MAE 0.1076 vs 0.1295) with up to 5 rules per class and fallback 0.45 (`scripts/experiments/run_discretizer_ablation.py`). Use only the G2 table below for like-for-like claims.

| Method | Thresholds | Rules | Cov | Covered acc | Covered fid | Conflict |
|---|---|---|---|---|---|---|
| WEDD | 54 | 54 | 0.8640 | 0.4073 | 0.3829 | 0.1354 |
| MDLP-like entropy (α = 1) | 54 | 53 | 0.8714 | 0.4507 | 0.4556 | 0.1125 |
| Equal frequency | 36 | 52 | 0.7474 | 0.3110 | 0.3126 | 0.2506 |
| Equal width | 36 | 61 | 0.5830 | 0.4324 | 0.4750 | 0.4170 |

G2 5-seed r = 64 (`revision_v1/awa2/awa2_discretizer_comparison_summary.csv`) — WEDD is slightly ahead:

| Method | Cov | Covered fid | Covered acc | All acc | Conflict | Rules |
|---|---|---|---|---|---|---|
| Equal-frequency | 0.7212 ± 0.0784 | 0.3087 | 0.2999 | 0.2161 | 0.2773 | 50.6 |
| Equal-width | 0.6401 ± 0.0534 | 0.4535 | 0.4532 | 0.2883 | 0.3599 | 66.8 |
| MDLP-like entropy | 0.8334 ± 0.0417 | 0.3975 | 0.3912 | 0.3261 | 0.1482 | 56.0 |
| WEDD | 0.8480 ± 0.0530 | 0.4048 | 0.3973 | 0.3373 | 0.1375 | 59.0 |

Paired WEDD − MDLP differences (n = 5): coverage +0.0146 (standardized effect 0.19), covered acc +0.0061 (0.35), covered fid +0.0073 (0.37), conflict −0.0107 (−0.14). These effects are **modest and come with no significance test**. The MDPI reviewer (comment 1.1) made the team describe WEDD as "density-aware, stability-oriented" and drop any "superior" claim. — NOT in conf.; MDPI: yes (main table + supplement Fig. 27a–e).

### 3.8 WEDD component ablation (G1, `protocol_a_wedd_rule_ablation.csv`, figure `fig10`) — NOT in conf.; **not in MDPI draft either**

Test metrics:

| Variant | Cov | Covered acc | Conflict | Rules | Avg len |
|---|---|---|---|---|---|
| WEDD | 0.8640 | 0.4073 | 0.1354 | 54 | 4.04 |
| Entropy-only | 0.9567 | 0.3817 | 0.0419 | 52 | 4.13 |
| Density-only | 1.0 | 0.0974 | 0 | 0 (all fallback) | — |
| WEDD without reducts | 0.8640 | 0.4073 | 0.1354 | 54 | 7.06 |
| "True-B semantic upper bound" | 0.5775 | 0.8098 | 0.4225 | 50 | 4.0 |

How these rows were made (`run_all_experiments.py`): the "without reducts" row is **not a separate run**; it copies the WEDD metrics and reports the pre-reduction antecedent length (7.06), so "identical decisions" is assumed, not measured. The "True-B" row is not a rough-set rulebook on true attributes: it is one class-mode rule per class over only the first four selected attributes (stripes, hooves, swims, paws), WEDD-discretized on the class-level true semantics with min bin 40, with confidence set to 1.0 by hand (`true_B_rule_upper_bound`). Its conflict 0.4225 comes from classes that share those four states. Takeaways that survive: reducts shorten antecedents from 7.06 to 4.04 conditions (−43%); density alone yields no rules (all fallback). "Perfect semantics give only 58% coverage" is **not** supported, because the template uses 4 of 18 attributes. **This is an unused asset**, but the AI4I "rules on true concepts" baseline (decision 16) must run the full `induce_rules` pipeline instead of reusing this helper.

### 3.9 Transition-operator ablation (G1 64-coord cache, `transition_operator_ablation.csv`) — NOT in conf.; MDPI: yes (main)

| Operator | MAE | RMSE | Corr | Prototype acc | Rule cov | Covered rule acc | Runtime (s) |
|---|---|---|---|---|---|---|---|
| Linear ridge | 0.1076 | 0.1573 | 0.7759 | 0.6252 | 0.8718 | 0.2226 | ≈0 (logged 0.0; MDPI table 0.0451) |
| RBF kernel ridge (Nyström, γ = 0.5, 64 comps) | 0.1958 | 0.2583 | 0.1176 | 0.0190 | 1.0 | 0.0027 | 2.857 |
| 2-layer MLP (32 hidden, max_iter = 25) | 0.1685 | 0.2355 | 0.4497 | 0.2494 | 0.8390 | 0.1091 | 0.691 |

Caveat: the nonlinear baselines are barely tuned (fixed γ, 25 iterations), so a reviewer could call them strawmen. The MDPI table prints "± 0.0000" standard deviations "across 5 seeds", which suggests single-run values formatted as 5-seed; do not copy it.

### 3.10 Protocol B: official xlsa17 zero-shot split as semantic-transfer validation — NOT in conf.; MDPI: yes (main)

- **G1 seed 42, r = 32** (`protocol_b_summary.json`):
  - unseen MAE 0.1863, RMSE 0.2605;
  - prototype unseen acc 0.4644 object-weighted / **0.4843 class-averaged**, macro-F1 0.3655; seen prototype acc 0.3898;
  - symbolic-template unseen acc 0.3378 object-weighted / 0.3993 class-averaged, macro-F1 0.3010, mean Hamming 0.4946.
- **G2 5-seed, r = 64** (`revision_v1/awa2/awa2_protocol_b_seedwise.csv`): unseen MAE 0.1888, prototype unseen acc **0.4402 ± 0.0122** (MDPI abstract: "44.02% ± 1.22%"), macro-F1 ≈ 0.381, symbolic template 0.2348 ± 0.0170.
- **Per class** (G1 prototype / symbolic): sheep 0.591 / 0.146; dolphin 0.107 / 0.206; **bat 0.000 / 0.366**; seal 0.275 / 0.233; blue whale 0.920 / 0.885; rat 0.797 / 0.613; horse 0.829 / 0.577; walrus 0.367 / 0.102; **giraffe 0.018 / 0.070**; bobcat 0.940 / 0.795. The G2 bat diagnostic has prototype 0.0078 and symbolic 0.0548, interpreted as "semantic-transfer rupture".
- **SOTA context** (`tables/sota_quantitative_comparison.csv`, published AwA2 PS class-averaged accuracy from Xian et al. 2019): DAP 46.1, IAP 35.9, CONSE 44.5, CMT 37.9, SSE 61.0, LATEM 55.8, ALE 62.5, DEVISE 59.7, SJE 61.9, ESZSL 58.6, SYNC 46.6, SAE 54.1, GFZSL 63.8; SEMTRA prototype 48.43, symbolic 39.93. MDPI frames this as context, not a leaderboard (reviewer 1.7, 2.4).

### 3.11 Rule stability under semantic noise (G1, `rule_stability_noise.csv`; noise ε ~ N(0, σ²ŝ_j²), clipped to [0, 1]) — NOT in conf.; MDPI: yes (appendix + Gaussian perturbation equation)

| σ | Rule consistency | Decision consistency | Coverage | Δcov | Abstention | Conflict |
|---|---|---|---|---|---|---|
| 0 | 1.0000 | 1.0000 | 0.8796 | 0 | 0.1204 | 0.1180 |
| 0.01 | 0.9745 | 0.9663 | 0.8792 | −0.0004 | 0.1208 | 0.1183 |
| 0.025 | 0.9326 | 0.9176 | 0.8808 | +0.0012 | 0.1192 | 0.1168 |
| 0.05 | 0.8667 | 0.8401 | 0.8816 | +0.0020 | 0.1184 | 0.1160 |
| 0.10 | 0.7307 | 0.7112 | 0.8940 | +0.0145 | 0.1060 | 0.1026 |

Base: 6,566 non-abstained objects. This is the real-data robustness evidence that the CPS framing needs, and the conference paper relied only on synthetic data. Caveat (`run_rule_stability.py`): the noise is added to the 64-coordinate cache semantics, and the r = 16 rulebook and thresholds are re-applied there (fallback 0.50); hence the σ = 0 coverage 0.8796 instead of 0.8640.

### 3.12 Confidence-threshold sweeps (two versions; they disagree)

- **G1** `coverage_abstention_tradeoff.csv` (τ 0–0.95; this is conference Fig. 4 and archived fig15): rules 54 → 8 (τ = 0.85) → 0 (τ ≥ 0.90); coverage 0.8796 → 0.9953 (τ = 0.20) → ≈0.997 → 0; covered acc 0.221 → 0.391; covered fid 0.213 → 0.381.
- **G2** `revision_v1/sensitivity/awa2_confidence_threshold_frontier.csv` (seed 42, τ 0.50–0.95): coverage stays at 0.837–0.868, covered acc 0.367–0.412, covered fid 0.348–0.410, rules 56–60. It is flat and never collapses. MDPI dev-draft supplement Fig. 28c.
- Why they disagree: they turn different knobs. G1 filters an existing rulebook by rule confidence at inference time, on the cache semantics (see 01 §9, Fig. 4). G2 re-runs `run_protocol_a_once(..., min_confidence=τ)`, i.e. τ is the purity/confidence threshold for rule *induction*, and the prototype rules always restore one rule per class, so coverage cannot collapse.

### 3.13 q (selected-attribute count) sensitivity (G2 seed 42; the MDPI caption wrongly says "means … across all 5 seeds") — NOT in conf.; MDPI: yes

| q | Cov | Covered fid | Covered acc | Conflict | Rules | Thresholds |
|---|---|---|---|---|---|---|
| 8 | 0.7999 | 0.3435 | 0.3422 | 0.1711 | 59 | 24 |
| 12 | 0.8251 | 0.4002 | 0.3889 | 0.1522 | 60 | 36 |
| 18 (default) | 0.8469 | 0.4109 | 0.4054 | 0.1378 | 57 | 54 |
| 24 | 0.8354 | 0.4343 | 0.4266 | 0.1365 | 54 | 72 |
| **32** | **0.8719** | **0.5522** | **0.5380** | 0.1027 | 50 | 96 |

**q = 32 beats the default on every audit metric.** A remake could use it, provided it is labelled as a sensitivity result and not re-tuned on test data.

### 3.14 Control-knob sensitivity (G1, `tables/control_knob_sensitivity.csv`) — NOT in conf.; MDPI: yes (appendix)

| Knob | Value | Rules | Cov | Covered fid | Covered acc |
|---|---|---|---|---|---|
| λ_s | 0.25 | 50 | 0.7687 | 0.4796 | 0.4414 |
| λ_s | 0.50 | 52 | 0.8764 | 0.4057 | 0.3983 |
| λ_s | 0.75 | 57 | 0.7847 | 0.3856 | 0.3935 |
| λ_H | 0.25 | 58 | 0.7136 | 0.3514 | 0.3535 |
| λ_H | 0.65 | 52 | 0.8764 | 0.4057 | 0.3983 |
| λ_H | **0.90** | 53 | **0.8977** | **0.4349** | **0.4205** |

**λ_H = 0.9 beats the default 0.65**, and λ_H → 1 (pure entropy) behaves like MDLP. The MDPI draft prints the λ = 0.5/0.65 rows as 54 / 0.8640 / 0.3829 / 0.4073 (the G1 rulebook), which does not match this CSV's 52 / 0.8764 / 0.4057 / 0.3983. The CSV's default row differs from the G1 rulebook because the sweep (`generate_reviewer_revision_artifacts.py`) runs on the 64-coordinate cache semantics.

### 3.15 Cross-domain: SUN and Derm7pt (G2) — NOT in conf.; MDPI: yes (main cross-domain table; supplement details)

| Dataset / scope | Objects | Attrs | MAE | Cov | Covered fid | Covered acc | Other |
|---|---|---|---|---|---|---|---|
| AwA2 Protocol A | 7,465 | 85 | 0.1029 | 0.8480 | 0.4048 | 0.3973 | — |
| AwA2 Protocol B | 7,913 | 85 | 0.1888 | — | — | 0.4402 | transfer metric only |
| **SUN** seen-test audit | 2,580 (unseen 1,440) | 102 | 0.0683 (unseen) | **0.0760** | 0.0918 | 0.0714 | abstention 0.9240, **conflict 0.9236**, 580 rules, 7,248 granules; prototype unseen acc 0.2465 (72 classes) |
| **Derm7pt** (v1, official test split) | 395 | 7 | 0.2433 | 0.9241 | 0.5288 | 0.4219 | **fallback 0.4709**, conflict 0.0051, 7 rules, 279 granules |
| Derm7pt v3 (ResNet-50 features) | 395 | 7 | 0.2359 | 0.9899 | 0.7417 | 0.5729 | conflict 0, fallback 0.1418, 10 rules |

- SUN discretizers (seed 42): MDLP cov 0.0601 / acc 0.0903 / fid 0.1355; equal-frequency 0.0012; equal-width 0.0341.
- Derm7pt q-sensitivity: q = 3 → cov 0.9848 / acc 0.4524 / fid 0.5835; q = 5 → 0.9671 / 0.5131 / 0.7147; q = 7 → 0.9241 / 0.4219 / 0.5288.
- **SUN is a portability failure** (92% conflict), and the MDPI draft says so. Derm7pt nearly halves its decisions through fallback.

### 3.16 Synthetic benchmark (G1, all 6 σ levels, 5 seeds each; `artifacts/synthetic/synthetic_summary_by_noise.csv`) — conference shows σ = 0, 0.1, 0.2 only

| σ | MAE | Thr. err | Rule Jaccard (sd) | Macro-F1 (sd) | Coverage | Abstention | Avg len (orig) |
|---|---|---|---|---|---|---|---|
| 0.00 | 4.0e-7 | 0.0135 | 0.700 (0.114) | 0.8788 (0.0101) | 0.9706 | 0.0294 | 2.84 (8.16) |
| 0.02 | 0.0043 | 0.0172 | 0.763 (0.064) | 0.8810 (0.0111) | 0.9631 | 0.0369 | 2.81 (7.11) |
| 0.05 | 0.0107 | 0.0149 | **0.638** (0.137) | 0.8595 (0.0238) | 0.9775 | 0.0225 | 3.11 (8.05) |
| 0.10 | 0.0211 | 0.0178 | 0.763 (0.064) | 0.8810 (0.0150) | 0.9620 | 0.0380 | 2.80 (6.85) |
| 0.15 | 0.0313 | 0.0165 | 0.747 (0.041) | 0.8626 (0.0077) | 0.9579 | 0.0421 | 2.87 (7.05) |
| 0.20 | 0.0410 | 0.0166 | 0.743 (0.099) | 0.8381 (0.0124) | 0.9515 | 0.0485 | 2.88 (5.92) |

Means across levels: Macro-F1 0.8668, Jaccard 0.7258, threshold error 0.0161, coverage 0.9638. The CSV also has 95% CI half-widths. Note that the σ = 0.05 Jaccard dip (0.638) is hidden by showing only 3 levels. MDPI: yes (main, with CI bands, Fig. 22).

### 3.17 Other diagnostics in `tables/` and `artifacts/`

- `complete_semantic_attribute_diagnostics.csv`: all 85 attributes (val/test MAE, salience, score). MDPI appendix.
  - Salience extremes: highest paws 0.0451, vegetation 0.0440, grazer 0.0418, meat 0.0412; lowest flys 0.0051, red 0.0066, tusks 0.0093.
  - Test-MAE extremes: worst inactive 0.2384, fast 0.1998, vegetation 0.1914; best tunnels 0.0326, flys 0.0361, plankton 0.0427.
- `example_rules.csv` (R0001–R0008), `representative_rule_traces.csv` (the conference Table 5). The MDPI walkthrough uses zebra object 36914 with R0004.
- `results_interpretation_matrix.csv`, `enhanced_baseline_synthesis.csv`, `main_quantitative_results.csv`: G1 summary tables.
- `protocol_a_wedd_thresholds.csv`: 54 thresholds, 3 per selected attribute, each with entropy, density and objective provenance.
- `protocol_a_threshold_stability.csv`: **empty** (bootstrap repeats 0), so there is no threshold-stability evidence.
- LaTeX-only tables: `table_related_work.tex` (method-family comparison matrix covering LIME, SHAP, TCAV, CBM, trees, RIPPER, rough sets, transition matrices and SEMTRA, a ready-made related-work table) and `table_abbreviations_variables.tex`.

## 4. Presence matrix: conference vs. repo vs. MDPI

| Result / experiment | In conference? | In repo | Likely in MDPI MAKE? (evidence) |
|---|---|---|---|
| Transition 5-seed (MAE 0.1029) | Yes (Table 1) | G2 | Yes: draft abstract and Table; v1 claim audit |
| Rulebook + CART + separate-and-conquer | Yes (Table 2, Fig. 2), fidelity of baselines omitted | G1 + G2 | Yes: reviewer matrix #13–14; draft Table rulebook_summary; fig19 is "Figure 3" in `revision_report.md` |
| Transition salience / attribute error (Fig. 3) | Yes | G1 | Yes (+ fig24 scatter) |
| Confidence-threshold sweep (Fig. 4) | Yes | G1 (fig15) + G2 frontier | Yes (fig15 main; frontier in supplement) |
| Example rules / traces | Yes (Tables 4–5) | G1 | Yes (main / appendix) |
| Synthetic σ ∈ {0, 0.1, 0.2} | Yes (Table 3) | G1, 6 levels | Yes (6 levels + CI bands + GT rule table) |
| Base predictor metrics (Top-1 0.7116) | **No** | G1 | Yes (appendix; reviewer #8–9) |
| Hyperparameters / ResNet-101 / SVD r | **No** (Fig. 1 only) | G1 | Yes (appendix; reviewer #7, #17) |
| Formal metric definitions (coverage, fidelity, conflict) | **No** | code + MDPI eqs | Yes (eqs. for Fid_covered, Acc_covered, Cov, Abs, CR; reviewer 1.8) |
| CBM baseline | **No** | G1 | Yes (reviewer #11) |
| TCAV baseline | **No** | G1 | Yes (reviewer #12) |
| LIME-/SHAP-style agreement | **No** | G1 | Yes (reviewer #5–6) |
| Discretizer ablation (WEDD vs MDLP / EF / EW), paired stats | **No** | G1 + G2 | Yes (main Table 5 per 04; dev-draft supplement figs 27a–e; reviewer 1.1/1.9) |
| WEDD component ablation (entropy-only, density-only, no reducts, true-B bound) | **No** | G1 | **No** (not found in draft) |
| Transition-operator ablation (kernel ridge, MLP) | **No** | G1 | Yes (main; hardware note) |
| Official xlsa17 Protocol B + per-class + bat diagnostic + SOTA context | **No** | G1 + G2 | Yes (main; reviewer 1.7, 1.12, 1.14, 2.4) |
| Rule stability under Gaussian noise (real data) | **No** | G1 | Yes (appendix; reviewer #25) |
| q sensitivity / SVD-rank sensitivity | **No** | G2 | Yes (main Tables 6–7 per 04; dev-draft supplement figs 28a–b; reviewer 1.5–1.6) |
| Control-knob λ_s / λ_H sensitivity | **No** | G1 | Yes (appendix; `revision_report.md` item 2) |
| Complete 85-attribute table | **No** | G1 | Yes (appendix; item 6) |
| SUN cross-domain | **No** | G2 (git history only) | Yes (main Table 13 per 04; dev-draft supplement uses fig31a and fig32b only) |
| Derm7pt cross-domain (incl. ResNet-50 v3) | **No** | G2 (git history only) | Main Table 13 prints the v1 row (MAE 0.2433, Cov 0.9241); the v3 ResNet-50 row is (unverified) as published; dev-draft supplement uses fig33a only |
| Runtime per phase | **No** | G2 | Dev-draft supplement fig28d; published (unverified); reviewer 1.10 |
| Object-level bootstrap CIs | **No** | G2 v3 | Yes (dev-draft supplement figs 26a–c; published S1 Figure S1 per 04) |
| ETM-vs-SEMTRA comparison table | **No** | MDPI draft | Yes (appendix; reviewer 1.3) |
| Use-case figure (local surrogate vs global rulebook) | **No** | figs_archived fig05_use-case | Yes (main; reviewer 1.11) |
| Revision-process figs 25 and 34 (pipeline, artifact hashes, QC gates) | **No** | figs_archived | Unlikely (audit meta-figures; not referenced in the draft) |
| Dashboard / quality-matrix / funnel figs 17, 18, 20, 21, 23 | **No** | figs_archived | Unlikely (from the 42-page May build; not in the June draft) |

## 5. Figure archive (`manuscript/figs_archived/`, 61 PDFs + 2 PNGs + v4 manifest = 65 files)

The "MDPI draft" column below follows the `\includegraphics` calls in `origin/dev:manuscript/main.tex` and `supply.tex`. The published article (per `04_mdpi_overlap.md`) has Figs 1–6 in the main text, consistent with the main-text column.

| Files | Content | Data source | Conf. | MDPI draft |
|---|---|---|---|---|
| fig01_semtra (pdf/png) | framework diagram (differs from the conference Fig. 1; `origin/dev` has a newer 3.68 MB version, commit d190136, 2026-06-27) | — | — | main Fig. 1 in the dev draft; which version MAKE printed is (unverified) |
| fig02 matrix alignment, fig03 class distribution, fig04 SVD variance | implementation diagnostics | protocol_a_* | — | — |
| fig05_transition_salience | top-15 salience | attribute_errors_and_salience | **Fig. 3a** (MD5 identical) | main |
| fig05_use-case (pdf/png) | local vs global conceptual | — | — | main |
| fig06_attribute_error | top-20 test MAE | same | **Fig. 3b** (identical) | main |
| fig07 WEDD threshold example, fig08 granules, fig09 rule support–confidence | | | — | fig07, fig09 main |
| fig10 WEDD ablation, fig11 Protocol B per-class, fig12 synthetic degradation, fig13 threshold recovery | | | — | fig13 main |
| fig14 traces (figure version), fig15 coverage–abstention, fig16 rule stability | | | **fig15 = Fig. 4** | fig15 main |
| fig17 dashboard, fig18 SOTA context, fig19 baseline trade-off, fig20 quality matrix, fig21 funnel, fig22 synthetic CI bands, fig23 Protocol B errors, fig24 salience–error scatter | enhanced set | | **fig19 = Fig. 2** | fig19, fig22, fig24 main |
| fig25a–d … fig34a–d (36 subfigure PDFs; manifest `fig25_34_revision_v4_subfigure_manifest.{md,csv}` has 36 rows) | revision v4: pipeline/QC (25, 34), object-level bootstrap (26), discretizers (27), q / SVD / confidence / runtime (28), Protocol B (29), synthetic (30), cross-domain (31), SUN (32), Derm7pt (33) | `outputs/revision_v1–v3` (git history only) | — | dev-draft supplement uses 26a–c, 27a–e, 28a–d, 29a–c, 31a, 32b, 33a (18 panels); 25, 30, 34 and the other 31–33 panels are unused |

`audit/` also holds contact sheets (`nature_figure_contact_sheet*.png`, `enhanced_render_contact_sheet.png`) and `fig16_rule_stability_noise_preview.png`.

## 6. How figures and tables are regenerated

**From checked-in G1 artifacts** (no raw data needed):
- `python scripts/generators/generate_nature_figures.py --root . [--formats pdf svg png] [--dpi 600]` produces figs 01–24. Each figure's sources and font profile are logged. Width profiles are 89 mm (single column) or 183 mm (double).
- `python scripts/generators/generate_enhanced_results.py --root .` produces the enhanced tables (main_quantitative_results, sota, enhanced_baseline_synthesis, placement map, interpretation matrix) and figs 17–24. `docs/reproducibility.md` calls the legacy path `scripts/generate_enhanced_results.py`.
- `python scripts/generators/generate_revision_tables.py` writes the `tables/*.tex` files from artifacts.
- `python scripts/generators/generate_reviewer_revision_artifacts.py --root .` writes the reviewer-targeted artifacts (control knobs, complete attributes, …).
- `scripts/generators/fix_table_layout.py` rewrites long TeX tables in an MDPI-friendly wrapped layout, and hard-codes some tables such as the synthetic GT rules. Note that **no script generates the "Numeric bounds" column** of the example-rules table (see §8).

**From G2 outputs:** `python scripts/generators/generate_revision_v4_figures.py` produces figs 25–34. It reads `outputs/revision_v1–v3/...`, which **does not exist in the working tree**, so first check out `origin/dev:outputs/` (for example into a worktree).

**Full re-run from raw data:**
- `python run_experiments.py --awa2_zip data/raw/awa2.zip --xlsa17_zip data/raw/xlsa17.zip --out . --seed 42`. This calls `scripts/runners/run_revision_experiments.py`, which runs train_base_predictor, local_xai, cbm_tcav, symbolic, discretizer, transition_operator, rule_stability and official_xlsa, then the table and figure generators (`--local_sample_size 1000`).
- The 5-seed, SUN, Derm7pt and v2/v3 bundles come from `scripts/runners/run_revision_v1.py`, `_v2.py` and `_v3.py`, orchestrated by `scripts/runners/semtra_revision.ps1`. It creates `.venv`, and installs torch/torchvision through `setup-vision`, falling back to `.venv-vision` with `py -3.12`.
- Experiment-script defaults point to `/mnt/data/awa2.zip` (Linux sandbox origin), so always pass paths.

**Style module `scripts/core/figure_style.py`:**
- "Nature-style" rcParams: sans-serif (Arial / Helvetica / DejaVu Sans), base 7.6 pt, ticks and legend 6.8 pt, axes linewidth 0.6, top/right spines off, no grid, `pdf.fonttype` = 42 (editable text), white backgrounds.
- Okabe–Ito palette: blue #0072B2, sky #56B4E9, teal #009E73, orange #E69F00, vermillion #D55E00, purple #CC79A7, yellow #F0E442.
- Helpers: `nature_size` (89 × 60 mm default), `add_panel_label`, `annotate_bars`, `contrast_text_color`, `clean_label(max_len = 28)`.
- `save_nature_figure()` **forces PDF only** and writes into `manuscript/figs_archived/` whatever path it is given. It also strips axis titles and multiplies all text by 1.10.
- The truncated labels in conference Fig. 2 ("separate-and-…", "CART decision…") come from `clean_label(..., 14)` in `fig19_tradeoff()`; raise the limit to fix them.

Duplicate script copies sit at the top level of `scripts/` (and an older set in `scripts/legacy/`). At the top level, `paper1_core.py`, `revision_common.py` and `fix_table_layout.py` match their `core/` or `generators/` copies, but `figure_style.py`, `generate_nature_figures.py`, `generate_revision_figures.py`, `generate_revision_tables.py`, `generate_enhanced_results.py`, `generate_from_artifacts.py` and `generate_reviewer_revision_artifacts.py` **differ**; `scripts/run_all_experiments.py` also differs from `scripts/legacy/run_all_experiments.py`. Use `scripts/core/` and `scripts/generators/`. The G1 AwA2 pipeline itself (`run_awa2_protocol_a`, `select_attributes`, `evaluate_rule_pipeline`, synthetic benchmark) exists only in `run_all_experiments.py` (legacy and top-level copies); it has no `core/` counterpart.

## 7. Environment needs

- `requirements.txt`: numpy ≥ 1.24, pandas ≥ 2.0, matplotlib ≥ 3.7, scikit-learn ≥ 1.3, scipy ≥ 1.10, pyarrow ≥ 14.0, h5py ≥ 3.10, Pillow ≥ 10.0. The README asks for Python ≥ 3.10. The G2 runs used Python 3.13.6 on Windows 11. The conference figures were made with Matplotlib 3.11.0.
- Extra for Derm7pt v3: torch and torchvision (ResNet-50 IMAGENET1K_V2; CUDA optional, the v3 run used CPU).
- For the MDPI build: pdflatex + bibtex8 (TeX Live). For the conference: LibreOffice and the CEUR ODT template.
- **On this PC right now:** the global Python 3.13 has **none** of the required packages (numpy, pandas, matplotlib, sklearn, scipy, pyarrow, h5py, PIL, torch all missing), and the repo has no `.venv`. Set up with `uv venv` and `uv pip install -r requirements.txt` before regenerating anything.
- Raw data are absent (§1), so only artifact-based regeneration (G1) works offline.

## 8. Number mismatches: conference manuscript vs. artifacts

| # | Conference item | Conference value | Repo value / source | Verdict |
|---|---|---|---|---|
| M1 | Table 1, abstract, §6: test MAE / corr | 0.1029 ± 0.0005 / 0.8070 | G2 v1 5-seed r = 64: 0.102875 / 0.80696 ✓. **Checked-in** `artifacts/awa2/protocol_a_*` and `tables/transition_metrics.csv`: **0.1295 / 0.6828** (r = 16) | Matches only git-history outputs; the working-tree artifacts disagree |
| M2 | Table 2 "ours" | 59.00 ± 2.55 rules; cov 0.8480; acc 0.3973; fid 0.4048; len 4.0397; abst 0.1520; conflict 0.1375 | G2 ✓ exactly. G1 (`tables/rulebook_summary.csv`): 54; 0.8640; 0.4073; 0.3829; 4.0370; 0.1360; 0.1354 | Same mismatch as M1 |
| M3 | Table 2 baselines | CART 53 / 1.0 / 0.4129 / 7.0; S&C 197 / 0.2620 / 0.6334 / 3.2589 / 0.7380 / 0.2301 | ✓ G1 seed 42 (`symbolic_baselines_metrics.csv`), fit on the 64-coordinate cache semantics; S&C uses the r = 16 WEDD thresholds on those semantics | Single run from a **different pipeline** than "ours"; not like-for-like; CART "7.0" is depth |
| M4 | Table 2 baseline fidelity | "-" / "-" | CART **0.4421**, S&C **0.5915** | Omitted, and both exceed SEMTRA |
| M5 | Fig. 2 SEMTRA point | (≈0.864, ≈0.383) | G1 0.8640 / 0.3829 | Contradicts Table 2 (0.8480 / 0.4048) |
| M6 | Fig. 3b scale | mean test MAE implied 0.1295 | G1 r = 16 | Contradicts Table 1 (0.1029) |
| M7 | Fig. 4 at τ = 0 | cov 0.8796, acc 0.221, fid 0.213 | G1 `coverage_abstention_tradeoff.csv`; the same rulebook's protocol metrics are 0.8640 / 0.4073 / 0.3829, and the G2 frontier is flat at 0.84–0.87 | Sweep re-applies the r = 16 rulebook to the 64-coordinate cache semantics (`generate_revision_figures.py`); see §3.12 |
| M8 | Table 4 numeric bounds | cut-points 0.15 / 0.40 / 0.70 (e.g., "hooves≥0.70", "paws≥0.40") | WEDD thresholds of the same seed-42 rulebook (`protocol_a_wedd_thresholds.csv`): paws 0.218 / 0.4021 / 0.5929; hunter 0.1907 / 0.3871 / 0.5077; small 0.1268 / 0.3682 / 0.566; yellow 0.0555 / 0.2288 / 0.3306; stripes 0.0711 / 0.1718 / 0.4101; hooves 0.1187 / 0.3044 / 0.4772; jungle 0.0559 / 0.2378 / 0.5486; water 0.0715 / 0.2826 / 0.5042; hands 0.0143 / 0.1285 / 0.3814 | **Not traceable.** No generator emits it; it was copied verbatim from the MDPI draft table, so the published MAKE paper probably carries it too |
| M9 | Table 4 rules | R0001 / R0003 / R0004, supports 115 / 132 / 434, conf 0.896 / 0.871 / 0.866 | ✓ G1 `protocol_a_rulebook.csv` (seed 42, r = 16) | Rules come from G1, while Table 2 "ours" comes from G2 |
| M10 | §4.3 "plankton … lowest" salience | — | flys 0.0051 lowest overall; skimmer 0.0161 < plankton 0.0164 among the selected | False |
| M11 | §4.1 "84.80% … deterministic logical explanation" | 0.8480 | includes fallback predictions (G2 per-seed fallback rate 0.075–0.111, of which 0.062–0.095 of all test objects are covered fallback predictions; G1 0.132) | Overclaim |
| M12 | Table 3 | 3 rows | ✓ `synthetic_summary_by_noise.csv` rows σ = 0, 0.1, 0.2 (the 0.9515 coverage prints as 0.952) | OK, but 3 of 6 levels |
| M13 | Table 5 | traces 5083 / 24024 / 16781 | ✓ `tables/representative_rule_traces.csv` (G1) | OK; rules with conf 0.208 / 0.195 are `semantic_prototype` |
| M14 | §5 S(y_k) | — | slide: Σ conf·supp; MDPI draft: Σ Conf·Supp·w_r; code: Σ conf·log1p(supp) / len | Three different definitions; pick the code's |

Errors inside the MDPI draft that the new paper should **not** copy (it cites MAKE; it does not reprint these numbers):
- the q-sensitivity table caption says "means evaluated across all 5 random seeds" but holds seed-42 values (the SVD-rank table makes no seed claim and is also seed 42);
- the transition-operator table attaches standard deviations "across 5 seeds" (e.g., MAE 0.1076 ± 0.0012, rule coverage 0.8718 ± 0.0075, RBF runtime 2.8573 ± 0.1250, plus several "± 0.0000") to values that exist in the repo only as a single seed-42 run; the non-zero SDs have no source (unverified);
- the hyperparameter table gives the soft-matching Hamming threshold τ_H = 0.25 (code: 0.45 or 0.50) and calls the auxiliary compression "PCA to 64 components retaining 95% variance" (code: top-64-variance raw coordinates; SVD r = 64 retains 0.53);
- the LIME row of the local-XAI table (0.2845 / 0.5412 / 0.1044) matches no repo artifact (repo: 0.2610 / 0.5907 / 0.0222);
- the synthetic ground-truth table lists 3 rules; the generator has 4 (class 4: b7 high ∧ b9 low), which is why `04_mdpi_overlap.md` reads it as a "3-class" benchmark;
- the CBM table gives SEMTRA MAE 0.1076 (64-coordinate cache), not 0.1029;
- the text says "CR of 13.54%" (G1) while the table says 0.1375 (G2);
- the control-knob rows were changed to G1 values that do not match the CSV;
- the example-rule bounds are untraceable (M8).

## 9. Formalism available in the MDPI draft (`origin/dev:manuscript/main.tex`)

The draft has 25 numbered equation environments (`\begin{equation}`); the conference paper has 2. Per decision 24 the new paper paraphrases and cites them (MAKE as source) rather than copying; where they disagree with the code (no centring in `fit_transition`, support score Σ conf·log1p(supp)/len, Hamming threshold), describe the code:
- rule form; decision system $S=(U,C,d,V,f)$;
- centring $A_c=A-\mathbf 1\bar a^\top$; compression $Z=A_cV_r$; ridge $W^\ast=\arg\min\|ZW-B\|_F^2+\alpha\|W\|_F^2$; $T=V_rW^\ast$, $\hat B=(A-\mathbf 1\bar a^\top)T+\mathbf 1 b_0^\top$;
- $\mathrm{MAE}_Q$; selection score $\lambda_s\tilde\eta_j+(1-\lambda_s)(1-\widetilde{e_j/(\sigma_j+\epsilon)})$;
- conditional entropy $H_j(\theta)$ and normalised $H(d\mid G)$ with $\log_{N_c}$; KDE $p_j(\theta)=\frac{1}{nh_j}\sum K(\cdot)$; WEDD $J_j$;
- $IND(P)$; lower approximation; reduct objective $\min|R|$ s.t. Conf ≥ τ, Supp ≥ s_min; discernibility cell;
- $S(y_k)$; Hamming $d_H$; Fid_covered, Acc_covered, Fid_all, Cov, Abs = 1 − Cov, CR;
- Gaussian perturbation $\epsilon_{ij}\sim\mathcal N(0,\sigma^2\hat s_j^2)$.

There are also two algorithms ("Neural-to-Semantic Transition and WEDD Discretization", "Rough-Set Granulation, Reduct Solver, and Inference").

MDPI draft section skeleton:
1. Introduction
2. Related works: local post-hoc; concept-based and ante-hoc; rough sets; semantic transfer
3. Materials and methods: Phases 1, 2.1, 2.2, 2.3; metrics; protocol
4. Results: reconstruction; rulebook and fidelity; Protocol B; cross-domain; local and concept baselines; synthetic
5. Discussion: audit tax; honest silence; linear transition as a defensive choice; limitations
6. Conclusions
Appendices: ETM vs SEMTRA; hyperparameters; traces and stability.

## 10. Implications for the AIT&AIS companion paper (overlap)

The agreed route (`06_decisions.md` decisions 1, 10, 12, 14, 24) is not a remake of the ICyberPhyS paper: it is a companion paper on AI4I 2020 that cites MAKE as the method source and reuses no AwA2 number. The points below explain why, and which repo material is only background.

- Every number in the conference paper is also in the MDPI draft, and all five conference table captions are identical or near-identical to MDPI captions (Table 3's is word-for-word; Tables 1, 2, 4 and 5 differ only by a hyphen, "5" vs "five", or a merged footnote). Rules R0001/R0003/R0004 and the three traces are shared too. The MDPI reviewers' comments (`origin/dev:manuscript/my_revision.md`) are the same ones the conference text is still exposed to:
  - WEDD vs MDLP; numeric consistency; ETM relation; cross-domain;
  - audit tax 71.16% → 40.73%; q choice; ZSL framing; fidelity definitions;
  - runtime; Fig. 5 role; bat failure; rough-set + DNN literature; CIs;
  - rulebook-quality claim; trade-off justification.
- **Material in the repo that is NOT in the MDPI draft** (AwA2 background only; under decision 14 none of it enters the new paper as a result, but it shows which questions MAKE left open):
  - WEDD component ablation; its "true-B" row is a 4-attribute class-mode template, not a true upper bound (§3.8);
  - reduct length reduction (7.06 → 4.04; the no-reduct row was not re-run, §3.8);
  - q = 32 and λ_H = 0.9 configurations, which beat the defaults;
  - rule-source composition (7 lower / 3 boundary / 44 prototype rules);
  - fallback share of coverage;
  - full 6-level synthetic curve, including the σ = 0.05 Jaccard dip;
  - SUN failure analysis as a negative result.
- The repo has no CPS or sensor data. The chosen new experiment is UCI AI4I 2020 (decision 12); the CSV must be downloaded and a project venv created, each after the author's go-ahead (`07_submission_plan.md` §3). The code to reuse is mapped in the next section.

## 11. Reuse map for the AI4I experiment

Target pipeline (`07_submission_plan.md` §2): standardised AI4I inputs → MLP (2 × 64, ReLU) → embedding A = last hidden layer → concept space B̂ through the transition → WEDD → rough-set granules, reducts and rules → conflict-aware inference with abstention; baselines: CART on the same predicted concepts, rules on the true concepts, MLP max-probability for triage. Line numbers refer to the working tree on `main`.

**Vendor, do not import.** `scripts/core/paper1_core.py` (871 lines) is self-contained: it imports only the standard library, numpy, pandas and scikit-learn, so it can be copied unchanged into the new repo (decision 22) with the source commit recorded. The useful helpers in `scripts/runners/run_revision_v1.py` should be copied as functions, because importing that module pulls in Pillow and `scipy.io` at import time.

### Stage 0. Data container and splits

- Reuse: `run_revision_v1.py` `SemanticDataset` dataclass (fields `name, A, y, B_class, B_obj, class_names, attr_names, meta`, l. 65) and `protocol_a_split(y, seed) -> (train, val, test)` (l. 290): stratified 60/20/20 via two `train_test_split` calls with `random_state=seed`. Seeds `SEED_DEFAULT = [42, 43, 44, 45, 46]`.
- Template for a non-AwA2 dataset: `load_derm7pt(root, out)` (l. 883) and `run_derm7pt(root, out, seed, smoke)` (l. 939). They use `B_class=None`, per-object concepts, categorical concepts encoded as ordinal codes / (k − 1), all concepts kept (no selection), `n_components=min(32, d − 1)`, WEDD `min_support=5`, rules `min_confidence=0.60, min_support=5`, fallback 0.50.
- AwA2-specific, replace: `paper1_core.load_awa2`, `maybe_extract_awa2`, `run_revision_v1.load_awa2_parquet`, `revision_common.load_protocol_a_indices`, `make_transition_cache`, `load_cache` (hard-wired to `artifacts/awa2/`, `/mnt/data/awa2.zip` defaults). Write `load_ai4i(csv) -> SemanticDataset` with `B_class=None` and `B_obj` = the per-row concept matrix (decision 15: ΔT, speed, torque, power, tool wear, strain, product type, plus raw air temp, raw process temp and one noise sensor). AwA2 semantics are class-level (`B_obj = B_class[y]`), AI4I concepts are per-row, so `nearest_prototype_predict` and every `B_class_scaled` step (Protocol B, transition-only prototype accuracy) have no AI4I counterpart. Drop RNF and multi-mode rows before splitting (decision 13); check that every failure mode keeps enough rows per split for stratification.

### Stage 1. MLP and embedding (new code)

- Nothing in the repo trains a classifier MLP or extracts embeddings. The only MLP is `sklearn.neural_network.MLPRegressor(hidden_layer_sizes=(32,), max_iter=25, early_stopping=True)` used as a transition operator in `scripts/experiments/run_transition_operator_ablation.py`; not reusable here.
- Suggested, staying inside `requirements.txt`: `sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(64, 64), activation="relu", early_stopping=True, random_state=seed)`; compute the embedding from `coefs_` and `intercepts_` (H1 = relu(X·W0 + b0), A = relu(H1·W1 + b1)). `MLPClassifier` has no `class_weight`, so oversample the minority modes in the training split only (07 §2). No torch is needed.
- The MLP's own test predictions become the base predictor for fidelity (`base_pred_eval` in Stage 5/6), replacing the AwA2 proxy `run_revision_v1.classifier_predictions(X_train, y_train, X_eval)` (RidgeClassifier α = 1 on SVD coordinates, l. 332) and `scripts/experiments/train_base_predictor.py`.

### Stage 2. Transition to concept space

- Reuse: `paper1_core.fit_transition(A_train, A_val, A_test, B_train, B_val, B_test, n_components=256, ridge_grid=(0.01, 0.1, 1.0, 10.0, 100.0), seed=42) -> TransitionResult` (l. 170). `TransitionResult` fields: `scaler_A, svd, scaler_B, ridge, alpha, n_components, explained_variance, X_train/val/test, Y_train/val/test, Yhat_train/val/test, salience, metrics`.
- How T is computed (no pseudo-inverse and no centred PCA anywhere in the pipeline):
  1. `StandardScaler(with_mean=False)` on A (scaling only, no centring);
  2. `TruncatedSVD(n_components=r, n_iter=2, random_state=seed)`; the basis is fit on a random subset of at most 5,000 training rows and then applied to all rows; `r = min(n_components, k − 1, n_train − 1)`;
  3. targets: `MinMaxScaler` fit on the training concepts, clipped to [0, 1];
  4. `Ridge(alpha=α, fit_intercept=True)` on the SVD scores for each α of `ridge_grid`; the α with the lowest mean validation MAE wins; predictions are clipped to [0, 1].
  The code never forms T explicitly. For reporting: T = diag(1/`scaler_A.scale_`) · `svd.components_`ᵀ · `ridge.coef_`ᵀ (k × l, MinMax target units), b₀ = `ridge.intercept_`, B̂ = clip(A·T + b₀, 0, 1); physical units via B̂·`scaler_B.data_range_` + `scaler_B.data_min_`. The Beamer slide's T = (AᵀA + αI)⁻¹AᵀB omits the SVD, the scaling and the intercept.
- MAKE settings to reproduce ("same estimator and settings as the MAKE code", 07): `n_components=64`, the default grid, seed per run. AwA2 picked α = 0.01 with validation MAE flat to 2·10⁻⁶ across the grid; the synthetic benchmark used `n_components=20` and grid (0.001 … 10). With a 64-unit embedding, `n_components=64` silently becomes **63**.
- Returned metrics: train/val/test MAE, RMSE and mean per-concept Pearson r (constant columns skipped). Per-concept R² and MAE (07 metrics) are not computed: add them from `Y_test` and `Yhat_test` (R² is unaffected by the MinMax scaling).
- `salience` = L2 norm of each concept's ridge weights in SVD-score space (`np.linalg.norm(ridge.coef_.T, axis=0)`), not a column norm of T.
- To generalise: the 5,000-row subset and `n_iter=2` were sized for 2048-d × 22k AwA2 rows (harmless at 64-d, but state them). The SVD is uncentred, so with non-negative ReLU activations the first component mostly tracks the mean. Clipping to the training min/max flattens test concept values beyond the training range (relevant for power and strain tails).

### Stage 3. Concept selection

- Reuse if needed: `run_revision_v1.select_attributes(result, attr_names, q) -> (indices, DataFrame)` (l. 297), score = 0.5·minmax(salience) + 0.5·(1 − minmax(val MAE)).
- Do **not** reuse G1 `run_all_experiments.py::select_attributes` (it forces `FORCED_AWA2_ATTRS = [10, 20, 36, 22, 24, 58, 73, 45]`). With 10 concepts, keep all of them (as `run_derm7pt` does), so that ignoring the distractors is decided by the rules, which is the question of decision 15.

### Stage 4. WEDD discretisation

- Reuse: `paper1_core.fit_discretizers(Yhat_train, y_train, attr_indices, alpha, max_depth=2, min_support=30) -> (thresholds: Dict[int, List[float]], provenance_df, objective_examples)` (l. 417), built on `wedd_thresholds(x, y, alpha=0.65, max_depth=2, min_support=30, min_gain=0.002, max_candidates=96)` (l. 378), `threshold_objective(x, y, alpha=0.65, min_support=30, max_candidates=96)` (l. 302), `candidate_thresholds(x, max_candidates=96)` (l. 274) and `local_density(values_sorted, candidates)` (l. 288). States: `quantize(Yhat, attr_indices, thresholds) -> int16 array` (l. 434).
- MAKE settings: α (λ_H) = 0.65, `max_depth=2` (≤ 3 cuts, 4 states), `min_support = max(10, s_min) = 18` in the G2 runs (30 in G1, 5 for Derm7pt). Ready ablations: `alpha=1.0` = "MDLP-like entropy"; `run_revision_v1.simple_thresholds(Y, attrs, kind)` (l. 318) = equal-frequency / equal-width with 2 cuts.
- To generalise:
  - thresholds are in MinMax [0, 1] units of B̂; convert them with `scaler_B` to compare with the documented physics (decision 13: ΔT < 8.6 K and speed < 1380 rpm; power < 3500 or > 9000 W; strain > 11000/12000/13000 minNm for L/M/H; wear 200–240 min);
  - the entropy is supervised on the failure-mode labels; minority modes have few training rows, and `min_support` (18–30) can block a split that isolates a small mode such as TWF; choose it on validation and freeze it;
  - for more than 97 unique values, candidates span only the 1st–99th percentiles, so a cut in an outer 1% tail cannot be found unless the quantile range is widened; whether any AI4I cut falls there is (unverified);
  - product type (L/M/H) needs an ordinal code (as in `load_derm7pt`); a type-dependent OSF limit cannot be expressed by one strain cut, so expect several rules or a strain × type interaction;
  - ties: the recursion sends x = t left, while `quantize` (`np.digitize(..., right=False)`) sends it right; this matters only for discrete-valued concepts.

### Stage 5. Granulation, reducts and rule induction

- Reuse: `paper1_core.induce_rules(Z, y, attr_names, class_names, min_confidence=0.90, min_support=20, max_rules_per_class=5, attr_scores=None, allow_prototypes=True, reduce=True) -> (rules_df, granules_df)` (l. 540), with `granule_table(Z, y)` (l. 446), `rule_stats(antecedent, consequent, Z, y)` (l. 471), `reduce_antecedent(antecedent, consequent, Z, y, min_confidence, min_support, attr_priority=None)` (l. 493; greedy removal, lowest priority first) and `class_mode_signatures(Z, y, labels)` (l. 526). MAKE-style wrapper: `run_revision_v1.evaluate_rulebook(Yhat_train, Yhat_eval, y_train, y_eval, attrs, attr_names, class_names, thresholds, base_pred_eval, min_confidence, min_support, fallback_max_distance, max_rules_per_class=4) -> (metrics, rules, pred)` (l. 338); it sets `attr_scores` = number of cuts + std of states and adds fidelity to the base predictor.
- MAKE settings: τ = 0.84, `s_min = max(8, min(18, int(0.002·n_train)))` = 18 on AwA2, `max_rules_per_class=4`; Derm7pt τ = 0.60, s_min = 5; synthetic τ = 0.86, s_min = 25.
- Rules table columns: `rule_id, antecedent` (dict concept position → state), `antecedent_text, consequent, consequent_name, support, confidence, coverage, conflict_count, antecedent_length, original_antecedent_length, source` (`strict_lower` / `boundary_high_confidence` / `semantic_prototype`). Rule ids are reassigned after sorting by confidence.
- To generalise:
  - `allow_prototypes=True` adds one rule per class even at near-zero confidence (AwA2 median 0.17); for a physics-recovery claim report the `source` mix, or run `allow_prototypes=False` as an ablation;
  - rule-recovery and threshold-recovery scores must be new code: `rule_recovery_jaccard(rules_df)` (l. 857) and `threshold_recovery_error(thresholds)` (l. 844) hard-code the synthetic ground truth;
  - the "rules on true concepts" baseline (decision 16) = the same `fit_discretizers` + `induce_rules` run on `tr.Y_train` / `tr.Y_test`; do not reuse `true_B_rule_upper_bound` (a 4-attribute class-mode template with confidence forced to 1.0, §3.8);
  - eligible granules are capped at 500 (largest first); with about 10 concepts this is unlikely to bind, but log it.

### Stage 6. Conflict-aware inference with abstention, metrics, triage

- Reuse: `paper1_core.infer_rules(Z, rules_df, class_prototypes_Z=None, fallback_max_distance=0.45, conflict_margin=0.05) -> DataFrame` (l. 685) with columns `row_index, prediction` (−1 = abstain), `mode` (`exact` / `fallback`), `abstained, conflict, activated_rules` (first 10 ids), `n_activated`. Vote = conf·log1p(support)/length; conflict if the top-two margin < 0.05·max(1, top) → abstain; no rule fired → nearest class-mode signature (`class_mode_signatures(Z_train, y_train, labels)`) if the mean Hamming distance ≤ the threshold, else abstain. Metrics: `prediction_metrics(y_true, pred_df, labels=None)` (l. 751) → `coverage, abstention_rate, conflict_rate, fallback_rate, exact_rate, accuracy_non_abstain, macro_f1_non_abstain, accuracy_all_with_abstention_wrong`; `evaluate_rulebook` adds `covered_fidelity_to_base, all_object_fidelity_to_base`. Object-level export and CIs: `run_revision_v3.py` `enhanced_prediction_df(*, dataset, seed, scope, pred, source_indices, true_labels, class_names, base_pred, extra=None)` (l. 154), `enhanced_metrics(df)` (l. 200), `bootstrap_ci_metric(df, metric, rng, n_boot)` (l. 220, percentile 95% CI); `revision_common.bootstrap_ci(values, rng=None, n_boot=500, alpha=0.05)`.
- MAKE settings: fallback threshold 0.45 (G2 AwA2) or 0.50 (G1, SUN, Derm7pt), conflict margin 0.05; the MAKE text states τ_H = 0.25 (per `04_mdpi_overlap.md`), which no script uses. Choose one on validation, freeze it in `PROTOCOL.md`, and report it.
- To generalise: triage AUROC/AURC (07 metrics) needs a continuous score, but `infer_rules` returns only flags and `n_activated`; patch it to also return the winning vote, the top-two margin and the fallback distance. Report conflict abstentions and far-fallback abstentions separately (they are merged in `abstained`), and per-mode recall (not built in). The MLP max-probability baseline comes from `MLPClassifier.predict_proba`.

### Stage 7. CART baseline

- Reuse the recipe in `scripts/experiments/run_symbolic_baselines.py`: `DecisionTreeClassifier(max_depth=7, min_samples_leaf=60, random_state=seed)` fit on `Yhat_train[:, selected]`, scored by `eval_pred(name, y, pred, base_pred, coverage_mask, rule_count, avg_len, conflict_rate=0.0)`. Its `main()` is AwA2-bound (cache, `artifacts/awa2/*.csv`).
- To generalise: tune `max_depth` on validation (decision 16); `min_samples_leaf=60` exceeds the training size of some failure modes, so lower or tune it; report the leaf count and the mean decision-path length (`tree.decision_path`), not the depth that the AwA2 code reported as "conditions per rule". Fit on the same predicted concepts; a true-concept CART is a cheap symmetric extra. Separate-and-conquer (`induce_ripper_like`) is not needed (decision 16).

### Stage 8. Aggregation and figures

- Reuse: `run_revision_v1.summarize_seedwise(df, group_cols, metrics)` (mean and SD with ddof = 1, l. 463), `write_csv(path, rows)`, `paper1_core.write_json`, `ensure_dir`.
- Figures: `scripts/core/figure_style.py` `apply_nature_style()`, `nature_size(width_mm=89, height_mm=60)`, `PALETTE` (Okabe–Ito), `style_axis`, `add_panel_label`, `clean_label(value, max_len=28)`, `save_nature_figure(fig, path, formats=("pdf", "svg"), dpi=600)`. Patch `save_nature_figure` before use: it overrides `formats` to PDF only, always writes into `<this repo>/manuscript/figs_archived/`, blanks axis titles and scales all text by 1.10; F2–F4 need PDF + SVG in the new repo.

### Hard-coded AwA2 constants to strip

`np.arange(50)` class labels (`train_base_predictor.py`, `run_transition_operator_ablation.py`, `run_rule_stability.py`, `generate_revision_figures.py`), `FORCED_AWA2_ATTRS`, `artifacts/awa2/...` paths, `/mnt/data/*.zip` defaults, the `load_selected_attributes` fallback `[10, 20, 36, 22, 24, 58, 73, 45]` (`revision_common.py`), `make_rule_examples`, and all class-prototype (`B_class`) steps.

### Packages (`requirements.txt`)

Needed: numpy ≥ 1.24, pandas ≥ 2.0, scikit-learn ≥ 1.3 (`Ridge`, `TruncatedSVD`, `StandardScaler`, `MinMaxScaler`, `MLPClassifier`, `DecisionTreeClassifier`, metrics), scipy ≥ 1.10 (a scikit-learn dependency), matplotlib ≥ 3.7 (figures). Not needed for AI4I: pyarrow ≥ 14.0 (parquet loaders only), h5py ≥ 3.10 (only listed in `package_versions()`), Pillow ≥ 10.0 (image features; imported at the top of `run_revision_v1.py`), torch/torchvision. The global Python 3.13 has none of these; create the venv with `uv venv` and `uv pip install -r requirements.txt` after the author's go-ahead (§7).

## Revision log (2026-10-22)

Audit against `artifacts/`, `tables/`, `scripts/`, `audit/`, `docs/`, `data/README.md`, `README.md`, `revision_report.md`, the `manuscript/figs_archived/` files and `origin/dev` (`outputs/revision_v1–v3`, `manuscript/main.tex`, `supply.tex`, `main.pdf`). Unchanged after checking: §0 audit-trail numbers, §1 dataset sizes and splits, §3.1–3.3, §3.5, §3.9–3.10, §3.13, §3.15–3.17 numbers, §4 rows not listed below, §6 commands and style-module facts, §7, §8 M1–M2, M4–M6, M8–M10, M12–M14.

| # | Where | Old → new | Evidence |
|---|---|---|---|
| 1 | Header | "remake" framing → companion AI4I paper; deadline (before 28 Oct 2026) and online talk by Pavlo Radiuk alone added | `06_decisions.md` (decisions 1, 12, 14, 27, 31); author statement 2026-10-22 |
| 2 | §0 G2 | "249 files; bbd4007 removed only the LaTeX build and submission-bundle files" → 248 files in `revision_v1–v3` (+ README = 249); bbd4007 deleted 51 LaTeX build files from the v1/v2 `latex/` folders; v3 `latex/` and `submission_bundle/` remain | `git ls-tree -r origin/dev`; `git show --stat bbd4007` |
| 3 | §0 G3 | "≈14k tokens" → ≈14k words (118 KB); added `main.pdf` (31 pages, 2026-06-20) and the v0.3 CEUR ODT on dev | `wc -w`; `pdfinfo`; `git log` |
| 4 | §0 caveat | "other agents' online check should confirm" → 04 confirms the main tables; published S1 = Tables S1–S3 + Fig. S1, so dev supplement figures marked (unverified) | `04_mdpi_overlap.md` §1 |
| 5 | §1 AwA2 A | "xlsa17-released features" → G1 `AwA2-features.parquet` (awa2.zip), G2 xlsa17 res101 parquet; semantics are class-level | `paper1_core.load_awa2`; `run_revision_v1.load_awa2_parquet` |
| 6 | §1 raw data | Derm7pt listed as an expected archive → only awa2.zip and xlsa17.zip per `data/README.md`; G2 extracted-file paths added | `data/README.md`; `run_revision_v1.py` loaders |
| 7 | §2 base predictor | One predictor → two (G1 cache, 0.7116; G2 SVD-64, 0.802–0.810) | `train_base_predictor.py`; `classifier_predictions`; v3 enhanced CSVs |
| 8 | §2 bridge | "TruncatedSVD then Ridge" → full recipe (uncentred scaling, ≤ 5,000-row SVD fit, n_iter 2, MinMax + clip); α grid flat | `paper1_core.py` l. 170–253; ridge grid in `protocol_a_transition_metrics.json` |
| 9 | §2 WEDD | "min_bin_size = 30" → 30 (G1) / 18 (G2) / 5 (Derm7pt); candidate rule and tie convention added | `evaluate_rule_pipeline`; `run_protocol_a_once`; `run_derm7pt` |
| 10 | §2 selection | λ_s formula with e_j/σ_j applied to the listed set → G1 = 8 forced + salience/(MAE + 0.02); G2 = 0.5/0.5 score without σ_j; G2 seed-42 set added | `select_attributes` in both files; `awa2_selected_attributes_seed42.csv` (dev) |
| 11 | §2 rules | "boundary rules (confidence ≥ max(0.55, τ − 0.20))" → boundary rules need purity ≥ τ; the 0.64 floor applies to prototype rules, which fall back to the top-4 states at any confidence | `paper1_core.induce_rules` l. 565–627 |
| 12 | §2 inference | "Hamming ≤ 0.45", "margin < 0.05·top" → 0.50 or 0.45 by script; margin < 0.05·max(1, top); MDPI τ_H = 0.25 is unused | `infer_rules` l. 723; grep of `fallback_max_distance`; `main.tex` l. 1167 |
| 13 | §3.1 | Audit tax 71.16% → 40.73% only → also ≈0.81 → 0.40 for G2 | v3 enhanced CSVs |
| 14 | §3.2 | Cache "used by CBM / operator ablation" → full list of users | `grep load_cache` |
| 15 | §3.4 | Added: baselines on cache semantics; CART rules = leaves, length = depth; S&C conflict definition | `run_symbolic_baselines.py` |
| 16 | §3.6 | Added: the MDPI LIME row matches no artifact (unverified) | `main.tex` l. 888; `local_xai_agreement.json` |
| 17 | §3.7 | "MDLP-like wins here" → confounded (WEDD on r = 16, others on cache semantics) | `run_discretizer_ablation.py` |
| 18 | §3.8 | "identical decisions", "true-semantics upper bound", "perfect semantics give only 58%" → no-reduct row not re-run; True-B is a 4-attribute class-mode template with confidence 1.0 | `run_all_experiments.py` l. 218–227, 475–505 |
| 19 | §3.11, §3.12, §3.14 | Added the cache-semantics caveat and why the two confidence sweeps differ (inference filter vs induction τ) | `run_rule_stability.py`; `generate_revision_figures.py`; `run_revision_v1.py` l. 590–592; `generate_reviewer_revision_artifacts.py` |
| 20 | §3.15 | Derm7pt v3 MAE "—" → 0.2359 (fallback 0.1418, 10 rules) | `derm7pt_rulebook_seedwise_v3.csv` (dev) |
| 21 | §4 | Supplement figure claims → the exact dev-draft panels; published status (unverified) where 04 lists only S1 Tables S1–S3 + Fig. S1; Derm7pt v3 row (unverified) | `supply.tex` `\includegraphics`; 04 §1 |
| 22 | §5 | "37 subfigures" → 36; "26–29, 31–33 in supplement" → the 18 panels actually used; newer dev fig01 noted | `ls`; manifest CSV (36 rows + header); `supply.tex` |
| 23 | §6 duplicates | Five differing copies, `legacy/` holding the core copies → seven differing top-level copies; `legacy/` holds a different, older set | `cmp` of each pair |
| 24 | §8 M3, M7, M11 | Baseline semantics, Fig. 4 cause and covered-fallback share made explicit | as rows 15 and 19; v3 CSVs |
| 25 | §8 MDPI errors | "q and SVD tables labelled 5-seed" → only the q caption claims 5 seeds; "± 0.0000" → mixed zero and non-zero SDs on single-run values; added τ_H, "PCA 95%", the LIME row and the 3-of-4 GT rules | `main.tex` l. 531–539, 650, 670, 888, 940–951, 1161, 1167 |
| 26 | §9 | "27 numbered equations" → 25; note to describe the code where it differs | `grep -c 'begin{equation}'` = 25 |
| 27 | §10 | "AITAIS remake" and "no CPS data, needs new runs" → companion paper per decisions 1, 10, 12, 14, 24; AI4I download after go-ahead | `06_decisions.md`, `07_submission_plan.md` |
| 28 | §11 (new) | Reuse map for the AI4I experiment added | `paper1_core.py`, `run_revision_v1.py`, `run_revision_v3.py`, `run_symbolic_baselines.py`, `figure_style.py`, `requirements.txt` |
