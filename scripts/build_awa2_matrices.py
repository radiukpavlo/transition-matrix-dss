#!/usr/bin/env python3
"""Build and audit AwA2 matrices used by the Paper 1 PoC experiments."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from paper1_core import maybe_extract_awa2, load_awa2, write_json, ensure_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--awa2_zip", default="/mnt/data/awa2.zip")
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    out = Path(args.out).resolve()
    tmp = ensure_dir(out / "artifacts" / "_tmp" / "awa2")
    awa2_dir = maybe_extract_awa2(args.awa2_zip, tmp)
    awa2 = load_awa2(awa2_dir)
    summary = {
        "A_shape": list(awa2.A.shape),
        "B_object_shape": list(awa2.B_obj_raw.shape),
        "B_class_shape": list(awa2.B_class_raw.shape),
        "n_classes": len(awa2.class_names),
        "n_predicates": len(awa2.predicate_names),
        "matrix_policy": "A is the representation matrix obtained through the trained ResNet-101 representation pipeline; cached trained representations are used for reproducibility.",
    }
    write_json(out / "audit" / "awa2_matrix_audit.json", summary)
    pd.DataFrame({"class_index": range(len(awa2.class_names)), "class_name": awa2.class_names}).to_csv(out / "artifacts" / "awa2" / "awa2_classes.csv", index=False)
    pd.DataFrame({"attribute_index": range(len(awa2.predicate_names)), "attribute_name": awa2.predicate_names}).to_csv(out / "artifacts" / "awa2" / "awa2_predicates.csv", index=False)
    print(summary)


if __name__ == "__main__":
    main()
