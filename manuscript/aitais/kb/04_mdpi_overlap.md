# 04. Overlap between the MDPI MAKE article and the ICyberPhyS-2026 manuscript

Compiled 2026-10-22; audited and re-verified the same day (see the revision log at the end). Web facts carry their URL. Local facts carry their file path. Policy texts are paraphrased, not quoted, except for one CEUR rule. Facts that could not be re-checked are marked "(not re-verified)".

## 0. Bottom line

- The MAKE article (published 29 June 2026) already contains every table, figure, equation idea and number in the ICyberPhyS paper. The ICyberPhyS paper adds only a cyber-physical-systems (CPS) framing (autonomous platforms, failsafe transitions, sensor noise, "digital twin" of the model logic, retrofitting legacy controllers) and 8 references that MAKE does not have, 2 of them CPS-specific.
- Estimated share already in MAKE: about 100% of the evidence (data, tables, figures, method) and about 85-90% of the content overall. Verbatim text overlap is low (about 4% of sampled prose 6-grams, 64% of caption 6-grams) because the prose was reworded.
- CEUR-WS does not allow an already-published study to be resubmitted, so the ICyberPhyS paper cannot go to AITAIS in its current form. AITAIS needs a companion paper that cites MAKE as the source of the method and whose main result is new.
- **Chosen direction (author, 2026-10-22; `06_decisions.md` decisions 12-16):** AI4I 2020 failure-mode classification with an MLP, recovery of the documented failure rules through the embedding-to-concept transition, and abstain/conflict-based error triage. AI4I only: AwA2 appears only through citations to MAKE, and no AwA2 number is reported as a result. The other angles in Section 6 are not pursued. AI4I facts are in Section 8.
- **Disclosure decision (author; decisions 10 and 30):** cite MAKE only (third person in the blinded PDF). No ICyberPhyS footnote and no note to the chairs. Rationale: ICyberPhyS was never published. The policy analysis that recommended disclosure is kept in Section 5, together with the residual risk.
- **Logistics (author, 2026-10-22; decisions 6, 27 and 31):** submit in CMT before 28 Oct 2026 (target 26 Oct, hard limit 27 Oct); the public AITAIS deadline of 1 Nov does not apply to this plan. The talk will be given online by Pavlo Radiuk alone, as agreed with the AIT&AIS'2026 organising committee.

## 1. The journal article (MAKE 8(7):181)

Sources: article page https://www.mdpi.com/2504-4990/8/7/181 (it also carries the full text) and https://www.mdpi.com/2504-4990/8/7/181/htm. Both were read in the in-app browser on 2026-10-22, because MDPI returns HTTP 403 to scripted fetches (re-confirmed 2026-10-22 for the article page, /ethics and /journal/make/instructions; the PDF was not opened). Crossref record: https://api.crossref.org/works/10.3390/make8070181 (re-fetched 2026-10-22).

