#!/usr/bin/env python3
"""Rewrite long TeX tables to MDPI-friendly wrapped layouts after table generation."""
from __future__ import annotations
import argparse
from pathlib import Path

EXAMPLE_RULES = r'''\begin{table}[H]
\caption{Representative induced production rules from AwA2 Protocol A.\label{tab:example_rules}}
\begin{adjustwidth}{-\extralength}{0cm}
\centering
\small
\begin{tabularx}{\fulllength}{l>{\raggedright\arraybackslash}Xlrr}
\toprule
Rule & Antecedent & Class & Support & Confidence \\
\midrule
R0001 & paws=s2 AND hunter=s2 AND small=s0 AND yellow=s2 & tiger & 115 & 0.896 \\
R0002 & stripes=s2 AND hooves=s1 AND paws=s3 AND hands=s1 AND small=s0 AND furry=s2 & tiger & 63 & 0.873 \\
R0003 & stripes=s1 AND hooves=s3 AND paws=s0 AND hands=s0 AND small=s1 AND yellow=s1 & antelope & 132 & 0.871 \\
R0004 & hunter=s0 AND water=s0 AND small=s0 AND jungle=s2 AND yellow=s1 & zebra & 434 & 0.866 \\
R0005 & hooves=s1 AND swims=s0 AND paws=s2 AND small=s0 AND furry=s1 & tiger & 163 & 0.865 \\
R0006 & paws=s3 AND hunter=s1 AND water=s1 AND small=s1 AND furry=s3 & giant panda & 160 & 0.863 \\
\bottomrule
\end{tabularx}
\end{adjustwidth}
\end{table}
'''

SYNTHETIC_GT = r'''\begin{table}[H]
\caption{Synthetic benchmark ground-truth rule dictionary.\label{tab:synthetic_ground_truth}}
\begin{adjustwidth}{-\extralength}{0cm}
\centering
\small
\begin{tabularx}{\fulllength}{l>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X}
\toprule
Class & Ground-truth rule & Numeric cut summary \\
\midrule
1 & \(b_1\) high and \(b_3\) low & \(b_1>0.70\); \(b_3<0.35\) \\
2 & \(b_2\) medium and \(b_5\) high & \(0.35<b_2\leq0.65\); \(b_5>0.70\) \\
3 & \(b_4\) low, \(b_6\) high, and \(b_8\) medium & \(b_4<0.35\); \(b_6>0.70\); \(0.35<b_8\leq0.65\) \\
4 & \(b_7\) high and \(b_9\) low & \(b_7>0.70\); \(b_9<0.35\) \\
\bottomrule
\end{tabularx}
\end{adjustwidth}
\end{table}
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    tables = Path(args.out).resolve() / "tables"
    (tables / "table_example_rules.tex").write_text(EXAMPLE_RULES, encoding="utf-8")
    (tables / "table_synthetic_ground_truth.tex").write_text(SYNTHETIC_GT, encoding="utf-8")
    print({"fixed": ["table_example_rules.tex", "table_synthetic_ground_truth.tex"]})


if __name__ == "__main__":
    main()
