# AIT&AIS'2026 submission plan

Shared understanding reached 2026-10-22, revised the same day (decisions in `06_decisions.md`).

> **Deadline: submit in CMT (https://cmt3.research.microsoft.com/AITAIS2026) before 28 October 2026.**
> Target Mon 26 Oct; hard limit Tue 27 Oct. The public 1 Nov deadline does not apply to our plan.
>
> **Presentation: online, by Pavlo Radiuk alone**, as agreed with the AIT&AIS'2026 organising committee
> (travel is unsafe under constant missile and drone attacks). Event: 8-9 Dec 2026.

## 1. The paper in one paragraph

A companion paper to MAKE 8(7):181. The SEMTRA pipeline (cited, condensed) is applied to a neural failure-mode classifier on the
UCI AI4I 2020 predictive-maintenance benchmark, whose failure modes have documented generating rules. The paper asks two new
questions: (1) do the rough-set rules extracted through the embedding-to-concept transition recover the documented physics
(thresholds, concepts) and ignore distractor concepts; (2) does disagreement between the rules and the MLP flag the MLP's errors,
compared with its own max-probability, as a human-review triage for decision support. Because the rulebook as published in MAKE
collapses to the majority class at 97:3 imbalance, the paper also contributes a class-reduct rulebook (one class-specific reduct
and rule set per failure mode, 'none' as the default class; decision 32). Answers (test stage, `09_ai4i_results.md`): with true
concepts the documented physics is recovered exactly in 5/5 seeds; through the MLP embedding it is recovered only partly, because
small transition errors blur narrow failure regions; rule flags complement max-probability at a matched review budget. Working
title: "Do Extracted Rules Recover the Physics? Rough-Set Auditing and Error Triage for Neural Predictive-Maintenance Models".
CMT topic 7 "Artificial Intelligence for Industrial Monitoring and Predictive Maintenance" (secondary 1 "Computational
Intelligence and Machine Learning Methods").

**Status 2026-10-23:** the experiment is complete in `E:\GitHub\semtra-ai4i` (frozen `PROTOCOL.md`, `RESULTS.md`, tables
T1-T4, plots F2-F4, F1 component list). The specification below is what was run.

## 2. Experiment specification (Claude; defaults the author may override)

| Item | Specification |
|------|---------------|
| Data | AI4I 2020 CSV from UCI (SHA-256 in `PROTOCOL.md`). Labels: none, HDF, PWF, OSF, TWF; dropped 19 RNF and 23 multi-mode rows; kept 9,958 (none 9652, HDF 106, PWF 80, OSF 78, TWF 42) |
| Splits | Stratified 60/20/20 train/validation/test, 5 seeds |
| Model | scikit-learn `MLPClassifier` (2 hidden layers of 64, ReLU) on standardised raw inputs (type one-hot, air temp, process temp, speed, torque, tool wear); minority classes oversampled in training; embedding = last hidden layer computed from `coefs_` (no torch) |
| Concepts | Rule-relevant: ΔT, speed, torque, power = torque·ω, tool wear, strain = wear·torque, product type. Distractors: raw air temp, raw process temp, one pure-noise sensor |
| Transition | The MAKE estimator `fit_transition`: scaling without centring, TruncatedSVD (at most 64 components, so 63 on a 64-d embedding), ridge with α in {0.01 ... 100} chosen by validation MAE (reuse map in `02_project_inventory.md`) |
| Rules | WEDD `wedd_thresholds` (λ_H 0.65, depth 2); MAKE rulebook `induce_rules` + conflict-aware inference unchanged (τ 0.84; s_min by the MAKE runner's formula max(8, min(18, ⌊0.002·n_train⌋)) = 11 for 5,974 training rows, not AwA2's 18; fallback 0.45; conflict margin 0.05); class-reduct rulebook on the same WEDD states (decision 32). `PROTOCOL.md` records every value actually used, because the MAKE text and the scripts disagree on some (e.g. Hamming fallback) |
| Baselines | Both rulebooks on true concepts (upper bound); depth-limited CART on the same predicted concepts (depth tuned on validation); MLP max-probability for triage |
| Metrics | Per-concept R²/MAE; concept-set Jaccard and threshold error in physical units vs documented rules; rule count, conditions per rule, coverage, fidelity to MLP, macro-F1, per-mode recall; triage AUROC, AURC, error recall at 5%/10%, budget-matched error catches, confident errors flagged |
| Freeze | Protocol and hyperparameters fixed on validation and written to `PROTOCOL.md` before any test evaluation |
| Outputs | Delivered 2026-10-23 in `E:\GitHub\semtra-ai4i\outputs`: tables T1-T4 (CSV, Markdown), data plots F2-F4 (PDF+SVG, house style), a component list for F1 in `RESULTS.md` §8 (the author draws F1), results memo `RESULTS.md` with every number and its source file; digest in `09_ai4i_results.md` |

## 3. Timeline (today Thu 22 Oct; 5 working days)

| Date | Claude | Author |
|------|--------|--------|
| Thu 22 Oct | Done: knowledge-base revision; project venv; AI4I download; local repo skeleton | Download the AIT&AIS CEUR-ART ODT; start sections 1-2 |
| Fri 23 Oct | Done: pipeline port; validation runs; `PROTOCOL.md` frozen; test runs; T1-T4, F2-F4, F1 component list, `RESULTS.md` (one day ahead of plan) | Sections 1-3 (Claude reviews as they land); make sure all three authors have CMT accounts |
| Sat 24 Oct | Review sections 1-3 as they arrive; reference DOI verification | Section 4 from `PROTOCOL.md` and section 5 from `RESULTS.md`; draw F1 |
| Sun 25 Oct | Review sections 4-7; claims vs artifacts; overlap check vs MAKE and ICyberPhyS; reference DOI verification | Sections 4-7 and references; **full draft to Barmak and Krak in the evening** |
| Mon 26 Oct | Final review pass; list of tools and uses for the GenAI declaration (the author words it); anonymous mirror live | Co-author feedback by midday; fixes; anonymise; export PDF; **register in CMT and submit** |
| Tue 27 Oct | Buffer: help replace the PDF in CMT if needed | **Hard limit: submission complete before 28 Oct** |
| 28 Oct - 30 Nov | Prepare the online talk early: slides plus a backup recording | Wait for notification |
| 1 Dec | - | Notification |
| After 1 Dec | Camera-ready support | Camera-ready; **Radiuk presents online on 8-9 Dec** |

If the work runs late, cut scope in this order and never cut the 5 seeds or the frozen protocol: (1) fold T4 into the F3
caption and text, (2) turn F4 into a column of T1, (3) shorten Related work to 1 page.

## 4. Pre-submission checklist

- [ ] Submitted in CMT before 28 Oct 2026 (target 26 Oct)
- [ ] Organisers' confirmation of the online talk kept with the submission records
- [ ] AIT&AIS CEUR-ART 1-column ODT template (URL in `03_aitais_venue.md`)
- [ ] At least 10 pages (target 12), last page at least 80% full, no page numbers
- [ ] Title in CEUR capitalisation; abstract and keywords new (no ICyberPhyS or MAKE sentences)
- [ ] Review PDF anonymised: no names, affiliations, emails, ORCIDs; ODT metadata scrubbed (File > Properties, and Tools > Options > Security: remove personal information on saving); MAKE and CARDIA-X cited in the third person; code link is the anonymous mirror
- [ ] MAKE cited as the method source in Introduction and Method; no MAKE numbers presented as results
- [ ] n-gram overlap vs MAKE and ICyberPhyS below ~10% for every passage
- [ ] Every number traced to a file in the experiment repo
- [ ] ~30 references, DOIs verified, at most 4 self-citations
- [ ] Figures F1-F4 new, captions below, alt text; tables T1-T4, captions above
- [ ] AI4I described as synthetic in the Discussion; no "guarantee safety" or uncited superiority claims
- [ ] Declaration on Generative AI (CEUR taxonomy terms in `05_icyberphys_ceur.md`, every tool actually used); no AI-written paragraphs, captions or alt text; F1 drawn by the authors; AI-assisted code described in plain words
- [ ] Code and data availability statement linking the anonymous mirror https://anonymous.4open.science/r/semtra-ai4i-CD9B (live since 2026-10-23, expires 31 Jan 2027; private repo https://github.com/radiukpavlo/semtra-ai4i; if the code changes before submission, update the mirror to the new commit)
- [ ] PDF exported from LibreOffice with all fonts embedded
- [ ] CMT: topic 7 primary (1 secondary), all three authors entered, Barmak's PC conflict declared
- [ ] Camera-ready (later): de-anonymise, make `semtra-ai4i` public and link it, restore the MAKE commit hash in `src/semtra_core.py`, ORCIDs, CC BY 4.0 footnote, AIT&AIS'2026 event footnote, current CEUR author agreement (NTP, no third-party material)

## 5. Risks

| Risk | Mitigation |
|------|------------|
| Five-day window | Results delivered 23 Oct (one day early); scope-cut order in section 3; submit on 26 Oct, keep 27 Oct as buffer |
| Deadline time zone unknown | Never plan on the evening of 27 Oct |
| Weak or partial rule recovery | Happened for predicted concepts (HDF 1/5 seeds); reported as an audit finding with the true-concept upper bound (decision 21) |
| Reviewers see the class-reduct rulebook as tuned to the answer | `PROTOCOL.md` §6 documents the validation-only design history; settings reused from MAKE; frozen before test |
| Online talk disrupted by an air-raid alert, power or internet outage | Pre-recorded backup video sent to the organisers in advance; UPS and mobile hotspot; agree a fallback slot with the session chair |
| Shared PC members recognise the ICyberPhyS paper | New data, new results, new text; MAKE cited |
| Reviewers dismiss AI4I as synthetic | Frame as a ground-truth audit benchmark; state it in the Discussion |
| Blinding leaks via the repo or MAKE | Separate repo, anonymous mirror, third-person citations |
| Environment gaps (no packages, no data) | uv venv; AI4I is a single small CSV |
