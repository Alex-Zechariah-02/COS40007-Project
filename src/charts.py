from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def metric_bar(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    if df.empty or x not in df or y not in df:
        return None
    return px.bar(df, x=x, y=y, color=color, title=title)

def line_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, title: str = ""):
    if df.empty or x not in df or y not in df:
        return None
    return px.line(df, x=x, y=y, color=color, markers=True, title=title)

def scatter_actual_pred(df: pd.DataFrame, actual_col: str, pred_col: str, color_col: str | None = None):
    if df.empty or actual_col not in df or pred_col not in df:
        return None
    fig = px.scatter(df, x=actual_col, y=pred_col, color=color_col, hover_data=df.columns, title="Actual versus Predicted")
    mn = min(df[actual_col].min(), df[pred_col].min())
    mx = max(df[actual_col].max(), df[pred_col].max())
    fig.add_trace(go.Scatter(x=[mn, mx], y=[mn, mx], mode="lines", name="Ideal", line=dict(dash="dash")))
    return fig

def histogram(df: pd.DataFrame, col: str, title: str):
    if df.empty or col not in df:
        return None
    return px.histogram(df, x=col, nbins=30, title=title)
