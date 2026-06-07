from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
CHECKS_DIR = DATA_DIR / "checks"
TABLES_DIR = DATA_DIR / "tables"
ARTIFACTS_DIR = DATA_DIR / "artifacts"
RAW_DATA_DIR = DATA_DIR / "raw"
FIGURES_DIR = ROOT_DIR / "figures"
SVR_FIGURES_DIR = FIGURES_DIR / "svr"
RF_FIGURES_DIR = FIGURES_DIR / "random_forest"
RF_DATA_DIR = DATA_DIR / "random_forest"
RF_CHECKS_DIR = RF_DATA_DIR / "checks"
RF_TABLES_DIR = RF_DATA_DIR / "tables"
RF_ARTIFACTS_DIR = RF_DATA_DIR / "artifacts"
MODELS_DIR = ROOT_DIR / "models"
SVR_MODELS_DIR = MODELS_DIR / "svr"
RF_MODELS_DIR = MODELS_DIR / "random_forest"
DOCS_DIR = ROOT_DIR / "docs"

COMPARISON_DATA_DIR = DATA_DIR / "comparison"
COMPARISON_CHECKS_DIR = COMPARISON_DATA_DIR / "checks"
COMPARISON_TABLES_DIR = COMPARISON_DATA_DIR / "tables"
COMPARISON_ARTIFACTS_DIR = COMPARISON_DATA_DIR / "artifacts"
COMPARISON_FIGURES_DIR = FIGURES_DIR / "comparison"
COMPARISON_NOTEBOOK_NAME = "COS40007_SVR_RF_Comparison_Demonstrator"
SELECTED_SUPERVISED_MODEL = "Support Vector Regression"
COMPARISON_PRIMARY_METRIC = "MAE"


APP_TITLE = "COS40007 State Completion Rate Prediction"
TASK_LABEL = "State Completion Rate Prediction"
TARGET_NAME = "next_year_completion_rate"
ACTIVE_MODEL = "Support Vector Regression"
PENDING_MODEL = "None"
RF_MODEL_NAME = "RandomForestRegressor"
COMPARISON_STATUS = "Available"

MODEL_DISPLAY_NAMES = {
    "selected_svr": "Support Vector Regression",
    "svr": "Support Vector Regression",
    "training_mean_baseline": "Training Mean Baseline",
    "persistence_baseline": "Persistence Baseline",
    "random_forest": "RandomForestRegressor",
    "rf": "RandomForestRegressor",
}

METRIC_LABELS = {
    "MAE": "MAE",
    "RMSE": "RMSE",
    "R2": "R²",
    "Median_AE": "Median AE",
    "Median Absolute Error": "Median AE",
}

RAW_DATASET_FILES = [
    "completion_school_state.csv",
    "schools_district.csv",
    "enrolment_school_district.csv",
    "teachers_district.csv",
    "fertility_state.csv",
    "population_state.csv",
    "hh_lq_state.csv",
    "hh_income_state.csv",
    "hh_poverty_state.csv",
]
