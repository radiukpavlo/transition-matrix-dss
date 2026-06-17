# Statistical Assessment

Revision v2 adds nonparametric bootstrap intervals around the v1 audit artifacts without rewriting the v1 bundle.

Bootstrap rows generated: 38 across 3 dataset scopes.
Object-level intervals: 18. Seed-level intervals: 20.

Paired WEDD-vs-MDLP intervals were generated over matched AwA2 seeds. These quantify the observed paired differences and do not justify wording that WEDD is universally superior.

Interpretation guardrails:

- Object-level intervals are available only for fields exported in v1 prediction files. Base-model labels are not present in those files, so covered-fidelity object-level intervals are intentionally omitted from the prediction-level bootstrap.
- Seed-wise intervals are based on five-seed v1 runs where available and should be read as stability diagnostics rather than population-level inferential guarantees.
- SUN and Derm7pt diagnostics remain scoped as portability and retrospective technical-validation checks.
