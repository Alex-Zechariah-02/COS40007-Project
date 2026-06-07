from __future__ import annotations
import pandas as pd
import streamlit as st
from .config import SVR_FIGURES_DIR
from .data_loader import load_table
from .figure_explanations import explain
from .ui_components import display_image


def infer_category(filename: str) -> str:
    f = filename.lower()
    if any(k in f for k in ["raw", "missing", "dataset"]): return "Raw data audit"
    if any(k in f for k in ["target", "completion_rate_trend", "gap", "row_unit"]): return "Target and trends"
    if any(k in f for k in ["feature", "population", "household", "education", "students", "economic"]): return "Feature engineering"
    if any(k in f for k in ["split", "baseline", "chronological"]): return "Validation and baselines"
    if any(k in f for k in ["svr", "ridge", "candidate"]): return "SVR training"
    if any(k in f for k in ["actual", "predicted", "residual", "error", "tolerance", "rmse", "mae", "r2", "model"]): return "Evaluation and diagnostics"
    if any(k in f for k in ["permutation", "importance"]): return "Feature influence"
    if any(k in f for k in ["representative", "forecast"]): return "AI demonstrator"
    return "Other visual evidence"


def render_explanation(filename: str):
    e = explain(filename)
    with st.expander("How to read this figure", expanded=False):
        st.dataframe(pd.DataFrame([
            {"Item": "Purpose", "Explanation": e["purpose"]},
            {"Item": "How to read", "Explanation": e["how"]},
            {"Item": "Better direction", "Explanation": e["better"]},
            {"Item": "Main takeaway", "Explanation": e["takeaway"]},
            {"Item": "Caveat", "Explanation": e["caveat"]},
        ]), width="stretch", hide_index=True)


def render_gallery():
    registry = load_table("visual_evidence_registry.csv")
    if registry.empty:
        st.info("Visual evidence registry is not available.")
        return
    registry = registry.copy()
    if "Figure Filename" not in registry.columns:
        st.dataframe(registry, width="stretch")
        return
    registry["App Category"] = registry["Figure Filename"].apply(infer_category)
    categories = ["All"] + sorted(registry["App Category"].dropna().unique().tolist())
    category = st.selectbox("Filter figure category", categories)
    view = registry if category == "All" else registry[registry["App Category"] == category]
    fig_names = view["Figure Filename"].tolist()
    if not fig_names:
        st.info("No figures for this category.")
        return
    selected = st.selectbox(
        "Select figure",
        fig_names,
        format_func=lambda x: registry.loc[registry["Figure Filename"] == x, "Figure Name"].iloc[0]
        if "Figure Name" in registry.columns and (registry["Figure Filename"] == x).any() else x,
    )
    row = registry[registry["Figure Filename"] == selected].iloc[0]
    st.markdown(f"#### {row.get('Figure Name', selected)}")
    if "Purpose" in row and pd.notna(row["Purpose"]):
        st.write(row["Purpose"])
    render_explanation(selected)
    display_image(SVR_FIGURES_DIR/selected)
    with st.expander("Show registry row for this figure"):
        st.dataframe(pd.DataFrame([row]), width="stretch", hide_index=True)
