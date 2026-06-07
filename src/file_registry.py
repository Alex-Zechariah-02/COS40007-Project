from src.config import CHECKS_DIR, TABLES_DIR, ARTIFACTS_DIR, SVR_FIGURES_DIR, SVR_MODELS_DIR

RAW_AUDIT = [
    CHECKS_DIR / "raw_file_availability.csv",
    CHECKS_DIR / "raw_dataset_inventory.csv",
    CHECKS_DIR / "raw_schema_audit.csv",
    CHECKS_DIR / "raw_coverage_audit.csv",
    CHECKS_DIR / "raw_data_quality_summary.csv",
    CHECKS_DIR / "missing_values_audit.csv",
    CHECKS_DIR / "duplicate_key_audit.csv",
]
TARGET = [
    TABLES_DIR / "completion_target_panel.csv",
    TABLES_DIR / "malaysia_benchmark.csv",
    TABLES_DIR / "main_target_panel.csv",
    TABLES_DIR / "both_only_target_panel.csv",
    TABLES_DIR / "main_supervised_target_panel.csv",
    CHECKS_DIR / "row_unit_validation.csv",
    TABLES_DIR / "target_distribution_review.csv",
]
FEATURES = [
    TABLES_DIR / "education_features.csv",
    TABLES_DIR / "population_features.csv",
    TABLES_DIR / "household_features.csv",
    TABLES_DIR / "economic_features.csv",
    TABLES_DIR / "fertility_features.csv",
    TABLES_DIR / "autoregressive_feature_panel.csv",
    TABLES_DIR / "final_feature_registry.csv",
    CHECKS_DIR / "leakage_audit.csv",
]
VALIDATION = [
    CHECKS_DIR / "split_integrity_check.csv",
    TABLES_DIR / "chronological_validation_folds.csv",
    TABLES_DIR / "baseline_metrics.csv",
    TABLES_DIR / "additional_rule_baseline_metrics.csv",
    TABLES_DIR / "all_baseline_metrics_pre_svr.csv",
]
TRAINING = [
    CHECKS_DIR / "svr_pipeline_readiness.csv",
    TABLES_DIR / "feature_set_registry.csv",
    TABLES_DIR / "svr_candidate_registry.csv",
    TABLES_DIR / "svr_validation_summary.csv",
    TABLES_DIR / "final_selected_svr_config.csv",
    ARTIFACTS_DIR / "best_svr_params.json",
]
EVALUATION = [
    TABLES_DIR / "test_predictions.csv",
    TABLES_DIR / "final_svr_metrics.csv",
    TABLES_DIR / "expanded_model_comparison_metrics.csv",
    TABLES_DIR / "expanded_baseline_vs_svr_delta.csv",
    TABLES_DIR / "residual_summary.csv",
]
