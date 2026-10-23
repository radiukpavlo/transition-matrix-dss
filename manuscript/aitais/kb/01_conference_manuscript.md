# 01 — Conference manuscript anatomy (ICyberPhyS-2026, submission ID 9)

Knowledge-base file for the AIT&AIS'2026 companion paper (new AI4I 2020 experiment that cites MAKE 8(7):181 as the method source; see `06_decisions.md` decisions 1, 12, 14). This file documents the old ICyberPhyS paper so that the new text avoids its defects and does not recycle it. Everything below comes from local files only. Where a number is checked against the repository, the source file is named.

> Context (author, 2026-10-22): the new manuscript must be submitted in CMT **before 28 October 2026** (target 26 Oct, hard limit 27 Oct); the AIT&AIS'2026 talk is **online, given by Pavlo Radiuk alone**, as agreed with the organising committee. See `07_submission_plan.md`.

## 0. Sources and which version is canonical

| File | Date (mtime) | Status |
|---|---|---|
| `manuscript/conference/submission/ICyberPhyS-2026_ID-9-Submission.pdf` | 2026-07-02 11:37 (LibreOffice 26.2.4.2, A4, **11 pages**) | **Canonical final.** Used for all quotes below. |
| `manuscript/conference/submission/ICyberPhyS-2026_ID-9-Submission.odt` | 2026-07-01 10:05 | Same text as the PDF; source of the math objects (StarMath) quoted in §7. |
| `manuscript/conference/presentation/ICyberPhyS-2026_ID-9-Submission.odt` | 2026-06-30 19:04 | **Earlier draft.** Different citation numbering and reference order. |
| `presentation/manuscript_items.txt`, `manuscript_summary.txt`, `manuscript_extracted.json`, `manuscript_converted/*.html` | 2026-07-01 19:14–19:17 | Extracted from the **earlier draft ODT** (the one in `presentation/`), so do not use their citation numbers or reference order. Body numbers and tables are the same as in the final. |

Differences between the earlier draft and the final (text only; numbers and tables are the same):
- Citation renumbering: Intro geometric-learning sentence ("deformations") [6]→[6, 7]; photovoltaic sentence [7]→[8]; fuzzy-logic sentence [8]→[9, 10]; Related Works [9]→[3, 11], [10]→[12], [11]→[13], VLG-CBM [13]→[14], CEM [14]→[15], post-hoc CBM sentence [15]→[5], Lie-group sentence [5]→[6], "AwA2 collection" [12]→[26, 27]; a "[12]" after "Concept-based methods address this issue…" was removed; "[26, 27]" in the gap paragraph was removed; Discussion [1, 3]→[3, 11], [8]→[9, 10], [6]→[6, 7].
- Reference list reordered to first-citation order (Musaelian, Tsybulskiy, Melnyk–Zimchenko, Kovalchuk, Bollaert, Xian, Lampert entries moved; no entry added or dropped).
- "Weighted Entropy-Density Discretization (WEDD)" shortened to "WEDD" in §3.2 and in the gap paragraph; "as shown in Equation (1):" became "as follows:".

Other conference-folder material:
- Beamer talk: `presentation/ICyberPhyS_SEMTRA_presentation/main.tex` (518 lines, KhNU theme) plus a compiled PDF. It repeats Tables 1–4 and adds two formulas that are **not in the paper**: $T=(A^\top A+\alpha I)^{-1}A^\top B$ and $S(y_k)=\sum_{r\in\mathcal{A}(x),\,y_r=y_k}\mathrm{conf}(r)\,\mathrm{supp}(r)$.
- `presentation/85_Pres_v0.1.zip`, `template_85_pres_v0_1/`, `tools/`, `agents.md`, logos (CEUR, KhNU, FIT, KIIS, USES, CS, ICyberPhyS).
- `prompts/`: six LLM prompt files, `85_Prompt_01_Refs-reorder`, `_02_Refine-outline`, `_03_Sections-intro-related`, `_04_Sections-abs-dis-conc`, `_05_Make-pres`, `_06_Make-script` (.docx). These matter for the GenAI declaration (§12).
- `template/CEUR-Template-1col-1.odt` (CEUR 1-column ODT template).
- `ICyberPhyS-2026_Email.pdf`: a Microsoft CMT notice titled "Important Notice Regarding Publication of the ICyberPhyS-2026 Proceedings", dated "6 [month name lost in text extraction] 2026, 15:19" (6 October 2026 per `06_decisions.md`; the PDF is a browser print made 2026-10-22). Its key sentence: "the CEUR-WS editorial team has decided not to proceed with the publication of the workshop proceedings". It adds that the decision "does not concern the scientific quality" of individual papers, and that "authors are completely free to submit their papers to other journals, conferences, workshops".
- `Claude outputs/` (repo root) holds `Presentation_Krak_3_updated_v2.pptx` and `_v3.pptx`. These are talk drafts and were not analysed.

## 1. Bibliographic identity

- **Title:** "Auditable Decision-Making in Intelligent Cyber-Physical Systems Using Semantic Transition and Rough Sets"
- **Venue footnote (verbatim):** "ICyberPhyS-2026: 3rd International Workshop on Intelligent & CyberPhysical Systems, July 2, 2026, Khmelnytskyi, Ukraine"
- Template: CEUR-WS 1-column (ODT), CC BY 4.0. CMT submission ID 9. Proceedings editors, from the CEUR agreement form: Tetiana Hovorushchenko, Oleh Savenko, Peter Popov, Sergii Lysenko.
- Status: presented on 2026-07-02 (per `06_decisions.md`; the only repo evidence is the CMT notice thanking authors for "preparing and presenting your work" and the Beamer slides compiled 2026-07-01; no programme or recording is stored). CEUR declined the whole volume, so the paper is **unpublished**.
- The paper does **not** cite the parallel MDPI SEMTRA manuscript or its preprint (Preprints.org 202606.0230.v1, DOI 10.20944/preprints202606.0230.v1, per `README.md`). The MDPI paper was not yet published at the time.

## 2. Authors, affiliations, contacts

As printed (superscripts taken from the ODT): **Pavlo Radiuk**^1,∗,†^, **Oleksander Barmak**^1,†^ and **Iurii Krak**^3,†^

| # | Affiliation (verbatim) |
|---|---|
| 1 | Khmelnytskyi National University, 11, Institutes str., Khmelnytskyi, 29016, Ukraine |
| 2 | Taras Shevchenko National University of Kyiv, 64/13, Volodymyrska str., Kyiv, 01601, Ukraine |
| 3 | Glushkov Cybernetics Institute, 40, Glushkov Ave., Kyiv, 03187, Ukraine |

- Footnotes: "⋆ Corresponding author." / "† These authors contributed equally." (all three authors carry †).
- Emails: radiukp@khmnu.edu.ua (P. Radiuk); barmako@khmnu.edu.ua (O. Barmak); iurii.krak@knu.ua (I. Krak)
- ORCIDs: 0000-0003-3609-112X (P. Radiuk); 0000-0003-0739-9678 (O. Barmak); 0000-0002-8043-0785 (I. Krak)
- **Defect:** affiliation 2 is listed but assigned to no author. The MDPI manuscript (`origin/dev:manuscript/main.tex`) gives Krak affiliations 2 and 3, which matches his knu.ua email. Fix to Krak^2,3^.

