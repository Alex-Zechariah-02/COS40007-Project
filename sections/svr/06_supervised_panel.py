import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image

page_header("6. Supervised Panel", "Merged modelling panel, feature registry, and leakage audit.")
purpose_box("This page verifies the final modelling table, feature list, and excluded leakage-prone fields before model training.")

tabs = st.tabs(["Panel", "Feature registry", "Feature sets", "Leakage audit", "Integrity", "Figures"])
with tabs[0]: show_dataframe(load_csv(TABLES_DIR / "supervised_modelling_panel.csv"), height=460)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "final_feature_registry.csv"), height=460)
with tabs[2]: show_dataframe(load_csv(TABLES_DIR / "feature_set_registry.csv"), height=460)
with tabs[3]: show_dataframe(load_csv(CHECKS_DIR / "leakage_audit.csv"), height=460)
with tabs[4]:
    show_dataframe(load_csv(CHECKS_DIR / "panel_integrity_check.csv"), height=320)
    show_dataframe(load_csv(TABLES_DIR / "supervised_rows.csv"), height=320)
with tabs[5]:
    show_image(SVR_FIGURES_DIR / "modelling_panel_row_flow.png")
    show_image(SVR_FIGURES_DIR / "feature_group_count_bar.png")
    show_image(SVR_FIGURES_DIR / "feature_set_size_comparison.png")
