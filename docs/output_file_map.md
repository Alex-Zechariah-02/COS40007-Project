# Output File Map

## SVR branch

- `data/tables/final_svr_metrics.csv` → SVR final evaluation
- `data/tables/test_predictions.csv` → SVR predictions and comparison
- `data/tables/residual_summary.csv` → SVR error diagnostics
- `data/tables/permutation_importance.csv` → SVR feature influence
- `figures/svr/` → SVR visual evidence

## RandomForestRegressor branch

- `data/random_forest/tables/final_rf_metrics.csv` → RF final evaluation
- `data/random_forest/tables/test_predictions.csv` → RF predictions and comparison
- `data/random_forest/tables/residual_summary.csv` → RF error diagnostics
- `data/random_forest/tables/native_feature_importance.csv` → RF native feature importance
- `data/random_forest/tables/permutation_importance.csv` → RF permutation importance
- `figures/random_forest/` → RF visual evidence

## Comparison section

- SVR and RF final metrics are combined in the metric leaderboard.
- SVR and RF test predictions are merged by state, stage, sex, input year, and target year for row-level comparison.
