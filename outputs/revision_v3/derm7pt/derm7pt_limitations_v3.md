# Derm7pt v3 Limitations

Derm7pt v3 replaces the handcrafted color/histogram baseline with a locked TorchVision ResNet-50 ImageNet-1K v2 encoder applied to dermoscopic images.

The encoder is not dermatology-specific and is not a clinical diagnostic model. Results remain retrospective technical-validation outputs using the official case-level train/validation/test splits.

Clinical validation, prospective evaluation, calibration, subgroup fairness, and reader-study comparisons remain out of scope.
