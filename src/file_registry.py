SHARED_SCOPE_FILES = [
    ("project_context_summary.csv", "Smart Government project context"),
    ("selected_public_sector_datasets.csv", "Selected public-sector datasets"),
    ("selected_dataset_context.csv", "Dataset role context"),
    ("supervised_regression_framing.csv", "Regression framing"),
    ("excluded_scope.csv", "Excluded methods and metrics"),
]

RAW_AUDIT_FILES = [
    ("raw_dataset_inventory.csv", "Raw dataset rows, columns, and files"),
    ("raw_schema_audit.csv", "Column and schema audit"),
    ("raw_coverage_audit.csv", "Year and category coverage audit"),
    ("raw_data_quality_summary.csv", "Data quality summary"),
    ("missing_values_audit.csv", "Missing-value audit"),
    ("duplicate_key_audit.csv", "Duplicate-key audit"),
]

TARGET_FILES = [
    ("completion_target_panel.csv", "Completion target panel"),
    ("malaysia_benchmark.csv", "Malaysia benchmark rows"),
    ("main_target_panel.csv", "Main male/female target panel"),
    ("both_only_target_panel.csv", "Both-only sensitivity panel"),
    ("main_supervised_target_panel.csv", "Rows with next-year target"),
    ("row_unit_validation.csv", "Row-unit validation"),
    ("target_distribution_review.csv", "Target distribution review"),
]

FEATURE_FILES = [
    ("education_features.csv", "Education capacity features"),
    ("population_features.csv", "Population features"),
    ("household_features.csv", "Household and living-quarter features"),
    ("economic_features.csv", "Economic as-of features"),
    ("fertility_features.csv", "Fertility features"),
    ("autoregressive_feature_panel.csv", "Completion-history features"),
]

PANEL_LEAKAGE_FILES = [
    ("supervised_modelling_panel.csv", "Final supervised modelling panel"),
    ("final_feature_registry.csv", "Final feature registry"),
    ("leakage_audit.csv", "Leakage audit"),
    ("panel_integrity_check.csv", "Panel integrity check"),
    ("forecast_candidate_panel.csv", "Forecast candidate rows"),
]

VALIDATION_FILES = [
    ("split_integrity_check.csv", "Split integrity check"),
    ("chronological_validation_folds.csv", "Chronological validation folds"),
    ("train_panel.csv", "Training panel"),
    ("test_panel.csv", "Held-out test panel"),
    ("forecast_candidate_panel.csv", "Forecast candidate panel"),
    ("baseline_metrics.csv", "Core baseline metrics"),
    ("additional_rule_baseline_metrics.csv", "Rule baseline metrics"),
    ("all_baseline_metrics_pre_svr.csv", "All pre-SVR baselines"),
]

SVR_TRAINING_FILES = [
    ("svr_pipeline_readiness.csv", "SVR pipeline readiness"),
    ("feature_set_registry.csv", "Feature-set registry"),
    ("svr_candidate_registry.csv", "SVR candidate registry"),
    ("svr_validation_summary.csv", "SVR validation summary"),
    ("svr_tuning_results.csv", "SVR tuning results"),
    ("final_selected_svr_config.csv", "Selected SVR configuration"),
    ("ridge_benchmark_metrics.csv", "Ridge benchmark metrics"),
]

SVR_EVALUATION_FILES = [
    ("final_svr_metrics.csv", "Final SVR held-out metrics"),
    ("test_predictions.csv", "Held-out test predictions"),
    ("expanded_model_comparison_metrics.csv", "Expanded model comparison"),
    ("expanded_baseline_vs_svr_delta.csv", "Improvement over baselines"),
]

SVR_DIAGNOSTIC_FILES = [
    ("residual_summary.csv", "Residual summary"),
    ("svr_tolerance_summary.csv", "Tolerance coverage"),
    ("worst_prediction_rows.csv", "Worst prediction rows"),
    ("error_by_state.csv", "Error by state"),
    ("error_by_stage.csv", "Error by stage"),
    ("error_by_sex.csv", "Error by sex"),
    ("error_by_state_stage_sex.csv", "Detailed group error"),
]

SVR_DEMONSTRATOR_FILES = [
    ("final_ai_demonstrator.csv", "Representative held-out demonstration row"),
    ("forecast_demonstrator_preview.csv", "Forecast demonstrator preview"),
    ("forecast_candidate_predictions.csv", "Forecast candidate predictions"),
]

RF_REQUIRED_FILES = [
    "rf_final_metrics.csv",
    "rf_test_predictions.csv",
    "rf_baseline_comparison.csv",
    "rf_error_by_state.csv",
    "rf_error_by_stage.csv",
    "rf_error_by_sex.csv",
    "rf_feature_importance.csv",
]