## 3. Abstract (verbatim, 181 words)

> Intelligent cyber-physical systems (CPS) increasingly rely on deep learning, but the opaque nature of these models introduces critical safety risks. Current local explainability methods fail to provide the verified, global decision logic required for reliable control systems, creating a significant barrier to safe deployment. In this paper, we propose the application of the SEMTRA (Global SEMantic TRAnsition) framework as a post-hoc layer for the quantitative auditing of control systems. The framework leverages Weighted Entropy-Density Discretization and rough set theory to extract physical semantic attributes, implementing an honest silence mechanism that explicitly identifies boundary conflicts and triggers failsafe transitions instead of making overconfident predictions. Experimental evaluations demonstrate a mean absolute error of 0.1029 for neural-to-semantic transitions, achieving a substantial logical coverage of 84.80% on test instances. Synthetic stress testing validates the robustness of the extracted rules against semantic noise, maintaining a Macro-F1 score of 0.838. By formalizing the concept of the audit tax, this approach provides a reliable, mathematically grounded tool for deploying auditable artificial intelligence, enabling engineers to inspect structural failures, ensure operational transparency, and guarantee safety in complex industrial environments.

## 4. Keywords (verbatim, 6)

"Explainable AI (XAI), cyber-physical systems, rough sets, model auditing, production rules, semantic transition"

Layout glitch: in the PDF the last word, "transition", is pushed out of the keyword box and appears to the left of "Abstract".

## 5. Outline, word counts, page estimate

Prose counts come from the final ODT and exclude tables, captions and footnotes. PDF counts are from `pdftotext` per section and include tables, captions and the first-page footnote block.

| Section | Prose words | PDF words | Pages |
|---|---:|---:|---|
| Title + authors + affiliations | ≈55 | — | p1 |
| Abstract | 181 | 182 | p1 |
| Keywords | 13 | 13 | p1 |
| 1. Introduction (incl. 3 numbered contributions) | 526 | 593 | p1–2 |
| 2. Related Works (4 paragraphs, no subsections) | 494 | 497 | p2–3 |
| 3. Methods (lead-in) | 37 | 39 | p3 |
| 3.1 Phase 1: Neural-to-Semantic Transition | 73 | 102 (+Fig. 1) | p3–4 |
| 3.2 Phase 2.1: Stable Discretization (WEDD) | 61 | 93 (Eq. 1) | p4 |
| 3.3 Phase 2.2: Knowledge Granulation and Rule Induction | 63 | 79 (Eq. 2) | p4 |
| 3.4 Conflict-Aware Inference and Auditing | 99 | 126 (+Fig. 2) | p4–5 |
| 4. Experimental Results (lead-in) | 42 | 45 | p5 |
| 4.1 Semantic-Space Reconstruction (Protocol A) and Rulebook Property Analysis | 210 | 323 (Tables 1–2) | p5–6 |
| 4.2 Robustness to Semantic Noise (Synthetic Benchmark) | 64 | 70 | p6 |
| 4.3 Visualization of Audit Results and Rule Interpretation | ≈285 | 528 (Tables 3–5, Figs 3–4) | p6–8 |
| 5. Discussion | 404 | 406 | p9 |
| 6. Conclusion | 184 | 186 | p9 |
| Declaration on Generative AI | 84 | 88 | p10 |
| References (27) | 859 | 891 | p10–11 |
| **Totals** | **Body §1–§6 ≈ 2,540; with abstract ≈ 2,725** (sum of the rows above) | **Whole PDF ≈ 4,300** (pdftotext: 4,291 raw, 4,300 with `-layout`; the per-section sum above is ≈ 4,315) | **11** |

**Page estimate (CEUR 1-column, A4):** the real PDF has **11 pages**. The body (title through Conclusion) runs over pp. 1–9, and the Declaration plus References take pp. 10–11. Pages that are all text hold about 500–565 words (p1 505, p2 525, p9 564). Floats take about 3 pages' worth of space: Fig. 1 on p4, Fig. 2 on p5, Figs 3a/3b on p7, Fig. 4 on p8, and five tables. Without references the paper would fill about 9.3 pages.

Page map: p1 title/abstract/intro; p2 intro + contributions + Related Works; p3 Related Works end + §3 + §3.1; p4 Fig. 1 + §3.2–3.4 (Eqs 1–2); p5 Fig. 2 + §4 + §4.1 + Table 1; p6 Table 2 + §4.2 + start of §4.3; p7 Tables 3–4 + Fig. 3(a,b); p8 Fig. 4 + Table 5 + findings paragraph; p9 §5 + §6; p10 Declaration + refs [1]–[12]; p11 refs [13]–[27].

## 6. Contributions (verbatim)

The Introduction ends with the goal and the objective, then lists the contributions:

> The goal of this study is to improve the interpretability, auditability, and safety of intelligent cyber-physical systems by establishing a mathematically transparent post-hoc framework that translates uninterpretable latent neural features into explicit, conflict-aware symbolic rulebooks.
>
> To achieve this goal, the explicit objective of this study is to develop and validate the SEMTRA (Global SEMantic TRAnsition) framework as a non-destructive auditing layer for existing neural controllers. The major contributions of this work are as follows:
> 1. We establish a linear transition-matrix formulation that maps compressed deep representations into physically interpretable semantic attributes without requiring the underlying controller to be retrained.
> 2. We implement a stable Weighted Entropy-Density Discretization (WEDD) module that balances entropy reduction with local data density to convert continuous signals into robust symbolic states.
> 3. We propose a rough-set rule-induction mechanism that forms a global rulebook featuring explicit management of structural failures, conflict regions, and algorithmic abstention.

Roadmap sentence: §2 related work, §3 architecture, §4 "empirical evaluation results on benchmark datasets and synthetic stress tests", §5 implications for CPS, §6 conclusion.

## 7. Equations

There are only **two numbered equations**, plus five inline math objects (StarMath in the ODT). LaTeX equivalents:

| ID | Where | As typeset (StarMath source) | LaTeX |
|---|---|---|---|
| (1) | §3.2 | `J_j(%theta) = %lambda_H {widetilde H}_j(%theta) + (1 - %lambda_H) {widetilde p}_j(%theta)` | `J_j(\theta)=\lambda_H\,\widetilde{H}_j(\theta)+(1-\lambda_H)\,\widetilde{p}_j(\theta)` |
| (2) | §3.3 | `r : oper ⋀ from {j in R_r} left [ s_j = v_j right ] Rightarrow d = y_r .` | `r:\ \bigwedge_{j\in R_r}\,[s_j=v_j]\;\Rightarrow\; d=y_r .` |
| inline | §3.1 | `A ∈ ℝ^m × k` | `A\in\mathbb{R}^{m\times k}`. **Typesetting bug:** the MathML superscript holds only *m*, so it renders as ℝ^m × k. |
| inline | §3.1 | `B ∈ ℝ^m × l` | `B\in\mathbb{R}^{m\times l}`. Same bug. |
| inline | §3.2 | `{widetilde H}_j(%theta)` | `\widetilde{H}_j(\theta)`, called "information entropy" |
| inline | §3.2 | `{widetilde p}_j(%theta)` | `\widetilde{p}_j(\theta)`, called "a proxy for local probability density, estimated through Kernel Density Estimation (KDE)" |
| inline | §3.4 | `S(y_k)` | `S(y_k)`, the "aggregate support score". **Never defined in the paper.** |

