RF_REQUIRED_OUTPUT_FILES = [
    "rf_final_metrics.csv",
    "rf_test_predictions.csv",
    "rf_baseline_comparison.csv",
    "rf_error_by_state.csv",
    "rf_error_by_stage.csv",
    "rf_error_by_sex.csv",
    "rf_feature_importance.csv",
]

RF_REQUIRED_PREDICTION_COLUMNS = [
    "state",
    "stage",
    "sex",
    "input_year",
    "target_year",
    "actual_next_year_completion_rate",
    "predicted_next_year_completion_rate",
    "residual",
    "absolute_error",
    "model_name",
]

RF_INTEGRATION_RULES = [
    "Use the same target: next_year_completion_rate.",
    "Use the same primary row unit: state-stage-sex-year, male/female rows.",
    "Use the same held-out test year and identical test rows.",
    "Use the same baselines and regression metrics.",
    "Export prediction files using the required schema.",
    "Do not use classification metrics for the regression branch.",
]
