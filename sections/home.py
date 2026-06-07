import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, next_steps, abbreviation_note
from src.summary_builders import build_svr_metric_summary, build_supervised_system_overview
from src.comparison_output_builders import build_comparison_overview_cards, build_comparison_metric_cards

page_header("COS40007 State Completion Rate Prediction", "Supervised-regression review system for Malaysian school completion-rate prediction.")
render_page_intro("home")

st.markdown("### Current branch status")
metric_cards({
    "Shared workflow": "Complete",
    "SVR branch": "Complete",
    "RandomForestRegressor": "Complete",
    "Model comparison": "Available",
}, columns=4, help_map={
    "Shared workflow": "Shared data, target, features, leakage control, validation, and baselines are available.",
    "SVR branch": "Completed Support Vector Regression branch is available for review.",
    "RandomForestRegressor": "Completed RandomForestRegressor branch is available for review.",
    "Model comparison": "Active comparison between SVR and RandomForestRegressor outputs.",
})



st.markdown("### Official model comparison summary")
metric_cards(build_comparison_overview_cards(), columns=5, help_map={
    "Selected model": "Model selected by the official comparison notebook.",
    "Compared rows": "Matched held-out rows used for the model comparison.",
    "Validity checks": "Comparison validity checks passed.",
    "SVR row wins": "Rows where SVR has lower absolute error.",
    "RF row wins": "Rows where RF has lower absolute error.",
})
metric_cards(build_comparison_metric_cards(), columns=4, help_map={
    "Selected model": "Selected supervised-regression model.",
    "Best MAE": "Lower is better.",
    "Best RMSE": "Lower is better.",
    "Best R²": "Higher is better; negative values still limit the model claim.",
})

st.markdown("### SVR branch headline metrics")
metric_cards(build_svr_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()

st.markdown("### Supervised-regression workflow summary")
st.dataframe(build_supervised_system_overview(), width="stretch", hide_index=True)

next_steps([
    "For the full shared methodology, open Supervised Regression System → 1. Overview.",
    "For SVR details, open SVR Branch → 1. Overview.",
    "For RandomForestRegressor details, open Random Forest Branch → 1. Overview.",
    "For final model selection evidence, open Supervised Model Comparison → 2. Metric Leaderboard.",
    "For one user-facing model comparison case, open Supervised Model Comparison → 6. AI Demonstrator Comparison.",
])

render_page_discussion("home")
