import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR
from src.figure_gallery import load_visual_registry, show_figure_gallery
from src.ui_components import page_header, purpose_box, show_dataframe
from src.data_loader import load_csv

page_header("11. Visual Evidence", "Registry-driven gallery of saved notebook figures.")
purpose_box("This page restores the notebook's visual evidence trail. It uses the saved visual evidence registry and local PNG files.")
registry = load_visual_registry(TABLES_DIR / "visual_evidence_registry.csv")
if not registry.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("Registered figures", len(registry))
    c2.metric("Local figures found", int(registry.get("Local Exists", False).sum()))
    c3.metric("Missing local figures", int((~registry.get("Local Exists", True)).sum()))
    show_dataframe(registry, "Visual evidence registry", height=280)
show_dataframe(load_csv(CHECKS_DIR / "visual_evidence_audit.csv"), "Visual evidence audit", height=260)
show_figure_gallery(registry, max_figures=20)
