#!/usr/bin/env python3
"""SEMTRA Research Project Experiments Entry-Point Wrapper

This wrapper acts as the unified entry point for running the revision experiments.
It automatically resolves paths and forwards all command-line arguments to the
underlying orchestrator script located in scripts/runners/run_revision_experiments.py.
"""
from __future__ import annotations
import sys
import subprocess
from pathlib import Path

def main() -> None:
    root = Path(__file__).resolve().parent
    script_path = root / "scripts" / "runners" / "run_revision_experiments.py"
    
    # Forward all arguments to the actual runner
    cmd = [sys.executable, str(script_path)] + sys.argv[1:]
    
    # Execute and exit with the corresponding return code
    result = subprocess.run(cmd, cwd=str(root))
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
