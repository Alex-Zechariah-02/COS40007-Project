from pathlib import Path
import pandas as pd
from .config import TABLES_DIR, CHECKS_DIR, RAW_DATA_DIR, SVR_FIGURES_DIR, SVR_MODELS_DIR, ARTIFACTS_DIR, RF_MODELS_DIR, DATA_DIR
from .file_registry import RF_REQUIRED_FILES


def exists_df(items):
    rows = []
    for label, path in items:
        path = Path(path)
        rows.append({
            "Item": label,
            "Path": str(path),
            "Exists": path.exists(),
            "Size KB": round(path.stat().st_size/1024, 2) if path.exists() and path.is_file() else None,
        })
    return pd.DataFrame(rows)


def app_readiness():
    items = [
        ("Final SVR metrics", TABLES_DIR/"final_svr_metrics.csv"),
        ("Test predictions", TABLES_DIR/"test_predictions.csv"),
        ("Supervised panel", TABLES_DIR/"supervised_modelling_panel.csv"),
        ("Visual registry", TABLES_DIR/"visual_evidence_registry.csv"),
        ("Best parameters JSON", ARTIFACTS_DIR/"best_svr_params.json"),
        ("Saved SVR model", SVR_MODELS_DIR/"final_selected_svr_pipeline.joblib"),
    ]
    return exists_df(items)


def rf_pending_status():
    items = [(f, DATA_DIR/"random_forest"/f) for f in RF_REQUIRED_FILES]
    return exists_df(items)
