import streamlit as st
from src.config import TABLES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe

page_header("Supervised Comparison Pending", "SVR is complete; RandomForestRegressor comparison activates later.")
purpose_box("For now, this page shows the available SVR versus baseline evidence. SVR-vs-RF comparison will be enabled when RF outputs are added.")
show_dataframe(load_csv(TABLES_DIR / "expanded_model_comparison_metrics.csv"), "Current available comparison: SVR, baselines, and Ridge benchmark", height=420)
show_dataframe(load_csv(TABLES_DIR / "expanded_baseline_vs_svr_delta.csv"), "SVR improvement over comparison methods", height=420)

st.info("RandomForestRegressor outputs are pending. No RF metrics are invented in this app.")
