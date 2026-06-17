#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd
SCRIPT_DIR=Path(__file__).resolve().parent; sys.path.insert(0, str(SCRIPT_DIR))
if str(SCRIPT_DIR.parent / "core") not in sys.path: sys.path.insert(0, str(SCRIPT_DIR.parent / "core"))
from paper1_core import ensure_dir, tex_escape

def fmt(x):
    try:
        if isinstance(x,str): return tex_escape(x)
        if pd.isna(x): return '--'
        if isinstance(x,(int,np.integer)): return str(int(x))
        return f'{float(x):.4f}'
    except Exception:
        return tex_escape(x)

def table(path, caption, label, headers, rows, spec=None, small=True, note=None):
    if spec is None: spec='l' * len(headers)
    s=[]; s.append('\\begin{table}[H]')
    s.append(f'\\caption{{{caption}\\label{{{label}}}}}')
    s.append('\\begin{adjustwidth}{-\\extralength}{0cm}')
    s.append('\\centering')
    if small: s.append('\\small')
    s.append(f'\\begin{{tabularx}}{{\\fulllength}}{{{spec}}}')
    s.append('\\toprule')
    s.append(' & '.join(headers) + ' \\\\')
    s.append('\\midrule')
    for r in rows:
        s.append(' & '.join(fmt(v) for v in r) + ' \\\\')
    s.append('\\bottomrule')
    s.append('\\end{tabularx}')
    if note:
        s.append(f'\\noindent\\footnotesize{{{note}}}')
    s.append('\\end{adjustwidth}')
    s.append('\\end{table}')
    Path(path).write_text('\n'.join(s),encoding='utf-8')

