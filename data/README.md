# SEMTRA Dataset Workspace and Reproducibility Specifications

This directory acts as the local data workspace for reproducing the experiments in the **SEMTRA (Semantic Transition Matrix and Rough-Set Rules for Explainable AI)** reproduction package.

---

## 📁 Workspace Policy and Version Control

To comply with licensing and storage boundaries, the public repository does not include raw downloaded archives, clinical/private files, or non-redistributable derived data. The following directories are governed by our [Gitignore Configuration](../.gitignore) and are kept local to this folder:

* `data/raw/` — Raw downloaded datasets, archives (`.zip`, `.tar.gz`), and unpack directories.
* `data/private/` — Local developer notes or private configurations.
* `data/derived_private/` — Intermediate precomputed matrices or logs.
* `data/tmp/` — Temporary files and cache folders.

Precomputed, public-facing evaluation metrics and rulebooks are checked into version control under the [artifacts/](../artifacts) folder.

---

## 📊 Dataset Breakdown

The project utilizes several standard datasets to validate semantic projection, weighted entropy-density discretization (WEDD), and rough-set symbolic rule induction.

### 1. Animals with Attributes 2 (AwA2)
* **Location**: `data/raw/awa2/` (and packed as `data/raw/awa2.zip`)
* **Overview**: A computer vision benchmark for attribute-based classification and zero-shot learning. It contains **37,322 images** from **50 animal categories** annotated with **85 binary and continuous attributes**.
* **Key Files**:
  * `classes.txt`: Mapping of 50 animal category names to 1-based class indices.
  * `predicates.txt`: List of the 85 semantic attributes (e.g., `stripes`, `hooves`, `swims`, `paws`, `hunter`, etc.).
  * `predicate-matrix-continuous.txt`: A $50 \times 85$ matrix representing continuous association strengths of attributes per class.
  * `predicate-matrix-binary.txt`: A $50 \times 85$ binary matrix created by thresholding the continuous values.
  * `Features/ResNet101/AwA2-features.txt`: Raw image features ($37,322 \times 2,048$) extracted from the `pool5` layer of a pretrained ResNet-101.
  * `Features/ResNet101/AwA2-filenames.txt`: Lists the original image filenames mapped to the row indices of the features file.
  * `Features/ResNet101/AwA2-labels.txt`: Labels matching each feature row to its class index.
* **Optimized Formats**:
  For performance, the extraction/ingestion pipeline caches these raw text tables into fast-loading Apache Parquet files (e.g., `AwA2-features.parquet`, `AwA2-labels.parquet`) within the `artifacts/_tmp_awa2` workspace during runtime.
* **Usage**:
  * **Protocol A**: Random train/val/test split of seen classes to fit the transition matrix $T$ and evaluate rule accuracy and coverage.
  * **Protocol B**: Evaluates generalization on unseen animal classes.
* **License**: CC BY-NC-ND 4.0 (Creative Commons Attribution-NonCommercial-NoDerivatives). Dr. Christoph Lampert/CVML IST Austria.

### 2. Standard Zero-Shot Learning Proposed Splits (xlsa17)
* **Location**: `data/raw/xlsa17/` (and packed as `data/raw/xlsa17.zip`)
* **Reference**: Y. Xian, B. Schiele, Z. Akata. *"Zero-shot Learning - The Good, the Bad and the Ugly"*, IEEE CVPR 2017.
* **Supported Datasets**: Contains standard zero-shot splits under `data/raw/xlsa17/data/` for:
  * **APY** (Attribute Pascal and Yahoo)
  * **AWA1** (Animals with Attributes 1)
  * **AWA2** (Animals with Attributes 2 - standard proposed split)
  * **CUB** (Caltech-UCSD Birds 200-2011)
  * **ImageNet** (large-scale image database)
  * **SUN** (Scene Understanding database)
