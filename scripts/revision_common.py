#!/usr/bin/env python3
"""Shared utilities for revision experiments."""
from __future__ import annotations
import json, zipfile, sys
from pathlib import Path
from typing import Any, Dict, Tuple, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from paper1_core import ensure_dir, maybe_extract_awa2, load_awa2, fit_transition

RANDOM_SEED = 42

def load_protocol_a_indices(pkg: Path, y: np.ndarray, seed: int = RANDOM_SEED) -> Tuple[np.ndarray,np.ndarray,np.ndarray]:
    """Recreate the Protocol A train/validation/test order used by the original experiment.

    The split CSV records membership by original row index but not the shuffled order
    returned by scikit-learn. Rule-prediction artifacts are ordered by the original
    shuffled test array, so revision experiments recreate that order deterministically.
    """
    idx = np.arange(len(y))
    train, temp = train_test_split(idx, test_size=0.40, random_state=seed, stratify=y)
    val, test = train_test_split(temp, test_size=0.50, random_state=seed, stratify=y[temp])
    return train, val, test

def load_selected_attributes(pkg: Path) -> List[int]:
    p = pkg / 'artifacts' / 'awa2' / 'protocol_a_selected_attributes.csv'
    if p.exists():
        df = pd.read_csv(p)
        col = 'attribute_index' if 'attribute_index' in df.columns else df.columns[0]
        return [int(x) for x in df[col].tolist()]
    return [10,20,36,22,24,58,73,45]

def _manual_minmax_fit_transform(B_train, B_val, B_test, B_class):
    bmin = np.nanmin(B_train, axis=0)
    bmax = np.nanmax(B_train, axis=0)
    den = np.where((bmax - bmin) < 1e-12, 1.0, bmax - bmin)
    def tr(X):
        return np.clip((X - bmin) / den, 0.0, 1.0)
    return tr(B_train), tr(B_val), tr(B_test), tr(B_class), bmin, den

def make_transition_cache(pkg: str|Path, awa2_zip: str|Path, n_components: int = 64, seed: int = RANDOM_SEED, force: bool=False) -> Path:
    """Create a lightweight transition cache for revision-only baselines.

    To keep the reviewer-response experiments reproducible in a constrained runtime,
    this cache uses deterministic variance-screened representation coordinates as the
    auxiliary compressed representation. The main manuscript keeps the SVD bridge in
    the formal method; the cache supports added baselines, fidelity targets, and
    stability analyses without altering the original rule-induction artifacts.
    """
    from sklearn.linear_model import Ridge
    pkg = Path(pkg).resolve()
    cache = pkg / 'artifacts' / 'awa2' / 'revision_transition_cache.npz'
    meta = pkg / 'artifacts' / 'awa2' / 'revision_transition_cache_meta.json'
    if cache.exists() and meta.exists() and not force:
        try:
            m = json.loads(meta.read_text())
            if int(m.get('n_components', -1)) == int(n_components):
                return cache
        except Exception:
            pass
    tmp = ensure_dir(pkg / 'artifacts' / '_tmp_awa2')
    awa2_dir = maybe_extract_awa2(awa2_zip, tmp)
    data = load_awa2(awa2_dir)
    train_idx, val_idx, test_idx = load_protocol_a_indices(pkg, data.y, seed)
    A = data.A.astype(np.float32, copy=False)
    n_components = int(min(n_components, A.shape[1]))
    # Select the highest-variance columns on the training subset.
    var = np.var(A[train_idx], axis=0)
    feature_idx = np.argsort(var)[::-1][:n_components].astype(int)
    mean = A[train_idx][:, feature_idx].mean(axis=0).astype(np.float32)
    std = A[train_idx][:, feature_idx].std(axis=0).astype(np.float32)
    std[~np.isfinite(std) | (std < 1e-6)] = 1.0
    def transform(indices):
        return ((A[indices][:, feature_idx] - mean) / std).astype(np.float32)
    X_train=transform(train_idx); X_val=transform(val_idx); X_test=transform(test_idx)
    Y_train,Y_val,Y_test,B_class_scaled,bmin,bden=_manual_minmax_fit_transform(data.B_obj_raw[train_idx], data.B_obj_raw[val_idx], data.B_obj_raw[test_idx], data.B_class_raw)
    grid=[0.01,0.1,1.0,10.0,100.0]
    best=None; grid_rows=[]
    for a in grid:
        model=Ridge(alpha=a, fit_intercept=True)
        model.fit(X_train,Y_train)
        P=np.clip(model.predict(X_val),0,1)
        mae=float(np.mean(np.abs(P-Y_val))); rmse=float(np.sqrt(np.mean((P-Y_val)**2)))
        grid_rows.append({'ridge_alpha':a,'val_mae':mae,'val_rmse':rmse})
        if best is None or mae<best[0]: best=(mae,a,model)
    model=best[2]; alpha=float(best[1])
    Yhat_train=np.clip(model.predict(X_train),0,1); Yhat_val=np.clip(model.predict(X_val),0,1); Yhat_test=np.clip(model.predict(X_test),0,1)
    def corr_mean(Y,P):
        cs=[]
        for j in range(Y.shape[1]):
            if np.std(Y[:,j])>1e-12 and np.std(P[:,j])>1e-12: cs.append(np.corrcoef(Y[:,j],P[:,j])[0,1])
        return float(np.nanmean(cs)) if cs else float('nan')
    metrics={
        'n_components': int(n_components), 'compression': 'top_variance_coordinates_for_revision_auxiliary_baselines', 'selected_ridge_alpha': alpha, 'ridge_grid': grid_rows,
        'train_mae': float(np.mean(np.abs(Yhat_train-Y_train))), 'train_rmse': float(np.sqrt(np.mean((Yhat_train-Y_train)**2))), 'train_semantic_correlation_mean': corr_mean(Y_train,Yhat_train),
        'val_mae': float(np.mean(np.abs(Yhat_val-Y_val))), 'val_rmse': float(np.sqrt(np.mean((Yhat_val-Y_val)**2))), 'val_semantic_correlation_mean': corr_mean(Y_val,Yhat_val),
        'test_mae': float(np.mean(np.abs(Yhat_test-Y_test))), 'test_rmse': float(np.sqrt(np.mean((Yhat_test-Y_test)**2))), 'test_semantic_correlation_mean': corr_mean(Y_test,Yhat_test),
    }
    salience=np.linalg.norm(model.coef_.T,axis=0)
    np.savez_compressed(cache,
        train_idx=train_idx, val_idx=val_idx, test_idx=test_idx,
        y_train=data.y[train_idx], y_val=data.y[val_idx], y_test=data.y[test_idx],
        Y_train=Y_train, Y_val=Y_val, Y_test=Y_test,
        Yhat_train=Yhat_train, Yhat_val=Yhat_val, Yhat_test=Yhat_test,
        X_train=X_train, X_val=X_val, X_test=X_test,
        B_class_scaled=B_class_scaled,
        salience=salience,
        feature_idx=feature_idx,
    )
    meta_obj={'n_components':int(n_components),'seed':int(seed),'transition_metrics':metrics,'train_size':int(len(train_idx)),'val_size':int(len(val_idx)),'test_size':int(len(test_idx)),'cache_file':str(cache.name),'cache_note':'Variance-screened auxiliary cache for reviewer-response baselines.'}
    meta.write_text(json.dumps(meta_obj,indent=2,sort_keys=True),encoding='utf-8')
    return cache

