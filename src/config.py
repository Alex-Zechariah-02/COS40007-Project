from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
CHECKS_DIR = DATA_DIR / "checks"
TABLES_DIR = DATA_DIR / "tables"
ARTIFACTS_DIR = DATA_DIR / "artifacts"
RF_DATA_DIR = DATA_DIR / "random_forest"
FIGURES_DIR = ROOT_DIR / "figures"
SVR_FIGURES_DIR = FIGURES_DIR / "svr"
RF_FIGURES_DIR = FIGURES_DIR / "random_forest"
MODELS_DIR = ROOT_DIR / "models"
SVR_MODELS_DIR = MODELS_DIR / "svr"
RF_MODELS_DIR = MODELS_DIR / "random_forest"
DOCS_DIR = ROOT_DIR / "docs"
NOTEBOOK_DIR = ROOT_DIR / "notebooks"

APP_TITLE = "COS40007 Smart Government SVR Notebook System"
TARGET_NAME = "next_year_completion_rate"
MODEL_NAME = "Support Vector Regression (SVR)"

METRIC_COLUMNS = ["MAE", "RMSE", "R2", "Median_AE", "Median Absolute Error"]

STAGE_LABELS = {
    "primary": "Primary",
    "secondary_lower": "Secondary Lower",
    "secondary_upper": "Secondary Upper",
}
SEX_LABELS = {"male": "Male", "female": "Female", "both": "Both"}

REQUIRED_CORE_FILES = {
    "Final SVR metrics": TABLES_DIR / "final_svr_metrics.csv",
    "Test predictions": TABLES_DIR / "test_predictions.csv",
    "Final output check": CHECKS_DIR / "final_output_check.csv",
    "Visual registry": TABLES_DIR / "visual_evidence_registry.csv",
    "Final model": SVR_MODELS_DIR / "final_selected_svr_pipeline.joblib",
    "Best params JSON": ARTIFACTS_DIR / "best_svr_params.json",
}
