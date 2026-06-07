from __future__ import annotations
import pandas as pd
from .data_loader import load_table, load_check, load_artifact_json, model_path
from .formatting import fmt_pp, fmt_r2, fmt_pct
from .config import ARTIFACTS_DIR


def _first(df: pd.DataFrame) -> pd.Series | None:
    return None if df is None or df.empty else df.iloc[0]


def safe_get(row, col, default="N/A"):
    try:
        val = row.get(col, default)
        if pd.isna(val): return default
        return val
    except Exception:
        return default


def build_svr_metric_summary() -> dict[str, str]:
    df = load_table("final_svr_metrics.csv")
    r = _first(df)
    if r is None: return {}
    return {
        "MAE": fmt_pp(safe_get(r, "MAE")),
        "RMSE": fmt_pp(safe_get(r, "RMSE")),
        "R²": fmt_r2(safe_get(r, "R2")),
        "Median AE": fmt_pp(safe_get(r, "Median_AE")),
    }


def build_svr_config_summary() -> pd.DataFrame:
    cfg = load_table("final_selected_svr_config.csv")
    r = _first(cfg)
    if r is None: return pd.DataFrame()
    rows = [
        ("Model", "Support Vector Regression"),
        ("Kernel", safe_get(r, "Kernel", "rbf")),
        ("Scaler", safe_get(r, "Scaler", "standard")),
        ("Selected feature set", safe_get(r, "Selected Feature Set")),
        ("Selected candidate", safe_get(r, "Selected Candidate Name", safe_get(r, "Candidate Name"))),
        ("C", safe_get(r, "C")),
        ("epsilon", safe_get(r, "epsilon")),
        ("gamma", safe_get(r, "gamma")),
        ("Calibration method", safe_get(r, "Calibration Method")),
        ("Calibration intercept", safe_get(r, "Calibration Intercept")),
        ("Validation MAE", safe_get(r, "Validation MAE")),
        ("Fold count", safe_get(r, "Fold Count")),
        ("Selection source", safe_get(r, "Selection Source")),
    ]
    return pd.DataFrame(rows, columns=["Item", "Value"]).astype(str)


def build_svr_diagnostic_summary() -> dict[str, str]:
    cards = load_table("svr_metric_card_summary.csv")
    residual = load_table("residual_summary.csv")
    c = _first(cards)
    r = _first(residual)
    out = {}
    if c is not None:
        out.update({
            "Mean residual": fmt_pp(safe_get(c, "Mean Residual")),
            "Underprediction": fmt_pct(safe_get(c, "Underprediction Percentage")),
            "Within ±2 pp": fmt_pct(safe_get(c, "Within 2pp Percentage")),
            "Within ±5 pp": fmt_pct(safe_get(c, "Within 5pp Percentage")),
            "P90 AE": fmt_pp(safe_get(c, "P90 Absolute Error")),
            "Max AE": fmt_pp(safe_get(c, "Max Absolute Error")),
        })
    bias = safe_get(r, "Bias Direction", "N/A") if r is not None else "N/A"
    if bias == "N/A" and c is not None:
        try:
            under = float(safe_get(c, "Underprediction Percentage", 0))
            over = float(safe_get(c, "Overprediction Percentage", 0))
            bias = "Underprediction" if under >= over else "Overprediction"
        except Exception:
            bias = "N/A"
    bias = str(bias).replace(" bias", "").strip().title() if bias != "N/A" else "N/A"
    out["Bias"] = bias
    return out


def build_baseline_summary() -> pd.DataFrame:
    df = load_table("baseline_vs_svr_summary.csv")
    if df.empty: return pd.DataFrame()
    r = df.iloc[0]
    rows = [
        {"Question": "Does SVR beat training mean on MAE/RMSE?", "Result": safe_get(r, "Beats Training Mean on MAE and RMSE")},
        {"Question": "Does SVR beat persistence on MAE/RMSE?", "Result": safe_get(r, "Beats Persistence on MAE and RMSE")},
        {"Question": "Is held-out R² positive?", "Result": safe_get(r, "Positive R2")},
        {"Question": "Result status", "Result": safe_get(r, "Result Status")},
        {"Question": "Result note", "Result": safe_get(r, "Result Note")},
    ]
    return pd.DataFrame(rows).astype(str)


def build_grouped_error_summary() -> pd.DataFrame:
    rows = []
    for label, fname, keycol in [
        ("Highest-error state", "error_by_state.csv", "state"),
        ("Highest-error stage", "error_by_stage.csv", "stage"),
        ("Highest-error sex", "error_by_sex.csv", "sex"),
    ]:
        df = load_table(fname)
        if not df.empty and "MAE" in df.columns:
            s = df.sort_values("MAE", ascending=False).iloc[0]
            rows.append({"Group": label, "Value": safe_get(s, keycol), "MAE": fmt_pp(safe_get(s, "MAE")), "RMSE": fmt_pp(safe_get(s, "RMSE"))})
    return pd.DataFrame(rows).astype(str)


def build_output_status_summary() -> pd.DataFrame:
    missing = load_check("missing_output_files.csv")
    check = load_check("final_output_check.csv")
    figures = load_table("visual_evidence_registry.csv")
    rows = [
        {"Evidence item": "Missing required output files", "Status": "0" if missing.empty else str(len(missing))},
        {"Evidence item": "Output checks", "Status": "Available" if not check.empty else "Missing"},
        {"Evidence item": "Registered figures", "Status": str(len(figures)) if not figures.empty else "Missing"},
        {"Evidence item": "SVR model artifact", "Status": "Present" if model_path("final_selected_svr_pipeline.joblib").exists() else "Missing"},
        {"Evidence item": "Best parameter JSON", "Status": "Present" if (ARTIFACTS_DIR/"best_svr_params.json").exists() else "Missing"},
    ]
    return pd.DataFrame(rows).astype(str)


def build_supervised_system_overview() -> pd.DataFrame:
    raw = load_check("raw_dataset_inventory.csv")
    panel = load_table("supervised_modelling_panel.csv")
    feat = load_table("final_feature_registry.csv")
    split = load_check("split_integrity_check.csv")
    target = load_table("main_supervised_target_panel.csv")
    rows = [
        {"Area": "Raw data", "Summary": f"{len(raw):,} raw datasets audited" if not raw.empty else "Raw audit table unavailable"},
        {"Area": "Target", "Summary": "Numeric next-year completion-rate target"},
        {"Area": "Row unit", "Summary": "state-stage-sex-year, male/female main rows"},
        {"Area": "Supervised panel", "Summary": f"{len(panel):,} panel rows" if not panel.empty else "Panel table unavailable"},
        {"Area": "Features", "Summary": f"{len(feat):,} registered features" if not feat.empty else "Feature registry unavailable"},
        {"Area": "Split", "Summary": "Chronological train/validation/test with input year 2021 held out" if not split.empty else "Split audit unavailable"},
        {"Area": "Baselines", "Summary": "Training-mean and persistence baselines used before model evaluation"},
    ]
    return pd.DataFrame(rows).astype(str)
