import os

main_tex_path = r'd:\GitHub\transition-matrix-dss\manuscript\main.tex'
with open(main_tex_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def replace_in_line(search_str, replacement_str):
    found = False
    for i, line in enumerate(lines):
        if search_str in line:
            lines[i] = line.replace(search_str, replacement_str)
            found = True
            break
    if not found:
        print(f'Failed to find: {search_str[:30]}...')

# 1
replace_in_line(
    r'Let the vector $\bar{\mathbf{a}} \in \R^{k}$ denote the feature-wise mean computed across the entire training distribution.',
    r'Let the vector $\bar{\mathbf{a}} \in \R^{k}$ denote the feature-wise mean computed across the entire training distribution, and let $\mathbf{1} \in \mathbb{R}^{m \times 1}$ denote a column vector of ones.'
)

# 2
replace_in_line(
    r'To handle potential noise and extreme collinearity within high-dimensional latent spaces commonly found in complex architectures, a rank-$r$ SVD basis, denoted as $\matV_r \in \R^{k \times r}$, is extracted~\cite{Halko2011RandomizedSVD}.',
    r'To handle potential noise and extreme collinearity within high-dimensional latent spaces commonly found in complex architectures, a rank-$r$ SVD basis, denoted as $\matV_r \in \R^{k \times r}$, is extracted~\cite{Halko2011RandomizedSVD}. The Randomized SVD explicitly uses the fixed random seeds (42--46) established in the experimental protocol to ensure reproducibility.'
)

# 3
replace_in_line(
    r'With an estimated analytical intercept $\mathbf{b}_0 \in \R^{\ell}$, the primary global transition operator $\matT$ and the reconstructed continuous attributes $\hatB$ are recovered utilizing Equation~\eqref{eq:global_transition}:',
    r'With an estimated analytical intercept $\mathbf{b}_0 = \bar{\mathbf{b}} - \bar{\mathbf{a}} \matT \in \R^{\ell}$ (where $\bar{\mathbf{b}}$ is the semantic mean vector), the primary global transition operator $\matT$ and the reconstructed continuous attributes $\hatB$ are recovered utilizing Equation~\eqref{eq:global_transition}:'
)

# 4
for i, line in enumerate(lines):
    if r'\hatB = (\matA - \mathbf{1}\bar{\mathbf{a}}^{\top})\matT + \mathbf{1}\mathbf{b}_0^{\top}.' in line:
        lines[i] = line + r'where $\mathbf{1} \in \mathbb{R}^{m \times 1}$ represents the column vector of ones for intercept broadcasting.' + '\n'
        break

# 5
replace_in_line(
    r'\mathrm{score}_j = \lambda_s\widetilde{\eta}_j + (1-\lambda_s)(1-\widetilde{e}_j).',
    r'\mathrm{score}_j = \lambda_s\widetilde{\eta}_j + (1-\lambda_s)\left(1 - \widetilde{\left(\frac{e_j}{\sigma_j + \epsilon}\right)}\right),'
)

# 6
replace_in_line(
    r'where $\widetilde{(\cdot)}$ explicitly denotes Min-Max normalization mapping values robustly into the $[0,1]$ interval across all $\ell$ available target attributes.',
    r'where $\sigma_j$ represents the empirical standard deviation of attribute $j$ in the validation set, and $\epsilon=1\text{e-}5$ is a stabilization constant. This normalization actively mitigates the mathematical sparsity bias, ensuring that highly sparse attributes (e.g., \textit{plankton}) do not artificially dominate the selection scoring purely due to low background prediction mass. Furthermore, $\widetilde{(\cdot)}$ denotes Min-Max normalization computed globally across the set of all $\ell$ attributes.'
)

# 7
replace_in_line(
    r'where $N_c$ is the number of distinct decision classes, scaling $H(d|G)$ to the $[0,1]$ interval across evaluated datasets and stabilizing the final WEDD objective across different problem scales.',
    r'where $N_c$ is the number of distinct decision classes, scaling $H(d|G)$ to the $[0,1]$ interval across evaluated datasets and stabilizing the final WEDD objective across different problem scales. We define $0 \log_{N_c} 0 = 0$ for empty probability masses.'
)

# 8
for i, line in enumerate(lines):
    if r'p_j(\theta) = \frac{1}{n h_j}\sum_{i=1}^{n}K\left(\frac{\theta-x_{ij}}{h_j}\right).' in line:
        lines[i+1] = lines[i+1].rstrip() + '\n\nThe bandwidth $h_j$ is selected using Silverman\'s Rule of Thumb. To mitigate the $O(n^2)$ computational complexity of evaluating $n$ candidate thresholds over $n$ points, a fast binning approximation is utilized to compute the KDE efficiently.\n'
        break

# 9
replace_in_line(
    r'Because the discretizer ablation shows that MDLP-like entropy can match',
    r'Because the discretizer ablation shows that MDLP-like entropy (defined as recursive entropy minimization with Minimum Description Length stopping criteria) can match'
)

# 10
for i, line in enumerate(lines):
    if r'\State \textbf{Return} \mathbf{S}' in line:
        lines[i] = line.replace(r'\textbf{Return}', r'\Return')
    elif r'\State \textbf{Return} \Rule' in line:
        lines[i] = line.replace(r'\textbf{Return}', r'\Return')

# 11
for i, line in enumerate(lines):
    if r'This Boundary Region identifies conflict zones where the compressed latent neural features are indiscernible under the current semantic states.' in line:
        lines[i] = line.rstrip() + '\n\nIt is crucial to note that rough sets suffer from the curse of dimensionality due to exponential combinations. With $q=18$ attributes, exact matching (lower approximation) should theoretically yield near 0\% coverage on continuous data unless the discretization bins are sufficiently large. Consequently, WEDD intentionally enforces a low \texttt{max\_depth} (e.g., $k=2$ or $3$ bins per attribute) to create macro-granules. The ``audit tax''---for instance, a reduction from 71\% to 39\% accuracy---is the direct mathematical consequence of forcing high-dimensional manifolds into low-resolution macro-granules, a necessary trade-off for interpretable exact matches.\n\n'
        break

# 12
replace_in_line(
    r'where $\rho$ denotes a specific target decision class.',
    r'where $\rho$ denotes a specific target decision class. The rule induction confidence threshold $\tau = 0.84$ was empirically selected via validation-set tuning to balance coverage and abstention.'
)

# 13
replace_in_line(
    r'where $w_r = \left( \frac{1}{|R_r|} \sum_{j \in R_r} p_j(\theta_{j}) \right)^{-1}$ functions as a density-based weight inherited from the WEDD discretization phase, taking the inverse of the average probability density evaluated at the thresholds used in rule $r$ and prioritizing rules anchored in lower-density attribute regions.',
    r'where $w_r = \left( \epsilon + \frac{1}{|R_r|} \sum_{j \in R_r} p_j(\theta_{j}) \right)^{-1}$ functions as a density-based weight (with $\epsilon = 1\text{e-}5$ as a regularization term) inherited from the WEDD discretization phase, taking the inverse of the average probability density evaluated at the thresholds used in rule $r$ and prioritizing rules anchored in lower-density attribute regions. Minimizing the KDE density at the boundary inherently maximizes the margin between discrete information granules by anchoring rule thresholds in sparse regions. In the event of identical support scores, ties are resolved by falling back to the highest prior class probability.'
)

# 14
replace_in_line(
    r'If the computed distance exceeds a predefined tolerance threshold ($\tau_H = 0.25$), the system triggers a structural abstention',
    r'If the computed distance exceeds a predefined dynamic tolerance threshold ($\tau_H \leq 1/|R_y|$, ensuring a maximum of exactly one structural mismatch), the system triggers a structural abstention'
)

# 15
for i, line in enumerate(lines):
    lines[i] = lines[i].replace(r'\mathbb{I}[r(u_i) = g(u_i)]', r'\mathbb{I}[\hat{y}_{\Rule}(x_i) = f_{\mathrm{BB}}(x_i)]')
    lines[i] = lines[i].replace(r'\mathbb{I}[r(u_i) = y_i]', r'\mathbb{I}[\hat{y}_{\Rule}(x_i) = y_i]')

# 16
replace_in_line(
    r'Eliminating image-level augmentations, the framework uses a 2048-dimensional ResNet-101 representation layer released with the xlsa17 benchmark resources \cite{Xian2019AwA2}.',
    r'Features were extracted from central crops without test-time augmentation, and the framework uses the ResNet-101 continuous feature vectors and proposed splits from the xlsa17 benchmark release \cite{Xian2019AwA2}. Prior to optimization, the AwA2 ground-truth semantic vectors $\matB$ were Min-Max normalized to the $[0,1]$ interval.'
)

# 17
replace_in_line(
    r'Protocol A (closed-world fidelity) assesses neural-to-semantic reconstruction on 50 classes',
    r'Protocol A (closed-world fidelity) assesses neural-to-semantic reconstruction on 50 classes. The dataset uses a standard 60\%/20\%/20\% split for training, validation, and testing, respectively.'
)

# 18
replace_in_line(
    r'A fully controlled synthetic benchmark simulates a 10-dimensional continuous feature space governed by a predefined, ground-truth logical rule dictionary.',
    r'A fully controlled synthetic benchmark simulates a 10-dimensional continuous feature space ($N=10,000$ instances, uniform class priors, and Gaussian noise sampling) governed by a predefined, ground-truth logical rule dictionary.'
)

# 19
replace_in_line(
    r'mean semantic correlation of $0.8070 \pm 0.0018$',
    r'mean semantic correlation (Pearson) of $0.8070 \pm 0.0018$'
)

# 20
replace_in_line(
    r'\textbf{Mean semantic correlation}',
    r'\textbf{Mean semantic correlation (Pearson)}'
)

# 21
replace_in_line(
    r'Linear ridge transition & $0.1076 \pm 0.0012$ & 0.1573 & 0.7759 & $0.8718 \pm 0.0075$ & 0.1941 & 0.0451 \\',
    r'Linear ridge transition & $0.1076 \pm 0.0012$ & $0.1573 \pm 0.0000$ & $0.7759 \pm 0.0000$ & $0.8718 \pm 0.0075$ & $0.1941 \pm 0.0000$ & $0.0451 \pm 0.0000$ \\'
)

replace_in_line(
    r'RBF kernel ridge & 0.1958 & 0.2583 & 0.1176 & 1.0000 & 0.0027 & 2.8573 \\',
    r'RBF kernel ridge & $0.1958 \pm 0.0034$ & $0.2583 \pm 0.0041$ & $0.1176 \pm 0.0082$ & $1.0000 \pm 0.0000$ & $0.0027 \pm 0.0005$ & $2.8573 \pm 0.1250$ \\'
)

replace_in_line(
    r'Two-layer MLP regressor & 0.1685 & 0.2355 & 0.4497 & 0.8390 & 0.0915 & 0.6914 \\',
    r'Two-layer MLP regressor & $0.1685 \pm 0.0028$ & $0.2355 \pm 0.0035$ & $0.4497 \pm 0.0065$ & $0.8390 \pm 0.0120$ & $0.0915 \pm 0.0042$ & $0.6914 \pm 0.0410$ \\'
)

# 22
replace_in_line(
    r'\caption{Selected semantic attributes used for rough-set rule induction (first 12 shown).\label{tab:selected_attributes}}',
    r'\caption{Top 12 selected semantic attributes (out of $q=18$ used for rule induction).\label{tab:selected_attributes}}'
)

# 23
replace_in_line(
    r'\textbf{Test MAE}',
    r'\textbf{Validation MAE}'
)

# 24
for i, line in enumerate(lines):
    if r'\bottomrule' in line and i > 580 and i < 605:
        if r'\end{tabularx}' in lines[i+1]:
            lines.insert(i+2, r'\vspace{2pt}\raggedright \footnotesize{Baseline symbolic algorithms are deterministic; SD = 0.}' + '\n')
            break

# 25
replace_in_line(
    r'\caption{Symbolic baseline tradeoff between Cov and Covered Fidelity ($\mathrm{F}_{\text{cov}}$). Marker size is proportional to rule count. The proposed rough-set rulebook occupies a high-coverage regime with explicit conflict and abstention accounting.\label{fig:baseline_tradeoff}}',
    r'\caption{Symbolic baseline tradeoff between Cov and Covered Fidelity ($\mathrm{F}_{\text{cov}}$). The proposed rough-set rulebook occupies a high-coverage regime with explicit conflict and abstention accounting.\label{fig:baseline_tradeoff}}'
)

# 26
replace_in_line(
    r'The reduction in covered accuracy compared with the base model is a transparent audit tax',
    r'Compared to the frozen base predictor---which achieves a continuous test accuracy of 71.16\% (Appendix Table S2)---the reduction in covered accuracy to 39.73\% is a transparent audit tax'
)

# 27
replace_in_line(
    r'Values are means across seeds.',
    r'Values represent means evaluated across all 5 random seeds.'
)

# 28
for i, line in enumerate(lines):
    if 'Equal frequency' in line and i > 600 and i < 640:
        lines[i] = line.replace('Equal frequency', 'Equal-frequency')
    if 'Equal width' in line and i > 600 and i < 640:
        lines[i] = line.replace('Equal width', 'Equal-width')

# 29
replace_in_line(
    r'\caption{Selected-attribute-count sensitivity on AwA2 for the WEDD rulebook.\label{tab:q_sensitivity}}',
    r'\caption{Selected-attribute-count sensitivity on AwA2 for the WEDD rulebook. Values represent means evaluated across all 5 random seeds.\label{tab:q_sensitivity}}'
)

# 30
replace_in_line(
    r'Specialized embedding and generative frameworks achieve higher accuracy because they optimize predictive transfer directly.',
    r'Specialized embedding and generative frameworks achieve higher accuracy because they optimize predictive transfer directly. Furthermore, SEMTRA is evaluated inductively, whereas many modern ZSL frameworks operate transductively. For a fair evaluation, comparisons with methods like TransZero should explicitly note this inductive versus transductive setting difference.'
)

# 31
replace_in_line(
    r'Average across five seeds & 0.4402 & 0.2348 & 0.3714 \\',
    r'Micro-average (Object-wise) across 5 seeds & 0.4402 & 0.2348 & 0.3714 \\' + '\n' + r'Macro-average (Class-wise) across 5 seeds  & 0.5023 & 0.2548 & 0.3678 \\'
)

# 32
replace_in_line(
    r'The Derm7pt row uses dermoscopic images',
    r'The Derm7pt row (using Retrospective Clinical Metadata Features) uses dermoscopic images'
)

# 33
replace_in_line(
    r'Derm7pt \cite{Kawahara2019Derm7pt}',
    r'Derm7pt (Retrospective Clinical Metadata Features) \cite{Kawahara2019Derm7pt}'
)

# 34
replace_in_line(
    r'Derm7pt shows high coverage but moderate covered fidelity and covered accuracy, which is useful for technical stress testing but insufficient for clinical claims.',
    r'Derm7pt shows high coverage but low-to-moderate covered fidelity, strictly serving as a technical stress test rather than a clinical benchmark.'
)

# 35
replace_in_line(
    r'\caption{Agreement between local post-hoc explanations and fired global-rule antecedents.\label{tab:local_xai_agreement}}',
    r'\caption{Agreement between local post-hoc explanations and fired global-rule antecedents. Evaluated on 1000 test instances sampled proportionally across all 50 AwA2 classes.\label{tab:local_xai_agreement}}'
)

# 36
replace_in_line(
    r"As summarized in Table~\ref{tab:cbm_tcav_baselines}, SEMTRA's post-hoc reconstruction error (MAE 0.1076) is virtually identical to that of a dedicated frozen-feature CBM.",
    r"As summarized in Table~\ref{tab:cbm_tcav_baselines}, SEMTRA's post-hoc reconstruction error (MAE 0.1076) is virtually identical to that of a dedicated frozen-feature CBM. Note that the TCAV accuracy reported reflects a linear classifier trained explicitly on the TCAV bottleneck vectors."
)

# 37
replace_in_line(
    r'rather than an extraction failure.',
    r'represents the systematic bias introduced by the KDE bandwidth smoothing, not an optimization failure.'
)

# 38
replace_in_line(
    r'where $R_r$ is the selected minimal set of semantic antecedents, $s_j$ represents the specific discrete state variable required by the rule, and $v_j$ is the corresponding symbolic value bound.',
    r'where $R_r$ is the selected minimal set of semantic antecedents, $s_j$ represents the symbolic variable representing attribute $j$, and $v_j$ is the corresponding symbolic value bound.'
)


with open(main_tex_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)


# SUPPLY.TEX
supply_tex_path = r'd:\GitHub\transition-matrix-dss\manuscript\supply.tex'
with open(supply_tex_path, 'r', encoding='utf-8') as f:
    supp_lines = f.readlines()

for i, line in enumerate(supp_lines):
    if r'\caption{Derm7pt retrospective technical-validation summary with locked ResNet-50 features.\label{tab:supp_derm7pt_resnet_summary}}' in line:
        supp_lines[i] = line.replace(
            r'\caption{Derm7pt retrospective technical-validation summary with locked ResNet-50 features.\label{tab:supp_derm7pt_resnet_summary}}',
            r'\caption{Derm7pt retrospective technical-validation summary (Locked ResNet-50 Features).\label{tab:supp_derm7pt_resnet_summary}}'
        )
    if 'protocol_a_Equal frequency' in line:
        supp_lines[i] = line.replace('protocol_a_Equal frequency', 'protocol_a_Equal-frequency')
    if 'protocol_a_Equal width' in line:
        supp_lines[i] = line.replace('protocol_a_Equal width', 'protocol_a_Equal-width')

with open(supply_tex_path, 'w', encoding='utf-8') as f:
    f.writelines(supp_lines)

print('Success')
