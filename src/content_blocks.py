SUPERVISED_OVERVIEW = """
This application presents the supervised-regression workflow for State Completion Rate Prediction. The shared workflow covers the data, target, features, leakage checks, chronological split, and baselines. The completed model branch is Support Vector Regression, and the RandomForestRegressor branch is reserved until validated outputs are available.
"""

WHY_REGRESSION = """
The target is a numeric next-year completion-rate value, so this is regression. Accuracy, precision, recall, F1-score, confusion matrix, and classification report are not used in the main supervised workflow.
"""

WHY_CHRONOLOGICAL = """
The task predicts a future year from current-year information. Chronological validation is used because shuffled K-Fold could train on future years and validate on earlier years, which would be misleading for forecasting-style regression.
"""

WHY_BASELINES = """
Baselines show whether the trained model adds value beyond simple rules. The model must be compared against a training-mean baseline and a persistence baseline, not judged by isolated RMSE or R² alone.
"""

WHY_LEAKAGE = """
Leakage control prevents future target information from entering the feature matrix. Current-year completion features are valid autoregressive predictors, but next-year targets, target-year values, and future source data are forbidden as inputs.
"""

NO_CLUSTERING = """
Clustering is excluded from this application. The focus is the supervised regression workflow: shared data preparation, the completed SVR branch, the reserved RandomForestRegressor branch, and the future supervised model comparison.
"""

METRIC_GUIDE = """
MAE is the primary error measure because it is directly interpretable in completion-rate percentage points. RMSE penalizes large mistakes. R² is a guardrail against weak held-out explanatory performance. Median absolute error describes a typical row more robustly than the mean.

Abbreviations: AE = Absolute Error; MAE = Mean Absolute Error; RMSE = Root Mean Squared Error; pp = percentage points.
"""

SVR_BRANCH_TAKEAWAYS = [
    "The SVR branch is a supervised regression workflow, not classification.",
    "The target is next-year school completion rate.",
    "The main row unit is state-stage-sex-year using male and female rows.",
    "Chronological validation is used to avoid future-year leakage.",
    "SVR improved MAE and RMSE over the tested baselines on the held-out test set.",
    "R² is negative, so the result should be interpreted cautiously.",
    "The residual diagnostics show underprediction bias.",
    "The branch is ready for later comparison with RandomForestRegressor once the RF outputs are validated.",
]
