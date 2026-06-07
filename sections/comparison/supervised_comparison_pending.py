import pandas as pd
import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, metric_direction_guide, next_steps
from src.data_loader import load_table
from src.validators import rf_pending_status

page_header("Supervised Model Comparison Pending", "Reserved page for the final SVR versus RandomForestRegressor comparison.")
render_page_intro("comparison_pending")

st.markdown("### Current available comparison: SVR versus baselines")
comp = load_table("expanded_model_comparison_metrics.csv")
if not comp.empty:
    show_table_with_guide(comp, "expanded_model_comparison_metrics.csv", "Current model and baseline leaderboard", max_rows=15)

st.markdown("### Future comparison validity checks")
checks = pd.DataFrame([
    {"Check": "Same target", "Required value": "next_year_completion_rate"},
    {"Check": "Same row unit", "Required value": "state-stage-sex-year"},
    {"Check": "Same held-out test rows", "Required value": "Exact same state/stage/sex/input-year/target-year keys"},
    {"Check": "Same actual target values", "Required value": "Actual completion targets must match row-by-row"},
    {"Check": "Same baselines", "Required value": "Training mean and persistence at minimum"},
    {"Check": "Same regression metrics", "Required value": "MAE, RMSE, R², Median AE"},
])
st.dataframe(checks, width="stretch", hide_index=True)
metric_direction_guide()

st.markdown("### RF file status")
st.dataframe(rf_pending_status(), width="stretch", hide_index=True)

render_page_discussion("comparison_pending")
next_steps(["Current valid comparison is SVR versus baselines only.", "Enable SVR versus RF only after RF files pass all alignment checks."])
