#!/usr/bin/env python3
"""Run the controlled synthetic benchmark for the Paper 1 PoC manuscript."""
from __future__ import annotations
import argparse
from pathlib import Path
from run_all_experiments import run_synthetic_benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--seeds", type=int, default=5)
    args = parser.parse_args()
    result = run_synthetic_benchmark(Path(args.out).resolve(), n_seeds=args.seeds)
    print(result["summary"])


if __name__ == "__main__":
    main()
