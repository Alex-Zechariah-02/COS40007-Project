import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, next_steps, abbreviation_note
from src.summary_builders import build_svr_metric_summary, build_supervised_system_overview

page_header("COS40007 State Completion Rate Prediction", "Supervised-regression review system for Malaysian school completion-rate prediction.")
render_page_intro("home")

st.markdown("### Current branch status")
metric_cards({
    "Shared workflow": "Complete",
    "SVR branch": "Complete",
    "RandomForestRegressor": "Pending",
    "Model comparison": "Pending",
}, columns=4, help_map={
    "Shared workflow": "Shared data, target, features, leakage control, validation, and baselines are available.",
    "SVR branch": "Completed Support Vector Regression branch is available for review.",
    "RandomForestRegressor": "Reserved for teammate outputs once validated.",
    "Model comparison": "Enabled only after RF outputs match the shared contract.",
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
    "For the completed model result, open SVR Branch → 1. Overview.",
    "For final metrics, open SVR Branch → 4. Final Evaluation.",
    "For practical model behaviour, open SVR Branch → 5. Error Diagnostics.",
    "For one user-facing example, open SVR Branch → 8. AI Demonstrator.",
])

render_page_discussion("home")
