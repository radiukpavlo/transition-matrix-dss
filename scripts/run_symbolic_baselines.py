#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, json, sys
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

SCRIPT_DIR=Path(__file__).resolve().parent
sys.path.insert(0,str(SCRIPT_DIR))
from revision_common import load_cache, read_thresholds, read_rulebook
from paper1_core import ensure_dir, quantize


def eval_pred(name,y,pred,base_pred,coverage_mask,rule_count,avg_len,conflict_rate=0.0):
    covered=coverage_mask.astype(bool)
    pred_all=pred.copy(); pred_all[~covered]=-1
    acc_all=float(np.mean(pred_all==y))
    acc_cov=float(accuracy_score(y[covered],pred[covered])) if covered.any() else float('nan')
    f1_cov=float(f1_score(y[covered],pred[covered],average='macro',zero_division=0)) if covered.any() else float('nan')
    cov=float(covered.mean()); abst=1-cov
    fidelity_cov=float(np.mean(pred[covered]==base_pred[covered])) if covered.any() else float('nan')
    fidelity_all=float(np.mean(pred_all==base_pred))
    return {'method':name,'accuracy_all':acc_all,'accuracy_covered':acc_cov,'macro_f1_covered':f1_cov,'coverage':cov,'abstention':abst,'covered_fidelity_to_base':fidelity_cov,'all_object_fidelity_to_base':fidelity_all,'rule_count':int(rule_count),'avg_antecedent_length':float(avg_len),'conflict_rate':float(conflict_rate)}

def induce_ripper_like(Z,y,min_support=18,min_conf=0.60,max_len=4,max_rules_per_class=4):
    rules=[]
    all_idx=np.arange(len(y))
    for c in sorted(np.unique(y)):
        remaining=set(np.where(y==c)[0].tolist())
        for _ in range(max_rules_per_class):
            if len(remaining)<min_support: break
            mask=np.ones(len(y),dtype=bool); ant=[]; used=set()
            best_stats=None
            for depth in range(max_len):
                best=None
                for a in range(Z.shape[1]):
                    if a in used: continue
                    for state in np.unique(Z[:,a]):
                        m=mask & (Z[:,a]==state)
                        supp=int(m.sum()); pos=int(np.sum(y[m]==c))
                        if supp<min_support or pos<min_support: continue
                        conf=pos/supp
                        score=(conf, pos, -supp)
                        if best is None or score>best[0]: best=(score,a,int(state),m,conf,pos,supp)
                if best is None: break
                _,a,state,m,conf,pos,supp=best
                ant.append((a,state)); used.add(a); mask=m; best_stats=(conf,pos,supp)
                if conf>=min_conf: break
            if best_stats is None: break
            conf,pos,supp=best_stats
            if pos<min_support: break
            rules.append({'rule_id':f'SC{len(rules)+1:04d}','class':int(c),'antecedent':dict(ant),'support':int(supp),'confidence':float(conf),'length':len(ant)})
            for i in np.where(mask & (y==c))[0].tolist(): remaining.discard(i)
    return pd.DataFrame(rules)

def infer_ripper(Z,rules):
    parsed=[]
    for _,r in rules.iterrows():
        ant=r['antecedent']
        if isinstance(ant,str): ant=ast.literal_eval(ant)
        parsed.append((int(r['class']), {int(a):int(s) for a,s in ant.items()}, float(r['confidence'])*np.log1p(float(r['support']))/max(1,int(r['length']))))
    pred=np.full(len(Z),-1,dtype=int); nmatch=np.zeros(len(Z),dtype=int)
    for i,z in enumerate(Z):
        votes=defaultdict(float)
        for cls,ant,score in parsed:
            ok=True
            for a,s in ant.items():
                if int(z[a]) != int(s): ok=False; break
            if ok:
                votes[cls]+=score; nmatch[i]+=1
        if votes:
            pred[i]=max(votes.items(), key=lambda kv:kv[1])[0]
    return pred,pred>=0,nmatch

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip'); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--n_components',type=int,default=64); args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    selected=pd.read_csv(out/'artifacts'/'awa2'/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist()
    ytr,yte=cache['y_train'].astype(int),cache['y_test'].astype(int)
    Xtr,Xte=cache['Yhat_train'][:,selected],cache['Yhat_test'][:,selected]
    base=pd.read_csv(art/'base_predictor_predictions.csv')
    base_test=base[base['split']=='test']['base_prediction'].to_numpy(dtype=int)
    rows=[]
    # Proposed rulebook from existing artifacts
    prop=pd.read_csv(art/'protocol_a_test_rule_predictions.csv')
    prop_pred=prop['prediction'].to_numpy(dtype=int); prop_cov=prop_pred>=0
    rules=read_rulebook(out)
    rows.append(eval_pred('Proposed rough-set rulebook',yte,prop_pred,base_test,prop_cov,len(rules),rules['antecedent_length'].mean(),prop['conflict'].mean()))
    # CART
    cart=DecisionTreeClassifier(max_depth=7,min_samples_leaf=60,random_state=args.seed).fit(Xtr,ytr)
    cpred=cart.predict(Xte)
    rows.append(eval_pred('CART decision tree',yte,cpred,base_test,np.ones_like(cpred,dtype=bool),cart.get_n_leaves(),float(cart.get_depth()),0.0))
    # RIPPER-like separate-and-conquer on symbolic states
    thresholds=read_thresholds(out)
    Ztr=quantize(cache['Yhat_train'],selected,thresholds); Zte=quantize(cache['Yhat_test'],selected,thresholds)
    rr=induce_ripper_like(Ztr,ytr)
    rr.to_csv(art/'ripper_like_rules.csv',index=False)
    rpred,rcov,nmatch=infer_ripper(Zte,rr)
    rows.append(eval_pred('Separate-and-conquer rule learner',yte,rpred,base_test,rcov,len(rr),float(rr['length'].mean()) if len(rr) else float('nan'),float(np.mean(nmatch>1))))
    df=pd.DataFrame(rows)
    df.to_csv(art/'symbolic_baselines_metrics.csv',index=False)
    print(json.dumps({'status':'ok','methods':df['method'].tolist()},indent=2))
if __name__=='__main__': main()
