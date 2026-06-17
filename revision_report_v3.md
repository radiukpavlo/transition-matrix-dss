# SEMTRA Revision v3 Report

Generated: 2026-06-17T11:45:20Z

## Completed Work

- Created `outputs/revision_v3/` without rewriting v1 or v2 artifacts.
- Exported enhanced prediction CSVs with true labels, base predictions, rule predictions, correctness flags, and fidelity flags.
- Generated object-level bootstrap intervals directly from enhanced prediction exports.
- Added SUN image hierarchy/category metadata from xlsa17 image paths joined to the official SUN Attribute Database image list.
- Replaced the Derm7pt handcrafted feature baseline with locked TorchVision ResNet-50 ImageNet-1K v2 dermoscopic-image features.
- Created v3 schemas, QC outputs, tables, LaTeX archive sync, and a submission bundle.

## Artifact Summary

- v3 artifact count: 128.
- Enhanced prediction summaries: 7.
- SUN category diagnostic rows: 645.
- Derm7pt diagnosis diagnostic rows: 7.

## QC Status

- Overall status: pass.
- Errors: none recorded.
- Warnings: none recorded.

## Remaining Limitations

- Derm7pt remains retrospective technical validation only; the ResNet-50 ImageNet encoder is locked and reproducible but not dermatology-specific clinical validation.
- SUN category diagnostics expose hierarchy-dependent weakness and should be inspected before strengthening portability claims.
- Object-level intervals depend on the generated prediction exports and do not replace external validation.

## Recommendations

- Keep enhanced prediction exports as the default format for future SEMTRA runs.
- Add a documented dermoscopy-specific encoder only if its checkpoint, preprocessing, license, and provenance are fully traceable.
- Use the SUN category diagnostics to guide targeted stress tests rather than broadening claims.
