# Supervised Regression Contract

The supervised-regression branch predicts numeric next-year school completion rate. SVR and future RandomForestRegressor outputs must share the same target, row unit, split, baselines, and metrics.

- Target: `next_year_completion_rate`
- Row unit: state-stage-sex-year
- Metrics: MAE, RMSE, R², Median Absolute Error
- Baselines: training mean and persistence
- Validation: chronological, not shuffled K-Fold
- Classification metrics: not used
- Cluster labels: not a supervised target
