#!/usr/bin/env python3
"""Orchestrate revision experiments for the Paper 1 PoC XAI manuscript package."""
from __future__ import annotations
import argparse, subprocess, sys, json, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

def run(cmd, log_path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    t0=time.time()
    with log_path.open('w') as fh:
        fh.write('$ ' + ' '.join(map(str,cmd)) + '\n')
        fh.flush()
        p=subprocess.run([str(x) for x in cmd], stdout=fh, stderr=subprocess.STDOUT, cwd=SCRIPT_DIR.parent)
    return {'command':' '.join(map(str,cmd)), 'log':str(log_path), 'returncode':p.returncode, 'seconds':time.time()-t0}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--awa2_zip', default='/mnt/data/awa2.zip')
    ap.add_argument('--xlsa17_zip', default='/mnt/data/xlsa17.zip')
    ap.add_argument('--out', default=str(SCRIPT_DIR.parent))
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--local_sample_size', type=int, default=1000)
    args=ap.parse_args()
    out=Path(args.out).resolve(); audit=out/'audit'; py=sys.executable
    commands=[
        [py,'scripts/experiments/train_base_predictor.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_local_xai_baselines.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed),'--sample_size',str(args.local_sample_size)],
        [py,'scripts/experiments/run_cbm_tcav_baselines.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_symbolic_baselines.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_discretizer_ablation.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_transition_operator_ablation.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_rule_stability.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/experiments/run_official_xlsa_protocol.py','--awa2_zip',args.awa2_zip,'--xlsa17_zip',args.xlsa17_zip,'--out',str(out),'--seed',str(args.seed)],
        [py,'scripts/generators/generate_revision_tables.py'],
        [py,'scripts/generators/generate_revision_figures.py','--awa2_zip',args.awa2_zip,'--out',str(out),'--seed',str(args.seed)],
    ]
    results=[]
    for i,cmd in enumerate(commands,1):
        name=Path(cmd[1]).stem if len(cmd)>1 else f'cmd{i}'
        res=run(cmd,audit/f'revision_orchestrator_{i:02d}_{name}.log')
        results.append(res)
        if res['returncode']!=0:
            break
    summary={'status':'ok' if all(r['returncode']==0 for r in results) else 'failed','results':results}
    (audit/'run_revision_experiments_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    return 0 if summary['status']=='ok' else 1
if __name__=='__main__': raise SystemExit(main())
