#!/usr/bin/env python3
from __future__ import annotations
import json, csv, re, hashlib, datetime
from pathlib import Path

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()

def main():
    root=Path(__file__).resolve().parents[1]
    manuscript=root/'manuscript'
    audit=root/'audit'; audit.mkdir(exist_ok=True)
    required=['manuscript/manuscript.tex','manuscript/references.bib','manuscript/manuscript.pdf','manuscript/manuscript.bbl','manuscript/Definitions','figs','tables','scripts','artifacts','audit','source_notes','README.md','revision_report.md']
    presence={r:(root/r).exists() for r in required}
    refs=len(re.findall(r'^@', (manuscript/'references.bib').read_text(encoding='utf-8'), flags=re.M))
    figs=len(list((root/'figs').glob('*.pdf')))
    tables=len(list((root/'tables').glob('table_*.tex')))
    matrix=root/'audit'/'reviewer_response_matrix.csv'
    statuses=[]
    if matrix.exists():
        with matrix.open(newline='',encoding='utf-8') as f:
            statuses=[r['status'] for r in csv.DictReader(f)]
    compile_status=(root/'audit'/'revision_compile_status.txt').read_text().strip() if (root/'audit'/'revision_compile_status.txt').exists() else 'unknown'
    pdf_pages=len(list((root/'audit'/'pdf_renders').glob('page-*.png')))
    manuscript_text=(manuscript/'manuscript.tex').read_text(encoding='utf-8')
    title_match=re.search(r'\\Title\{([^}]*)\}', manuscript_text)
    manuscript_title=title_match.group(1) if title_match else 'unknown'
    fig19_svg=(root/'figs'/'fig19_baseline_tradeoff_scatter.svg').read_text(encoding='utf-8') if (root/'figs'/'fig19_baseline_tradeoff_scatter.svg').exists() else ''
    attr_csv=root/'tables'/'complete_semantic_attribute_diagnostics.csv'
    attr_count=0
    if attr_csv.exists():
        with attr_csv.open(newline='',encoding='utf-8') as f:
            attr_count=max(0, sum(1 for _ in csv.reader(f))-1)
    checks={
        'required_files_present': all(presence.values()),
        'reviewer_rows_30': len(statuses)==30,
        'no_pending_status': all(s!='pending' for s in statuses),
        'references_at_least_35': refs >= 35,
        'figures_at_least_10': figs >= 10,
        'tables_at_least_12': tables >= 12,
        'compile_success': compile_status == '0 0 0 0',
        'pdf_rendered': pdf_pages >= 1,
        'no_paragraph_command': '\\paragraph' not in manuscript_text,
        'tradeoff_axes_aligned': 'Rulebook Coverage' in fig19_svg and 'Covered Fidelity' in fig19_svg and 'Accuracy on covered cases' not in fig19_svg,
        'control_knob_sensitivity_present': 'tab:control_knob_sensitivity' in manuscript_text and (root/'tables'/'table_control_knob_sensitivity.tex').exists(),
        'complete_attribute_table_85_rows': attr_count == 85 and 'tab:complete_semantic_attributes' in manuscript_text,
        'trace_table_not_figure': 'tab:traces' in manuscript_text and 'fig:traces' not in manuscript_text,
        'hardware_note_present': 'NVIDIA RTX 3090 GPU' in manuscript_text and 'Intel Core i9-10900K CPU' in manuscript_text,
        'sota_framing_present': '2024 zero-shot learning leaderboards' in manuscript_text and 'foundational attribute-transfer models' in manuscript_text,
        'semantic_rupture_mitigation_present': 'Large Language Models (LLMs)' in manuscript_text and 'outlier classes' in manuscript_text,
        'gaussian_perturbation_present': 'perturbed' in manuscript_text and '\\mathcal{N}' in manuscript_text and '\\sigma^2' in manuscript_text,
    }
    limitations=[
        'No original CNN logits or fine-tuned end-to-end CNN were supplied; a deterministic base predictor was trained on representation features.',
        'TCAV is performed at the released representation layer because raw activation stacks are not supplied.',
        'AwA2 semantic attributes are class-level rather than object-level.'
    ]
    failed=[k for k,v in checks.items() if not v]
    score=100 if not failed else max(0, 100-4*len(failed))
    out={
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'package_path': str(root),
        'manuscript_title': manuscript_title,
        'presence': presence,
        'reference_count': refs,
        'figure_pdf_count': figs,
        'table_tex_count': tables,
        'reviewer_response_status_counts': {s:statuses.count(s) for s in sorted(set(statuses))},
        'compile_status': compile_status,
        'pdf_rendered_pages': pdf_pages,
        'checks': checks,
        'quality_gate_score_out_of_100': score,
        'score_rationale': 'Reviewer-targeted revision checks pass.' if score == 100 else 'Some reviewer-targeted revision checks failed: ' + ', '.join(failed),
        'documented_limitations': limitations,
        'key_artifact_hashes': {p: sha256(root/p) for p in ['manuscript/manuscript.tex','manuscript/references.bib','manuscript/manuscript.pdf','manuscript/manuscript.bbl','revision_report.md'] if (root/p).exists()}
    }
    (audit/'revision_final_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
