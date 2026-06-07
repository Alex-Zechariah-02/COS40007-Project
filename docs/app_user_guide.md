# App User Guide

Use the Streamlit application as a supervised-regression review system for state school completion-rate prediction.

## Recommended review order

1. Home
2. Supervised Regression System → 1. Overview
3. Supervised Regression System → 6. Validation and Baselines
4. SVR Branch → 1. Overview
5. Random Forest Branch → 1. Overview
6. Supervised Model Comparison → 2. Metric Leaderboard
7. Supervised Model Comparison → 6. AI Demonstrator Comparison
8. Limitations pages for each branch

## How to read metrics

- AE = Absolute Error.
- MAE = Mean Absolute Error. Lower is better.
- RMSE = Root Mean Squared Error. Lower is better.
- R² = R-squared. Higher is better.
- pp = percentage points.

## Main interpretation

The application compares two supervised-regression model branches: Support Vector Regression and RandomForestRegressor. Both are evaluated as numeric regression models, not classifiers. The current saved outputs favour SVR over RandomForestRegressor on the main held-out metrics.

## Current V4.1 status

- SVR branch: complete.
- RandomForestRegressor branch: complete.
- Official comparison branch: complete.
- Selected supervised model: Support Vector Regression.

Recommended review path:
1. Supervised Regression System → 1. Overview
2. SVR Branch → 1. Overview
3. Random Forest Branch → 1. Overview
4. Supervised Model Comparison → 1. Overview
5. Supervised Model Comparison → 2. Metric Leaderboard
6. Supervised Model Comparison → 6. AI Demonstrator Comparison
7. Supervised Model Comparison → 7. Forecast Preview Comparison