| Field | Value |
|---|---|
| Title | SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-Hoc Explainability |
| Authors | Pavlo Radiuk (1, corresponding), Oleksander Barmak (1), Iurii Krak (2, 3) |
| Affiliations | 1: Dept. of Computer Science, Khmelnytskyi National University; 2: Dept. of Theoretical Cybernetics, Taras Shevchenko National University of Kyiv; 3: Laboratory of Communicative Information Technologies, V.M. Glushkov Institute of Cybernetics |
| Journal | Mach. Learn. Knowl. Extr. 2026, 8(7), 181; 33 pages |
| Special issue | Explainable Artificial Intelligence: Theoretical Foundations and Methodological Advances |
| Academic editors | Sheng Du; Javier Del Ser (MDPI page) |
| Dates | Received 29 May 2026; Revised 20 June 2026; Accepted 24 June 2026; Published 29 June 2026 (Crossref "published-online" 2026-06-29) |
| DOI | 10.3390/make8070181 |
| License | CC BY 4.0, from 2026-06-29 (Crossref license field: https://creativecommons.org/licenses/by/4.0/; MDPI page: "© 2026 by the authors. Licensee MDPI") |
| Keywords | explainable artificial intelligence (XAI); transition matrix; semantic attributes; rough sets; production rules; discretization; zero-shot learning |
| Funding / COI | "This research received no external funding"; "The authors declare no conflicts of interest" |
| Data/code | AwA2, xlsa17 (AwA2/SUN features), SUN Attribute Database and Derm7pt from their official sources. Scripts and artifacts at https://github.com/radiukpavlo/transition-matrix-dss (this repository; "accessed on 21 June 2026" in the Data Availability Statement). Supplementary File S1 at https://www.mdpi.com/article/10.3390/make8070181/s1 with Tables S1-S11 and Figures S1-S7 (captions listed on the article page; the file itself was not opened) |
| Extras | Graphical abstract, Version Notes, open Review Reports; the page lists "Article Figures (7)" (6 numbered figures plus the graphical abstract) |

Abstract (paraphrased; numbers re-verified against Crossref and the MDPI page). SEMTRA is a post hoc framework. It maps frozen representation features to semantic attributes, discretizes those attributes, and induces rough-set production rules, reporting coverage, conflict, fidelity and abstention. Reported results:
- AwA2 Protocol A: transition MAE 0.1029 ± 0.0005; the rulebook covers 84.80% of test instances, with covered accuracy 39.73% and covered fidelity 40.48%.
- Protocol B (xlsa17): unseen-object accuracy 44.02% ± 1.22%.
- SUN and Derm7pt: the audit protocol is portable but its results depend strongly on the dataset.
- Synthetic benchmark: macro-F1 0.879 at zero noise and 0.838 at the highest noise level.

The article presents SEMTRA as an audit layer that sits beside the predictor, not as a replacement for it.

Section outline (exact headings): 1 Introduction; 2 Related Works (2.1 Local Post Hoc Explanation; 2.2 Concept-Based and Ante Hoc Models; 2.3 Formal Knowledge Granulation and Rough Sets; 2.4 Semantic Transfer as a Validation Proxy); 3 Materials and Methods (3.1 Framework Architecture Overview; 3.2 Phase 1: Neural-to-Semantic Transition; 3.3 Phase 2.1: Semantic Attribute Selection and Stable Discretization (WEDD); 3.4 Phase 2.2: Rough-Set Granulation and Knowledge Discovery; 3.5 Phase 2.3: Conflict-Aware Inference and Evaluation, with 3.5.1 Conflict Resolution and Soft Matching and 3.5.2 Fidelity and Coverage Metrics; 3.6 Evaluation Metrics for Auditability; 3.7 Experimental Protocol and Proof-of-Concept Design); 4 Results (4.1 Semantic Reconstruction Performance (Protocol A); 4.2 Rulebook Auditability and Fidelity; 4.3 Zero-Shot Transfer as Semantic Validation (Protocol B); 4.4 Cross-Domain Technical Validation; 4.5 Comparison with Local Surrogates and Concept Baselines; 4.6 Algorithmic Recovery (Synthetic Benchmark)); 5 Discussion (5.1 The Scientific Value of Global Auditability; 5.2 Interpreting the Audit Tax: Accuracy vs. Verifiability; 5.3 The Power of Honest Silence and Indiscernibility; 5.4 Linear Transition as a Defensive Choice; 5.5 Limitations and Open Challenges); 6 Conclusions; Appendix A ETM vs. SEMTRA Comparison; Appendix B Experimental Protocol and Hyperparameters; Appendix C Rule Inference Traces and Structural Perturbation Stability.

Equations: 27 numbered equations, (1)-(27), plus (A1) in the appendices; Algorithms 1 and 2. By section: §3.1 Eqs. 1-2; §3.2 Eqs. 3-7; §3.3 Eqs. 8-12; §3.4 Eqs. 13-16; §3.5.1 Eqs. 17-18; §3.5.2 Eqs. 19-21; §3.6 Eqs. 22-24; §3.7.2 Eqs. 25-27.

Contributions (4, "First ... Second ... Third ... Finally"): (1) a dimensionally explicit transition-matrix formulation from compressed deep representations to semantic attributes, without retraining the feature extractor; (2) a density-aware discretization module (WEDD); (3) a rough-set rulebook with explicit handling of structural abstentions and boundary regions; (4) a multi-domain evaluation (benchmarks plus synthetic data) in which coverage, fidelity, accuracy, conflict and sensitivity together define the "audit tax". The introduction separates SEMTRA from the authors' earlier ETM paper (MAKE 8(4):92), and Table A1 sets out the differences.

Datasets: AwA2 Protocol A (closed-world, 85 attributes); AwA2 Protocol B (official xlsa17 split); SUN (102 attributes, xlsa17 ResNet-101 split); Derm7pt (7 checklist concepts, retrospective technical validation only); a synthetic 3-class benchmark with known ground-truth rules (Table 15).

Setup (Table A3): ResNet-101 ILSVRC features, 2048-d, with PCA to 64 components (95% variance); ridge classifier as the base predictor; seeds 42-46; ridge semantic bridge (alpha grid 0.01-100); WEDD alpha 0.65, max_depth 2, min_bin_size 30, min_gain 0.002; greedy reducts with tau 0.84 and s_min 18; soft-matching threshold τH = 0.25 (maximum masked Hamming distance).

Baselines: CART; separate-and-conquer (RIPPER-like); equal-frequency, equal-width and MDLP-like discretizers; RBF kernel ridge and a 2-layer MLP regressor as transition operators; LIME and SHAP-style local explanations; a frozen-feature CBM; TCAV; 14 published zero-shot learning (ZSL) baselines (DAP, IAP, CONSE, CMT, SSE, ALE, DEVISE, SJE, ESZSL, SYNC, SAE, GFZSL, TransZero, I2DFormer+).

Main numbers (all re-read from the HTML tables on 2026-10-22):
- T1 Protocol A reconstruction. Test MAE 0.1029 ± 0.0005, RMSE 0.1484 ± 0.0007, correlation 0.8070 ± 0.0018. Train MAE 0.1027, validation MAE 0.1030.
- T2 operator ablation. Linear ridge: MAE 0.1076 ± 0.0012, Cov 0.8718, rule accuracy 0.1941, runtime 0.0451 s. RBF: MAE 0.1958, Cov 1.0, rule accuracy 0.0027, runtime 2.86 s. MLP: MAE 0.1685, Cov 0.8390, rule accuracy 0.0915.
- T3 top-12 selected attributes (q = 18 used).
- T4 rulebook vs baselines:

  | Method | Rules | Coverage | Covered accuracy | Abstention | Conflict |
  |---|---|---|---|---|---|
  | SEMTRA | 59.00 ± 2.55 | 0.8480 ± 0.0530 | 0.3973 ± 0.0109 | 0.1520 ± 0.0530 | 0.1375 ± 0.0532 |
  | CART | 53 | 1.0 | 0.4129 | 0 | 0 |
  | Separate-and-conquer | 197 | 0.2620 | 0.6334 | 0.7380 | 0.2301 |

  SEMTRA also reports covered fidelity 0.4048 ± 0.0078 and 4.0397 ± 0.0543 conditions per rule (CART 7.0, separate-and-conquer 3.2589).
- T5 discretizers (Cov, fidelity, conflict): WEDD 0.8480 / 0.4048 / 0.1375; MDLP-like 0.8334 / 0.3975 / 0.1482; equal-frequency Cov 0.7212; equal-width Cov 0.6401.
- T6 q-sensitivity: q = 8 to 32 gives Cov 0.80 to 0.87 and fidelity 0.34 to 0.55.
- T7 SVD rank 16 to 128: MAE 0.1295 down to 0.0942.
- T8 example rules R0001 tiger (support 115, conf. 0.896), R0003 antelope (132, 0.871), R0004 zebra (434, 0.866).
- T9-T11 ZSL. Prototype transfer 44.02 ± 1.22%; symbolic template 23.48 ± 1.70%; unseen semantic MAE 0.1888.
- T12 agreement between local explanations and fired rules on 1000 instances: LIME soft Jaccard 0.5412, SHAP-style 0.6071.
- T13 cross-domain:

  | Dataset | MAE | Cov | Fidelity | Accuracy |
  |---|---|---|---|---|
  | SUN | 0.0683 | 0.0760 | 0.0918 | 0.0714 |
  | Derm7pt | 0.2433 | 0.9241 | 0.5288 | 0.4219 |

- T14 concept baselines. Frozen-feature CBM accuracy 0.7232; SEMTRA 0.4073; TCAV 0.4850.
- T15-T16 synthetic benchmark:

  | Noise σ | Macro-F1 | Rule Jaccard | Coverage |
  |---|---|---|---|
  | 0 | 0.879 | 0.700 | 0.971 |
  | 0.1 | 0.881 | 0.763 | 0.962 |
  | 0.2 | 0.838 | 0.743 | 0.952 |

- A2 control knobs (λs, λH; default row: 54 rules, Cov 0.8640, covered fidelity 0.3829, covered accuracy 0.4073); A4 base predictor test top-1 0.7116, AUROC 0.9836, ECE 0.6645; A5 rule traces (objects 5083 collie, 24,024 ox, 16,781 hamster to mole); A6 rule consistency under semantic perturbation (σ ≤ 0.1: rule consistency 0.73 to 1.0, coverage 0.88 to 0.89).

Figures (6 numbered plus a graphical abstract; captions re-read 2026-10-22):
- Fig 1: conceptual architecture of the SEMTRA framework.
- Fig 2(a-c): transition salience by attribute; attribute-wise reconstruction error on AwA2; salience against test error.
- Fig 3: symbolic baseline trade-off between Cov and covered fidelity.
- Fig 4(a-c): "Rulebook and threshold optimization": WEDD threshold example; rule support and confidence distribution; coverage, abstention, covered accuracy and covered fidelity as the minimum rule-confidence threshold varies.
- Fig 5: conceptual local-vs-global comparison (illustrative, not measured).
- Fig 6(a, b): synthetic benchmark with 95% confidence bands; synthetic threshold recovery error across noise levels.

Table captions (MDPI page): T1 AwA2 Protocol A transition reconstruction metrics; T2 operator ablation; T3 top 12 selected attributes (of q = 18); T4 general rulebook properties and symbolic baseline comparison; T5 discretizer comparison; T6 selected-attribute-count sensitivity; T7 SVD-rank sensitivity; T8 representative induced production rules; T9 comparison with published ZSL baselines; T10 official AwA2 xlsa17 unseen-class transfer; T11 Protocol B validation across seeds; T12 local-vs-global agreement; T13 cross-domain summary; T14 concept-based baselines; T15 synthetic ground-truth rule dictionary; T16 synthetic stress-test results; A1-A6 (ETM vs SEMTRA; control knobs; hyperparameters; base predictor; inference traces; perturbation consistency).

Supplementary File S1 captions (from the article page; file not opened): Tables S1-S3 (hyperparameters, base predictor, SUN audit summary); Figure S1 object-level audit outcomes with bootstrap intervals; Figure S2 SUN category-level coverage and conflict map; Tables S4-S5 and Figure S3 Derm7pt; Table S6 and Figure S4 attribute count and discretizer evidence, including paired WEDD-minus-MDLP-like intervals, with the note that WEDD's advantages are modest; Tables S7-S8 and Figure S5 SVD rank, runtime and sensitivity; Table S9 and Figure S6 Protocol B; Table S10 and Figure S7 cross-domain; Table S11 object-level bootstrap intervals. Section 4.4 points to Supplementary Sections S3 and S8 for "category-level conflict maps".

Limitations and future work (Section 5.5 and Section 6):
- Limitations: dependence on human-annotated concept dictionaries; error propagation through the sequential stages; combinatorial cost of reduct search; strong dataset dependence (very low SUN coverage; ImageNet encoders are not good enough for Derm7pt).
- Future work: differentiable rough sets; automated concept discovery, possibly with Large Language Models; instance-level semantic supervision; faster search; domain-specific validation.

Does MAKE mention the ICyberPhyS paper? No. A full-text search of the body (Introduction to Appendix C, excluding the reference list) on 2026-10-22 found no hits for "ICyberPhyS", "CEUR", "conference", "workshop", "cyber-physical", "CPS", "sensor", "failsafe"/"fail-safe" or "digital twin". "Conference" occurs only in reference venue names. The 45 references (Crossref) include the authors' own earlier papers: Mathematics 2024, Front. AI 2024, ETM MAKE 2026, Technologies 2025 and Energies 2025.

Preprint: DOI 10.20944/preprints202606.0230.v1, posted 2026-06-03, CC BY 4.0. Crossref marks it as a preprint of 10.3390/make8070181 (https://api.crossref.org/works/10.20944/preprints202606.0230.v1, re-fetched 2026-10-22). The page https://www.preprints.org/manuscript/202606.0230 returned 403. The v1 abstract has numbers from an earlier configuration: MAE 0.1295, coverage 86.40%, covered accuracy 40.73%, separate-and-conquer coverage 26.20%, ZSL 48.43% vs DAP 46.10%, synthetic macro-F1 0.8668. Several of these match MAKE Table 7 (rank 16: MAE 0.1295) and Table A2 (default knobs: Cov 0.8640, covered accuracy 0.4073). The ICyberPhyS paper uses the final MAKE numbers, not the preprint numbers.

Related later paper (verified 2026-10-22 via Crossref https://api.crossref.org/works/10.3390/ai7090376 and the MDPI page https://www.mdpi.com/2673-2688/7/9/376):

> Radiuk, P.; Barmak, O.; Klymenko, L.; Krak, I. CARDIA-X: Global Semantic Transition and Rough-Set Rules for Auditable Post Hoc Electrocardiographic Explainability. *AI* **2026**, *7*(9), 376. https://doi.org/10.3390/ai7090376

- Received 3 Aug 2026; revised 11 Sep 2026; accepted 14 Sep 2026; published 18 Sep 2026; CC BY 4.0; 29 pages; special issue "Explainable and Trustworthy AI in Health and Biology: Enabling Transparent and Actionable Decision-Making".
- Not quite the same team: it adds a fourth author, Liliana Klymenko (Dept. of Family Medicine and Outpatient Care, Shupyk National Healthcare University of Ukraine).
- It is an ECG instantiation of the SEMTRA sequence (52-target semantic contract, evidence-gated class eligibility). It cites SEMTRA as ref. 15, with the reference text pointing to MAKE but the DOI of the preprint.
- The Crossref search https://api.crossref.org/works?query.bibliographic=CARDIA-X&filter=from-pub-date:2026-01-01 (166 results) did not return it in the top 10 (gastric "cardia" papers rank first), so it was verified by direct DOI lookup.
- Relevance to the chosen angle: CARDIA-X discusses abstention as possible clinical "deferral" (it states that a reason-coded abstention is not evidence of clinically safe deferral, and clinicians rated "deferral appropriateness"). It has no risk-coverage, AURC, error-detection or triage analysis and no hits for "AI4I", "predictive maintenance" or "tabular". The ECG/medical application angle is already published.

## 2. The conference manuscript (ICyberPhyS-2026, ID 9)

Local sources:
- `E:\GitHub\transition-matrix-dss\manuscript\conference\presentation\manuscript_items.txt` and `manuscript_summary.txt` (extracted 2026-07-01 from the ODT of 30 June);
- `presentation\ICyberPhyS-2026_ID-9-Submission.odt` (meta.xml: last saved 2026-06-30 19:00, 11 pages, 4289 words, 9 tables, 7 images);
- `submission\ICyberPhyS-2026_ID-9-Submission.odt` (last saved 2026-07-01 10:05, 11 pages, 4283 words);
- `submission\ICyberPhyS-2026_ID-9-Submission.pdf` (final PDF, LibreOffice export of 2026-07-02 11:37, 11 pages; read with `pdftotext -layout` on 2026-10-22).

Facts:
- Title: Auditable Decision-Making in Intelligent Cyber-Physical Systems Using Semantic Transition and Rough Sets. Authors: Radiuk, Barmak, Krak. The workshop (ICyberPhyS-2026: 3rd International Workshop on Intelligent & Cyber-Physical Systems) took place on 2 July 2026 in Khmelnytskyi, online in practice (`06_decisions.md`).
- Structure: Introduction; Related Works; Methods (3.1 Phase 1 transition; 3.2 Phase 2.1 WEDD with Eq. 1; 3.3 Phase 2.2 granulation with Eq. 2; 3.4 conflict-aware inference and auditing); Experimental Results (4.1 Protocol A and rulebook; 4.2 synthetic noise; 4.3 visualization of the audit); Discussion; Conclusion; GenAI declaration (Gemini 3.1 Pro Preview and Grammarly, for copyediting); 27 references.
- Neither the ODTs nor the final PDF cite MAKE or its preprint. The contribution list claims three novelties that are MAKE's contributions 1-3.
- Reference overlap with MAKE (final PDF list against the 45 MAKE references in Crossref): 19 of 27 are also in MAKE. Twelve match by DOI: Mathematics 2024, Front. AI 2024, ETM, Energies 2025, Technologies 2025, Mienye 2024, FRRI, Şenozan 2024, Biroli 2026, Lampert 2014, Xian 2019 and I2DFormer+. Seven match by title: AwA2 website, Lampert 2009 (the conference gives the DOI as CVPRW.2009.5206594, MAKE as CVPR.2009.5206594), VLG-CBM, concept embedding models, "Dissect black box", TransZero and TransZero++. Not in MAKE: [1] Yang 2023, [2] Ali 2023, [3] Jin 2023, [7] Musaelian 2023, [8] Tsybulskiy 2026 (PV control, CPS), [10] Melnyk 2025 (crisp-fuzzy rules for CPS), [11] van der Velden 2022 and [12] Hassija 2024.

Manuscript defects to avoid in any remake (checked against both versions):

| Defect | ODT of 30 June (`manuscript_items.txt`) | Final PDF of 2 July |
|---|---|---|
| In-text citation numbers do not match the reference list ([8] "fuzzy logic" points to Musaelian; [12] "AwA2" points to the Xian ZSL survey; [26, 27] "post-hoc CBM" point to I2DFormer+ and TransZero++) | Present | Fixed by renumbering (fuzzy [9, 10]; AwA2 [26, 27]). But "post-hoc CBM" now cites [5], the authors' Front. AI paper; Yuksekgonul et al. (MAKE ref. 14) is still not cited |
| Krak affiliation: only 3 is given and affiliation 2 is listed but never used | Present | Present |
| Table 5 header row duplicated | Present | Present (the header repeats after the last row) |
| "Compactness: ... 59.00% ± 2.55% rules": a percent sign on a rule count | Present (P069) | Present |
| Unsupported claims: "high reproducibility across datasets" (only AwA2 is used) and that the rulebook "easily outperforms fragile local XAI tools such as LIME and SHAP" (MAKE reports only agreement, in Table 12) | Present | Present |

## 3. Timeline

| Date | Event | Source |
|---|---|---|
| 2026-05-18 | ICyberPhyS submission deadline | `05_icyberphys_ceur.md` (not re-verified) |
| 2026-05-29 | MAKE manuscript received | MDPI page |
| 2026-06-03 | Preprint posted | Crossref |
| 2026-06-20 / 06-24 | MAKE revised / accepted | MDPI page |
| 2026-06-23 | ICyberPhyS camera-ready deadline | `05_icyberphys_ceur.md` (not re-verified) |
| 2026-06-29 | MAKE published (CC BY 4.0) | MDPI page, Crossref |
| 2026-06-30 | Presentation-folder ODT last saved; no citation of MAKE | ODT meta.xml |
| 2026-07-01 | Submission ODT last saved; no citation of MAKE | ODT meta.xml |
| 2026-07-02 | Final PDF exported; ICyberPhyS-2026 presentation | PDF metadata; manuscript header |
| 2026-08-03 | CARDIA-X received by MDPI AI | MDPI page |
| 2026-09-18 | CARDIA-X published | MDPI page, Crossref |
| 2026-10-06 | CEUR declines the whole ICyberPhyS volume; authors released | `06_decisions.md`, `05_icyberphys_ceur.md` |
| 2026-10-22 | Author's decisions: AI4I direction, MAKE-only citation, deadline, online talk | `06_decisions.md` |
| before 2026-10-28 | AITAIS submission in CMT (target 26 Oct, hard limit 27 Oct) | `06_decisions.md` decision 31 |
| 2026-11-01 | Public AITAIS deadline (does not apply to this plan) | `06_decisions.md` |
| 2026-12-08/09 | AIT&AIS'2026; online talk by Pavlo Radiuk | `06_decisions.md` decisions 6, 27 |

Going by the dates in `05_icyberphys_ceur.md`, the ICyberPhyS paper was submitted before the MAKE manuscript was received, and its camera-ready deadline fell inside MAKE's review window (29 May to 24 June). The two versions were therefore under consideration at the same time, and neither mentions the other. Nothing was published twice, because the ICyberPhyS volume was never published. This analysis originally recommended disclosing the history to the AITAIS chairs; the author decided against it (Section 5, "Disclosure decision").

## 4. Overlap matrix (conference section against MAKE)

Text-match method: each conference paragraph was cut into non-overlapping lowercase word 6-grams (505 in total), hashed with SHA-1, and looked up against all 6-grams of the MAKE /htm full text (13,101 words) inside the browser. "Match" is the share of sampled 6-grams found verbatim. Tables were compared cell by cell. The 6-gram figures come from the ODT text in `manuscript_items.txt` and were not re-run on 2026-10-22. The final PDF differs from the ODT mainly in citation numbers and a few deleted citations, so the figures should still hold approximately. Table values, captions, section mapping and reference overlap were re-checked against the final PDF and the MDPI page on 2026-10-22.

| Conference section | MAKE counterpart | Class | 6-gram match | Notes and reused numbers |
|---|---|---|---|---|
| Abstract | Abstract | Same content, different wording | 0/31 | Reuses 0.1029, 84.80%, 0.838. The CPS, failsafe and "guarantee safety" framing is conference-only |
| Intro: motivation (P017-P019) | §1 paragraphs 1-2 | Same problem, different wording, plus conference-only CPS framing | 0-5% | Conference-only: autonomous vehicles, medical monitoring, PV control ([7] in the ODT, [8] in the final PDF), fuzzy safety ([8] ODT, [9, 10] final) |
| Intro: goal and objective (P020-P021) | §1 goal and objective | Same content, different wording | 0-17% | Both aim to improve auditability and transparency by translating latent features into a conflict-aware rulebook |
| Intro: 3 contributions (P022-P024) | §1 contributions 1-3 | Near-verbatim paraphrase | up to 25% | Same order and key phrases ("maps compressed deep representations ... without retraining"). MAKE adds contribution 4 |
| Paper outline (P025) | §1 last paragraph | Same structure | 9% | Same allocation of Sections 2-6 |
| Related work (P026-P029) | §2.1-2.4 | Same content, different wording | 0% | 19 of 27 conference references are also in MAKE (Section 2). The gap paragraph matches MAKE's problem statement |
| Phase 1: transition matrix | §3.2 (Eqs. 3-7: centering, randomized SVD rank r, ridge) | Same content, condensed (subset) | 0% | The conference gives no equation for T. MAKE has the full derivation |
| WEDD, Eq. 1 | §3.3 (Eqs. 8-12; λH = 0.65) | Same content, different wording; same objective (entropy and density weighted by λH) | 0% | MAKE adds the attribute-selection score and the control knobs |
| Rough-set granulation and rules, Eq. 2 | §3.4 (Eqs. 13-16: indiscernibility, lower approximation, discernibility matrix, reducts) | Same content, condensed | 0% | |
| Conflict-aware inference and auditing | §3.5-3.6 (Eqs. 17-18 conflict resolution and Hamming soft matching; Eqs. 19-24 fidelity, coverage and audit metrics) | Same content, condensed, plus conference-only "failsafe mode" wording | 0% | |
| Table 1, Protocol A | Table 1 | Identical (9/9 values; caption verbatim) | caption 100% | 0.1027 / 0.1030 / 0.1029; 0.1482 / 0.1486 / 0.1484; 0.8079 / 0.8065 / 0.8070 |
| Table 2, rulebook vs CART and separate-and-conquer | Table 4 | Identical (21/21 values; caption verbatim) | caption 100% | 59.00 ± 2.55; 0.8480; 0.3973; 0.4048; 4.0397; 0.1520; 0.1375; CART and separate-and-conquer columns |
| Table 3, synthetic noise | Table 16 | Identical (15/15 values; caption verbatim) | caption 100% | 0.879 → 0.838; coverage 0.971 → 0.952 |
| Table 4, example rules | Table 8 | Identical (3 rules, bounds, support, confidence) | caption 33% | R0001 / R0003 / R0004 (zebra support 434, conf. 0.866). The conference adds a sentence on support |
| Table 5, inference traces | Table A5 | Identical (3 cases) | caption 100% | Objects 5083 (collie, R0027), 24024 (ox, R0029), 16781 (hamster to mole) |
| Figure 1, architecture | Fig. 1 | Same figure (caption shortened) | 0% | Not pixel-checked. Local file `presentation/fig1-semtra-architecture.svg` |
| Figure 2, coverage vs fidelity | Fig. 3 | Same plot, caption paraphrased | 0% | |
| Figure 3a,b, semantic diagnostics | Fig. 2a,b | Same panels; caption verbatim (MAKE adds panel c) | 67% | |
| Figure 4, threshold sweep | Fig. 4c | Same panel; caption verbatim (MAKE adds a, b) | 100% | |
| Results prose (Protocol A, rulebook, audit tax) | §4.1-4.2, §5.2 | Same content, different wording | 0% | 84.80 ± 5.30%, 4.04 conditions, 40.48% fidelity, "audit tax" |
| Noise robustness prose | §4.6 | Same content, different wording | 0% | 0.879, 0.838, 95.2% |
| Audit visualization and cases (P110-P170, P218) | §4.2, Appendix C, Fig. 2 text | Same content, different wording, plus conference-only "audit dashboard" and CPS wording | 0% | paws / vegetation highest salience; plankton lowest; 13.75% conflict; Hamming soft matching |
| Discussion | §5.1-5.5 | Same content, different wording, plus conference-only CPS implications | 0-8% | 13.75% conflict and 15.20% abstention (identical); LLM concept discovery (also in MAKE §5.5). "Retrofit legacy controllers" and "digital twin of the model's logic" are conference-only |
| Conclusion | §6 | Same content, different wording | 0% | MAE 0.1029, 84.80%, 0.838. MAKE also covers Protocol B and the cross-domain results |
| GenAI declaration | none | Conference-only (CEUR requirement) | 0% | |
| (absent from conference) | Protocol B / ZSL (T9-T11), SUN and Derm7pt (T13), operator ablation (T2), discretizer ablation (T5), q and SVD sensitivity (T6-T7), LIME/SHAP agreement (T12), CBM/TCAV (T14), synthetic ground truth (T15), A1-A6, Supplementary S1 | Journal-only | n/a | |

Aggregate verbatim match, by group:

| Group | Matched / sampled 6-grams | Share |
|---|---|---|
| Abstract | 0/31 | 0% |
| Introduction | 4/89 | 4% |
| Related work | 0/85 | 0% |
| Methods | 0/54 | 0% |
| Captions | 14/22 | 64% |
| Results | 0/46 | 0% |
| Visualization | 0/43 | 0% |
| Discussion | 1/68 | 1% |
| Conclusion | 0/32 | 0% |
| **Overall** | **19/505** | **about 4%** |

Caveats: sampling non-overlapping 6-grams underestimates short verbatim phrases. MathJax spacing in MAKE can break a few n-grams. Equations and tables were not included in the prose check, which is why tables were compared cell by cell.

Overlap estimate:
- Empirical content: 100% of the conference's results, tables (all about 60 numeric cells), figures (4 figures, 5 panels) and method are in MAKE.
- Prose: about 85-90% of it discusses material MAKE already publishes. The conference-only part, about 10-15%, is the CPS framing, the 8 references not in MAKE (2 of them CPS-specific) and the GenAI declaration.
- What a similarity checker would see: low prose similarity, but exact matches in the tables and captions.

## 5. Policy findings

All paraphrased except the single CEUR quote. Every URL below was re-opened on 2026-10-22: COPE, MDPI and ACM in the in-app browser (scripted fetches got 403); TRRP, CEUR, IEEE, Springer Nature, Atlantis Press and Creative Commons with a scripted fetch (HTTP 200).

**COPE, text recycling** (https://publicationethics.org/guidance/cope-position/handling-text-recycling-also-known-self-plagiarism, COPE Council, last reviewed 20 Aug 2024, DOI 10.24318/6eWbU5xd)
- COPE defines text recycling as reusing one's own earlier writing without being transparent about it or referencing or quoting the original. It also adopts the TRRP definition, which covers prose, visuals and equations.
- Editors decide case by case. They weigh how much text and data overlap, where it sits (methods are more tolerable than discussion) and whether related papers were declared or cited.
- If the later paper is still unpublished, the authors can be asked to expand and rewrite it while citing the earlier publication.
- Copyright should be considered when the overlap with an earlier copyrighted publication is substantial.
- Authors should always cite and clarify the overlap between a later publication and the original publication.

**COPE, concurrent and duplicate submissions** (https://publicationethics.org/guidance/cope-position/handling-concurrent-and-duplicate-submissions, last reviewed 20 Aug 2024, DOI 10.24318/y9lyqPiR)
- Submitting a paper to several journals at once, or submitting an already published paper to another journal, are both unethical practices; concurrent submission is called poor practice.
- Authors should not recycle work that has already been published.
- Deliberate recycling can lead to rejection and to the authors' institution being informed.

**COPE flowchart, redundant (duplicate) publication in a submitted manuscript** (https://publicationethics.org/guidance/flowchart/redundant-duplicate-publication-submitted-manuscript, last reviewed 31 Mar 2025, DOI 10.24318/cope.2019.2.12)
- Re-verified key points: the journal's response depends on the extent and nature of the overlap; authors are contacted for clarification; journals should ask authors to confirm that the manuscript is original and not published elsewhere.
- The tiers (major overlap means the same data with identical or very similar findings, which would be the case for any resubmission of the ICyberPhyS results; minor or legitimate overlap, such as methods or a reanalysis, is handled by asking for a citation) come from the flowchart PDF as summarized by a web search. The PDF itself was not opened (not re-verified).

**COPE/BioMed Central text recycling guidelines for editors** (https://members.publicationethics.org/files/Web_A29298_COPE_Text_Recycling.pdf, summarized by web search, not opened; a scripted fetch got 403; not re-verified)
- Some methods overlap can be acceptable if it is cited.
- Recycling in results that duplicates published data is almost always unacceptable.
- Editors should not rely on a similarity-percentage cutoff alone.

**Text Recycling Research Project, Best Practices for Researchers** (https://textrecycling.org/resources/best-practices-for-researchers/)
- Recycled material can include prose, visuals and equations. Reuse can be ethical if it is accurate, appropriate to the new work, and does not infringe copyright or violate publisher policy.
- Authors should tell editors about recycled material at submission. If the journal has no specific policy, a footnote at the start of the paper listing the sources of recycled material tells readers.
- Some venues do not allow previously published material to be recycled in Results or Discussion.
- For published work, reuse rights depend on copyright law and the publication contract.

**MDPI publication ethics** (https://www.mdpi.com/ethics)
- Plagiarism includes copying text, ideas, images or data from another source, including one's own publications, without credit. Reused text must be in quotation marks and cited, and a design, structure or language inspired by earlier studies must be cited.
- Submissions are screened with iThenticate. Simultaneous submission to more than one journal is not permitted.
- Authors keep copyright, and articles are CC BY 4.0, so they may be reused if the original is cited.

**MAKE instructions** (https://www.mdpi.com/journal/make/instructions)
- An expanded conference paper can become a MAKE article if it is expanded to research-article length, cites the conference paper and notes it on the first page, has the copyright holder's permission where needed, and comes with a cover-letter statement of what changed. Unpublished conference papers that do not meet these conditions are steered to MDPI's Proceedings Series.
- A manuscript must not contain information that has already been published. MAKE accepts papers previously posted as preprints that were not peer reviewed.
- Inference, not policy text: MDPI's norm is conference paper first, journal paper second.

**CEUR-WS** (https://ceur-ws.org/HOWTOSUBMIT.html, procedure valid from 2019-08-01)
- Proceedings papers must be original, i.e., "not published in an earlier workshop or conference or journal".
- CEUR discourages republishing papers already published by another publisher, notes that this can be regarded as self-plagiarism or double publication, and states that it is not a re-publisher of already published proceedings or papers.
- Peer review by an international programme committee is required.
- A regular paper has at least 10 standard pages; a short paper has 5-9 (about 2500 characters per standard page).
- The licence is CC BY 4.0. Authors sign an author agreement in one of two forms, depending on whether third-party copyrighted material is included (the NTP form when there is none).
- The Declaration on Generative AI is mandatory (CEURART template). Generating paragraphs or whole sections with AI is in general not permitted; improving grammar or style with AI is a borderline case and is not allowed if it adds to or changes the content.

**IEEE conference submission policies** (https://conferences.ieeeauthorcenter.ieee.org/author-ethics/guidelines-and-policies/submission-policies/)
- Submit only original work that has neither appeared elsewhere nor is under review for another refereed publication.
- Disclose prior publications and current submissions, state clearly how the new submission differs from them, and cite them.
- IEEE recognizes an evolutionary path, for example workshop, then conference, then journal, provided it is fully referenced.
- Recycled material (text, charts, photographs, other graphics) must be clearly indicated and fully referenced, within copyright policy.
- Each IEEE organizational unit decides whether to allow multiple submissions; authors must inform editors of them.

**ACM, Prior Publication and Simultaneous Submissions** (https://www.acm.org/publications/policies/simultaneous-submissions)
- Submit original, unpublished work only; otherwise it can be viewed as self-plagiarism.
- A revised version of a published paper is acceptable only when all of these hold: it is substantially revised (generally at least 25% new material, a subjective threshold left to each publication), the PC or editor-in-chief is notified on submission, and neither venue's policy forbids it.

**Springer Nature (books and proceedings)** (https://www.springernature.com/gp/policies/book-publishing-policies)
- Proceedings papers must be peer reviewed, and accepted papers are expected to be presented at the conference.
- Atlantis Press, a Springer Nature imprint, states that its proceedings manuscripts are evaluated to ensure that they do not substantially overlap with previously published work (e.g., https://www.atlantis-press.com/proceedings/pesd-24/peer-review-and-ethics).
- I did not find a Springer rule specifically on journal-to-conference republication.

**Licence (CC BY 4.0)** (https://creativecommons.org/licenses/by/4.0/)
- MAKE figures may legally be reused or adapted with appropriate credit, a link to the licence and an indication of any changes. No permission request is needed, and the authors keep copyright (per the MDPI ethics page).
- This settles copyright only, not redundancy: a reused figure is still recycled evidence and must be labelled, for example "Reproduced/adapted from [MAKE], CC BY 4.0". The chosen plan avoids this: all figures are new (decision 20).
- Because the authors hold the copyright, the CEUR form for papers without third-party material (NTP) applies (`07_submission_plan.md` checklist).

### What is acceptable for AITAIS (CEUR)

Not acceptable:
- Submitting the ICyberPhyS paper as it is, or lightly revised. It has the same data and findings as a journal article, so COPE would class it as major overlap, and it breaks the CEUR originality rule.
- The ACM "25% new" route. CEUR has no such exception for previously published work.

Acceptable: a companion or follow-up paper that meets all of the following. The chosen AI4I paper is designed to meet them (`07_submission_plan.md`).
1. It cites MAKE prominently, in the abstract or introduction and at the start of Methods ("the pipeline of [MAKE]"), in the third person in the blinded PDF. CARDIA-X is cited as related work (decision 29).
2. Its contribution is new: a new experiment, dataset, analysis or use case (here: AI4I rule recovery and error triage).
3. It condenses the method into a cited summary of about half a page; the methods section is where cited recycling is most tolerated.
4. It does not present MAKE numbers as results. At most one sentence or one baseline row should be clearly attributed to MAKE. Under decision 14, no AwA2 number appears as a result.
5. It generates new figures from the new experiment. If an architecture figure is needed, redraw it for the tabular pipeline (F1 is a new draw.io figure).
6. It does not reuse ICyberPhyS or MAKE paragraphs verbatim (decision 24: n-gram check, rewrite any passage above about 10%).
7. Disclosure: see the decision below. The earlier recommendation, a first-page footnote on the presented-but-unpublished ICyberPhyS version plus a submission note to the chairs, is **not adopted**.

### Disclosure decision (author, 2026-10-22)

- **Decision** (`06_decisions.md` decisions 10 and 30): cite MAKE as the method source only. No ICyberPhyS footnote, no note or e-mail to the AITAIS chairs about ICyberPhyS. The author is in direct contact with the organising committee only about the online talk.
- **Rationale:** the ICyberPhyS paper was never published. CEUR declined the whole proceedings, and the organisers' CMT notice of 6 Oct 2026 leaves the authors free to submit elsewhere with no conditions (`05_icyberphys_ceur.md`). The rules analysed above (CEUR originality, COPE redundant and duplicate publication, MAKE's prior-publication rules, IEEE and ACM prior publication) concern published or concurrently submitted work. The only prior publication is MAKE, and it is cited. The new paper shares no data, results, figures or text with ICyberPhyS.
- **Supporting consideration (mine, not the author's stated reason):** in a double-blind review, a footnote naming the authors' own unpublished workshop paper would identify them.
- **Residual risk:**
  - Transparency guidance favours telling editors about closely related work at submission: TRRP best practice 7 and its footnote advice, IEEE "disclose all prior publication(s) and current submissions", and COPE "cite and clarify the overlap". A reviewer or chair who applies these norms broadly could read silence about a presented paper on the same method as a lack of transparency.
  - The ICyberPhyS title and authors are public in the workshop programme. Three AITAIS PC members also sat on the ICyberPhyS-2026 PC, and Barmak sits on the AITAIS PC (`06_decisions.md`), so the link may be recognised.
  - Both earlier versions were under consideration at the same time (Section 3) and neither cites the other. This is outside AITAIS's remit, but it could come up if someone asks.
- **Mitigation:** new dataset, results, figures and text; MAKE cited prominently; keep the CMT release notice of 6 Oct 2026 with the submission records; have a short factual answer ready if the chairs or reviewers ask (presented 2 July 2026, never published, CEUR volume declined, no shared data or text).

## 6. Differentiation angles

**Status (2026-10-22): the AI4I direction is chosen; all other angles are not pursued.** Gap evidence comes from a full-text search of the MAKE body (references excluded) on 2026-10-22.

Constraint from `06_decisions.md`: one small new experiment, hours of compute; submission before 28 Oct 2026.

**Chosen: AI4I 2020 failure-mode classification, rule recovery and abstain/conflict error triage** (decisions 12-16; specification in `07_submission_plan.md` Section 2). This merges former angles 1 and 2 and applies both to AI4I only.
- What it does: a small MLP classifies AI4I failure modes (none, HDF, PWF, OSF, TWF; RNF and multi-mode rows dropped and counted). Its last hidden layer is mapped to physical concepts (ΔT, speed, torque, power, tool wear, strain = wear × torque, product type) plus distractors.
  - Test 1: do the extracted rough-set rules recover the documented thresholds (Section 8) and ignore the distractors?
  - Test 2: do the rulebook's abstain and conflict flags detect the MLP's errors better than its max-probability? Measured with error-detection AUROC, risk-coverage curves and AURC.
- MAKE gap:
  - zero hits for "predictive maintenance", "cyber-physical", "sensor", "selective", "risk-coverage", "deferral", "human-in-the-loop", "error detection", "misclassif" and "confusion";
  - "industrial" appears once, in an Introduction sentence that cites the authors' wind-turbine paper [10];
  - "triage" appears once, in §4.2, where "dataset triage" is listed as a suitable use with no analysis behind it. Cite that sentence and claim only the quantitative triage evaluation.
- CARDIA-X gap: it discusses abstention versus clinical deferral qualitatively but has no risk-coverage, AURC or error-detection analysis. Cite it for the deferral framing.
- The AI4I failure rules are synthetic and documented, which gives a ground-truth audit target. The Discussion must say that AI4I is synthetic (decision 21).
- Not used: the AwA2 artifacts listed under the former angle 1 (`artifacts/awa2/base_predictor_predictions.csv`, `protocol_a_test_rule_predictions.csv`, `coverage_abstention_tradeoff.csv`), because no AwA2 number may appear as a result (decision 14).

Not pursued (kept for the record):
1. ~~Abstention as error triage on AwA2~~. Folded into the chosen direction, on AI4I data instead of AwA2.
2. ~~Industrial/CPS benchmark (AI4I) as a stand-alone rule-recovery study~~. Folded into the chosen direction.
3. **WEDD threshold stability under bootstrap.** Not pursued. MAKE has zero hits for "threshold stability", but Supplementary Figure S4(e) already gives paired WEDD-minus-MDLP-like intervals and calls WEDD's advantages modest, and Appendix C covers rule consistency under perturbation. The file `artifacts/awa2/protocol_a_threshold_stability.csv` (rows entropy_only, wedd, density_only) has empty values. Too close to MAKE's core, and AwA2-based.
4. **Rule-level conflict anatomy (class-pair confusion).** Not pursued. MAKE has zero hits for "confusion", but its Supplementary Sections S3 and S8 contain "category-level conflict maps" (Figure S2 is the SUN category-level coverage and conflict map). AwA2-based.
5. **Backbone or concept-source sensitivity (CLIP, DINOv2, LLM-generated concepts).** Not pursued. MAKE has zero hits for "CLIP", "ViT", "DINO" and "LLM" (§5.5 names Large Language Models as future work), but this needs AwA2 images and a GPU, which is beyond the budget.

Avoid ECG (published as CARDIA-X) and SUN/Derm7pt (already in MAKE).

## 7. Open checks

- MAKE Supplementary File S1 was not downloaded. Its captions are now known (Section 1), which makes the former angle-4 check moot.
- Figure identity is inferred from the captions and data, not from a pixel comparison.
- AITAIS 2026: the call is now documented (AIT&AIS'2026, 8-9 Dec 2026, Chernivtsi, CMT, CEUR; `03_aitais_venue.md`, `06_decisions.md`). The 2025 edition was re-verified on 2026-10-22: AIT&AIS 2025, Chernivtsi, 18-19 Dec 2025, CEUR Vol-4160, 42 papers submitted and 25 accepted (all regular), submitted to CEUR 2026-01-05 and published 2026-02-07 (https://ceur-ws.org/Vol-4160/).
- AI4I counts at CSV level (Section 8) must be recomputed from `ai4i2020.csv` after the download is approved, before writing the setup section and T1/T2.
- The 6-gram figures in Section 4 were not re-run against the final PDF text. Re-run them if the conference text is ever reused (decision 24 already requires an n-gram check of the new paper against MAKE and ICyberPhyS).
- The COPE flowchart PDF and the COPE/BMC text-recycling PDF were not opened.
- The ICyberPhyS deadlines (18 May, 23 June) are taken from `05_icyberphys_ceur.md` and were not re-verified here.

## 8. AI4I 2020 fact sheet

Sources, all read on 2026-10-22:
- UCI page https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset (scripted fetch, HTTP 200);
- DataCite record https://api.datacite.org/dois/10.24432/C5HS5C;
- Crossref record of the paper https://api.crossref.org/works/10.1109/AI4I49448.2020.00023.

The CSV itself was not downloaded, because decision 12 requires the author's go-ahead.

| Field | Value |
|---|---|
| Name | AI4I 2020 Predictive Maintenance Dataset (UCI Machine Learning Repository, id 601); donated 29 Aug 2020 |
| DOI | 10.24432/C5HS5C (DataCite: publisher UCI Machine Learning Repository, 2020, creator "Unknown", type Dataset). UCI citation: AI4I 2020 Predictive Maintenance Dataset [Dataset]. (2020). UCI Machine Learning Repository. https://doi.org/10.24432/C5HS5C |
| License | CC BY 4.0 (UCI page; the DataCite rights field is empty) |
| Nature | Synthetic; described as reflecting real predictive maintenance data encountered in industry. UCI lists it as Multivariate, Time-Series; tasks Classification, Regression, Causal-Discovery; no missing values |
| Size | 10,000 rows × 14 columns (UCI counts 6 features); file `ai4i2020.csv`, 509.8 KB |
| Original paper | S. Matzka, "Explainable Artificial Intelligence for Predictive Maintenance Applications," in *2020 Third International Conference on Artificial Intelligence for Industries (AI4I)*, Irvine, CA, USA, 21-23 Sep 2020, pp. 69-74, IEEE. DOI 10.1109/AI4I49448.2020.00023 (Crossref; issued Sep 2020). UCI lists it as the introductory paper. Full text not read (IEEE) |

Columns and units (UCI variables table and "Additional Variable Information"):

| Column | Role | Units | Generation (UCI text) |
|---|---|---|---|
| UID | ID | - | 1 to 10000 (UCI writes "UID"; the CSV header is "UDI", verified 2026-10-23; the file starts with a UTF-8 BOM) |
| Product ID | ID | - | Letter L, M or H plus a variant-specific serial number |
| Type | Feature (categorical) | - | Quality variant L / M / H, documented as 50% / 30% / 20% of products |
| Air temperature | Feature | K | Random walk normalized to SD 2 K around 300 K |
| Process temperature | Feature | K | Random walk normalized to SD 1 K, added to air temperature plus 10 K |
| Rotational speed | Feature | rpm | Calculated from a power of 2860 W, overlaid with normal noise |
| Torque | Feature | Nm | Normal around 40 Nm, σ = 10 Nm, no negative values |
| Tool wear | Feature | min | Variants H / M / L add 5 / 3 / 2 min of tool wear per process |
| Machine failure | Target | 0/1 | 1 if at least one failure mode is true; the label does not say which mode caused the failure |
| TWF, HDF, PWF, OSF, RNF | Targets | 0/1 | One flag per failure mode |

Failure modes (UCI text; the expected definitions in the task brief and in decision 13 are confirmed, with the TWF wording made precise):

| Mode | Generating rule | Count stated by UCI |
|---|---|---|
| TWF, tool wear failure | The tool is replaced or fails at a randomly selected tool-wear time between 200 and 240 min | 120 events: replaced 69 times, failed 51 times (randomly assigned) |
| HDF, heat dissipation failure | Process − air temperature difference < 8.6 K **and** rotational speed < 1380 rpm | 115 |
| PWF, power failure | Power = torque × rotational speed in rad/s (ω = 2π·rpm/60) < 3500 W **or** > 9000 W | 95 |
| OSF, overstrain failure | Tool wear × torque > 11,000 minNm (L), 12,000 minNm (M), 13,000 minNm (H) | 98 |
| RNF, random failure | Each process fails with probability 0.1%, regardless of its parameters | 5 ("less than could be expected" for 10,000 points) |

UCI does not state the number of rows with Machine failure = 1.

CSV-level counts (verified 2026-10-23 on the downloaded CSV, `E:\GitHub\semtra-ai4i\outputs\data_audit.json`):
- Machine failure = 1: 339 rows (3.39%).
- Per-column sums: TWF 46, HDF 115, PWF 95, OSF 98, RNF 19. TWF and RNF differ from the UCI text (120 events, of which 51 failures; 5).
- Type counts: L 6000, M 2997, H 1003 (60/30/10%), not the documented 50/30/20.
- 9 rows have Machine failure = 1 with no mode flag; 18 rows carry a mode flag (all RNF-only) with Machine failure = 0; 24 rows have more than one mode.
- HDF, PWF and OSF labels match the documented rules on every row; 43 of 790 rows in the TWF window (200-240 min) are labelled, plus 3 outside it.

After dropping 19 RNF and 23 further multi-mode rows (decision 13), 9,958 rows remain: none 9652, HDF 106, PWF 80, OSF 78,
TWF 42 (`09_ai4i_results.md` §2).

Implications for the experiment (decisions 13 and 15):
- Concept units: ΔT = process − air temperature [K]; power [W] = torque [Nm] × 2π × speed [rpm] / 60; strain = tool wear [min] × torque [Nm], in minNm.
- Recoverable ground truth:
  - HDF: two cuts, 8.6 K and 1380 rpm;
  - PWF: two cuts, 3500 W and 9000 W;
  - OSF: a strain cut that depends on Type, so the rule must combine Type with strain (11,000 / 12,000 / 13,000 minNm).
- Only partly recoverable: TWF. The necessary condition is tool wear of about 200 min or more, but the failure time within 200-240 min is random.
- Not recoverable by design: RNF, which is dropped.

## Revision log (2026-10-22)

| # | Old | New | Source |
|---|---|---|---|
| 1 | Header: compiled, no audit note | Audit note; "(not re-verified)" convention | This audit |
| 2 | §0: "three CPS-flavoured references" | 8 references not in MAKE, 2 CPS-specific ([8] PV control, [10] crisp-fuzzy CPS) | Final conference PDF reference list vs MAKE references in Crossref |
| 3 | §0: "Section 6 lists candidate angles" | Chosen direction recorded (AI4I failure-mode classification + rule recovery + abstain/conflict triage, AI4I only, no AwA2 numbers); other angles not pursued | `06_decisions.md` decisions 12-16; author |
| 4 | §0/§3/§5: disclosure to the AITAIS chairs and an ICyberPhyS footnote recommended | Author's decision recorded (MAKE only; no footnote; no note to the chairs), with rationale (ICyberPhyS never published) and residual risk; policy analysis kept | `06_decisions.md` decisions 10, 30; author |
| 5 | No deadline or presenter information | Submit before 28 Oct 2026 (target 26, hard limit 27 Oct); online talk by Pavlo Radiuk, agreed with the organisers | Author; `06_decisions.md` decisions 6, 27, 31 |
| 6 | §1: "About 89 numbered equation references" | 27 numbered equations (1)-(27) plus (A1); Algorithms 1-2; equation ranges per section | MDPI article page |
| 7 | §1: Supplementary S1 = "Tables S1-S3, Figure S1" | Tables S1-S11, Figures S1-S7, with caption summary | MDPI article page |
| 8 | §1: paraphrased section outline | Exact headings, including 3.5.1/3.5.2 and the appendix titles | MDPI article page |
| 9 | §1: setup and baseline details partial | Added PCA 95% variance, ridge alpha grid, WEDD max_depth/min_bin_size/min_gain, τH; full list of 14 ZSL baselines; academic editors; data-availability access date; table-caption list; SDs for abstention and conflict | MDPI article page |
| 10 | §1: CARDIA-X "by the same team", minimal citation | Full citation with four authors (adds L. Klymenko), exact title, received/revised/accepted/published dates, 29 pages, special issue, ref. 15 = SEMTRA via the preprint DOI; Crossref keyword search does not surface it; deferral discussion noted | Crossref 10.3390/ai7090376; MDPI page 2673-2688/7/9/376 |
| 11 | §1: full-text search "no hits ... conference" | Search scope stated (body only; "conference" only in reference venues) | MDPI article page |
| 12 | §2: defects listed for one version; ODT only as source | Final PDF (2 Jul 2026) and submission ODT (1 Jul) added; citation mismatches are ODT-only (fixed by renumbering in the final PDF, but post-hoc CBM now cites [5] and Yuksekgonul is still missing); added the "59.00% ± 2.55% rules" typo | `conference/submission/*.pdf` (`pdftotext -layout`), ODT meta.xml, `manuscript_items.txt` |
| 13 | §2/§4: "at least 14 of 27 references are also in MAKE"; "TransZero probably also shared" | 19 of 27 (12 by DOI, 7 by title, including TransZero and TransZero++) | Final PDF references vs Crossref MAKE references |
| 14 | §3: two ODT-era rows; "review windows probably overlapped" | Added ICyberPhyS deadlines, 1 Jul ODT, 2 Jul PDF, CARDIA-X dates, decision date, 28 Oct submission, 1 Nov public deadline, 8-9 Dec talk; overlap stated with dates | ODT/PDF metadata; MDPI; `05_icyberphys_ceur.md`; `06_decisions.md` |
| 15 | §4: WEDD "Eqs. 8-13"; rough sets "Eqs. 14-15"; inference "Eq. 18" | WEDD Eqs. 8-12; rough sets Eqs. 13-16; inference and metrics Eqs. 17-24 | MDPI article page |
| 16 | §4: intro citation numbers [7], [8] given without version | ODT [7]/[8] vs final PDF [8]/[9, 10]; "digital twin" added as conference-only wording; note that the 6-gram figures were not re-run | `manuscript_items.txt`; final PDF |
| 17 | §5: COPE pages "dated 20 Aug 2024" | "Last reviewed 20 Aug 2024", DOIs added; COPE "cite and clarify the overlap" added; "another venue" → "another journal" | COPE pages (browser) |
| 18 | §5: MAKE instructions, three conditions | All four conditions (adds copyright permission); Proceedings Series note; preprint rule; "conference first" marked as inference | MAKE instructions page (browser) |
| 19 | §5: TRRP, IEEE, CEUR, ACM, Springer, CC BY summaries | Re-verified; minor wording made precise (TRRP footnote and Results/Discussion limits; IEEE "clearly indicate"; CEUR NTP form and GenAI "adds or changes content"; ACM 25% "subjective") | Respective URLs |
| 20 | §5 list items 1 and 7 (footnote, chairs note) | Item 1 = cite MAKE in the third person; item 7 = not adopted; new subsection "Disclosure decision" | `06_decisions.md`; author |
| 21 | §6: angle 1 "Recommended" on AwA2 data; angles 2-5 open | Chosen direction marked; angles 1-2 folded in on AI4I; 3-5 not pursued with reasons (Supplementary Figure S4(e), Figure S2/S3/S8 conflict maps); MAKE "triage" and "industrial" hits disclosed | MDPI article page; `06_decisions.md` |
| 22 | §7: "did not find a 2026 AITAIS call" | Call documented elsewhere; Vol-4160 facts re-verified (adds 2026-01-05 submission to CEUR); new open checks (AI4I CSV counts, COPE PDFs, ICyberPhyS deadlines) | https://ceur-ws.org/Vol-4160/; `03_aitais_venue.md` |
| 23 | §6 angle 2: brief AI4I facts (CC BY 4.0, 10,000 rows, DOI, four rules, "TWF and RNF are random") | New §8 "AI4I 2020 fact sheet": DOI, licence, size, columns and units, generation details, five rules with UCI counts, CSV-level caveats, original paper. Expected values confirmed; TWF made precise ("replaced or fails" at 200-240 min; 120 events, 51 failures) | UCI page; DataCite; Crossref |
| 24 | Matzka paper cited without venue details | Verified: S. Matzka, 2020 Third International Conference on Artificial Intelligence for Industries (AI4I), Irvine, CA, 21-23 Sep 2020, pp. 69-74, IEEE, DOI 10.1109/AI4I49448.2020.00023 | Crossref |
