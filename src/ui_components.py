from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
from src.formatting import fmt_num

def page_header(title: str, subtitle: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()

def purpose_box(text: str):
    st.info(text)

def caution_box(text: str):
    st.warning(text)

def success_box(text: str):
    st.success(text)

def show_dataframe(df: pd.DataFrame, caption: str | None = None, height: int = 360):
    if caption:
        st.caption(caption)
    if df is None or df.empty:
        st.warning("No table found for this output.")
    else:
        st.dataframe(df, width="stretch", height=height)

def show_table_section(title: str, df: pd.DataFrame, caption: str | None = None, height: int = 360):
    st.subheader(title)
    show_dataframe(df, caption=caption, height=height)

def metric_row(items: list[tuple[str, object, str | None]]):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        col.metric(label, value if isinstance(value, str) else fmt_num(value), help=help_text)

def file_status_table(mapping: dict[str, Path]):
    rows = []
    for label, path in mapping.items():
        rows.append({"Item": label, "Path": str(path.relative_to(path.parents[1]) if len(path.parents)>1 else path), "Exists": path.exists()})
    st.dataframe(pd.DataFrame(rows), width="stretch")

def show_image(path: Path, caption: str | None = None, width: str | int = "stretch"):
    if path.exists():
        st.image(str(path), caption=caption, width=width)
    else:
        st.warning(f"Missing figure: `{path.name}`")

def discussion(title: str, text: str):
    with st.expander(title, expanded=False):
        st.markdown(text)
