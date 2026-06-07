METRIC_DEFINITIONS = {
    "MAE": {
        "full_name": "Mean Absolute Error",
        "better": "Lower is better",
        "meaning": "Average absolute prediction error in completion-rate percentage points.",
    },
    "RMSE": {
        "full_name": "Root Mean Squared Error",
        "better": "Lower is better",
        "meaning": "Error metric that penalises larger prediction errors more strongly than MAE.",
    },
    "R²": {
        "full_name": "R-squared",
        "better": "Higher is better",
        "meaning": "Held-out explanatory performance relative to a mean-style reference. Negative values indicate weak held-out explanatory power.",
    },
    "Median AE": {
        "full_name": "Median Absolute Error",
        "better": "Lower is better",
        "meaning": "Typical absolute prediction error for the middle held-out row.",
    },
    "Mean residual": {
        "full_name": "Mean residual = actual minus predicted",
        "better": "Closer to 0 is better",
        "meaning": "Positive values mean the model underpredicted on average; negative values mean it overpredicted on average.",
    },
    "Within tolerance": {
        "full_name": "Tolerance coverage",
        "better": "Higher is better",
        "meaning": "Percentage of predictions within a specified absolute-error band, such as ±2 percentage points.",
    },
}

ABBREVIATION_NOTE = "AE = Absolute Error; MAE = Mean Absolute Error; RMSE = Root Mean Squared Error; R² = R-squared; pp = percentage points."
