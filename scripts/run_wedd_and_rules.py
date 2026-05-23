#!/usr/bin/env python3
"""Run AwA2 Protocol A, including WEDD discretization and rough-set rules."""
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
    awa2 = load_awa2(maybe_extract_awa2(args.awa2_zip, out / "artifacts" / "_tmp" / "awa2"))
    result = run_awa2_protocol_a(awa2, out, n_components=args.n_components)
    print({"rule_count": result["summary"]["rule_count"], "coverage": result["summary"]["rule_test_coverage"]})


if __name__ == "__main__":
    main()
