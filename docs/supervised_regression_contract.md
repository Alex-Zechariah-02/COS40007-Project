# Supervised Regression Contract

The supervised model branches are compared only because they use the same modelling target and compatible held-out evaluation design.

## Shared target

- Main target: `next_year_completion_rate`
- Task type: supervised regression
- Classification metrics are excluded.

## Shared evaluation metrics

- MAE
- RMSE
- R²
- Median AE

## Comparison rule

MAE is the primary ranking metric because it is directly interpretable in completion-rate percentage points. RMSE, R², Median AE, residual diagnostics, tolerance coverage, and grouped errors are supporting evidence.