def load_cache(pkg: str|Path, awa2_zip: str|Path, n_components: int = 32, seed: int = RANDOM_SEED, force: bool=False) -> Dict[str, Any]:
    pkg = Path(pkg).resolve()
    cache_path = make_transition_cache(pkg, awa2_zip, n_components=n_components, seed=seed, force=force)
    z = np.load(cache_path, allow_pickle=True)
    return {k:z[k] for k in z.files}

def load_names(pkg: str|Path, awa2_zip: str|Path):
    pkg=Path(pkg); tmp=ensure_dir(pkg/'artifacts'/'_tmp_awa2'); data=load_awa2(maybe_extract_awa2(awa2_zip,tmp))
    return data.class_names, data.predicate_names

def read_thresholds(pkg: str|Path) -> Dict[int, List[float]]:
    p = Path(pkg)/'artifacts'/'awa2'/'protocol_a_wedd_thresholds.csv'
    df=pd.read_csv(p)
    thresholds={}
    if 'attribute_index' in df.columns and 'threshold' in df.columns:
        for j,g in df.groupby('attribute_index'):
            thresholds[int(j)] = sorted([float(x) for x in g['threshold'].dropna().tolist()])
    return thresholds

def read_rulebook(pkg: str|Path) -> pd.DataFrame:
    return pd.read_csv(Path(pkg)/'artifacts'/'awa2'/'protocol_a_rulebook.csv')

def bootstrap_ci(values, rng=None, n_boot=500, alpha=0.05):
    values=np.asarray(values, dtype=float)
    values=values[np.isfinite(values)]
    if len(values)==0: return (float('nan'), float('nan'), float('nan'))
    mean=float(np.mean(values))
    if len(values)==1: return (mean, mean, mean)
    rng = np.random.default_rng(42) if rng is None else rng
    boots=[]
    for _ in range(n_boot):
        boots.append(float(np.mean(rng.choice(values, size=len(values), replace=True))))
    lo,hi=np.percentile(boots,[100*alpha/2,100*(1-alpha/2)])
    return mean,float(lo),float(hi)

