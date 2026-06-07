import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, discussion
from src import notebook_discussions as nd

page_header("5. Feature Engineering", "Education, demographic, household, economic, fertility, and completion-history features.")
purpose_box("This page shows how predictor variables were created while preserving the input-year to next-year prediction logic.")

tabs = st.tabs(["Education", "Population", "Household", "Economic", "Fertility", "Autoregressive", "Figures"])
with tabs[0]:
    show_dataframe(load_csv(TABLES_DIR / "education_features.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "district_education_aggregation_audit.csv"), height=260)
with tabs[1]:
    show_dataframe(load_csv(TABLES_DIR / "population_features.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "population_feature_audit.csv"), height=260)
with tabs[2]:
    show_dataframe(load_csv(TABLES_DIR / "household_features.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "household_feature_audit.csv"), height=260)
with tabs[3]:
    show_dataframe(load_csv(TABLES_DIR / "economic_features.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "economic_asof_merge_audit.csv"), height=260)
    st.warning("Economic features were prepared with as-of logic, but the selected final SVR feature set is `full_without_economic`.")
with tabs[4]:
    show_dataframe(load_csv(TABLES_DIR / "fertility_features.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "fertility_feature_audit.csv"), height=260)
with tabs[5]:
    show_dataframe(load_csv(TABLES_DIR / "autoregressive_feature_panel.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "autoregressive_feature_audit.csv"), height=260)
with tabs[6]:
    for name in ["students_per_teacher_by_stage.png", "students_per_school_by_stage.png", "education_capacity_correlation_heatmap.png", "school_age_population_share_by_state.png", "household_ratio_vs_completion_gap.png", "economic_data_age_by_year.png", "completion_lag_relationship_scatter.png", "rolling_gap_vs_target_scatter.png"]:
        show_image(SVR_FIGURES_DIR / name)

discussion("Notebook discussion", nd.FEATURE_ENGINEERING)
