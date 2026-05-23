#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys,time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, f1_score
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0,str(SCRIPT_DIR))
from revision_common import load_cache, read_thresholds, read_rulebook, load_names
from paper1_core import ensure_dir, nearest_prototype_predict, quantize, infer_rules, class_mode_signatures

def corr_mean(Y,P):
    cs=[]
    for j in range(Y.shape[1]):
        if np.std(Y[:,j])>1e-12 and np.std(P[:,j])>1e-12: cs.append(np.corrcoef(Y[:,j],P[:,j])[0,1])
    return float(np.nanmean(cs)) if cs else float('nan')
def rule_eval(Yhat,cache,attrs,thresholds,rules):
    Ztr=quantize(cache['Yhat_train'],attrs,thresholds)
    prot=class_mode_signatures(Ztr,cache['y_train'].astype(int),np.arange(50))
    Z=quantize(Yhat,attrs,thresholds)
    pred=infer_rules(Z,rules,prot,fallback_max_distance=0.45)
    p=pred['prediction'].to_numpy(dtype=int); cov=p>=0; y=cache['y_test'].astype(int)
    return {'rule_coverage':float(cov.mean()),'rule_accuracy_all':float(np.mean(p==y)),'rule_accuracy_covered':float(accuracy_score(y[cov],p[cov])) if cov.any() else float('nan'),'rule_macro_f1_covered':float(f1_score(y[cov],p[cov],average='macro',zero_division=0)) if cov.any() else float('nan')}
def summarize(name,Yhat,cache,B_class_scaled,attrs,thresholds,rules,seconds):
    y=cache['y_test'].astype(int); labels=np.arange(50)
    pred,_=nearest_prototype_predict(Yhat,B_class_scaled,labels)
    out={'operator':name,'semantic_mae':float(np.mean(np.abs(Yhat-cache['Y_test']))),'semantic_rmse':float(np.sqrt(np.mean((Yhat-cache['Y_test'])**2))),'semantic_correlation_mean':corr_mean(cache['Y_test'],Yhat),'prototype_accuracy':float(accuracy_score(y,pred)),'prototype_macro_f1':float(f1_score(y,pred,average='macro',zero_division=0)),'runtime_seconds':float(seconds)}
    out.update(rule_eval(Yhat,cache,attrs,thresholds,rules))
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip'); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--n_components',type=int,default=64); ap.add_argument('--sample_size',type=int,default=6000); args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2')
    cache=load_cache(out,args.awa2_zip,n_components=args.n_components,seed=args.seed)
    attrs=pd.read_csv(art/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist(); thresholds=read_thresholds(out); rules=read_rulebook(out)
    rows=[]; rng=np.random.default_rng(args.seed)
    # Linear cache result
    rows.append(summarize('Linear ridge transition',cache['Yhat_test'],cache,cache['B_class_scaled'],attrs,thresholds,rules,0.0))
    Xtr,Ytr=cache['X_train'],cache['Y_train']; Xte=cache['X_test']
    if len(Xtr)>args.sample_size:
        idx=rng.choice(len(Xtr),size=args.sample_size,replace=False)
    else: idx=np.arange(len(Xtr))
    # RBF kernel ridge via Nyström features
    t=time.time(); kr=make_pipeline(Nystroem(kernel='rbf',gamma=0.5,n_components=64,random_state=args.seed),Ridge(alpha=1.0)); kr.fit(Xtr[idx],Ytr[idx]); P=np.clip(kr.predict(Xte),0,1); rows.append(summarize('RBF kernel ridge (Nystroem)',P,cache,cache['B_class_scaled'],attrs,thresholds,rules,time.time()-t))
    # MLP regressor
    t=time.time(); mlp=MLPRegressor(hidden_layer_sizes=(32,),activation='relu',alpha=1e-4,learning_rate_init=1e-3,max_iter=25,early_stopping=True,random_state=args.seed,verbose=False); mlp.fit(Xtr[idx],Ytr[idx]); P=np.clip(mlp.predict(Xte),0,1); rows.append(summarize('Two-layer MLP regressor',P,cache,cache['B_class_scaled'],attrs,thresholds,rules,time.time()-t))
    df=pd.DataFrame(rows); df.to_csv(art/'transition_operator_ablation.csv',index=False)
    print(json.dumps({'status':'ok','operators':df['operator'].tolist()},indent=2))
if __name__=='__main__': main()