* **Data Organization**:
  * `res101.mat`: MATLAB file with deep ResNet-101 features, labels, and image filenames.
  * `att_splits.mat`: MATLAB file containing:
    * `att` / `original_att`: Normalised and raw class-level attribute matrices.
    * `trainval_loc`: Instance indexes of the train+val set (seen classes).
    * `test_seen_loc` / `test_unseen_loc`: Indexes for seen and unseen classes in the test partition.
  * Split text files: Class listings separating seen (`trainvalclasses.txt`) from unseen (`testclasses.txt`).
* **Python Indexing Conversion**:
  The script [run_official_xlsa_protocol.py](../scripts/experiments/run_official_xlsa_protocol.py) maps the 1-based MATLAB indices in `att_splits.mat` to 0-based Python row indices, matching them against the corresponding parquet feature rows.
* **Usage**: Used to run Protocol B under the official evaluation split proposed by Xian et al.

### 3. Dermatology 7-Point Checklist (Derm7pt)
* **Location**: `data/raw/Derm7pt/`
* **Overview**: A clinical skin lesion dataset containing clinical and dermoscopic images along with structured annotations for the 7-point checklist.
* **Key Files**:
  * `meta/meta.csv`: Metadata table with clinical and dermoscopic attributes.
  * `meta/train_indexes.csv`, `meta/valid_indexes.csv`, `meta/test_indexes.csv`: Official partitions.
  * `images/`: Image files of skin lesions.
* **Scope boundary**: This methodology package focuses on a general, non-medical XAI paradigm. While the raw dataset is retained locally under the workspace boundaries, it is excluded from the active manuscript and public runner scripts (focusing instead on general benchmarks like AwA2).
* **License**: CC BY-NC-ND 4.0. Dr. Giuseppe Argenziano (http://derm.cs.sfu.ca/).

### 4. SUN Scene Attribute Database
* **Location**: `data/raw/sun/`
* **Archives**:
  * `SUNAttributeDB.tar.gz`: Text and mat attribute databases.
  * `SUNAttributeDB_Images.tar.gz`: Raw images.
  * `sceneattributepredictor.zip`: Predetermined predictors.

---

## 📈 Mathematical Representation Formats

During experiment execution, the datasets are formatted into matrices corresponding to the SEMTRA framework layer boundaries:

1. **Representation Matrix ($A$)**:
   The input matrix of latent representations, where $A \in \mathbb{R}^{N \times D}$ ($D=2048$ for ResNet-101 features). For tractability, SVD projects this to $X \in \mathbb{R}^{N \times d}$ ($d=192$ or $64$).
2. **True Concept Matrix ($B$)**:
   The ground-truth concept matrix, where $B \in \mathbb{R}^{N \times M}$ ($M=85$ attributes). The continuous class-attribute matrix is scaled to $[0, 1]$.
3. **Transition Operator ($T$)**:
   A linear matrix $T \in \mathbb{R}^{d \times M}$ fitted via Ridge regression to map deep representations onto reconstructed semantic concepts $\hat{B} = X \cdot T + \text{intercept}$.
4. **Discretized Concept Signatures ($Z$)**:
   Quantized vectors $Z \in \{0, 1, 2\}^M$ generated using WEDD thresholds. These feed into rough-set granule generation.

---

## ⚙️ Acquisition and Setup Instructions

To reproduce all experiments from scratch:

1. **Download Raw Data**:
   * Obtain the **AwA2** dataset features and attributes from the [CVML IST Austria AwA2 page](https://cvml.ist.ac.at/AwA2/).
   * Obtain the **xlsa17** proposed splits and features from the [MPI Informatics Zero-Shot Learning benchmark page](http://d2.mpi-inf.mpg.de/zero-shot-learning/).

2. **File Placement**:
   Place the downloaded archives into the `data/raw/` directory:
   * `data/raw/awa2.zip`
   * `data/raw/xlsa17.zip`

3. **Execution**:
   Run the full replication suite using the orchestration wrapper:
   ```bash
   python run_experiments.py \
     --awa2_zip data/raw/awa2.zip \
     --xlsa17_zip data/raw/xlsa17.zip \
     --out .
   ```
