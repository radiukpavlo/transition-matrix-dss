# Reproducibility Notes

## Minimal Public Rebuild

With the checked-in artifacts available, regenerate enhanced public figures and tables:

```bash
python scripts/generators/generate_enhanced_results.py --root .
```

Then compile the manuscript:

```bash
cd manuscript
pdflatex -interaction=nonstopmode manuscript.tex
bibtex8 manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

## Full Experiment Rebuild

Place local dataset archives in ignored storage:

```text
data/raw/awa2.zip
data/raw/xlsa17.zip
```

Run:

```bash
python run_experiments.py --awa2_zip data/raw/awa2.zip --xlsa17_zip data/raw/xlsa17.zip --out . --seed 42 --local_sample_size 1000
```

## Public-Release Checklist

- Keep source code, manuscript sources, figures, tables, public artifacts, and audit evidence tracked.
- Keep raw datasets, private notes, credentials, and temporary extraction directories untracked.
- Re-run `python scripts/utils/audit_revision_package.py` before release.
- Recompile `manuscript/manuscript.tex` after changing tables, figures, bibliography, or manuscript text.
