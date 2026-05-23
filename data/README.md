# Data Workspace

This directory is for local data needed to reproduce the experiments.

The public repository should not include raw downloaded archives, private files, credentials, or non-redistributable derived data. The `.gitignore` keeps these local folders out of git:

- `data/raw/`
- `data/private/`
- `data/derived_private/`
- `data/tmp/`

Expected local archives for the full pipeline:

- `data/raw/awa2.zip`
- `data/raw/xlsa17.zip`

The checked-in `artifacts/` directory contains public computed outputs used by the manuscript.
