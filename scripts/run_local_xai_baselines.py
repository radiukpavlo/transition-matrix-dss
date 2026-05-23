#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge, RidgeClassifier

SCRIPT_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(SCRIPT_DIR))
from revision_common import load_cache, bootstrap_ci, read_rulebook
from paper1_core import ensure_dir


def parse_ant(x):
    if isinstance(x,dict): return {int(k):int(v) for k,v in x.items()}
    return {int(k):int(v) for k,v in ast.literal_eval(str(x)).items()}

def direction_agreement(attrib, ant):
    vals=[]
    for j,state in ant.items():
        if state==0: vals.append(1.0 if attrib[j] < 0 else 0.0)
        elif state>=2: vals.append(1.0 if attrib[j] > 0 else 0.0)
        else: pass
    return float(np.mean(vals)) if vals else np.nan

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip')
    ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--n_components',type=int,default=64)
    ap.add_argument('--sample_size',type=int,default=1000)
    args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    rng=np.random.default_rng(args.seed)
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    sel=pd.read_csv(out/'artifacts'/'awa2'/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist()
    Ytr=cache['Yhat_train'][:,sel]; Yte=cache['Yhat_test'][:,sel]
    ytr=cache['y_train'].astype(int); yte=cache['y_test'].astype(int)
    # A deterministic local-explanation target over reconstructed semantics.
    surrogate=RidgeClassifier(alpha=1.0).fit(Ytr,ytr)
    S=surrogate.decision_function(Yte)
    pred=S.argmax(axis=1)
    base_class_scores=S
    bg=Ytr.mean(axis=0)
    global_coef=surrogate.coef_  # classes x selected semantic attrs
    pred_df=pd.read_csv(out/'artifacts'/'awa2'/'protocol_a_test_rule_predictions.csv')
    rules=read_rulebook(out); rule_map={str(r.rule_id):parse_ant(r.antecedent) for _,r in rules.iterrows()}
    eligible=[]
    for i,row in pred_df.iterrows():
        acts=str(row.get('activated_rules',''))
        if not acts or acts=='nan' or bool(row.get('abstained',False)): continue
        rid=acts.split(';')[0]
        if rid in rule_map: eligible.append((i,rid,rule_map[rid]))
    if len(eligible)>args.sample_size:
        chosen=rng.choice(len(eligible), size=args.sample_size, replace=False)
        eligible=[eligible[int(j)] for j in chosen]
    rows=[]
    for i,rid,ant in eligible:
        x=Yte[i]
        cls=int(pred[i])
        # LIME-style: local Gaussian perturbations in semantic space with proximity weights.
        n_pert=160
        scale=np.maximum(Ytr.std(axis=0), 0.05)
        Z=np.clip(x + rng.normal(0,0.15,size=(n_pert,len(sel))) * scale,0,1)
        scores=surrogate.decision_function(Z)[:,cls]
        dist=np.sqrt(((Z-x)**2).sum(axis=1))
        weights=np.exp(-(dist**2)/(0.35**2))
        lime=Ridge(alpha=0.01).fit(Z,scores,sample_weight=weights).coef_.astype(float)
        shap=(global_coef[cls] * (x-bg)).astype(float)
        ant_set=set(ant.keys())
        k=max(1,len(ant_set))
        for method,attrib in [('LIME-style',lime),('SHAP-style',shap)]:
            top=set(np.argsort(np.abs(attrib))[-k:].astype(int).tolist())
            agreement=len(top & ant_set)/max(1,len(ant_set))
            dir_agree=direction_agreement(attrib,ant)
            mask=np.zeros(len(sel)); mask[list(ant_set)]=1.0
            try:
                rho=float(spearmanr(np.abs(attrib),mask).correlation)
            except Exception:
                rho=float('nan')
            rows.append({'sample_position':int(i),'rule_id':rid,'method':method,'rule_length':int(len(ant_set)),'topk_antecedent_agreement':float(agreement),'signed_direction_agreement':float(dir_agree),'spearman_rule_salience':rho,'surrogate_predicted_class':cls,'true_label':int(yte[i])})
    raw=pd.DataFrame(rows)
    raw.to_csv(art/'local_xai_agreement_raw.csv',index=False)
    summary=[]
    for method,g in raw.groupby('method'):
        for metric in ['topk_antecedent_agreement','signed_direction_agreement','spearman_rule_salience']:
            mean,lo,hi=bootstrap_ci(g[metric].to_numpy())
            summary.append({'method':method,'metric':metric,'mean':mean,'ci95_low':lo,'ci95_high':hi,'n':int(g[metric].notna().sum()),'mean_rule_length':float(g['rule_length'].mean())})
    outj={'seed':args.seed,'sample_size_requested':args.sample_size,'evaluated_rule_covered_samples':int(len(eligible)),'summary':summary}
    (art/'local_xai_agreement.json').write_text(json.dumps(outj,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'status':'ok','evaluated':len(eligible),'rows':len(raw)},indent=2))
if __name__=='__main__': main()
