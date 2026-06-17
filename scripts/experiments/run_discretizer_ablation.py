#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from revision_common import load_cache, read_thresholds, read_rulebook, load_names
from paper1_core import ensure_dir, quantize, fit_discretizers, induce_rules, class_mode_signatures, infer_rules

def eval_metrics(name,y,pred_df,base_pred,rules):
    pred=pred_df['prediction'].to_numpy(dtype=int); cov=pred>=0
    out={'method':name,'threshold_count':np.nan,'rule_count':int(len(rules)),'coverage':float(cov.mean()),'abstention':float(1-cov.mean()),'accuracy_all':float(np.mean(pred==y)),'accuracy_covered':float(accuracy_score(y[cov],pred[cov])) if cov.any() else float('nan'),'macro_f1_covered':float(f1_score(y[cov],pred[cov],average='macro',zero_division=0)) if cov.any() else float('nan'),'covered_fidelity_to_base':float(np.mean(pred[cov]==base_pred[cov])) if cov.any() else float('nan'),'all_object_fidelity_to_base':float(np.mean(pred==base_pred)),'mean_rule_length':float(rules['antecedent_length'].mean()) if len(rules) else float('nan'),'conflict_rate':float(pred_df['conflict'].mean()) if 'conflict' in pred_df.columns else 0.0}
    return out

def simple_thresholds(Y,attrs,kind):
    th={}
    for j in attrs:
        x=Y[:,j]
        if kind=='equal_frequency': th[int(j)]=[float(np.quantile(x,1/3)),float(np.quantile(x,2/3))]
        elif kind=='equal_width':
            lo,hi=float(np.min(x)),float(np.max(x)); th[int(j)]=[lo+(hi-lo)/3,lo+2*(hi-lo)/3]
    return th

def fit_and_eval(name,thresholds,cache,attrs,attr_names,class_names,base_pred,min_conf=0.84,min_sup=18):
    Ztr=quantize(cache['Yhat_train'],attrs,thresholds); Zte=quantize(cache['Yhat_test'],attrs,thresholds)
    rules,gran=induce_rules(Ztr,cache['y_train'].astype(int),attr_names,class_names,min_confidence=min_conf,min_support=min_sup,max_rules_per_class=5,reduce=True)
    prot=class_mode_signatures(Ztr,cache['y_train'].astype(int),np.arange(len(class_names)))
    pred=infer_rules(Zte,rules,prot,fallback_max_distance=0.45)
    out=eval_metrics(name,cache['y_test'].astype(int),pred,base_pred,rules)
    out['threshold_count']=int(sum(len(v) for v in thresholds.values()))
    return out,rules,pred

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip'); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--n_components',type=int,default=64); args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    class_names,pred_names=load_names(out,args.awa2_zip)
    attrs=pd.read_csv(art/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist(); attr_names=[pred_names[j] for j in attrs]
    base=pd.read_csv(art/'base_predictor_predictions.csv'); base_test=base[base['split']=='test']['base_prediction'].to_numpy(dtype=int)
    rows=[]
    # Existing WEDD row
    prop=pd.read_csv(art/'protocol_a_test_rule_predictions.csv'); rules=read_rulebook(out)
    row=eval_metrics('WEDD',cache['y_test'].astype(int),prop,base_test,rules); row['threshold_count']=sum(len(v) for v in read_thresholds(out).values()); rows.append(row)
    # MDLP-like entropy stopping
    md_th,_,_=fit_discretizers(cache['Yhat_train'],cache['y_train'].astype(int),attrs,alpha=1.0,max_depth=2,min_support=30)
    row,rr,pp=fit_and_eval('MDLP-like entropy',md_th,cache,attrs,attr_names,class_names,base_test); rows.append(row)
    # Equal frequency and width
    for kind,label in [('equal_frequency','Equal frequency'),('equal_width','Equal width')]:
        th=simple_thresholds(cache['Yhat_train'],attrs,kind)
        row,rr,pp=fit_and_eval(label,th,cache,attrs,attr_names,class_names,base_test); rows.append(row)
    df=pd.DataFrame(rows); df.to_csv(art/'discretizer_ablation_metrics.csv',index=False)
    print(json.dumps({'status':'ok','methods':df['method'].tolist()},indent=2))
if __name__=='__main__': main()
