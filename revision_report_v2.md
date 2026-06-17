# SEMTRA Revision v2 Report

Generated: 2026-06-16T21:30:22Z

## Completed Work

- Created a v2 artifact bundle under `outputs/revision_v2/` while preserving `outputs/revision_v1/`.
- Added machine-readable schemas, v1 baseline validation, package/git status capture, file hashes, and a v2 manifest.
- Added automated claim-gating metadata and manuscript claim consistency checks for the central numeric and wording constraints.
- Added bootstrap and paired WEDD-vs-MDLP interval diagnostics without rewriting v1 results.
- Added SUN class-level stress-test diagnostics and Derm7pt diagnosis/concept diagnostics.
- Created a clean submission bundle with manuscript sources, generated tables, final PDFs/logs when available, referenced figures, and a bundle manifest.

## Artifact Summary

- v2 artifact count: 101.
- Bootstrap interval rows: 38.
- Paired discretizer interval rows: 6.
- SUN diagnostic rows: 645.
- Derm7pt diagnosis diagnostic rows: 7.

## QC Status

- Overall status: pass.
- Errors: none recorded.
- Warnings: none recorded.

## Remaining Limitations

- SUN remains a stress-test/portability result; the v2 diagnostics expose class-dependent coverage and conflict rather than converting SUN into a competitive benchmark.
- Derm7pt remains retrospective technical validation only. The simple image-feature baseline is reproducible but not a clinical validation pipeline.
- Object-level bootstrap intervals are limited to fields exported by v1 prediction files; base-model labels are not present in those prediction exports, so object-level covered-fidelity intervals are intentionally absent.
- Seed-wise intervals are based on the completed v1 seed set and should be interpreted as stability diagnostics.

## Recommendations

- Export true labels and base-model predictions in future prediction CSVs so object-level accuracy and fidelity confidence intervals can be generated directly.
- For SUN, add category metadata beyond class names where available and inspect low-coverage/high-conflict classes before strengthening portability claims.
- For Derm7pt, replace the simple handcrafted baseline with a locked, documented dermoscopic encoder and keep official case-level splits.
- Keep WEDD wording as a tunable discretization option unless a larger paired study demonstrates robustness across datasets and metrics.
- Preserve the submission bundle as the shareable artifact while keeping `manuscript/` ignored.
