#!/usr/bin/env python3
"""Audit generated Paper 1 PoC outputs and write a compact JSON report."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    out = Path(args.out).resolve()
    manuscript_dir = out / "manuscript"
    key_files = [
        manuscript_dir / "manuscript.tex",
        manuscript_dir / "references.bib",
        out / "artifacts" / "awa2" / "protocol_a_summary.json",
        out / "artifacts" / "awa2" / "protocol_b_summary.json",
        out / "artifacts" / "synthetic" / "synthetic_summary.json",
    ]
    report = {
        "figures_pdf": len(list((out / "figs").glob("*.pdf"))),
        "tables_tex": len(list((out / "tables").glob("table_*.tex"))),
        "artifacts_json": len(list((out / "artifacts").rglob("*.json"))),
        "key_file_hashes": {str(p.relative_to(out)): sha256(p) for p in key_files if p.exists()},
    }
    (out / "audit").mkdir(parents=True, exist_ok=True)
    with (out / "audit" / "artifact_audit.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print(report)


if __name__ == "__main__":
    main()
