from __future__ import annotations

import pandas as pd
from .data_loader import load_comparison_table, load_comparison_check, load_comparison_artifact_json, load_comparison_artifact_csv
from .formatting import fmt_pp, fmt_r2, fmt_pct


def _empty() -> pd.DataFrame:
    return pd.DataFrame()


def _pass_mask(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty:
        return pd.Series(dtype=bool)
    if "status_label" in df.columns:
        return df["status_label"].astype(str).str.strip().str.lower().isin({"pass", "passed", "true", "yes"})
    if "status" in df.columns:
        status = df["status"]
        if status.dtype == bool:
            return status.fillna(False)
        return status.astype(str).str.strip().str.lower().isin({"pass", "passed", "true", "yes"})
    return pd.Series([False] * len(df), index=df.index)


def _model_row(df: pd.DataFrame, key: str) -> pd.Series | None:
    if df is None or df.empty:
        return None
    if "model_key" in df.columns:
        hit = df[df["model_key"].astype(str).str.lower().eq(key.lower())]
        if not hit.empty:
            return hit.iloc[0]
    if "model_name" in df.columns:
        if key.lower() == "svr":
            hit = df[df["model_name"].astype(str).str.lower().str.contains("support vector", na=False)]
        else:
            hit = df[df["model_name"].astype(str).str.lower().str.contains("randomforest|random forest", na=False, regex=True)]
        if not hit.empty:
            return hit.iloc[0]
    return None


def _winner_count(wins: pd.DataFrame, key: str) -> int | None:
    if wins is None or wins.empty or "winner_by_row" not in wins.columns:
        return None
    hit = wins[wins["winner_by_row"].astype(str).str.lower().eq(key.lower())]
    if hit.empty:
        return None
    return int(hit.iloc[0].get("row_count", 0))



def load_comparison_validity_summary() -> pd.DataFrame:
    return load_comparison_check("comparison_validity_summary.csv")


def load_supervised_model_leaderboard() -> pd.DataFrame:
    return load_comparison_table("supervised_model_leaderboard.csv")


def load_combined_final_metrics() -> pd.DataFrame:
    return load_comparison_table("combined_final_metrics.csv")


def load_final_model_selection() -> pd.DataFrame:
    return load_comparison_table("final_model_selection.csv")


def load_final_selection_artifact() -> dict:
    return load_comparison_artifact_json("final_supervised_model_selection.json")


def load_row_level_prediction_comparison() -> pd.DataFrame:
    return load_comparison_table("row_level_prediction_comparison.csv")


def load_row_level_winner_summary() -> pd.DataFrame:
    return load_comparison_table("row_level_winner_summary.csv")


def load_largest_disagreements() -> pd.DataFrame:
    return load_comparison_table("largest_model_disagreement_rows.csv")


def load_tolerance_comparison() -> pd.DataFrame:
    return load_comparison_table("tolerance_comparison.csv")


def load_residual_bias_comparison() -> pd.DataFrame:
    return load_comparison_table("residual_bias_comparison.csv")


def load_grouped_error_comparison(group: str) -> pd.DataFrame:
    return load_comparison_table(f"error_comparison_by_{group}.csv")


def load_feature_influence_comparison() -> pd.DataFrame:
    return load_comparison_table("feature_influence_comparison.csv")


def load_top_feature_influence_comparison() -> pd.DataFrame:
    return load_comparison_table("top_feature_influence_comparison.csv")


def load_ai_demonstrator_comparison() -> pd.DataFrame:
    return load_comparison_table("combined_ai_demonstrator.csv")


def load_forecast_preview_comparison() -> pd.DataFrame:
    return load_comparison_table("forecast_preview_model_comparison.csv")


def load_comparison_output_check() -> pd.DataFrame:
    return load_comparison_check("comparison_output_check.csv")


def load_missing_comparison_outputs() -> pd.DataFrame:
    return load_comparison_check("missing_comparison_outputs.csv")


def load_comparison_manifest() -> pd.DataFrame:
    return load_comparison_artifact_csv("comparison_output_manifest.csv")



def build_comparison_metric_cards() -> dict[str, str]:
    leader = load_supervised_model_leaderboard()
    if leader.empty:
        return {}
    best = leader.sort_values(["mae", "rmse"], ascending=[True, True]).iloc[0]
    return {
        "Selected model": str(best.get("model_name", "N/A")),
        "Best MAE": fmt_pp(best.get("mae")),
        "Best RMSE": fmt_pp(best.get("rmse")),
        "Best R²": fmt_r2(best.get("r2")),
    }


def build_comparison_overview_cards() -> dict[str, str]:
    validity = load_comparison_validity_summary()
    wins = load_row_level_winner_summary()
    leader = load_supervised_model_leaderboard()
    rows = load_row_level_prediction_comparison()
    pass_mask = _pass_mask(validity)
    total_count = len(validity) if validity is not None else 0
    pass_count = int(pass_mask.sum()) if total_count else 0
    selected = "N/A"
    if not leader.empty:
        selected = str(leader.sort_values(["mae", "rmse"], ascending=[True, True]).iloc[0].get("model_name", "N/A"))
    svr_wins = _winner_count(wins, "svr")
    rf_wins = _winner_count(wins, "rf")
    return {
        "Selected model": selected,
        "Compared rows": str(len(rows)) if not rows.empty else "N/A",
        "Validity checks": f"{pass_count}/{total_count} pass" if total_count else "N/A",
        "SVR row wins": str(svr_wins) if svr_wins is not None else "N/A",
        "RF row wins": str(rf_wins) if rf_wins is not None else "N/A",
    }


def build_comparison_decision_cards() -> dict[str, str]:
    leader = load_supervised_model_leaderboard()
    wins = load_row_level_winner_summary()
    if leader.empty:
        return {}
    svr = _model_row(leader, "svr")
    rf = _model_row(leader, "rf")
    selected = leader.sort_values(["mae", "rmse"], ascending=[True, True]).iloc[0]
    cards = {"Selected model": str(selected.get("model_name", "N/A"))}
    if svr is not None:
        cards["SVR MAE"] = fmt_pp(svr.get("mae"))
    if rf is not None:
        cards["RF MAE"] = fmt_pp(rf.get("mae"))
    svr_wins = _winner_count(wins, "svr")
    rf_wins = _winner_count(wins, "rf")
    if svr_wins is not None:
        cards["SVR row wins"] = str(svr_wins)
    if rf_wins is not None:
        cards["RF row wins"] = str(rf_wins)
    return cards



def build_comparison_metric_decision_table() -> pd.DataFrame:
    leader = load_supervised_model_leaderboard()
    if leader.empty:
        return pd.DataFrame()
    metrics = [
        ("MAE", "mae", "Lower is better", True),
        ("RMSE", "rmse", "Lower is better", True),
        ("R²", "r2", "Higher is better", False),
        ("Median AE", "median_absolute_error", "Lower is better", True),
    ]
    svr = _model_row(leader, "svr")
    rf = _model_row(leader, "rf")
    if svr is None or rf is None:
        return pd.DataFrame()
    rows = []
    for label, col, direction, lower_is_better in metrics:
        svr_val = float(svr.get(col))
        rf_val = float(rf.get(col))
        if lower_is_better:
            better = "SVR" if svr_val < rf_val else "RF" if rf_val < svr_val else "Tie"
        else:
            better = "SVR" if svr_val > rf_val else "RF" if rf_val > svr_val else "Tie"
        rows.append({
            "metric": label,
            "svr": svr_val,
            "random_forest": rf_val,
            "better_direction": direction,
            "better_model": better,
        })
    return pd.DataFrame(rows)


def format_metric_decision_table(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    for col in ["svr", "random_forest"]:
        out[col] = out.apply(
            lambda r: fmt_r2(r[col]) if str(r.get("metric", "")) in {"R²", "R2"} else fmt_pp(r[col]),
            axis=1,
        )
    out = out.rename(columns={
        "metric": "Metric",
        "svr": "Support Vector Regression",
        "random_forest": "RandomForestRegressor",
        "better_direction": "Better direction",
        "better_model": "Better model",
    })
    return out


def build_comparison_error_summary_cards() -> dict[str, str]:
    tol = load_tolerance_comparison()
    resid = load_residual_bias_comparison()
    cards: dict[str, str] = {}
    svr_tol = _model_row(tol, "svr")
    rf_tol = _model_row(tol, "rf")
    svr_resid = _model_row(resid, "svr")
    rf_resid = _model_row(resid, "rf")
    if svr_tol is not None:
        cards["SVR within ±2 pp"] = fmt_pct(svr_tol.get("within_2pp_percentage"))
        cards["SVR within ±5 pp"] = fmt_pct(svr_tol.get("within_5pp_percentage"))
    if rf_tol is not None:
        cards["RF within ±2 pp"] = fmt_pct(rf_tol.get("within_2pp_percentage"))
        cards["RF within ±5 pp"] = fmt_pct(rf_tol.get("within_5pp_percentage"))
    if svr_resid is not None:
        cards["SVR mean residual"] = fmt_pp(svr_resid.get("mean_residual"))
    if rf_resid is not None:
        cards["RF mean residual"] = fmt_pp(rf_resid.get("mean_residual"))
    return cards


def build_grouped_comparison_summary() -> pd.DataFrame:
    rows = []
    for group in ["stage", "sex", "state"]:
        df = load_grouped_error_comparison(group)
        if df.empty or group not in df.columns:
            continue
        work = df.copy()
        work["model_key"] = work["model_key"].astype(str).str.strip().str.lower()
        work["group_value"] = work[group].astype(str).str.strip().str.lower()
        pivot = work.pivot_table(index="group_value", columns="model_key", values="mae", aggfunc="first").reset_index()
        if {"svr", "rf"}.issubset(set(pivot.columns)):
            pivot["better_model"] = pivot.apply(lambda r: "SVR" if r["svr"] <= r["rf"] else "RF", axis=1)
            svr_count = int((pivot["better_model"] == "SVR").sum())
            rf_count = int((pivot["better_model"] == "RF").sum())
            total = int(len(pivot))
            rows.append({
                "group": group,
                "items_compared": total,
                "svr_better_count": svr_count,
                "rf_better_count": rf_count,
                "summary": f"SVR lower MAE in {svr_count} of {total} {group} groups",
            })
    return pd.DataFrame(rows)


def build_ai_demo_cards() -> dict[str, str]:
    ai = load_ai_demonstrator_comparison()
    if ai.empty:
        return {}
    r = ai.iloc[0]
    return {
        "State": str(r.get("state", "N/A")),
        "Stage": str(r.get("stage", "N/A")),
        "Sex": str(r.get("sex", "N/A")),
        "Actual": f"{float(r.get('actual_next_year_completion_rate')):.2f}%",
        "SVR prediction": f"{float(r.get('svr_prediction')):.2f}%",
        "RF prediction": f"{float(r.get('rf_prediction')):.2f}%",
        "Winner": str(r.get("winner_for_row", r.get("winner_by_row", "N/A"))).upper(),
    }


def build_tolerance_cards() -> dict[str, str]:
    tol = load_tolerance_comparison()
    if tol.empty:
        return {}
    out = {}
    for _, row in tol.iterrows():
        model = str(row.get("model_key", row.get("model_name", "model"))).upper()
        short = "SVR" if "SVR" in model else "RF"
        out[f"{short} within ±2 pp"] = fmt_pct(row.get("within_2pp_percentage"))
        out[f"{short} within ±5 pp"] = fmt_pct(row.get("within_5pp_percentage"))
    return out


def build_forecast_cards() -> dict[str, str]:
    df = load_forecast_preview_comparison()
    if df.empty:
        return {}
    return {
        "Forecast rows": str(len(df)),
        "SVR mean preview": fmt_pp(df["svr_forecast_prediction"].mean()),
        "RF mean preview": fmt_pp(df["rf_forecast_prediction"].mean()),
        "Mean model difference": fmt_pp(df["absolute_forecast_prediction_difference"].mean()),
    }


def build_output_status_cards() -> dict[str, str]:
    missing = load_missing_comparison_outputs()
    manifest = load_comparison_manifest()
    validity = load_comparison_validity_summary()
    artifact = load_final_selection_artifact()
    pass_count = int(_pass_mask(validity).sum()) if validity is not None and not validity.empty else 0
    return {
        "Missing outputs": str(len(missing)) if missing is not None else "N/A",
        "Validity checks passed": str(pass_count),
        "Manifest rows": str(len(manifest)) if manifest is not None else "N/A",
        "Selection artifact": "Present" if artifact else "Missing",
    }
