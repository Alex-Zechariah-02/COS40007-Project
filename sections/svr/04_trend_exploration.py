import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image
from src.charts import line_chart

page_header("4. Trend Exploration", "Observed completion-rate trends before model training.")
purpose_box("This page displays exploratory evidence using observed completion-rate history. These plots are not model predictions and do not use next-year target columns as input features.")

tabs = st.tabs(["Trend source", "Stage trends", "Stage-sex trends", "Figures"])
with tabs[0]:
    df = load_csv(TABLES_DIR / "completion_rate_trend_source.csv")
    show_dataframe(df, height=420)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "completion_rate_trend_by_stage.csv"), height=420)
with tabs[2]: show_dataframe(load_csv(TABLES_DIR / "completion_rate_trend_by_stage_sex.csv"), height=420)
with tabs[3]:
    for name in ["completion_rate_trend_by_stage.png", "completion_rate_trend_by_sex.png", "selected_state_completion_trend_grid.png", "completion_gap_trend_by_stage.png", "state_gap_from_malaysia_distribution.png", "completion_change_distribution.png"]:
        show_image(SVR_FIGURES_DIR / name)
    show_dataframe(load_csv(CHECKS_DIR / "completion_rate_trend_audit.csv"), "Trend audit", height=280)
