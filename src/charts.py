from __future__ import annotations
import pandas as pd
import plotly.express as px


def bar_metric(df: pd.DataFrame, x: str, y: str, title: str):
    if df.empty or x not in df.columns or y not in df.columns:
        return None
    return px.bar(df, x=x, y=y, title=title)


def actual_vs_predicted(df: pd.DataFrame, actual_col: str, pred_col: str):
    if df.empty or actual_col not in df.columns or pred_col not in df.columns:
        return None
    fig = px.scatter(df, x=actual_col, y=pred_col, hover_data=[c for c in ["state", "stage", "sex"] if c in df.columns], title="Actual vs predicted completion rate")
    return fig


def simple_line(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    if df.empty or x not in df.columns or y not in df.columns:
        return None
    return px.line(df, x=x, y=y, color=color, markers=True, title=title)



def _prepare_grouped_metric(df: pd.DataFrame, group_col: str, metric_col: str = "mae") -> pd.DataFrame:
    if df is None or df.empty or group_col not in df.columns or metric_col not in df.columns:
        return pd.DataFrame()
    keep = [group_col, "model_name", "model_key", metric_col, "row_count", "rmse", "median_absolute_error"]
    keep = [c for c in keep if c in df.columns]
    work = df[keep].copy()
    work[metric_col] = pd.to_numeric(work[metric_col], errors="coerce")
    work = work.dropna(subset=[metric_col])
    if "model_name" not in work.columns and "model_key" in work.columns:
        work["model_name"] = work["model_key"].map({"svr": "Support Vector Regression", "rf": "RandomForestRegressor"}).fillna(work["model_key"])
    return work


def grouped_model_mae_chart(df: pd.DataFrame, group_col: str, title: str, orientation: str = "h"):
    work = _prepare_grouped_metric(df, group_col, "mae")
    if work.empty:
        return None
    # Order groups by the larger MAE so the hardest groups appear clearly.
    order = work.groupby(group_col)["mae"].max().sort_values(ascending=True).index.tolist()
    if orientation == "h":
        fig = px.bar(
            work,
            y=group_col,
            x="mae",
            color="model_name",
            barmode="group",
            category_orders={group_col: order},
            title=title,
            labels={"mae": "MAE (percentage points)", group_col: group_col.replace("_", " ").title(), "model_name": "Model"},
            hover_data=[c for c in ["row_count", "rmse", "median_absolute_error"] if c in work.columns],
        )
        fig.update_layout(yaxis={"categoryorder": "array", "categoryarray": order})
    else:
        fig = px.bar(
            work,
            x=group_col,
            y="mae",
            color="model_name",
            barmode="group",
            category_orders={group_col: list(reversed(order))},
            title=title,
            labels={"mae": "MAE (percentage points)", group_col: group_col.replace("_", " ").title(), "model_name": "Model"},
            hover_data=[c for c in ["row_count", "rmse", "median_absolute_error"] if c in work.columns],
        )
    fig.update_layout(legend_title_text="Model", margin=dict(l=10, r=10, t=55, b=10))
    return fig


def mae_difference_chart(df: pd.DataFrame, group_col: str, title: str):
    work = _prepare_grouped_metric(df, group_col, "mae")
    if work.empty or not {"model_key", group_col, "mae"}.issubset(work.columns):
        return None
    pivot = work.pivot_table(index=group_col, columns="model_key", values="mae", aggfunc="first").reset_index()
    if not {"svr", "rf"}.issubset(pivot.columns):
        return None
    pivot["rf_minus_svr_mae"] = pivot["rf"] - pivot["svr"]
    pivot["better_model"] = pivot["rf_minus_svr_mae"].apply(lambda v: "SVR" if v > 0 else "RandomForestRegressor" if v < 0 else "Tie")
    pivot = pivot.sort_values("rf_minus_svr_mae", ascending=True)
    fig = px.bar(
        pivot,
        y=group_col,
        x="rf_minus_svr_mae",
        color="better_model",
        orientation="h",
        title=title,
        labels={"rf_minus_svr_mae": "RF MAE minus SVR MAE (percentage points)", group_col: group_col.replace("_", " ").title(), "better_model": "Lower MAE"},
        hover_data=["svr", "rf"],
    )
    fig.add_vline(x=0, line_width=1, line_dash="dash")
    fig.update_layout(legend_title_text="Lower MAE", margin=dict(l=10, r=10, t=55, b=10))
    return fig
