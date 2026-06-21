#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, top_k_accuracy_score, roc_auc_score
from sklearn.preprocessing import label_binarize

SCRIPT_DIR=Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from revision_common import load_cache, load_names
from paper1_core import ensure_dir


def softmax(S):
    S=S-S.max(axis=1,keepdims=True); E=np.exp(S); return E/E.sum(axis=1,keepdims=True)

def metrics(y, proba, labels):
    pred=proba.argmax(axis=1)
    out={'top1_accuracy':float(accuracy_score(y,pred)),'top5_accuracy':float(top_k_accuracy_score(y,proba,k=5,labels=labels)),'macro_f1':float(f1_score(y,pred,average='macro',labels=labels,zero_division=0)),'weighted_f1':float(f1_score(y,pred,average='weighted',labels=labels,zero_division=0))}
    try:
        out['macro_auroc_ovr']=float(roc_auc_score(label_binarize(y,classes=labels),proba,average='macro',multi_class='ovr'))
    except Exception: out['macro_auroc_ovr']=float('nan')
    return out

def corr_mean(A,B):
    cs=[]
    for j in range(A.shape[1]):
        if np.std(A[:,j])>1e-12 and np.std(B[:,j])>1e-12: cs.append(np.corrcoef(A[:,j],B[:,j])[0,1])
    return float(np.nanmean(cs)) if cs else float('nan')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip')
    ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--n_components',type=int,default=64)
    args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    Xtr,Xte=cache['X_train'],cache['X_test']; ytr,yte=cache['y_train'].astype(int),cache['y_test'].astype(int)
    Yhat_tr,Yhat_te=cache['Yhat_train'],cache['Yhat_test']; Ytr,Yte=cache['Y_train'],cache['Y_test']
    labels=np.arange(50)
    # Frozen-feature CBM: concept predictor is the cached ridge transition; label head is trained on predicted concepts.
    label_head=RidgeClassifier(alpha=1.0).fit(Yhat_tr,ytr)
    proba=softmax(label_head.decision_function(Yhat_te))
    cbm={'semantic_mae':float(np.mean(np.abs(Yhat_te-Yte))),'semantic_rmse':float(np.sqrt(np.mean((Yhat_te-Yte)**2))),'concept_correlation_mean':corr_mean(Yte,Yhat_te),**metrics(yte,proba,labels)}
    (art/'cbm_metrics.json').write_text(json.dumps({'seed':args.seed,'variant':'frozen-feature concept bottleneck using cached transition concepts','test':cbm},indent=2,sort_keys=True),encoding='utf-8')
    class_names,pred_names=load_names(out,args.awa2_zip)
    selected=pd.read_csv(out/'artifacts'/'awa2'/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist()
    preferred=['stripes','paws','hooves','ocean','swims','longneck','hunter','furry']
    concept_idx=[]
    for name in preferred:
        matches=[i for i,n in enumerate(pred_names) if n.replace(' ','').lower()==name.lower()]
        if matches: concept_idx.append(matches[0])
    for j in selected:
        if j not in concept_idx: concept_idx.append(j)
    concept_idx=concept_idx[:12]
    base=RidgeClassifier(alpha=1.0).fit(Xtr,ytr)
    base_coef=base.coef_
    base_pred=base.predict(Xte)
    rows=[]
    for j in concept_idx:
        pos=(Ytr[:,j] >= np.median(Ytr[:,j])).astype(int)
        if pos.min()==pos.max(): continue
        cav=RidgeClassifier(alpha=1.0).fit(Xtr,pos)
        vec=cav.coef_.reshape(-1)
        denom=np.linalg.norm(vec)+1e-12
        vec=vec/denom
        sens=[]
        for i,c in enumerate(base_pred):
            sens.append(float(base_coef[int(c)].dot(vec)))
        sens=np.asarray(sens)
        rows.append({'attribute_index':int(j),'concept':pred_names[int(j)],'tcav_score_positive_sensitivity':float(np.mean(sens>0)),'mean_directional_sensitivity':float(np.mean(sens)),'selected_by_transition':bool(j in selected),'positive_train_fraction':float(pos.mean())})
    tcav=pd.DataFrame(rows).sort_values('tcav_score_positive_sensitivity',ascending=False)
    tcav.to_csv(art/'tcav_metrics.csv',index=False)
    overlap=float(tcav['selected_by_transition'].mean()) if len(tcav) else float('nan')
    (art/'tcav_summary.json').write_text(json.dumps({'seed':args.seed,'representation_layer':'released ResNet-101 feature layer / revision compressed coordinates','n_concepts':int(len(tcav)),'overlap_fraction_with_selected_attributes':overlap},indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'status':'ok','cbm_top1':cbm['top1_accuracy'],'tcav_concepts':len(tcav)},indent=2))
if __name__=='__main__': main()
