import streamlit as st
from src.config import TABLES_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, caution_box

page_header("12. Permutation Importance", "Post-evaluation feature influence diagnostics.")
purpose_box("This page shows the trained SVR's feature influence diagnostics. It is not causal evidence and was not used for model selection.")
caution_box("Permutation importance is diagnostic: it estimates how held-out performance changes when a feature is shuffled. It does not prove policy causality.")

tabs = st.tabs(["Feature importance", "Grouped importance", "Figures"])
with tabs[0]: show_dataframe(load_csv(TABLES_DIR / "permutation_importance.csv"), height=460)
with tabs[1]:
    show_dataframe(load_csv(TABLES_DIR / "permutation_importance_with_groups.csv"), height=360)
    show_dataframe(load_csv(TABLES_DIR / "feature_group_importance_summary.csv"), height=300)
with tabs[2]:
    show_image(SVR_FIGURES_DIR / "permutation_importance.png")
    show_image(SVR_FIGURES_DIR / "permutation_importance_grouped_by_feature_source.png")
    show_image(SVR_FIGURES_DIR / "feature_group_importance_summary.png")
