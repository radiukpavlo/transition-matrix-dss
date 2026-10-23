# AITAIS submission: decision log

Record of the grill-me interview held 2026-10-22, revised the same day. The execution plan is in `07_submission_plan.md`.

> **Submission deadline: the manuscript must be submitted in CMT before 28 October 2026** (author's instruction, 2026-10-22).
> Target: Mon 26 Oct. Hard limit: Tue 27 Oct. The public AITAIS deadline (1 Nov 2026) does not apply to our plan.
>
> **Presentation: online.** The AIT&AIS'2026 organising committee agreed with Pavlo Radiuk that our paper is presented online,
> because travel in Ukraine is unsafe under constant missile and drone attacks. **Pavlo Radiuk presents alone.**

## Facts established

- **ICyberPhyS-2026** (3rd Int. Workshop on Intelligent & Cyber-Physical Systems, 2 July 2026, Khmelnytskyi, online in practice), paper ID 9:
  "Auditable Decision-Making in Intelligent Cyber-Physical Systems Using Semantic Transition and Rough Sets",
  P. Radiuk, O. Barmak, I. Krak. Presented; unpublished. Only the title and authors are public (programme PDF, paper #11).
- **Release:** Microsoft CMT notice from the ICyberPhyS-2026 Organizing Committee (6 Oct 2026, 15:19): CEUR-WS declined the whole
  proceedings; the decision "does not concern the scientific quality, relevance, or originality" of individual papers; authors are
  "completely free to submit their papers to other journals, conferences, workshops". No conditions (see `05_icyberphys_ceur.md`).
- **MAKE:** "SEMTRA: Global Semantic Transition and Rough-Set Rules for Auditable Post-Hoc Explainability", Mach. Learn. Knowl. Extr.
  2026, 8(7):181, DOI 10.3390/make8070181, received 29 May, revised 20 Jun, accepted 24 Jun, published 29 Jun 2026, CC BY 4.0.
  About 100% of the ICyberPhyS evidence (all 5 tables, all 4 figures) is in MAKE, and the ICyberPhyS paper cites neither MAKE nor
  its preprint (see `04_mdpi_overlap.md`). The ECG application is taken by CARDIA-X: Radiuk, Barmak, Klymenko, Krak, "CARDIA-X:
  Global Semantic Transition and Rough-Set Rules for Auditable Post Hoc Electrocardiographic Explainability", AI 2026, 7(9):376,
  DOI 10.3390/ai7090376, published 18 Sep 2026.
- **Code facts for the port** (`02_project_inventory.md`, reuse map): the MAKE transition is `fit_transition` (scaling without
  centring, TruncatedSVD to 64 components, ridge with α chosen on validation MAE); WEDD `wedd_thresholds` (λ_H 0.65, depth 2);
  rules `induce_rules` (τ 0.84; s_min = max(8, min(18, ⌊0.002·n_train⌋)) in `run_revision_v1.py`, so 18 on AwA2 and 11 on AI4I, where n_train = 5,974); inference `infer_rules` (conflict margin 0.05). The MAKE text and the scripts disagree on
  some settings (e.g. Hamming fallback 0.25 in the text vs 0.45/0.50 in the scripts), so the new paper must report the values
  actually used.
- **AIT&AIS'2026** (written AITAIS in URLs and CMT): 2nd International Scientific Workshop on Applied Information Technologies and
  Artificial Intelligence Systems, 8-9 Dec 2026, Chernivtsi National University, announced as an offline event, free. Public deadline
  for CMT registration and full paper: 1 Nov 2026 (superseded for us, see the box above); notification 1 Dec. CEUR-WS, CEUR-ART
  1-column ODT; regular papers only, **at least 10 pages** (2025 median 13), last page at least 80% full; **double-blind**; GenAI
  declaration and figure alt text required; no page numbers. Rule 2.1: author with the most DBLP-indexed papers first; rule 2.2: all
  authors Candidate of Sciences or higher. Barmak sits on the AITAIS PC; Hovorushchenko, Savenko and Zaitseva sit on both the AITAIS
  and ICyberPhyS-2026 PCs (see `03_aitais_venue.md`). The newsletter (`08_aitais_newsletter.md`) adds: at least three PC reviewers,
  a second review round before CEUR, a talk at a section session as a condition of publication, and (Ukrainian text only) possible
  extended versions in MECS, CEUR-WS or Springer on the PC's recommendation.
- **ICyberPhyS paper weaknesses** a reviewer would hit: CPS framing on animal images only; covered accuracy 0.397 and fidelity 0.405
  against an unreported base predictor (RidgeClassifier on SVD-64 ResNet features, test accuracy about 0.81; the often-quoted 0.7116
  belongs to a different, single-run predictor, see `01_conference_manuscript.md`); CART beats SEMTRA in Fig. 2; unsupported "outperforms LIME and SHAP"; mixed 5-seed and single-run results
  (see `01_conference_manuscript.md`). Global Python lacks the project packages and raw datasets are absent (see `02_project_inventory.md`).
- **AI4I experiment done (2026-10-23)** under a protocol frozen before any test evaluation: code, outputs, tables T1-T4,
  plots F2-F4 and the results memo in `E:\GitHub\semtra-ai4i` (private GitHub repo radiukpavlo/semtra-ai4i since 2026-10-23); digest and
  writing map in `09_ai4i_results.md`.
- CEUR author agreement must be re-signed for AIT&AIS at camera-ready (current version in `05_icyberphys_ceur.md`; the local copy is older).

## Resolved branches

| # | Branch | Decision | Consequence |
|---|--------|----------|-------------|
| 1 | Positioning vs MAKE | Companion paper with a new angle | MAKE cited as the method source; method condensed; contribution is something MAKE lacks |
| 2 | Effort budget | One small new experiment (hours of compute, existing scripts) | Realised as decision 12 |
| 3 | Authorship | Pavlo Radiuk (corresponding), Oleksander Barmak, Iurii Krak | Same order as ICyberPhyS |
| 4 | Affiliations | Radiuk, Barmak: 1 Khmelnytskyi National University. Krak: 2,3 Taras Shevchenko National University of Kyiv; Glushkov Cybernetics Institute | Fixes the ICyberPhyS error (affiliation 2 unused) |
| 5 | Toolchain | ODT in LibreOffice, from the AIT&AIS CEUR-ART 1-column ODT template | References kept by hand: verify every DOI before pasting |
| 6 | Presentation mode | **Online**, agreed with the AIT&AIS'2026 organising committee (war-related travel risk) | Replaces the earlier in-person/co-author plan; see decision 27 |
| 7 | GenAI declaration | Full disclosure of every tool actually used (Claude, plus Gemini/Grammarly if used), CEUR GenAI taxonomy wording | Write it last, from the real tool log. CEUR's GenAI policy calls AI-generated paragraphs and AI-created "diagrams, charts, and illustrations" unacceptable, and the 13 taxonomy terms (listed in `05_icyberphys_ceur.md`) cover writing tasks only. Expected terms for Claude's review role: "Grammar and spelling check", "Improve writing style", "Plagiarism detection", "Citation management", "Formatting assistance"; avoid "Drafting content", "Generate images", "Abstract drafting", "Content enhancement". Describe the AI-assisted analysis and plotting code in plain words in the same declaration |
| 8 | Code/data availability | Statement with the code link and public dataset source | Review version uses the anonymous mirror (decision 22) |
| 9 | Funding/acknowledgments | None | - |
| 10 | Disclosure | Cite MAKE as the method source (third person in the blinded PDF); no ICyberPhyS footnote, no note to the chairs | Defensible because ICyberPhyS was never published. Text must differ visibly from ICyberPhyS (3 shared PC members). Keep the CMT release email on file |
| 11 | Author order vs rule 2.1 | Radiuk has the highest DBLP count (author's statement); the order complies | Barmak declares the PC conflict in CMT |
| 12 | New result | UCI AI4I 2020 predictive maintenance (10,000 rows, CC BY 4.0): MLP, embedding-to-physical-concept transition, recovery of the documented failure rules, plus abstain/conflict-based error triage | Dataset download and new repo need the author's go-ahead at that step; project venv required. Facts in the AI4I fact sheet of `04_mdpi_overlap.md` |
| 13 | AI4I labels | Failure-mode multi-class: none, HDF, PWF, OSF, TWF; drop RNF and multi-mode rows (report counts recomputed from the CSV: the UCI description, e.g. TWF 120 and L/M/H 50/30/20%, differs from commonly reported CSV label counts, e.g. TWF 46 and about 60/30/10%) | Rules checked per mode against the documented generating rules (HDF: ΔT < 8.6 K and speed < 1380 rpm; PWF: power < 3500 W or > 9000 W; OSF: wear×torque > 11000/12000/13000 minNm for L/M/H; TWF: wear 200-240 min, partly random) |
| 14 | AwA2 scope | AI4I only; AwA2 appears only through citations to MAKE | Every number in the paper is new |
| 15 | Concept dictionary | 7 physical concepts (ΔT, speed, torque, power, tool wear, strain = wear×torque, product type) plus distractors: raw air and raw process temperature (components of ΔT that appear in no rule by themselves) and one pure-noise sensor | Report whether rules select the rule-relevant concepts and ignore the distractors |
| 16 | Baselines | Rules on true concepts (upper bound), depth-limited CART on the same predicted concepts, MLP max-probability as the triage baseline. No RIPPER | - |
| 17 | CMT topic | **Primary 7 "Artificial Intelligence for Industrial Monitoring and Predictive Maintenance"; secondary 1 "Computational Intelligence and Machine Learning Methods"** (revised 2026-10-22: the first choice, 1 + 15, came from a shortlist drawn up before AI4I was chosen; see `08_aitais_newsletter.md`) | Abstract leads with the predictive-maintenance audit (rule recovery), triage second |
| 18 | Title | Working title: "Do Extracted Rules Recover the Physics? Rough-Set Auditing and Error Triage for Neural Predictive-Maintenance Models" | No "SEMTRA" in the title; finalise after results |
| 19 | Structure and length | 7 sections, 12 pages: Intro 1.25, Related 1.25, Method 2.0, Setup 1.5, Results 3.0, Discussion 1.0, Conclusion 0.4, GenAI + ~30 refs 1.6 | Last page at least 80% full |
| 20 | Figures and tables | F1 AI4I pipeline (draw.io), F2 thresholds vs physics, F3 risk-coverage curves, F4 per-concept fidelity; T1 concept dictionary, T2 threshold recovery, T3 method comparison, T4 triage AUROC/AURC | All new; house style `scripts/core/figure_style.py`; alt text for every figure. CEUR GenAI compliance (revised 2026-10-22): **the authors draw F1 themselves** (Claude may supply a component list only); F2-F4 are plotted by analysis code from real results, and the author reviews the plotting code and decides the final design; **the author writes the captions and alt text** |
| 21 | Weak-results policy | Freeze protocol and hyperparameters on validation before touching test; report whatever comes out as audit findings; **results by end of Sat 24 Oct** (moved from 26 Oct by decision 31) | Discussion states AI4I is itself synthetic (Matzka 2020): ground-truth recovery, not plant validation |
| 22 | Code location and blinding | New repo for the AI4I experiment, `semtra-ai4i` (created private on GitHub 2026-10-23; public for the camera-ready); review mirror https://anonymous.4open.science/r/semtra-ai4i-CD9B; review PDF links an anonymous.4open.science mirror; camera-ready links the real repo | Scrub ODT metadata; no names, affiliations or ORCIDs in the review PDF; MAKE cited in the third person |
| 23 | Drafting | The author writes all paper text in the CEUR-ART ODT (CEUR does not permit AI-generated paragraphs); Claude reviews each section and flags problems rather than writing replacement paragraphs | Claude supplies numbers, table data and data plots from the experiment; captions, alt text and F1 are the author's (revised 2026-10-22 for CEUR GenAI compliance) |
| 24 | Text recycling | No sentence carried over from ICyberPhyS or MAKE; method recap paraphrased and cited; n-gram overlap check before submission, rewrite any passage above ~10% | Needs MAKE full text locally |
| 25 | Experiment ownership | Claude implements, freezes the protocol, runs 5 seeds, delivers tables, figures and a results memo **by end of Sat 24 Oct** (moved from 26 Oct) | The author writes sections 1-3 in parallel |
| 26 | Co-author review | **Full draft to Barmak and Krak Sun 25 Oct evening, feedback by Mon 26 Oct midday** (moved from 29 Oct with 24 h; shortened to fit decision 31) | Fixes and submission Mon 26 Oct; Tue 27 Oct buffer |
| 27 | Presenter | **Pavlo Radiuk presents alone, online**, on 8-9 Dec 2026 | Keep the organisers' confirmation of the online talk with the submission records |
| 28 | Degree rule 2.2 | All three authors qualify (author's statement) | - |
| 29 | Self-citations | MAKE + CARDIA-X + at most 2 more directly relevant ones (about 4 of ~30), third person | Drop the two KhNU-journal citations unless directly needed |
| 30 | Communication with the chairs | No email about ICyberPhyS or open formal questions; the author is in direct contact with the organising committee (online talk agreed) | Anonymise conservatively; follow the published formatting rules |
| 32 | Rulebook variants (decided 2026-10-22 on validation data only) | Report MAKE's rulebook unchanged as the as-published baseline, plus a class-reduct rulebook: per failure mode, a greedy class-specific rough-set reduct (with pair lookahead) and rules on it, 'none' as the default class; same WEDD cuts | MAKE settings collapse to 'none' at 97:3 imbalance (test macro-F1 0.28). The class-reduct rulebook is the paper's method contribution; results in `09_ai4i_results.md` |
| 31 | Submission deadline | **Before 28 Oct 2026**: target Mon 26 Oct, hard limit Tue 27 Oct (time zone unknown, so do not rely on the last evening) | Compresses decisions 21, 25 and 26; see the timeline in `07_submission_plan.md` |