Symbols that appear in the text without a definition: the transition matrix $T$ (no formula; the text only says "linear ridge-regression operator"), discretized states $S$, rulebook $R$, noise level σ ∈ [0, 0.20], "minimal reducts", "Hamming distance" (soft matching). Nothing in the paper defines coverage, fidelity, accuracy, conflict rate or abstention.

Formula visible only inside Figure 1: "Linear ridge mapping (A − 1āᵀ)ᵀ + 1b₀ᵀ". This is a garbled version of the MDPI equation $\hat B=(A-\mathbf 1\bar a^\top)T+\mathbf 1 b_0^\top$.

The MDPI dev draft (`origin/dev:manuscript/main.tex`) has **25** numbered equation environments (centring, SVD, ridge, $T=V_rW^\ast$, MAE, selection score, conditional entropy, KDE, indiscernibility, lower approximation, reduct objective, discernibility, $S(y_k)$, Hamming, fidelity/accuracy/coverage/abstention/conflict, perturbation); the count in the published MAKE article is (unverified). See `02_project_inventory.md` §9. Note that none of these formulas matches the code exactly: the implemented transition is TruncatedSVD on *uncentred*, std-scaled features followed by ridge with an intercept, and the code's support score is Σ conf·log1p(supp)/len (see 02 §2 and the reuse map). Under decision 24 the new paper paraphrases and cites MAKE rather than importing its equations verbatim.

## 8. Tables (full content, as printed)

**Table 1.** "AwA2 Protocol A transition reconstruction metrics. Metrics are reported as mean ± standard deviation across five seeds"

| Split | MAE | RMSE | Mean semantic correlation |
|---|---|---|---|
| train | 0.1027 ± 0.0003 | 0.1482 ± 0.0004 | 0.8079 ± 0.0009 |
| validation | 0.1030 ± 0.0003 | 0.1486 ± 0.0005 | 0.8065 ± 0.0014 |
| test | 0.1029 ± 0.0005 | 0.1484 ± 0.0007 | 0.8070 ± 0.0018 |

**Table 2.** "General rulebook properties and symbolic-baseline comparison. Point estimates are reported alongside standard deviations evaluated over five random seeds for the proposed method"

| Metric | Value (ours) | CART baseline | Separate-and-conquer |
|---|---|---|---|
| Number of rules | 59.00 ± 2.55 | 53 | 197 |
| Test coverage | 0.8480 ± 0.0530 | 1.0000 | 0.2620 |
| Covered accuracy | 0.3973 ± 0.0109 | 0.4129 | 0.6334 |
| Covered fidelity to base | 0.4048 ± 0.0078 | - | - |
| Average conditions per rule | 4.0397 ± 0.0543 | 7.0000 | 3.2589 |
| Test abstention rate | 0.1520 ± 0.0530 | 0.0000 | 0.7380 |
| Test conflict rate | 0.1375 ± 0.0532 | 0.0000 | 0.2301 |

How the baseline cells were computed (`scripts/experiments/run_symbolic_baselines.py`): CART "Number of rules" 53 is the leaf count, and CART "Average conditions per rule" 7.0000 is the tree **depth** (`cart.get_depth()`), not the mean path length. Separate-and-conquer "conflict" is the share of objects matched by more than one rule. Both baselines were fit on the 64-coordinate variance-screened cache semantics (test MAE 0.1076), a third semantic space that is neither the "ours" column (G2, SVD r = 64) nor the seed-42 r = 16 rulebook.

**Table 3.** "Synthetic stress-test results averaged over random seeds"

| Noise (σ) | MAE | Threshold error | Rule Jaccard | Macro-F1 | Coverage |
|---|---|---|---|---|---|
| 0.000 | 0.000 | 0.014 | 0.700 | 0.879 | 0.971 |
| 0.100 | 0.021 | 0.018 | 0.763 | 0.881 | 0.962 |
| 0.200 | 0.041 | 0.017 | 0.743 | 0.838 | 0.952 |

**Table 4.** "Representative induced production rules from AwA2 Protocol A. Support refers to the number of instances covered in the training partition"

| Rule | Antecedent | Numeric bounds | Class | Support | Conf. |
|---|---|---|---|---|---|
| R0001 | paws=s2 AND hunter=s2 AND small=s0 AND yellow=s2 | paws≥ 0.40; hunter≥ 0.40; small<0.15; yellow≥ 0.40 | tiger | 115 | 0.896 |
| R0003 | stripes=s1 AND hooves=s3 AND paws=s0 AND hands=s0 AND small=s1 AND yellow=s1 | stripes∈[0.15,0.40]; hooves≥ 0.70; paws<0.15; hands<0.15; small∈[0.15,0.40]; yellow∈[0.15,0.40] | antelope | 132 | 0.871 |
| R0004 | hunter=s0 AND water=s0 AND small=s0 AND jungle=s2 AND yellow=s1 | hunter<0.15; water<0.15; small<0.15; jungle≥ 0.40; yellow∈[0.15,0.40] | zebra | 434 | 0.866 |

**Table 5.** "Representative rule inference traces with object ID, prediction, matched-rule evidence, and antecedent states"

| Case | Object | True | Pred. | Mode | Rule | Support | Conf. | Antecedent states |
|---|---|---|---|---|---|---|---|---|
| correct exact | 5083 | collie | collie | exact | R0027 | 1675 | 0.208 | stripes=s0; hooves=s0; swims=s1; paws=s3; longneck=s0; hunter=s1; ocean=s1; quadrapedal=s3 |
| abstention | 24024 | ox | abstain | exact | R0029 | 2820 | 0.195 | stripes=s0; hooves=s2; swims=s1; paws=s0; longneck=s1; hunter=s0; ocean=s1; quadrapedal=s2 |
| fallback error or boundary | 16781 | hamster | mole | fallback | - | - | - | stripes=s0; hooves=s1; swims=s1; paws=s2; longneck=s0; hunter=s0; ocean=s1; quadrapedal=s2 |
| *Case* | *Object* | *True* | *Pred.* | *Mode* | *Rule* | *Support* | *Conf.* | *Antecedent states* ← **duplicated header row printed at the bottom (layout defect)** |

Reading Table 5 correctly: the "Antecedent states" column lists the object's states on the first eight selected attributes (the eight hand-forced ones, see §15 W4), not the antecedent of the matched rule. For example R0027 is `stripes=s0 AND paws=s3 AND quadrapedal=s3 AND toughskin=s0` (collie, `semantic_prototype`), and R0029 is the **elephant** prototype rule `paws=s0 AND small=s0 AND furry=s1 AND toughskin=s2`; the ox object abstained because of a vote conflict (`artifacts/awa2/protocol_a_rulebook.csv`).

There are also two layout-only tables: the copyright block (§14) and a "(a) | (b)" table that holds the Fig. 3 panel labels.

## 9. Figures

