#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import accuracy_score, f1_score, top_k_accuracy_score, roc_auc_score
from sklearn.preprocessing import label_binarize

SCRIPT_DIR=Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from revision_common import load_cache, load_names
from paper1_core import ensure_dir


def ece_score(proba, y, n_bins=10):
    conf=proba.max(axis=1); pred=proba.argmax(axis=1); acc=(pred==y).astype(float)
    edges=np.linspace(0,1,n_bins+1); ece=0.0
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(conf>=lo)&(conf<hi if hi<1 else conf<=hi)
        if mask.any():
            ece += mask.mean() * abs(acc[mask].mean() - conf[mask].mean())
    return float(ece)


def metrics(y, proba, labels):
    pred=proba.argmax(axis=1)
    out={
        'top1_accuracy': float(accuracy_score(y,pred)),
        'top5_accuracy': float(top_k_accuracy_score(y,proba,k=min(5,len(labels)),labels=labels)),
        'macro_f1': float(f1_score(y,pred,average='macro',labels=labels,zero_division=0)),
        'weighted_f1': float(f1_score(y,pred,average='weighted',labels=labels,zero_division=0)),
        'ece_10bin': ece_score(proba,y),
    }
    try:
        Y=label_binarize(y,classes=labels)
        out['macro_auroc_ovr']=float(roc_auc_score(Y,proba,average='macro',multi_class='ovr'))
    except Exception:
        out['macro_auroc_ovr']=float('nan')
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip')
    ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--seed',type=int,default=42)
    ap.add_argument('--n_components',type=int,default=64)
    ap.add_argument('--max_iter',type=int,default=350)
    args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    labels=np.arange(50)
    Xtr,Xv,Xte=cache['X_train'],cache['X_val'],cache['X_test']
    ytr,yv,yte=cache['y_train'].astype(int),cache['y_val'].astype(int),cache['y_test'].astype(int)
    clf=RidgeClassifier(alpha=1.0)
    clf.fit(Xtr,ytr)
    def softmax_scores(X):
        S=clf.decision_function(X)
        S=S - S.max(axis=1, keepdims=True)
        E=np.exp(S)
        return E / E.sum(axis=1, keepdims=True)
    pv=softmax_scores(Xv); pt=softmax_scores(Xte)
    res={'seed':args.seed,'n_components':args.n_components,'model':'RidgeClassifier on variance-screened representation cache with softmax-normalized decision scores','ridge_alpha':1.0,'validation':metrics(yv,pv,labels),'test':metrics(yte,pt,labels)}
    Path(art/'base_predictor_metrics.json').write_text(json.dumps(res,indent=2,sort_keys=True),encoding='utf-8')
    class_names,_=load_names(out,args.awa2_zip)
    rows=[]
    for split,idx,y,proba in [('validation',cache['val_idx'],yv,pv),('test',cache['test_idx'],yte,pt)]:
        pred=proba.argmax(axis=1)
        top5=np.argsort(proba,axis=1)[:,-5:][:,::-1]
        for i,row_idx in enumerate(idx):
            d={'row_index':int(row_idx),'split':split,'true_label':int(y[i]),'true_class':class_names[int(y[i])],'base_prediction':int(pred[i]),'base_prediction_class':class_names[int(pred[i])],'base_confidence':float(proba[i,pred[i]]),'top5_labels':';'.join(map(str,top5[i].astype(int).tolist())),'top5_classes':';'.join(class_names[int(j)] for j in top5[i])}
            for j in top5[i]: d[f'prob_{int(j)}']=float(proba[i,int(j)])
            rows.append(d)
    pd.DataFrame(rows).to_csv(art/'base_predictor_predictions.csv',index=False)
    print(json.dumps({'status':'ok','test_top1':res['test']['top1_accuracy'],'test_top5':res['test']['top5_accuracy']},indent=2))
if __name__=='__main__': main()
