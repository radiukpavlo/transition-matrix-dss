#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from figure_style import apply_nature_style, save_nature_figure
from revision_common import load_cache, read_thresholds, read_rulebook
from paper1_core import ensure_dir, quantize, infer_rules, class_mode_signatures

def first_rule(s):
    s=str(s)
    return s.split(';')[0] if s and s!='nan' else ''
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip'); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--n_components',type=int,default=64); ap.add_argument('--sigmas',default='0.00,0.01,0.025,0.05,0.10'); args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2'); figs=ensure_dir(out/'figs')
    apply_nature_style()
    rng=np.random.default_rng(args.seed)
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    attrs=pd.read_csv(art/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist(); thresholds=read_thresholds(out); rules=read_rulebook(out)
    Ztr=quantize(cache['Yhat_train'],attrs,thresholds); prot=class_mode_signatures(Ztr,cache['y_train'].astype(int),np.arange(50))
    Y=cache['Yhat_test'].copy(); std=np.maximum(np.std(Y,axis=0),1e-6)
    Z_base=quantize(Y,attrs,thresholds)
    baseline=infer_rules(Z_base,rules,prot,fallback_max_distance=0.50)
    base_pred=baseline['prediction'].to_numpy(dtype=int); base_rule=np.array([first_rule(x) for x in baseline['activated_rules']]); base_cov=base_pred>=0
    rows=[]
    for sigma in [float(x) for x in args.sigmas.split(',')]:
        if sigma==0: Yp=Y.copy()
        else: Yp=np.clip(Y + rng.normal(0,sigma,size=Y.shape)*std,0,1)
        Z=quantize(Yp,attrs,thresholds); pred=infer_rules(Z,rules,prot,fallback_max_distance=0.50)
        pp=pred['prediction'].to_numpy(dtype=int); rr=np.array([first_rule(x) for x in pred['activated_rules']]); cov=pp>=0
        denom=base_cov & (base_rule!='')
        rule_cons=float(np.mean(rr[denom]==base_rule[denom])) if denom.any() else float('nan')
        dec_cons=float(np.mean(pp[base_cov]==base_pred[base_cov])) if base_cov.any() else float('nan')
        rows.append({'sigma':sigma,'rule_consistency':rule_cons,'decision_consistency':dec_cons,'coverage':float(cov.mean()),'coverage_change':float(cov.mean()-base_cov.mean()),'abstention':float(1-cov.mean()),'conflict_rate':float(pred['conflict'].mean()),'non_abstained_baseline_objects':int(base_cov.sum())})
    df=pd.DataFrame(rows); df.to_csv(art/'rule_stability_noise.csv',index=False)
    plt.figure(figsize=(5.5,3.4))
    plt.plot(df['sigma'],df['rule_consistency'],marker='o',label='Rule consistency')
    plt.plot(df['sigma'],df['decision_consistency'],marker='s',label='Decision consistency')
    plt.xlabel('Gaussian noise sigma')
    plt.ylabel('Consistency')
    plt.ylim(0,1.05); plt.grid(True,alpha=.3); plt.legend(frameon=False); plt.tight_layout()
    save_nature_figure(plt.gcf(), figs/'fig16_rule_stability_noise.pdf')
    print(json.dumps({'status':'ok','rows':len(df)},indent=2))
if __name__=='__main__': main()