def main():
    pkg=Path(__file__).resolve().parents[1]; tdir=ensure_dir(pkg/'tables'); art=pkg/'artifacts'/'awa2'
    # Feature extractor and base predictor hyperparameters
    meta=json.loads((art/'revision_transition_cache_meta.json').read_text())
    rows=[
        ['Feature extractor','ResNet-101 features released with AwA2','ILSVRC-pretrained representation layer; no image-level augmentation in this package'],
        ['Feature dimension','2048','Global average/penultimate representation coordinates'],
        ['Auxiliary compression',meta['n_components'],meta.get('cache_note','revision cache')],
        ['Base predictor','Ridge classifier','Trained on variance-screened representation coordinates'],
        ['Random seed',meta['seed'],'Used for all stochastic revision experiments'],
        ['Semantic bridge','Ridge regression','Grid alpha in {0.01, 0.1, 1, 10, 100}'],
        ['Rule thresholds','WEDD','alpha=0.65, max_depth=2, min_bin_size=30, min_gain=0.002'],
        ['Rule induction','Greedy reducts','tau=0.84, s_min=18 for AwA2 Protocol A']]
    table(tdir/'table_feature_extractor_hyperparameters.tex','Feature extractor, base predictor, and revision-experiment hyperparameters.','tab:feature_hyperparameters',['Component','Value','Implementation detail'],rows,'lXX')
    pd.DataFrame(rows,columns=['Component','Value','Implementation detail']).to_csv(tdir/'feature_extractor_hyperparameters.csv',index=False)
    # Base predictor performance
    base=json.loads((art/'base_predictor_metrics.json').read_text())
    rows=[]
    for split in ['validation','test']:
        m=base[split]; rows.append([split.title(),m['top1_accuracy'],m['top5_accuracy'],m['macro_f1'],m['weighted_f1'],m.get('macro_auroc_ovr',np.nan),m.get('ece_10bin',np.nan)])
    table(tdir/'table_base_predictor_performance.tex','Base predictor performance on AwA2 Protocol A.','tab:base_predictor_performance',['Split','Top-1','Top-5','Macro-F1','Weighted-F1','AUROC','ECE'],rows,'lXXXXXX')
    pd.DataFrame(rows,columns=['Split','Top-1','Top-5','Macro-F1','Weighted-F1','AUROC','ECE']).to_csv(tdir/'base_predictor_performance.csv',index=False)
    # Local XAI agreement
    loc=json.loads((art/'local_xai_agreement.json').read_text())['summary']; ldf=pd.DataFrame(loc)
    rows=[]
    for method,g in ldf.groupby('method'):
        vals={r['metric']:r for _,r in g.iterrows()}
        rows.append([method,vals['topk_antecedent_agreement']['n'],vals['topk_antecedent_agreement']['mean_rule_length'],vals['topk_antecedent_agreement']['mean'],vals['signed_direction_agreement']['mean'],vals['spearman_rule_salience']['mean'],f"[{vals['topk_antecedent_agreement']['ci95_low']:.4f}, {vals['topk_antecedent_agreement']['ci95_high']:.4f}]"])
    table(tdir/'table_local_xai_agreement.tex','Agreement between local post-hoc explanations and fired global-rule antecedents.','tab:local_xai_agreement',['Method','n','Mean rule length','Top-k agreement','Direction agreement','Rank correlation','95\\% CI'],rows,'lXXXXXX')
    pd.DataFrame(rows,columns=['Method','n','Mean rule length','Top-k agreement','Direction agreement','Rank correlation','95\\% CI']).to_csv(tdir/'local_xai_agreement.csv',index=False)
    # CBM and TCAV
    cbm=json.loads((art/'cbm_metrics.json').read_text())['test']; tcav=pd.read_csv(art/'tcav_metrics.csv')
    rows=[['Frozen-feature CBM',cbm['semantic_mae'],cbm['semantic_rmse'],cbm['concept_correlation_mean'],cbm['top1_accuracy'],cbm['top5_accuracy'],cbm['macro_f1']],['TCAV at released representation layer',np.nan,np.nan,np.nan,float(tcav['tcav_score_positive_sensitivity'].mean()),float(tcav['selected_by_transition'].mean()),float(tcav['mean_directional_sensitivity'].mean())]]
    table(tdir/'table_cbm_tcav_baselines.tex','Concept-based baselines on AwA2.','tab:cbm_tcav_baselines',['Baseline','MAE','RMSE','Concept corr.','Score/Top-1','Overlap/Top-5','Macro-F1/Sensitivity'],rows,'lXXXXXX',note='For TCAV, the score column reports mean positive directional sensitivity; the overlap column reports overlap with transition-selected attributes.')
    pd.DataFrame(rows,columns=['Baseline','MAE','RMSE','Concept corr.','Score/Top-1','Overlap/Top-5','Macro-F1/Sensitivity']).to_csv(tdir/'cbm_tcav_baselines.csv',index=False)
    # Symbolic baselines
    sym=pd.read_csv(art/'symbolic_baselines_metrics.csv')
    rows=[]
    for _,r in sym.iterrows(): rows.append([r['method'],r['rule_count'],r['avg_antecedent_length'],r['coverage'],r['abstention'],r['accuracy_all'],r['accuracy_covered'],r['covered_fidelity_to_base'],r['all_object_fidelity_to_base'],r['conflict_rate']])
    table(tdir/'table_symbolic_baselines.tex','Symbolic baseline comparison on reconstructed semantic attributes.','tab:symbolic_baselines',['Method','Rules','Avg. len.','Coverage','Abstention','All acc.','Cov. acc.','Cov. fidelity','All fidelity','Conflict'],rows,'lXXXXXXXXX')
    # Discretizer ablation replaces WEDD table
    disc=pd.read_csv(art/'discretizer_ablation_metrics.csv')
    rows=[]
    for _,r in disc.iterrows(): rows.append([r['method'],r['threshold_count'],r['rule_count'],r['mean_rule_length'],r['coverage'],r['abstention'],r['accuracy_all'],r['covered_fidelity_to_base'],r['conflict_rate']])
    table(tdir/'table_wedd_ablation.tex','Discretization ablation using the same reconstructed semantics and rule-induction logic.','tab:wedd_ablation',['Method','Thresholds','Rules','Avg. len.','Coverage','Abstention','All acc.','Cov. fidelity','Conflict'],rows,'lXXXXXXXX',note='MDLP-like entropy uses entropy-improvement stopping; equal-frequency and equal-width use two thresholds per selected attribute. No fallback-only row is reported as rule coverage.')
    disc.to_csv(tdir/'wedd_ablation.csv',index=False)
    # Transition operator ablation
    tr=pd.read_csv(art/'transition_operator_ablation.csv')
    rows=[]
    for _,r in tr.iterrows(): rows.append([r['operator'],r['semantic_mae'],r['semantic_rmse'],r['semantic_correlation_mean'],r['prototype_accuracy'],r['rule_coverage'],r['rule_accuracy_all'],r['runtime_seconds']])
    table(tdir/'table_transition_operator_ablation.tex','Semantic reconstruction and rule-transfer ablation for linear and nonlinear operators.','tab:transition_operator_ablation',['Operator','MAE','RMSE','Corr.','Proto. acc.','Rule cov.','Rule acc.','Runtime (s)'],rows,'lXXXXXXX')
    # Explainability metrics
    rules=pd.read_csv(art/'protocol_a_rulebook.csv'); prop=pd.read_csv(art/'protocol_a_test_rule_predictions.csv'); base_pred=pd.read_csv(art/'base_predictor_predictions.csv'); base_test=base_pred[base_pred['split']=='test']['base_prediction'].to_numpy(dtype=int); pp=prop['prediction'].to_numpy(dtype=int); cov=pp>=0
    ex=[['Number of rules',len(rules)],['Average conditions per rule',rules['antecedent_length'].mean()],['Median conditions per rule',rules['antecedent_length'].median()],['Sparsity score',1-rules['antecedent_length'].mean()/len(pd.read_csv(art/'protocol_a_selected_attributes.csv'))],['Coverage',cov.mean()],['Abstention',1-cov.mean()],['Conflict rate',prop['conflict'].mean()],['Mean support',rules['support'].mean()],['Mean confidence',rules['confidence'].mean()],['Covered fidelity',np.mean(pp[cov]==base_test[cov])],['All-object fidelity',np.mean(pp==base_test)],['Top-1 accuracy (all)',np.mean(pp==np.load(art/'revision_transition_cache.npz')['y_test'])],['Top-5 accuracy','--']]
    table(tdir/'table_explainability_metrics.tex','Quantitative explainability and fidelity metrics for the proposed rulebook.','tab:explainability_metrics',['Metric','Value'],ex,'lX')
    pd.DataFrame(ex,columns=['Metric','Value']).to_csv(tdir/'explainability_metrics.csv',index=False)
    # Rule stability
    st=pd.read_csv(art/'rule_stability_noise.csv')
    rows=[[r['sigma'],r['rule_consistency'],r['decision_consistency'],r['coverage'],r['coverage_change'],r['abstention'],r['conflict_rate']] for _,r in st.iterrows()]
    table(tdir/'table_rule_stability.tex','Rule consistency under semantic-representation perturbations.','tab:rule_stability',['Sigma','Rule consistency','Decision consistency','Coverage','Coverage change','Abstention','Conflict'],rows,'XXXXXXX')
    # Protocol B official
    pb=pd.read_csv(art/'protocol_b_unseen_per_class.csv')
    rows=[[r['class_name'],r['n_objects'],r['prototype_accuracy'],r['symbolic_template_accuracy'],r['mean_hamming']] for _,r in pb.iterrows()]
    table(tdir/'table_protocol_b.tex','Official AwA2 xlsa17 unseen-class transfer results.','tab:protocol_b',['Unseen class','Objects','Prototype acc.','Symbolic template acc.','Mean Hamming'],rows,'lXXXX')
    # Related work table
    rw=[['LIME','Yes','Local','Weighted local surrogate','No','Optional','No','Stability and locality depend on perturbations'],['SHAP','Yes','Local','Additive feature attributions','No','Optional','No','Can be costly and not a rulebook'],['TCAV','Yes','Global/local','Concept directional sensitivity','No','Yes','No','Requires concept examples and layer choice'],['CBM','No/partial','Global','Concept bottleneck predictions','Usually yes','Yes','No','Requires concept supervision or retraining'],['Decision trees','No/yes','Global','Tree paths','Yes','No','Implicit rules','May become large or unstable'],['RIPPER','No/yes','Global','Separate-and-conquer rules','Yes','No','Yes','Sensitive to discretization and order'],['Rough sets','Yes','Global','Reducts and lower approximations','No','Yes if table semantic','Yes','Needs symbolic decision table'],['Transition matrices','Yes','Global','Semantic reconstruction matrix','No','Yes','No','Continuous concepts are not yet rules'],['Proposed framework','Yes','Global plus instance traces','Transition, WEDD, rough-set rules','No','Yes','Yes','Trades accuracy for auditability and abstention']]
    table(tdir/'table_related_work.tex','Comparison of XAI method families.','tab:related_work',['Method','Post-hoc','Scope','Artifact','Retraining','Concepts','Rules','Typical limitation'],rw,'lXXXXXXX')
    # Abbreviations and variables (manual to preserve math macros)
    (tdir/'table_abbreviations_variables.tex').write_text(r"""
\begin{table}[H]
\caption{Abbreviations and variables used in the manuscript.\label{tab:abbreviations_variables}}
\begin{adjustwidth}{-\extralength}{0cm}
\centering
\small
\begin{tabularx}{\fulllength}{lX}
\toprule
Symbol/term & Meaning \\
\midrule
$\matA$ & Formal/trained representation matrix \\
$\matB$ & Semantic attribute matrix \\
$\hatB$ & Reconstructed semantic attribute matrix \\
$\matT$ & Global transition operator \\
$\matW$ & Compressed transition weights \\
$V_r$ & Right singular vectors or compression basis \\
$\U$ & Universe of objects \\
$\C$ & Conditional attributes \\
$d$ & Decision attribute \\
$\V$ & Attribute-value domains \\
$f$ & Information function \\
$\theta$ & Candidate discretization threshold \\
$\lambda$ & WEDD entropy-density mixing coefficient or ridge regularization coefficient, depending on context \\
$q$ & Number of selected semantic attributes \\
$\tau$ & Minimum rule confidence \\
$s_{\min}$ & Minimum rule support \\
WEDD & Weighted Entropy-Density Discretization \\
CBM & Concept Bottleneck Model \\
TCAV & Testing with Concept Activation Vectors \\
LIME & Local Interpretable Model-agnostic Explanations \\
SHAP & SHapley Additive exPlanations \\
CART & Classification and Regression Trees \\
MDLP & Minimum Description Length Principle discretization \\
KDE & Kernel density estimation \\
MAE & Mean absolute error \\
RMSE & Root mean squared error \\
F1 & Harmonic mean of precision and recall \\
AUROC & Area under the receiver operating characteristic curve \\
Coverage & Fraction of objects receiving a non-abstained rule decision \\
Abstention & Fraction of objects without a rule decision \\
Confidence & Empirical rule precision \\
Support & Number of objects satisfying a rule antecedent \\
Fidelity & Agreement between the rulebook and base predictor \\
Rule consistency & Same rule fires after perturbation \\
\bottomrule
\end{tabularx}
\end{adjustwidth}
\end{table}
""".lstrip(), encoding='utf-8')
    # Synthetic combined table (already exists but copy CSV with four decimals remains)
    print('revision tables generated')
if __name__=='__main__': main()