| Fig. | Caption (verbatim) | File in `manuscript/conference/figures/` | Identical archived source | What it shows / issues |
|---|---|---|---|---|
| 1 | "Conceptual SEMTRA architecture: from the latent space of a neural network to a verified rulebook." | `fig1-semtra-architecture.pdf/.svg` (1.15 MB / 1.56 MB, 1320×737 pt; both wrap a single 5504×3072 JPEG at 300 ppi, with no vector text, so labels cannot be edited) | None. It differs from `figs_archived/fig01_semtra.pdf` (MD5 differs). | Shows four phases. **Phase 1:** real images (tiger, zebra, whale) → "ResNet-101 black-box extractor" → Matrix A → "SVD basis (V_r)" → "Compressed latent space Z" → "Linear ridge mapping (A − 1āᵀ)ᵀ + 1b₀ᵀ" → "Global transition matrix T" → B / B̂ with icons for paws, swims, stripes. **Phase 2.1:** "Semantic Attribute Selection and Stable Discretization": salience and MAE filter (q) → WEDD → discrete symbolic states (S). **Phase 2.2:** rough-set information granules → lower approximation (deterministic) / boundary region (conflict and ambiguity) → "Discernibility matrix and minimal reduct search" R*. **Phase 2.3:** "Conflict-Aware Inference and Evaluation", with the example rule "IF paws=s2 AND hunter=s2 AND yellow=s2 => tiger" and gauges for Coverage, Fidelity, Auditability, Abstention rate and Conflict rate. **Issues:** the text never mentions ResNet-101, SVD/Z, q-selection, the discernibility matrix or "Phase 2.3" (the text uses §3.4). The formula is garbled. "Matrix A" is labelled twice. The example rule is R0001 with `small=s0` dropped, so it is not a rule from the rulebook. |
| 2 | "Trade-off between rulebook coverage and fidelity. SEMTRA occupies a high-coverage region while explicitly reporting conflicts." | `fig2-coverage-fidelity.pdf/.svg` | `figs_archived/fig19_baseline_tradeoff_scatter.pdf` (**MD5 identical**) | Scatter of Rulebook Coverage (Cov) against Covered Fidelity (F_cov), with marker size = rule count. Data are seed-42 values from `artifacts/awa2/symbolic_baselines_metrics.csv`: separate-and-conquer (0.2620, 0.5915), "rough-set" (0.8640, 0.3829), CART (1.0000, 0.4421). The SEMTRA point is the r = 16 SVD rulebook, while CART and separate-and-conquer were fit on the 64-coordinate cache semantics, so the three points do not share one semantic space (§8 note under Table 2). **Issues:** the labels are truncated ("separate-and-…", "CART decision…"). **CART dominates SEMTRA on both axes**, which contradicts the caption's framing. The plotted SEMTRA point (0.864, 0.383) differs from Table 2 (0.848, 0.4048). The baseline fidelities shown here are printed as "-" in Table 2. |
| 3a | "Semantic attribute diagnostics: (a) transition salience by semantic attribute; (b) attribute-wise semantic reconstruction error on AwA2." | `fig3a-semantic-diagnostics.pdf/.svg` | `figs_archived/fig05_transition_salience.pdf` (MD5 identical) | Horizontal bars of the top 15 attributes by "Transition column norm" (axis 0–0.045). Order: paws, vegetation, grazer, meat, meatteeth, claws, hunter, fields, hooves, domestic, big, furry, lean, walks, stalker (paws = 0.0451). Data: `protocol_a_attribute_errors_and_salience.csv` (seed 42, SVD r = 16). **Plankton does not appear in the panel**, yet the text cites it as lowest. |
| 3b | (same caption) | `fig3b-semantic-diagnostics.pdf/.svg` | `figs_archived/fig06_attribute_error.pdf` (MD5 identical) | Top 20 attributes by test MAE (axis 0–0.25): inactive (0.2384), fast (0.1998), vegetation (0.1914), timid (0.1902), slow, black, tail, solitary, active, paws, domestic, white, group, grazer, agility, fierce, forest, pads, brown, big. Same seed-42 r = 16 run, whose **mean MAE is 0.1295, not the 0.1029 of Table 1**. Vegetation is both the 2nd-most salient and the 3rd-worst reconstructed attribute. |
| 4 | "Rulebook and threshold optimization. Coverage, abstention, covered accuracy, and covered fidelity as the minimum rule-confidence threshold varies." | `fig4-threshold-optimization.pdf/.svg` | `figs_archived/fig15_coverage_abstention_tradeoff.pdf` (MD5 identical) | Data: `artifacts/awa2/coverage_abstention_tradeoff.csv`, τ = 0.00–0.95 in steps of 0.05. Coverage goes 0.8796 (τ=0, 54 rules) → 0.9953 (τ=0.20, 27 rules) → plateau ≈0.997 → **0 at τ ≥ 0.90 (0 rules, abstention 1.0)**. Covered accuracy rises 0.2214 → max 0.3910 (τ=0.80); covered fidelity 0.2131 → 0.3815. **Issues:** coverage *rises* as the confidence floor rises, which is counter-intuitive and unexplained (fewer rules leave fewer conflicts and more Hamming fallbacks). At τ = 0 the accuracy and fidelity (0.221 / 0.213) do not match Table 2 or the seed-42 rulebook (0.4073 / 0.3829). Cause (`scripts/generators/generate_revision_figures.py`): the sweep applies the seed-42 r = 16 rulebook and its WEDD thresholds to the *64-coordinate cache semantics* (a different transition), recomputes class-mode prototypes there, and filters existing rules by confidence at inference time with Hamming fallback 0.50. The τ = 0 coverage 0.8796 is the same value as the σ = 0 row of the rule-stability study, which uses the same mismatched setup. The Discussion wrongly cites Fig. 4 as evidence that WEDD puts thresholds in sparse regions. |

In the ODT all figures are embedded as SVG with PNG fallbacks (the five SVGs in the ODT have the same byte sizes as the files in `figures/`). The figure files are dated 2026-06-26. The PDFs of Figs 2–4 were made with Matplotlib 3.11.0; the Fig. 1 PDF carries no producer metadata (raster image). `origin/dev` holds newer versions of `fig01_semtra.pdf` (3,683,970 B, commit d190136, 2026-06-27) and `fig19_baseline_tradeoff_scatter.pdf` (53,691 B, commit e96f97f) than the working tree.

## 10. Every numeric claim in the running text

✓ means the value was reproduced from repo data. "v1" means `outputs/revision_v1/awa2/awa2_protocol_a_summary.csv` (5 seeds, 42–46, SVD r = 64, q = 18). That file is **only in git history** (`origin/dev`), not in the working tree; see 02 §0.

