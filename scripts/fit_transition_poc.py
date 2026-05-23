#!/usr/bin/env python3
"""Fit the AwA2 transition matrix and write reconstruction/prototype metrics."""
from __future__ import annotations
import argparse
from pathlib import Path
from paper1_core import maybe_extract_awa2, load_awa2
from run_all_experiments import run_awa2_protocol_a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--awa2_zip", default="/mnt/data/awa2.zip")
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--n_components", type=int, default=16)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    awa2_dir = maybe_extract_awa2(args.awa2_zip, out / "artifacts" / "_tmp" / "awa2")
    awa2 = load_awa2(awa2_dir)
    result = run_awa2_protocol_a(awa2, out, n_components=args.n_components)
    print(result["summary"])


if __name__ == "__main__":
    main()
