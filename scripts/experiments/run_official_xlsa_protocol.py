#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,zipfile,sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, f1_score
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from paper1_core import ensure_dir, fit_discretizers, quantize, nearest_prototype_predict
from revision_common import load_names

def extract(zip_path,out):
    out=ensure_dir(out)
    if (out/'xlsa17_res101_features.parquet').exists(): return out
    with zipfile.ZipFile(zip_path) as z: z.extractall(out)
    return out
def read_idx(p,name): return pd.read_parquet(p/f'xlsa17_att_splits_{name}.parquet').iloc[:,0].to_numpy(dtype=int)-1
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--xlsa17_zip',default='/mnt/data/xlsa17.zip'); ap.add_argument('--awa2_zip',default='/mnt/data/awa2.zip'); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--n_components',type=int,default=64); args=ap.parse_args()
    out=Path(args.out).resolve(); art=ensure_dir(out/'artifacts'/'awa2'); tmp=extract(args.xlsa17_zip,out/'artifacts'/'_tmp_xlsa17')
    A=pd.read_parquet(tmp/'xlsa17_res101_features.parquet').to_numpy(dtype=np.float32)
    y=pd.read_parquet(tmp/'xlsa17_res101_labels.parquet').iloc[:,0].to_numpy(dtype=int)-1
    classes=pd.read_parquet(tmp/'xlsa17_att_splits_allclasses_names.parquet').iloc[:,0].astype(str).str.replace('+',' ',regex=False).tolist()
    testclasses=pd.read_parquet(tmp/'xlsa17_testclasses.parquet').iloc[:,0].astype(str).str.replace('+',' ',regex=False).tolist()
    trainclasses=pd.read_parquet(tmp/'xlsa17_trainvalclasses.parquet').iloc[:,0].astype(str).str.replace('+',' ',regex=False).tolist()
    Braw=pd.read_parquet(tmp/'xlsa17_att_splits_original_att.parquet').to_numpy(dtype=float)
    train=read_idx(tmp,'train_loc'); val=read_idx(tmp,'val_loc'); trainval=read_idx(tmp,'trainval_loc'); seen=read_idx(tmp,'test_seen_loc'); unseen=read_idx(tmp,'test_unseen_loc')
    n_components=min(args.n_components,A.shape[1])
    var=np.var(A[train],axis=0); cols=np.argsort(var)[::-1][:n_components]
    mu=A[np.ix_(train,cols)].mean(axis=0); sd=A[np.ix_(train,cols)].std(axis=0); sd[sd<1e-6]=1
    def X(idx): return ((A[np.ix_(idx,cols)]-mu)/sd).astype(np.float32)
    Xtrain=X(train); Xval=X(val); Xun=X(unseen); Xseen=X(seen)
    bmin=np.min(Braw[y[train]],axis=0); bmax=np.max(Braw[y[train]],axis=0); den=np.where(bmax-bmin<1e-12,1,bmax-bmin)
    def B(idx): return np.clip((Braw[y[idx]]-bmin)/den,0,1)
    def Bc(): return np.clip((Braw-bmin)/den,0,1)
    best=None; grid=[]
    for alpha in [0.01,0.1,1,10,100]:
        m=Ridge(alpha=alpha).fit(Xtrain,B(train)); Pv=np.clip(m.predict(Xval),0,1); mae=float(np.mean(np.abs(Pv-B(val)))); grid.append({'alpha':alpha,'val_mae':mae})
        if best is None or mae<best[0]: best=(mae,alpha,m)
    model=best[2]
    Pun=np.clip(model.predict(Xun),0,1); Pseen=np.clip(model.predict(Xseen),0,1)
    Bclass=Bc(); unseen_labels=[classes.index(c) for c in testclasses]; seen_labels=[classes.index(c) for c in trainclasses]
    pred_un,_=nearest_prototype_predict(Pun,Bclass[unseen_labels],np.array(unseen_labels))
    pred_seen,_=nearest_prototype_predict(Pseen,Bclass[seen_labels],np.array(seen_labels))
    # Symbolic class-template matching on unseen prototypes.
    selected=pd.read_csv(art/'protocol_a_selected_attributes.csv')['attribute_index'].astype(int).tolist()
    _,pred_names=load_names(out,args.awa2_zip)
    thresholds,_,_=fit_discretizers(np.clip(model.predict(Xtrain),0,1),y[train],selected,alpha=0.65,max_depth=2,min_support=30)
    Zun=quantize(Pun,selected,thresholds); Zproto=quantize(Bclass,selected,thresholds)
    h=[]; hpred=[]
    for z in Zun:
        d=np.mean(Zproto[unseen_labels] != z[None,:],axis=1); j=int(np.argmin(d)); h.append(float(d[j])); hpred.append(unseen_labels[j])
    hpred=np.array(hpred)
    metrics={'protocol':'official_xlsa17_proposed_split','n_components':int(n_components),'ridge_alpha':float(best[1]),'train_objects':int(len(train)),'validation_objects':int(len(val)),'trainval_objects':int(len(trainval)),'test_seen_objects':int(len(seen)),'test_unseen_objects':int(len(unseen)),'unseen_classes':testclasses,'seen_classes':trainclasses,'mae_unseen':float(np.mean(np.abs(Pun-B(unseen)))),'rmse_unseen':float(np.sqrt(np.mean((Pun-B(unseen))**2))),'prototype_unseen_accuracy':float(accuracy_score(y[unseen],pred_un)),'prototype_unseen_macro_f1':float(f1_score(y[unseen],pred_un,labels=unseen_labels,average='macro',zero_division=0)),'prototype_seen_accuracy':float(accuracy_score(y[seen],pred_seen)),'symbolic_template_unseen_accuracy':float(accuracy_score(y[unseen],hpred)),'symbolic_template_unseen_macro_f1':float(f1_score(y[unseen],hpred,labels=unseen_labels,average='macro',zero_division=0)),'symbolic_template_mean_hamming':float(np.mean(h)),'ridge_grid':grid}
    (art/'protocol_b_zero_shot_metrics.json').write_text(json.dumps(metrics,indent=2,sort_keys=True),encoding='utf-8')
    rows=[]
    for lab in unseen_labels:
        mask=y[unseen]==lab
        rows.append({'class_index':int(lab),'class_name':classes[lab],'n_objects':int(mask.sum()),'prototype_accuracy':float(np.mean(pred_un[mask]==lab)),'symbolic_template_accuracy':float(np.mean(hpred[mask]==lab)),'mean_hamming':float(np.mean(np.array(h)[mask]))})
    pd.DataFrame(rows).to_csv(art/'protocol_b_unseen_per_class.csv',index=False)
    pd.DataFrame([{'attribute_index':k,'threshold':t} for k,v in thresholds.items() for t in v]).to_csv(art/'protocol_b_thresholds.csv',index=False)
    (art/'protocol_b_summary.json').write_text(json.dumps(metrics,indent=2,sort_keys=True),encoding='utf-8')
    (out/'source_notes'/'awa2_split_note.md').write_text('Protocol B was revised to use the supplied xlsa17.zip official proposed split files. Indices are converted from MATLAB one-based locations to zero-based Python row indices. The transition, WEDD, and symbolic-template logic are unchanged.\n',encoding='utf-8')
    print(json.dumps({'status':'ok','unseen_accuracy':metrics['prototype_unseen_accuracy'],'unseen_classes':testclasses},indent=2))
if __name__=='__main__': main()
