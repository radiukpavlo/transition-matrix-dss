# Revision Run Outputs Directory

This directory stores the outputs, logs, tables, figures, and compiled LaTeX PDFs generated across the different revision cycles.

---

## 📁 Directory Structure

### 1. [revision_v1/](file:///d:/GitHub/transition-matrix-dss/outputs/revision_v1)
Contains the initial results and diagnostics generated for the revision response.
* **`awa2/`**: Baseline results, discretizer comparison summaries, and q-sensitivity tables.
* **`synthetic/`**: Noise degradation summary tables.
* **`tables/`**: LaTeX tables prepared for the manuscript.
* **`figs/`**: Figure outputs generated from v1 experiments.

### 2. [revision_v2/](file:///d:/GitHub/transition-matrix-dss/outputs/revision_v2)
Houses the hardened metrics, quality control validations, and bootstrap checks.
* **`qc/`**: Output files from automated schema validations and consistency check logs.
* **`statistics/`**: Paired discretizer effect sizes and bootstrap interval calculations.
* **`latex/`**: First draft LaTeX build logs.

### 3. [revision_v3/](file:///d:/GitHub/transition-matrix-dss/outputs/revision_v3)
Houses the final, auditable publication package, which incorporates the locked deep feature encoder on Derm7pt, SUN image/category hierarchies, and finalized PDF builds.
* **`awa2/`**: Enhanced prediction exports across seeds.
* **`sun/`**: Image metadata manifest, category hierarchies, and failure mode reviews.
* **`derm7pt/`**: Encoded ResNet-50 ImageNet1K features parquet file (`derm7pt_resnet50_imagenet1k_v2_features.parquet`), classification/concept diagnostics, and limitations statements.
* **`statistics/`**: Comprehensive object-level bootstrap intervals.
* **`latex/`**: Final compiled main paper (`main.pdf`) and supplementary material (`supply.pdf`) with full build logs.
* **`submission_bundle/`**: A finalized, self-contained sub-package that isolates all public LaTeX papers and vector figures while leaving raw private dataset files out.

---

## ⚙️ Tracking Status
Like the raw datasets, this outputs directory is excluded from version control under the `outputs/` gitignore pattern to keep the git index focused on source code, precomputed artifacts, and final document sheets.
