from __future__ import annotations
import pandas as pd
from .data_loader import load_rf_table, load_rf_check, load_rf_artifact_json, rf_model_path, RF_ARTIFACTS_DIR
from .formatting import fmt_pp, fmt_r2, fmt_pct


def _first(df: pd.DataFrame) -> pd.Series | None:
    return None if df is None or df.empty else df.iloc[0]


def safe_get(row, col, default="N/A"):
    try:
        val = row.get(col, default)
        if pd.isna(val): return default
        return val
    except Exception:
        return default


def build_rf_metric_summary() -> dict[str, str]:
    df = load_rf_table("final_rf_metrics.csv")
    r = _first(df)
    if r is None: return {}
    return {
        "MAE": fmt_pp(safe_get(r, "MAE")),
        "RMSE": fmt_pp(safe_get(r, "RMSE")),
        "R²": fmt_r2(safe_get(r, "R2")),
        "Median AE": fmt_pp(safe_get(r, "Median_AE")),
    }


def build_rf_config_summary() -> pd.DataFrame:
    cfg = load_rf_table("final_selected_rf_config.csv")
    r = _first(cfg)
    if r is None: return pd.DataFrame()
    rows = [
        ("Model", "RandomForestRegressor"),
        ("Selected feature set", safe_get(r, "Selected Feature Set")),
        ("Selected candidate", safe_get(r, "Selected Candidate")),
        ("n_estimators", safe_get(r, "n_estimators")),
        ("max_depth", "None" if safe_get(r, "max_depth") == "N/A" else safe_get(r, "max_depth")),
        ("min_samples_leaf", safe_get(r, "min_samples_leaf")),
        ("Validation MAE", safe_get(r, "Validation MAE")),
        ("Validation RMSE", safe_get(r, "Validation RMSE")),
        ("Validation R²", safe_get(r, "Validation R2")),
        ("Validation Median AE", safe_get(r, "Validation Median_AE")),
        ("Fold count", safe_get(r, "Fold Count")),
        ("Numeric feature count", safe_get(r, "Numeric Feature Count")),
        ("Categorical feature count", safe_get(r, "Categorical Feature Count")),
        ("Selection note", safe_get(r, "Selection Note")),
    ]
    return pd.DataFrame(rows, columns=["Item", "Value"]).astype(str)


def build_rf_diagnostic_summary() -> dict[str, str]:
    cards = load_rf_table("rf_metric_card_summary.csv")
    residual = load_rf_table("residual_summary.csv")
    c = _first(cards)
    r = _first(residual)
    out = {}
    if c is not None:
        out.update({
            "Test MAE": fmt_pp(safe_get(c, "Test MAE")),
            "Test RMSE": fmt_pp(safe_get(c, "Test RMSE")),
            "Underprediction": fmt_pct(safe_get(r, "Underprediction Percentage")) if r is not None else "N/A",
            "Within ±2 pp": fmt_pct(safe_get(c, "Within 2pp %")),
            "Within ±5 pp": fmt_pct(safe_get(c, "Within 5pp %")),
        })
    if r is not None:
        out.update({
            "Mean residual": fmt_pp(safe_get(r, "Mean Residual")),
            "Bias": str(safe_get(r, "Bias Direction", "N/A")).replace(" bias", "").strip().title(),
            "P90 AE": "N/A",
            "Max AE": fmt_pp(safe_get(r, "Maximum Residual")),
        })
    return out


def build_rf_grouped_error_summary() -> pd.DataFrame:
    rows = []
    for label, fname, keycol in [
        ("Highest-error state", "error_by_state.csv", "state"),
        ("Highest-error stage", "error_by_stage.csv", "stage"),
        ("Highest-error sex", "error_by_sex.csv", "sex"),
    ]:
        df = load_rf_table(fname)
        if not df.empty and "MAE" in df.columns:
            s = df.sort_values("MAE", ascending=False).iloc[0]
            rows.append({"Group": label, "Value": safe_get(s, keycol), "MAE": fmt_pp(safe_get(s, "MAE")), "RMSE": fmt_pp(safe_get(s, "RMSE"))})
    return pd.DataFrame(rows).astype(str)


def build_rf_output_status_summary() -> pd.DataFrame:
    manifest = load_rf_table("final_output_manifest.csv")
    visual = load_rf_table("visual_evidence_registry.csv")
    checks = load_rf_check("output_file_audit.csv")
    rows = [
        {"Evidence item": "RF output manifest", "Status": f"{len(manifest):,} rows" if not manifest.empty else "Missing"},
        {"Evidence item": "RF visual registry", "Status": f"{len(visual):,} figures" if not visual.empty else "Missing"},
        {"Evidence item": "RF output audit", "Status": "Available" if not checks.empty else "Missing"},
        {"Evidence item": "RF model artifact", "Status": "Present" if rf_model_path("final_selected_rf_pipeline.joblib").exists() else "Missing"},
        {"Evidence item": "RF best parameter JSON", "Status": "Present" if (RF_ARTIFACTS_DIR/"best_rf_params.json").exists() else "Missing"},
    ]
    return pd.DataFrame(rows).astype(str)


def build_rf_validation_issue_summary() -> pd.DataFrame:
    df = load_rf_table("rf_validation_results.csv")
    if df.empty or "Fit Status" not in df.columns:
        return pd.DataFrame()
    counts = df["Fit Status"].value_counts(dropna=False).rename_axis("Fit status").reset_index(name="Rows")
    return counts.astype(str)
