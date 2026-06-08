from __future__ import annotations
import pandas as pd
from .data_loader import load_rf_table, load_rf_check, load_rf_artifact_json, rf_model_path, RF_ARTIFACTS_DIR
from .config import RF_TABLES_DIR, RF_CHECKS_DIR, RF_FIGURES_DIR, RF_MODELS_DIR
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


def build_rf_baseline_summary() -> pd.DataFrame:
    summary = load_rf_table("rf_result_summary.csv")
    delta = load_rf_table("expanded_baseline_vs_rf_delta.csv")
    rows = []
    if not summary.empty:
        r = summary.iloc[0]
        rows.extend([
            {"Question": "Does RF beat all compared models on MAE?", "Result": safe_get(r, "RF Beats All Compared Models on MAE")},
            {"Question": "Does RF beat all compared models on RMSE?", "Result": safe_get(r, "RF Beats All Compared Models on RMSE")},
            {"Question": "Is held-out R² positive?", "Result": safe_get(r, "RF R2 Positive")},
        ])
    if not delta.empty and "Compared Model" in delta.columns:
        beats_mae = delta[delta.get("RF Beats Compared Model on MAE", False) == True]["Compared Model"].tolist() if "RF Beats Compared Model on MAE" in delta.columns else []
        not_beats_mae = delta[delta.get("RF Beats Compared Model on MAE", False) == False]["Compared Model"].tolist() if "RF Beats Compared Model on MAE" in delta.columns else []
        rows.append({"Question": "Baselines beaten by RF on MAE", "Result": ", ".join(beats_mae) if beats_mae else "None reported"})
        rows.append({"Question": "Stronger baselines not beaten by RF on MAE", "Result": ", ".join(not_beats_mae[:5]) if not_beats_mae else "None reported"})
    rows.append({"Question": "Result note", "Result": "RF is a valid second supervised-regression branch, but current held-out results do not support selecting RF as the best model."})
    return pd.DataFrame(rows).astype(str)


def build_rf_artifact_status() -> pd.DataFrame:
    rows = [
        {"Artifact": "RF model artifact", "Status": "Present" if rf_model_path("final_selected_rf_pipeline.joblib").exists() else "Missing"},
        {"Artifact": "Best RF parameter JSON", "Status": "Present" if (RF_ARTIFACTS_DIR/"best_rf_params.json").exists() else "Missing"},
        {"Artifact": "RF pipeline artifact", "Status": "Present" if (RF_ARTIFACTS_DIR/"final_selected_rf_pipeline.joblib").exists() else "Missing"},
    ]
    return pd.DataFrame(rows).astype(str)


def _pass_status(condition: bool) -> str:
    return "Pass" if bool(condition) else "Missing"


def _bool_from_exists(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes", "present", "pass"])


def build_rf_normalized_output_check() -> pd.DataFrame:
    audit = load_rf_check("output_file_audit.csv")
    manifest = load_rf_table("final_output_manifest.csv")
    visual = load_rf_table("visual_evidence_registry.csv")

    audited_exists = None
    if not audit.empty and "Exists" in audit.columns:
        audited_exists = _bool_from_exists(audit["Exists"])

    missing_count = int((~audited_exists).sum()) if audited_exists is not None else 0
    registered_count = int(len(visual)) if not visual.empty else 0
    registered_exists = None
    if not visual.empty and "File Exists" in visual.columns:
        registered_exists = _bool_from_exists(visual["File Exists"])
    registered_available = int(registered_exists.sum()) if registered_exists is not None else registered_count
    saved_png_count = len(list(RF_FIGURES_DIR.glob("*.png"))) if RF_FIGURES_DIR.exists() else 0
    model_exists = rf_model_path("final_selected_rf_pipeline.joblib").exists()
    params_exists = (RF_ARTIFACTS_DIR / "best_rf_params.json").exists()
    pipeline_artifact_exists = (RF_ARTIFACTS_DIR / "final_selected_rf_pipeline.joblib").exists()

    checks = [
        ("Table output directory exists", RF_TABLES_DIR.exists()),
        ("Check output directory exists", RF_CHECKS_DIR.exists()),
        ("Figure output directory exists", RF_FIGURES_DIR.exists()),
        ("Model output directory exists", RF_MODELS_DIR.exists()),
        ("Artifact output directory exists", RF_ARTIFACTS_DIR.exists()),
        ("Missing required file count", missing_count == 0, missing_count),
        ("Registered figure count", registered_count > 0, registered_count),
        ("Saved PNG figure count", saved_png_count >= registered_available and saved_png_count > 0, saved_png_count),
        ("Saved RF model file exists", model_exists),
        ("Best-parameter JSON exists", params_exists),
        ("RF pipeline artifact exists", pipeline_artifact_exists),
    ]

    rows = []
    for item in checks:
        if len(item) == 2:
            label, ok = item
            value = bool(ok)
        else:
            label, ok, value = item
        rows.append({"Check": label, "Value": value, "Status": _pass_status(ok)})
    return pd.DataFrame(rows).astype(str)


def build_rf_output_completion_summary() -> pd.DataFrame:
    audit = load_rf_check("output_file_audit.csv")
    manifest = load_rf_table("final_output_manifest.csv")
    visual = load_rf_table("visual_evidence_registry.csv")
    normalized = build_rf_normalized_output_check()
    pass_count = int((normalized["Status"] == "Pass").sum()) if not normalized.empty else 0
    rows = [
        {"Item": "RF output audit rows", "Value": f"{len(audit):,}" if not audit.empty else "0"},
        {"Item": "RF output manifest rows", "Value": f"{len(manifest):,}" if not manifest.empty else "0"},
        {"Item": "Registered RF figures", "Value": f"{len(visual):,}" if not visual.empty else "0"},
        {"Item": "Normalized status checks passed", "Value": f"{pass_count}/{len(normalized)}" if not normalized.empty else "0/0"},
        {"Item": "Output-status source", "Value": "Derived from saved RF output files, manifest, visual registry, model artifact, and parameter artifact."},
    ]
    return pd.DataFrame(rows).astype(str)


def build_rf_output_check_summary() -> pd.DataFrame:
    return build_rf_output_completion_summary()


def build_rf_missing_output_summary() -> pd.DataFrame:
    audit = load_rf_check("output_file_audit.csv")
    if audit.empty or "Exists" not in audit.columns:
        return pd.DataFrame()
    missing = audit[audit["Exists"] == False].copy()
    return missing.astype(str)
