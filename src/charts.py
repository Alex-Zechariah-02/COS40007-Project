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
