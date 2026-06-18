#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, textwrap, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from figure_style import apply_style, save_nature_figure
from revision_common import load_cache, read_thresholds, read_rulebook
from paper1_core import ensure_dir, quantize, infer_rules, class_mode_signatures

def first_rule(s: object) -> str:
    s = str(s)
    return s.split(';')[0] if s and s != 'nan' else ''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--awa2_zip', default='/mnt/data/awa2.zip')
    ap.add_argument('--out', default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--n_components', type=int, default=64)
    args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2'); figs=ensure_dir(out/'figs')
    apply_style()
    # Coverage-abstention-confidence tradeoff. Recompute inference as the rule-confidence cutoff changes.
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    attrs=pd.read_csv(art/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist()
    thresholds=read_thresholds(out); rules=read_rulebook(out)
    Ztr=quantize(cache['Yhat_train'],attrs,thresholds)
    prot=class_mode_signatures(Ztr,cache['y_train'].astype(int),np.arange(50))
    Zte=quantize(cache['Yhat_test'],attrs,thresholds)
    y=cache['y_test'].astype(int)
    base=pd.read_csv(art/'base_predictor_predictions.csv')
    base_pred=base[base['split']=='test']['base_prediction'].to_numpy(dtype=int)
    rows=[]
    for tau in np.linspace(0.0,0.95,20):
        rsub=rules[rules['confidence'].astype(float)>=tau].copy()
        if len(rsub)==0:
            rows.append({'confidence_threshold':tau,'rule_count':0,'coverage':0.0,'abstention':1.0,'accuracy_all':0.0,'covered_accuracy':np.nan,'covered_fidelity':np.nan,'all_fidelity':0.0})
            continue
        pred=infer_rules(Zte,rsub,prot,fallback_max_distance=0.50)
        pp=pred['prediction'].to_numpy(dtype=int); cov=pp>=0
        rows.append({'confidence_threshold':float(tau),'rule_count':int(len(rsub)),'coverage':float(cov.mean()),'abstention':float(1-cov.mean()),'accuracy_all':float(np.mean(pp==y)), 'covered_accuracy':float(np.mean(pp[cov]==y[cov])) if cov.any() else np.nan, 'covered_fidelity':float(np.mean(pp[cov]==base_pred[cov])) if cov.any() else np.nan, 'all_fidelity':float(np.mean(pp==base_pred))})
    df=pd.DataFrame(rows); df.to_csv(art/'coverage_abstention_tradeoff.csv', index=False)
    fig,ax=plt.subplots(figsize=(5.6,3.5))
    ax.plot(df['confidence_threshold'],df['coverage'],marker='o',label='Coverage')
    ax.plot(df['confidence_threshold'],df['abstention'],marker='s',label='Abstention')
    ax.plot(df['confidence_threshold'],df['covered_accuracy'],marker='^',label='Covered accuracy')
    ax.plot(df['confidence_threshold'],df['covered_fidelity'],marker='d',label='Covered fidelity')
    ax.set_xlabel('Minimum rule confidence threshold')
    ax.set_ylabel('Score')
    ax.set_ylim(0,1.20)
    ax.legend(frameon=False,ncol=2,loc='upper center')
    save_nature_figure(fig, figs/'fig15_coverage_abstention_tradeoff.pdf')
    # Representative rule trace figure as a compact table-like panel.
    traces=pd.read_csv(art/'protocol_a_representative_traces.csv')
    rule_df=pd.read_csv(art/'protocol_a_rulebook.csv').set_index('rule_id')
    table_rows=[]
    for _,row in traces.head(3).iterrows():
        rid=first_rule(row.get('activated_rules',''))
        support='--'; conf='--'; source=str(row.get('mode',''))
        antecedents=str(row.get('semantic_states_sample',''))
        if rid in rule_df.index:
            support=str(int(rule_df.loc[rid,'support']))
            conf=f"{float(rule_df.loc[rid,'confidence']):.3f}"
            source=str(rule_df.loc[rid,'source'])
            antecedents=str(rule_df.loc[rid,'antecedent_text'])
        table_rows.append([
            str(row.get('object_index','')),
            textwrap.shorten(str(row.get('true_class','')),width=14,placeholder='...'),
            textwrap.shorten(str(row.get('predicted_class','')),width=14,placeholder='...'),
            rid if rid else 'fallback',
            support,
            conf,
            textwrap.shorten(source,width=18,placeholder='...'),
            textwrap.fill(textwrap.shorten(antecedents,width=90,placeholder='...'),width=42),
        ])
    headers=['Object','True','Pred.','Rule','Supp.','Conf.','Source','Antecedent states']
    fig,ax=plt.subplots(figsize=(8.2,2.8)); ax.axis('off')
    tbl=ax.table(cellText=table_rows,colLabels=headers,loc='center',cellLoc='left',colLoc='left',colWidths=[0.08,0.09,0.09,0.08,0.07,0.07,0.13,0.39])
    tbl.auto_set_font_size(False); tbl.set_fontsize(7.0); tbl.scale(1,1.8)
    for (r,c),cell in tbl.get_celld().items():
        cell.set_edgecolor('0.8'); cell.set_linewidth(0.4)
        if r==0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('0.93')
    save_nature_figure(fig, figs/'fig14_representative_rule_traces.pdf')
    print({'status':'ok','figures':['fig14_representative_rule_traces.pdf','fig15_coverage_abstention_tradeoff.pdf']})
if __name__=='__main__': main()
