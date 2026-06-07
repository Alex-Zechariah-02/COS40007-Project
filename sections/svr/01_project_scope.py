import streamlit as st
from src.config import TABLES_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, discussion
from src import notebook_discussions as nd

page_header("1. Project Scope", "SVR supervised-regression framing and Smart Government context.")
purpose_box("This section establishes that the notebook is a supervised regression branch for numeric State Completion Rate Prediction, using Support Vector Regression rather than classification or clustering.")

tabs = st.tabs(["Context", "Datasets", "Regression Framing", "Excluded Scope", "Role Diagram"])
with tabs[0]:
    show_dataframe(load_csv(TABLES_DIR / "project_context_summary.csv"), "Project context summary")
with tabs[1]:
    show_dataframe(load_csv(TABLES_DIR / "selected_public_sector_datasets.csv"), "Selected public-sector datasets")
    show_dataframe(load_csv(TABLES_DIR / "selected_dataset_context.csv"), "Dataset context and modelling roles")
with tabs[2]:
    show_dataframe(load_csv(TABLES_DIR / "supervised_regression_framing.csv"), "Regression framing")
with tabs[3]:
    show_dataframe(load_csv(TABLES_DIR / "excluded_scope.csv"), "Explicitly excluded scope")
with tabs[4]:
    show_image(SVR_FIGURES_DIR / "dataset_role_flow_diagram.png", "Dataset role flow diagram")

discussion("Notebook discussion", nd.PROJECT_SCOPE)
