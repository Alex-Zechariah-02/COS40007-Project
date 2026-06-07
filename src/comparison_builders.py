from __future__ import annotations
import pandas as pd
from .data_loader import load_table, load_rf_table
from .formatting import fmt_pp, fmt_r2, fmt_pct


def _norm_key(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ["state", "stage", "sex"]:
        if col in out.columns:
            out[col+"_key"] = out[col].astype(str).str.strip().str.lower()
    for col in ["Input Year", "Target Year"]:
        if col in out.columns:
            out[col+"_key"] = out[col].astype(int)
    return out


def load_model_metric_comparison() -> pd.DataFrame:
    svr = load_table("final_svr_metrics.csv")
    rf = load_rf_table("final_rf_metrics.csv")
    rows = []
    if not svr.empty:
        r = svr.iloc[0]
        rows.append({"Model": "Support Vector Regression", "Branch": "SVR", "MAE": r.get("MAE"), "RMSE": r.get("RMSE"), "R²": r.get("R2"), "Median AE": r.get("Median_AE")})
    if not rf.empty:
        r = rf.iloc[0]
        rows.append({"Model": "RandomForestRegressor", "Branch": "Random Forest", "MAE": r.get("MAE"), "RMSE": r.get("RMSE"), "R²": r.get("R2"), "Median AE": r.get("Median_AE")})
    df = pd.DataFrame(rows)
    if not df.empty:
        df["MAE Rank"] = df["MAE"].rank(method="min", ascending=True).astype(int)
        df["RMSE Rank"] = df["RMSE"].rank(method="min", ascending=True).astype(int)
        df["R² Rank"] = df["R²"].rank(method="min", ascending=False).astype(int)
        df["Median AE Rank"] = df["Median AE"].rank(method="min", ascending=True).astype(int)
    return df


def comparison_metric_cards() -> dict[str, str]:
    df = load_model_metric_comparison()
    if df.empty: return {}
    best = df.sort_values(["MAE", "RMSE"], ascending=[True, True]).iloc[0]
    return {
        "Best by MAE": str(best["Model"]),
        "Best MAE": fmt_pp(best["MAE"]),
        "Best RMSE": fmt_pp(best["RMSE"]),
        "Best R²": fmt_r2(df.sort_values("R²", ascending=False).iloc[0]["R²"]),
    }


def build_prediction_comparison() -> pd.DataFrame:
    svr = load_table("test_predictions.csv")
    rf = load_rf_table("test_predictions.csv")
    if svr.empty or rf.empty:
        return pd.DataFrame()
    s = _norm_key(svr)
    r = _norm_key(rf)
    keys = ["state_key", "stage_key", "sex_key", "Input Year_key", "Target Year_key"]
    s_cols = keys + ["state", "stage", "sex", "Input Year", "Target Year", "Actual Next-Year Completion Rate", "Predicted Next-Year Completion Rate", "Absolute Error", "Residual"]
    r_cols = keys + ["Predicted Next-Year Completion Rate", "Absolute Error", "Residual"]
    merged = s[s_cols].merge(r[r_cols], on=keys, suffixes=("_SVR", "_RF"), how="inner")
    merged = merged.rename(columns={
        "Predicted Next-Year Completion Rate_SVR": "SVR Prediction",
        "Predicted Next-Year Completion Rate_RF": "RF Prediction",
        "Absolute Error_SVR": "SVR Absolute Error",
        "Absolute Error_RF": "RF Absolute Error",
        "Residual_SVR": "SVR Residual",
        "Residual_RF": "RF Residual",
        "Actual Next-Year Completion Rate": "Actual Next-Year Completion Rate",
    })
    merged["Winner by row"] = merged.apply(lambda x: "SVR" if x["SVR Absolute Error"] < x["RF Absolute Error"] else ("RF" if x["RF Absolute Error"] < x["SVR Absolute Error"] else "Tie"), axis=1)
    merged["Absolute Error Difference (RF - SVR)"] = merged["RF Absolute Error"] - merged["SVR Absolute Error"]
    return merged


def row_winner_summary() -> pd.DataFrame:
    df = build_prediction_comparison()
    if df.empty: return pd.DataFrame()
    return df["Winner by row"].value_counts().rename_axis("Winner").reset_index(name="Row Count")


def alignment_check() -> pd.DataFrame:
    svr = load_table("test_predictions.csv")
    rf = load_rf_table("test_predictions.csv")
    rows=[]
    rows.append({"Check": "SVR prediction rows", "Status": len(svr)})
    rows.append({"Check": "RF prediction rows", "Status": len(rf)})
    comp = build_prediction_comparison()
    rows.append({"Check": "Matched rows", "Status": len(comp)})
    same_actual = "N/A"
    if not comp.empty:
        # RF actual is not retained in merged because SVR actual kept; compare separately
        same_actual = "Pass" if len(comp)==min(len(svr),len(rf)) else "Review"
    rows.append({"Check": "Comparable held-out rows", "Status": same_actual})
    return pd.DataFrame(rows).astype(str)


def tolerance_comparison() -> pd.DataFrame:
    svr = load_table("svr_tolerance_summary.csv")
    rf = load_rf_table("rf_tolerance_summary.csv")
    rows=[]
    if not svr.empty:
        for _,r in svr.iterrows():
            rows.append({"Model":"SVR", "Tolerance Band":r.get("Tolerance Band"), "Percentage":r.get("Percentage")})
    if not rf.empty:
        rr=rf.iloc[0]
        for band,col in [("Within ±1pp","Within 1pp"),("Within ±2pp","Within 2pp"),("Within ±5pp","Within 5pp")]:
            rows.append({"Model":"RandomForestRegressor", "Tolerance Band":band, "Percentage":rr.get(col)})
    return pd.DataFrame(rows)


def grouped_error_comparison(group: str) -> pd.DataFrame:
    fname=f"error_by_{group}.csv"
    svr=load_table(fname)
    rf=load_rf_table(fname)
    if svr.empty or rf.empty:
        return pd.DataFrame()
    key=group
    left=svr[[key,"MAE","RMSE"]].copy().rename(columns={"MAE":"SVR MAE","RMSE":"SVR RMSE"})
    right=rf[[key,"MAE","RMSE"]].copy().rename(columns={"MAE":"RF MAE","RMSE":"RF RMSE"})
    left[key+"_key"]=left[key].astype(str).str.lower()
    right[key+"_key"]=right[key].astype(str).str.lower()
    out=left.merge(right, on=key+"_key", suffixes=("", "_rf"))
    if key+"_rf" in out.columns:
        out.drop(columns=[key+"_rf"], inplace=True)
    out["MAE Winner"] = out.apply(lambda x: "SVR" if x["SVR MAE"] < x["RF MAE"] else ("RF" if x["RF MAE"] < x["SVR MAE"] else "Tie"), axis=1)
    out["MAE Difference (RF - SVR)"] = out["RF MAE"] - out["SVR MAE"]
    return out.drop(columns=[key+"_key"])


def feature_group_comparison() -> pd.DataFrame:
    svr=load_table("feature_group_importance_summary.csv")
    rf=load_rf_table("feature_group_importance_summary.csv")
    rows=[]
    if not svr.empty:
        d=svr.copy(); d["Model"]="SVR"; rows.append(d)
    if not rf.empty:
        d=rf.copy(); d["Model"]="RandomForestRegressor"; rows.append(d)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