| # | Location | Claim (quoted) | Source / check |
|---|---|---|---|
| 1 | Abstract, §6 | "mean absolute error of 0.1029" | ✓ v1 test_mae_mean 0.102875 |
| 2 | Abstract, §6 | "logical coverage of 84.80% on test instances" | ✓ v1 coverage_mean 0.848011. ⚠ This includes Hamming-fallback predictions: covered fallback predictions are 6.2–9.5% of test objects per seed (`origin/dev:outputs/revision_v3/awa2/awa2_rule_predictions_enhanced_seed4[2-6].csv`); the fallback rate including fallbacks that then abstained is 7.5–11.1%. So "deterministic logical explanation" (§4.1) overclaims. |
| 3 | Abstract, §4.2, §5, §6 | "Macro-F1 score of 0.838" (σ = 0.20) | ✓ `artifacts/synthetic/synthetic_summary_by_noise.csv` 0.838094 |
| 4 | §4 | "50 object classes described by 85 semantic attributes" | ✓ (37,322 images are not mentioned) |
| 5 | §4.1 | "five-run results" | ✓ seeds 42–46 (seeds not named in the paper) |
| 6 | §4.1 | "MAE … of 0.1029 ± 0.0005" | ✓ v1 sd 0.000532 |
| 7 | §4.1 | "The Pearson correlation … was 0.8070 ± 0.0018" | ✓ v1 per-seed values 0.8060/0.8050/0.8099/0.8072/0.8066 average to 0.80696. It is a *mean per-attribute* correlation, and Table 1 calls it "Mean semantic correlation". |
| 8 | §4.1 | "CART … provide 100% coverage" | ✓ seed-42 `symbolic_baselines_metrics.csv` |
| 9 | §4.1 | "Coverage: 84.80% ± 5.30%of test instances received a deterministic logical explanation" | ✓ numbers (sd 0.0530); typo "5.30%of"; overclaim (see #2). Per-seed range 0.7721 (seed 46) – 0.9027 (seed 45). |
| 10 | §4.1 | "The generated base contained only 59.00% ± 2.55% rules, with an average of only 4.04 conditions per rule" | ✓ 59.0 ± 2.5495 rules (57, 61, 56, 59, 62); **"%" is wrong**; 4.0397 conditions. |
| 11 | §4.1 | "Covered fidelity reached 40.48%" | ✓ v1 0.404834 |
| 12 | §4.2 | "σ ∈ [0,0.20]" | ✓, but the repo has 6 levels (0, 0.02, 0.05, 0.10, 0.15, 0.20) × 5 seeds and the paper shows 3. |
| 13 | §4.2 | "With zero noise, a Macro-F1 score of 0.879" | ✓ 0.878823 |
| 14 | §4.2 | "decreased only to 0.838, while coverage remained at 95.2%" | ✓ 0.838094; coverage 0.9515 |
| 15 | §4.3 | zebra rule R0004 bounds ("low hunter and water…") | Rule ✓ (seed-42 rulebook, support 434, conf 0.8664). The numeric bounds are **not** traceable (§15, W5). |
| 16 | §4.3 | "'paws' and 'vegetation' have the highest transition salience, whereas 'plankton' has the lowest" | Paws 0.0451 and vegetation 0.0440 ✓. **Plankton ✗**: the lowest of all 85 is flys (0.0051); among the 18 selected, skimmer (0.0161) is below plankton (0.0164). Plankton has the 3rd-lowest *test MAE* (0.0427). Source: `tables/complete_semantic_attribute_diagnostics.csv`. |
| 17 | §4.3 | "a hamster being identified as a mole" | ✓ trace object 16781 (fallback) |
| 18 | §4.3 | "observed conflict rate of 13.75%" | ✓ v1 0.137522 |
| 19 | §4.3 | "the method demonstrates high reproducibility across datasets" | ✗ only one real dataset in the paper |
| 20 | §5 | "rule conflicts in 13.75% of cases and … structured abstentions in 15.20%" | ✓ v1 0.13752 / 0.15199. Every conflict is an abstention by construction (`infer_rules`, conflict margin 0.05). |
| 21 | §5 | "even at a 0.20 noise level, it preserved a 0.838 Macro-F1 score" | ✓ |
| 22 | §5 | "rule-covered fidelity of 40.48%, representing the proportion of network knowledge that is perfectly replicated as legally auditable logic" | Number ✓; the interpretation is wrong, since it is agreement on covered cases only. |
| 23 | §6 | "neural-to-semantic reconstruction with a mean absolute error of 0.1029 … 84.80% … 0.838" | ✓ (repeats) |
| — | Not stated anywhere | Base-predictor accuracy, against which fidelity and the "audit tax" are defined | Two different base predictors exist. **G1** (Fig. 2, single-run numbers): Top-1 0.7116, Top-5 0.9291, macro-F1 0.5434 (`artifacts/awa2/base_predictor_metrics.json`, seed 42, RidgeClassifier on the 64 variance-screened cache coordinates); MDPI reviewers asked about this 71.16% → 40.73% gap. **G2** (the base behind Table 2's 0.4048 fidelity): RidgeClassifier(α = 1) on each seed's 64 SVD coordinates, test accuracy 0.8068 / 0.8017 / 0.8076 / 0.8102 / 0.8056 for seeds 42–46 (mean 0.806), computed from the `base_prediction` and `true_label` columns of the v3 enhanced prediction exports on `origin/dev`. So the audit tax behind the printed Table 2 is about 0.81 → 0.40, not 0.71 → 0.40. |

## 11. References (27 total, numbered in order of first citation)

Legend: **[SELF]** = cites an author of this paper (Radiuk, Barmak or Krak). **[HOST]** = KhNU's own journal *Computer Systems and Information Technologies* (CSIT). **[FMT]** = formatting defect.

1. W. Yang, Y. Wei, H. Wei, Y. Chen, G. Huang, Survey on explainable AI: From approaches, limitations and applications aspects, Hum.-Centric Intell. Syst. 3 (2023) 161-188. doi:10.1007/s44230-023-00038-y.
2. S. Ali, T. Abuhmed, S. El-Sappagh, K. Muhammad, J. M. Alonso-Moral, R. Confalonieri, R. Guidotti, J. Del Ser, N. Diaz-Rodriguez, F. Herrera, Explainable artificial intelligence (XAI): What we know and what is left to attain trustworthy artificial intelligence, Inf. Fusion 99 (2023) 101805. doi:10.1016/j.inffus.2023.101805.
3. W. Jin, X. Li, M. Fatehi, G. Hamarneh, Guidelines and evaluation of clinical explainable AI in medical image analysis, Med. Image Anal. 84 (2023) 102684. doi:10.1016/j.media.2022.102684.
4. **[SELF]** P. Radiuk, O. Barmak, E. Manziuk, I. Krak, Explainable deep learning: A visual analytics approach with transition matrices, Mathematics 12 (2024) 1024. doi:10.3390/math12071024.
5. **[SELF]** O. Barmak, I. Krak, S. Yakovlev, E. Manziuk, P. Radiuk, V. Kuznetsov, Toward explainable deep learning in healthcare through transition matrix and user-friendly features, Front. Artif. Intell. 7 (2024) 1482141. doi:10.3389/frai.2024.1482141.
6. **[SELF]** P. Radiuk, O. Barmak, L. Bedratyuk, I. Krak, Equivariant transition matrices for explainable deep learning: A Lie group linearization approach, Mach. Learn. Knowl. Extraction 8 (2026) 92. doi:10.3390/make8040092. *(This is a different MAKE paper, the "ETM" work that MDPI reviewers asked to distinguish from SEMTRA.)*
7. A. Musaelian, S. Batzner, A. Johansson, L. Sun, C. J. Owen, M. Kornbluth, B. Kozinsky, Learning local equivariant representations for large-scale atomistic dynamics, Nat. Commun. 14 (2023) 579. doi:10.1038/s41467-023-36329-y.
8. **[HOST]** Y. Tsybulskiy, O. Atamaniuk, E. Fedorov, Expert system for controlling operating modes of solar panels with neural network-based optimality assessment of decisions, Comput. Syst. Inf. Technol. No. 2 (2026) 185-197. doi:10.31891/csit-2026-2-16.
9. **[SELF]** **[FMT: "uav" lower-case]** P. Radiuk, B. Rusyn, O. Melnychenko, T. Perzynski, A. Sachenko, S. Svystun, O. Savenko, Criticality assessment of wind turbine defects via multispectral uav fusion and fuzzy logic, Energies 18 (2025) 4523. doi:10.3390/en18174523. *(Co-author O. Savenko was also an ICyberPhyS proceedings editor.)*
10. **[HOST]** A. Melnyk, B. Zimchenko, Crisp-fuzzy rule management in the cloud: Enabling scalable decision-making for cyber-physical systems, Comput. Syst. Inf. Technol. No. 1 (2025) 163-170. doi:10.31891/csit-2025-1-19.
11. B. H. M. van der Velden, H. J. Kuijf, K. G. A. Gilhuijs, M. A. Viergever, Explainable artificial intelligence (XAI) in deep learning-based medical image analysis, Med. Image Anal. 79 (2022) 102470. doi:10.1016/j.media.2022.102470.
12. V. Hassija, V. Chamola, A. Mahapatra, A. Singal, D. Goel, K. Huang, S. Scardapane, I. Spinelli, M. Mahmud, A. Hussain, Interpreting black-box models: A review on explainable artificial intelligence, Cogn. Comput. 16 (2024) 45-74. doi:10.1007/s12559-023-10179-8.
13. **[SELF]** **[FMT: "ai", "ecg" lower-case]** O. Kovalchuk, O. Barmak, P. Radiuk, L. Klymenko, I. Krak, Towards transparent ai in medicine: Ecg-based arrhythmia detection with explainable deep learning, Technologies 13 (2025) 34. doi:10.3390/technologies13010034.
14. D. Srivastava, G. Yan, T.-W. Weng, VLG-CBM: Training concept bottleneck models with vision-language guidance, in: A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, C. Zhang (Eds.), Advances in Neural Information Processing Systems 37, volume 37, Curran Associates, Inc., Red Hook, NY, USA, 2024, pp. 79057-79094. doi:10.52202/079017-2510.
15. M. Espinosa Zarlenga, P. Barbiero, G. Ciravegna, G. Marra, F. Giannini, M. Diligenti, Z. Shams, F. Precioso, S. Melacci, A. Weller, P. Lio, M. Jamnik, Concept embedding models: Beyond the accuracy-explainability trade-off, in: S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural Information Processing Systems 35, volume 35, Curran Associates, Inc., Red Hook, NY, USA, 2022, pp. 21400-21413. URL: https://proceedings.neurips.cc/paper_files/paper/2022/hash/867c06823281e506e8059f5c13a57f75-Abstract-Conference.html.
16. I. D. Mienye, N. R. Jere, A survey of decision trees: Concepts, algorithms, and applications, IEEE Access 12 (2024) 86716-86727. doi:10.1109/ACCESS.2024.3416838.
17. Y. Zhang, R. Li, N. Wu, Q. Li, X. Lin, Y. Hu, T. Li, Y. Jiang, Dissect black box: Interpreting for rule-based explanations in unsupervised anomaly detection, in: A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, C. Zhang (Eds.), Advances in Neural Information Processing Systems 37, volume 37, Curran Associates, Inc., Red Hook, NY, USA, 2024, pp. 84169-84196. doi:10.52202/079017-2675.
18. **[FMT: LaTeX escape printed literally, "Palangeti\'c"; should be Palangetić; Słowiński written as "Slowinski"]** H. Bollaert, M. Palangeti\'c, C. Cornelis, S. Greco, R. Slowinski, FRRI: A novel algorithm for fuzzy-rough rule induction, Inf. Sci. 686 (2025) 121362. doi:10.1016/j.ins.2024.121362.
19. **[FMT: the "Ş" glyph drops out of the PDF text layer ("H. enozan")]** H. Şenozan, B. Soylu, A flexible non-monotonic discretization method for pre-processing in supervised learning, Pattern Recognit. Lett. 181 (2024) 77-85. doi:10.1016/j.patrec.2024.03.024.
20. G. Biroli, M. Mezard, Kernel density estimators in large dimensions, SIAM J. Math. Data Sci. 8 (2026) 46-76. doi:10.1137/24M1703677.
21. C. H. Lampert, H. Nickisch, S. Harmeling, Learning to detect unseen object classes by between-class attribute transfer, in: 2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2009), IEEE, Miami, FL, USA, 2009, pp. 951-958. doi:10.1109/CVPRW.2009.5206594.
22. C. H. Lampert, H. Nickisch, S. Harmeling, Attribute-based classification for zero-shot visual object categorization, IEEE Trans. Pattern Anal. Mach. Intell. 36 (2014) 453-465. doi:10.1109/TPAMI.2013.140.
23. S. Chen, Z. Hong, Y. Liu, G.-S. Xie, B. Sun, H. Li, Q. Peng, K. Lu, X. You, TransZero: Attribute-guided transformer for zero-shot learning, Proc. AAAI Conf. Artif. Intell. 36 (2022) 330-338. doi:10.1609/aaai.v36i1.19909.
24. M. F. Naeem, Y. Xian, L. Van Gool, F. Tombari, I2DFormer+: Learning image to document summary attention for zero-shot image classification, Int. J. Comput. Vis. 132 (2024) 3806-3822. doi:10.1007/s11263-024-02053-3.
25. S. Chen, Z. Hong, W. Hou, G.-S. Xie, Y. Song, J. Zhao, X. You, S. Yan, L. Shao, TransZero++: Cross attribute-guided transformer for zero-shot learning, IEEE Trans. Pattern Anal. Mach. Intell. 45 (2023) 12805-12821. doi:10.1109/TPAMI.2022.3229526.
26. Y. Xian, C. H. Lampert, B. Schiele, Z. Akata, Zero-shot learning: A comprehensive evaluation of the good, the bad and the ugly, IEEE Trans. Pattern Anal. Mach. Intell. 41 (2019) 2251-2265. doi:10.1109/TPAMI.2018.2857768.
27. C. H. Lampert, D. Pucher, J. Dostal, Animals with attributes 2, Dataset website, 2017. URL: https://cvml.ista.ac.at/AwA2/.

**Statistics.**
- Self-citations: **5/27 (18.5%)**: [4], [5], [6], [9], [13]. Host-journal (CSIT, KhNU) citations: 2 ([8], [10]); these suited ICyberPhyS, and decision 29 drops them for AIT&AIS unless directly needed (at most about 4 self-citations: MAKE, CARDIA-X and up to 2 more).
- Years: 2009 ×1, 2014 ×1, 2017 ×1, 2019 ×1, 2022 ×3, 2023 ×5, 2024 ×8, 2025 ×4, 2026 ×3. 15 of 27 are from 2024–2026.
- Types: 21 journal articles, 5 conference papers (NeurIPS ×3, CVPR ×1, AAAI ×1), 1 dataset website. All refs are cited, in order.
- **Missing foundational refs a reviewer will expect:** Pawlak (rough sets), the core method, has no citation at all; LIME (Ribeiro 2016) and SHAP (Lundberg 2017), which are **named in §5 without citation**; TCAV (Kim 2018); CBM (Koh 2020) and post-hoc CBM (Yuksekgonul 2023); CART (Breiman 1984); MDLP (Fayyad–Irani 1993); RIPPER (Cohen 1995); reject-option/selective classification (Chow 1970; Geifman–El-Yaniv 2017); rule-extraction fidelity (Craven–Shavlik); Anchors (Ribeiro 2018). The MDPI bib (`origin/dev:manuscript/references.bib`, 45 entries) is a ready pool. The AIT&AIS paper must cite the published MDPI SEMTRA article (MAKE 8(7):181, DOI 10.3390/make8070181) as the method source (decision 10); citing the preprint as well is optional.

## 12. Declaration on Generative AI (verbatim)

> During the preparation of this work, the authors utilized generative artificial intelligence tools to enhance the linguistic quality of this manuscript. The language model Gemini 3.1 Pro Preview (Google LLC) and the language service Grammarly (Grammarly, Inc.) were employed for copyediting assistance, specifically to refine grammar, spelling, and stylistic consistency. Following this, the authors conducted a comprehensive review and revision, ensuring all content accurately reflects their research and conclusions. The authors retain full responsibility for the scientific integrity and final content of this paper.

**Risk:** the declaration claims copyediting only. The `prompts/` folder holds prompts named "Refs-reorder", "Refine-outline", "Sections-intro-related" and "Sections-abs-dis-conc", which point to LLM-assisted drafting of sections and reference ordering. For the new venue, the declaration should state actual use accurately (CEUR's GenAI taxonomy distinguishes drafting from grammar checking).

## 13. Funding / acknowledgments

**None.** The paper has no Funding or Acknowledgments section. For comparison, the MDPI manuscript states "This research received no external~funding."

## 14. Copyright block and CEUR agreement

- Footer on p1 (verbatim): "© 2026 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0)." It is accompanied by the CC BY and CEUR logos (EMF/PNG images in the ODT).
- `agreement/ceur-author-agreement-ccby-ntp.pdf`: "Author Agreement to Publish a Contribution as Open-Access on CEUR-WS.org", Version 1.06-ntp, 2025-06-10, 1 page, CC BY 4.0. The event field is pre-filled: "The 3rd International Workshop on Intelligent & CyberPhysical Systems (ICyberPhyS-2026)", with editors Hovorushchenko, Savenko, Popov and Lysenko. The PDF has an AcroForm but **no filled field values** (title, authors and signature are blank in this copy). A handwritten signature is required. Because CEUR never published the volume, no CC BY dedication took effect through CEUR, and the authors keep full rights.

## 15. Reviewer-facing weaknesses visible in the text

Ordered by expected severity. W-numbers are reused in the report.

- **W1 Domain mismatch.** The paper is framed around CPS, controllers, failsafe and "sensor specifications", but all real-data evidence is AwA2 animal images. There is no CPS dataset, no controller and no sensor signal. The attributes ("jungle", "yellow", "small") are called "physical boundaries". "High reproducibility across datasets" is claimed with one dataset. "Guarantee safety" (abstract) is an overclaim.
- **W2 Weak headline metrics, framed as a virtue, with selective baselines.**
  - Covered accuracy is 0.3973 and covered fidelity 0.4048, while the base predictor's Top-1 is about 0.81 for the G2 runs behind these numbers (0.7116 for the G1 single-run predictor); neither is reported in the paper (§10, last row).
  - CART reaches *higher* covered accuracy (0.4129) at 100% coverage (on different, better semantics: the 64-coordinate cache; see the note under Table 2). Its fidelity, 0.4421 in `symbolic_baselines_metrics.csv`, is printed as "-" in Table 2, as is separate-and-conquer's 0.5915. Both exceed SEMTRA.
  - Fig. 2 itself shows CART dominating SEMTRA on both axes.
  - The "audit tax" is used to reframe a ~60% disagreement with the model as a feature.
  - The 84.80% "deterministic logical explanation" includes Hamming-distance prototype fallbacks (fallback rate 7.5–11.1% per seed).
- **W3 Unsupported or incorrect statements.**
  - "This derived symbolic rulebook easily outperforms fragile local XAI tools such as LIME and SHAP": no experiment and no citation. The repo's agreement study measures only 26–32% top-k agreement and makes no superiority claim.
  - "Proportion of network knowledge … perfectly replicated".
  - "Plankton has the lowest salience" is false (§10 #16).
  - Fig. 4 is cited for WEDD threshold placement, but it is a confidence-threshold sweep.
  - "Audit tax (Equation 2)": Eq. 2 is the rule form.
  - Minimal reducts, aggregate support S(y_k) and Hamming soft-matching are asserted but never defined.
- **W4 Methods not reproducible from the text.** Missing:
  - the formula for T;
  - the ResNet-101 2048-d features and SVD rank r = 64 (only in Fig. 1);
  - λ_H = 0.65, KDE bandwidth, max depth / number of states (4), min bin (30 in the G1 seed-42 run; 18 in the G2 runs behind Tables 1–2);
  - attribute selection q = 18 of 85 (in G1 the first eight are hand-forced: stripes, hooves, swims, paws, longneck, hunter, ocean, quadrapedal, via `FORCED_AWA2_ATTRS` in `scripts/legacy/run_all_experiments.py`; G2 uses a 0.5/0.5 salience–error score), and the reduct thresholds τ = 0.84, s_min = 18;
  - the base predictor, the split sizes (22,393 / 7,464 / 7,465) and the seeds;
  - the synthetic generator (5 classes, 10 attributes, 10,000 objects/run, 4 ground-truth rules);
  - definitions of coverage, fidelity and conflict.
  The paper has only 2 equations, against 25 in the MDPI dev draft.
- **W5 Internal inconsistencies from mixing two result generations.**
  - Tables 1–2 are 5-seed r = 64 values (outputs/revision_v1).
  - Figs 2–4 and Tables 4–5 come from the older seed-42 r = 16 run (test MAE 0.1295, 54 rules, coverage 0.8640); Fig. 4 additionally re-evaluates that rulebook on the 64-coordinate cache semantics (§9).
  - Table 2 puts 5-seed "ours" next to single-run baselines fit on the 64-coordinate cache semantics.
  - The attribute sets differ: G2 seed 42 selects stripes, hooves, stalker, ocean, grazer, paws, flippers, hairless, yellow, claws, hops, jungle, water, hands, vegetation, bipedal, tree, hunter (`origin/dev:outputs/revision_v1/awa2/awa2_selected_attributes_seed42.csv`); only 10 of these 18 are in the G1 set. Attributes used by Tables 4–5 (small, swims, longneck, quadrapedal, toughskin) are not in the G2 set behind Table 2.
  - Table 4's "Numeric bounds" (cut-points 0.15 / 0.40 / 0.70) match no artifact. The WEDD thresholds of that very rulebook are, for example, paws 0.218 / 0.4021 / 0.5929 and hooves 0.1187 / 0.3044 / 0.4772, so "hooves = s3" means ≥ 0.4772, not ≥ 0.70. No script generates that column; it was copied from the MDPI draft.
  - The text says rules come from the "rough-set lower approximation", but in the seed-42 rulebook only 7 of 54 rules are `strict_lower` (conf 0.846–0.896) and 3 are `boundary_high_confidence`. **44 are `semantic_prototype` rules with confidence 0.041–0.767 (median 0.17).** Table 5's traces use rules with conf 0.208 and 0.195.
- **W6 Missing comparisons and statistics that the repo already has.** No CBM/TCAV, no LIME/SHAP agreement, no discretizer ablation (WEDD vs MDLP-like), no q or SVD-rank sensitivity, no rule-stability-under-noise, no Protocol B/SUN/Derm7pt, and no confidence intervals or tests. The synthetic table shows 3 of 6 σ levels, with "random seeds" uncounted. Rule Jaccard is only 0.700 at σ = 0, and Macro-F1 is non-monotone (0.879 → 0.881 → 0.838).
- **W7 Presentation defects.**
  - Typos: "59.00% ± 2.55% rules" and "5.30%of".
  - Duplicated header row at the bottom of Table 5.
  - Affiliation 2 is unassigned.
  - ℝ^m × k superscript bug.
  - Truncated labels in Fig. 2.
  - Fig. 1 labels ("Phase 2.3", SVD, q) do not match the text.
  - Keyword spills out of its box.
  - Ref [18] prints the escape "\'c".
  - LIME/SHAP are uncited, and Pawlak and the other foundational refs are missing.
  - 5/27 refs are self-citations, plus 2 citations to the host-institution journal.
- **W8 Overlap with prior work.** The numbers and the rule and trace content are identical, and the captions of Tables 1–5 are identical or near-identical, to the MDPI SEMTRA manuscript, now published as MAKE 2026, 8(7), 181. The ICyberPhyS paper therefore cannot be resubmitted. The agreed route (`06_decisions.md` decisions 1, 10, 14, 24) is a companion paper on AI4I 2020 that cites MAKE as the method source (third person in the blinded PDF), reuses no AwA2 result, carries no ICyberPhyS footnote, and recycles no sentence from ICyberPhyS or MAKE (see 02 §10 and the reuse map).

## Revision log (2026-10-22)

Audit against the final PDF and ODT (`manuscript/conference/submission/`), the earlier ODT in `presentation/`, the figure files, `artifacts/`, `tables/`, `scripts/` and `origin/dev`. Everything not listed here was checked and left unchanged (abstract, keywords, all 5 tables cell by cell, all 27 references and their statistics, both equations and the 5 inline math objects, author block, page map, per-page word counts, figure MD5 identities, Fig. 3 attribute orders, §10 claims #1, #3–#23).

| # | Where | Old → new | Evidence |
|---|---|---|---|
| 1 | Header | "remaking the SEMTRA conference paper for AITAIS" → companion AI4I paper citing MAKE; deadline (before 28 Oct 2026) and online talk by Pavlo Radiuk alone added | `06_decisions.md` (decisions 1, 12, 14, 27, 31), `07_submission_plan.md`; author statement 2026-10-22 |
| 2 | §0 table | final ODT is the source of the math quoted in "§6" → "§7" | §6 is Contributions, §7 is Equations |
| 3 | §0 draft-vs-final | Renumbering list incomplete → added Intro [6]→[6, 7], [13]→[14], [14]→[15], post-hoc CBM [15]→[5], Lie-group [5]→[6], AwA2 [12]→[26, 27]; Musaelian added to the moved entries | word-level diff of the two ODTs' `content.xml` text |
| 4 | §0 email | Month unknown → 6 Oct 2026 per `06_decisions.md`; the PDF is a print dated 2026-10-22 | `ICyberPhyS-2026_Email.pdf` header line |
| 5 | §1 status | "presented on 2026-07-02" → kept, with its evidence (CMT notice wording; slides) and a note that no programme or recording is stored | email text; `presentation/ICyberPhyS_SEMTRA_presentation/` |
| 6 | §5 | Keywords prose words 12 → 13; body total ≈2,570 → ≈2,540 and with abstract ≈2,750 → ≈2,725 (row sums); whole PDF 4,315 → ≈4,300 (pdftotext 4,291 / 4,300) | `pdftotext`; sum of the table's own rows |
| 7 | §7 | "MDPI manuscript has 27 equations" → 25 numbered equation environments in the dev draft; published count (unverified); added note that no formula matches the code exactly | `grep -c 'begin{equation}'` on `origin/dev:manuscript/main.tex` = 25; `scripts/core/paper1_core.py::fit_transition`, `infer_rules` |
| 8 | §8 Table 2 | Added: CART rules = leaves, CART "conditions" 7.0 = tree depth, S&C conflict = >1 matching rule, both fit on the 64-coordinate cache semantics | `scripts/experiments/run_symbolic_baselines.py` |
| 9 | §8 Table 5 | Added: the antecedent-state column shows the object's states on the 8 forced attributes, not the rule; R0029 is an elephant prototype rule | `artifacts/awa2/protocol_a_rulebook.csv` |
| 10 | §9 Fig. 1 | "raster-heavy illustration" → one embedded 5504×3072 JPEG, no vector text | `pdfimages -list`; SVG has 0 `<text>` and 1 `<image>` |
| 11 | §9 Fig. 2 | Added: SEMTRA point on r = 16 semantics, baselines on cache semantics | `run_symbolic_baselines.py` uses `load_cache(...)` |
| 12 | §9 Fig. 4 | "came from a different pipeline run" → exact cause: r = 16 rulebook and thresholds re-applied to cache semantics, post-hoc confidence filter, fallback 0.50 | `scripts/generators/generate_revision_figures.py` lines 28–47 |
| 13 | §9 note | "PDFs were made with Matplotlib 3.11.0" → Figs 2–4 only; Fig. 1 has no producer; newer fig01/fig19 on `origin/dev` noted | `pdfinfo`; `git cat-file -s origin/dev:...` |
| 14 | §10 header | "see 02 §1" → "see 02 §0" | 02 §0 holds the git-history provenance |
| 15 | §10 #2 | Fallback share refined: covered fallbacks 6.2–9.5% of test objects; 7.5–11.1% is the fallback rate incl. abstained fallbacks | v3 enhanced prediction CSVs, seeds 42–46 |
| 16 | §10 last row, W2 | Base predictor 0.7116 only → two base predictors; G2 base (behind Table 2) has test accuracy 0.802–0.810 (mean 0.806) | computed from `origin/dev:outputs/revision_v3/awa2/awa2_rule_predictions_enhanced_seed*.csv` |
| 17 | §11 | "worth revisiting" host-journal refs and "cite MAKE and/or the preprint" → aligned with decisions 10 and 29 | `06_decisions.md` |
| 18 | §15 W4 | "min bin 30" → 30 (G1) / 18 (G2); q = 18 selection now notes the 8 hand-forced attributes in G1; 27 → 25 equations | `run_all_experiments.py::select_attributes`, `FORCED_AWA2_ATTRS`; `run_revision_v1.py::run_protocol_a_once` (`min_support=max(10, 18)`) |
| 19 | §15 W5 | Added Fig. 4 semantics mismatch, baselines on cache semantics, and the G1/G2 attribute-set mismatch (10 of 18 shared) | `awa2_selected_attributes_seed42.csv` (dev) vs `artifacts/awa2/protocol_a_selected_attributes.csv` |
| 20 | §15 W8 | "A remake for AITAIS must disclose that relation" → companion paper route per decisions 1, 10, 14, 24 (no ICyberPhyS footnote) | `06_decisions.md` |
