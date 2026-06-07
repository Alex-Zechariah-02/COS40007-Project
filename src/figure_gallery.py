from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
from src.config import SVR_FIGURES_DIR
from src.data_loader import load_csv

def load_visual_registry(path: Path) -> pd.DataFrame:
    df = load_csv(path)
    if df.empty:
        return df
    if "Figure Filename" not in df.columns:
        return df
    df = df.copy()
    df["Local Path"] = df["Figure Filename"].apply(lambda x: str(SVR_FIGURES_DIR / str(x)))
    df["Local Exists"] = df["Local Path"].apply(lambda p: Path(p).exists())
    return df

def show_figure_gallery(registry: pd.DataFrame, max_figures: int = 12):
    if registry.empty:
        st.warning("Visual evidence registry is not available.")
        return
    categories = sorted(registry["Source Table"].dropna().astype(str).unique().tolist()) if "Source Table" in registry.columns else []
    selected = st.selectbox("Filter by source table", ["All"] + categories) if categories else "All"
    df = registry if selected == "All" else registry[registry["Source Table"].astype(str) == selected]
    st.caption(f"Showing {min(len(df), max_figures)} of {len(df)} registered figures.")
    for _, row in df.head(max_figures).iterrows():
        name = row.get("Figure Name", row.get("Figure Filename", "Figure"))
        filename = row.get("Figure Filename", "")
        purpose = row.get("Purpose", "")
        p = SVR_FIGURES_DIR / str(filename)
        st.subheader(str(name))
        if purpose:
            st.caption(str(purpose))
        if p.exists():
            st.image(str(p), width="stretch")
        else:
            st.warning(f"Missing local figure: `{filename}`")
