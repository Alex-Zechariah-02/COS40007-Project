import streamlit as st
import pandas as pd
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, show_table, show_table_with_guide, show_detail_table, guided_figure, next_steps, table_guide
from src.summary_builders import build_svr_metric_summary, build_svr_config_summary, build_svr_diagnostic_summary, build_baseline_summary, build_grouped_error_summary, build_output_status_summary
from src.data_loader import load_table, figure_path

page_header("SVR Branch: Overview", "Executive overview of the completed Support Vector Regression branch.")
render_page_intro("svr_overview")

st.markdown("### Branch overview")
metric_cards({
    "Task": "Regression",
    "Model": "SVR (RBF)",
    "Target": "next_year_completion_rate",
    "Row unit": "state-stage-sex-year",
}, columns=4, help_map={
    "Task": "Numeric target, so regression metrics are used.",
    "Model": "Support Vector Regression with radial basis function kernel.",
    "Target": "Predicts next-year school completion rate.",
    "Row unit": "State, education stage, sex, and input year.",
})

st.markdown("### Methodology flow")
st.write("Raw CSVs → target and benchmark construction → feature engineering → leakage audit → chronological validation → baselines → SVR tuning → held-out evaluation → diagnostics → AI demonstrator")

st.markdown("### Selected SVR configuration")
config_summary = build_svr_config_summary()
if not config_summary.empty:
    st.dataframe(config_summary, width="stretch", hide_index=True)

st.markdown("### Final held-out performance")
metric_cards(build_svr_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()

st.markdown("### Baseline comparison summary")
base = build_baseline_summary()
if not base.empty:
    st.dataframe(base, width="stretch", hide_index=True)

st.markdown("### Practical diagnostics")
diag = build_svr_diagnostic_summary()
metric_cards({
    "Mean residual": diag.get("Mean residual", "N/A"),
    "Bias": diag.get("Bias", "N/A"),
    "Within ±2 pp": diag.get("Within ±2 pp", "N/A"),
    "Within ±5 pp": diag.get("Within ±5 pp", "N/A"),
}, columns=4, help_map={
    "Mean residual": "Residual = actual minus predicted. Closer to 0 is better.",
    "Bias": "Dominant residual direction. Underprediction means actual values were often higher than predicted.",
    "Within ±2 pp": "Percentage of held-out rows within ±2 percentage points. Higher is better.",
    "Within ±5 pp": "Percentage of held-out rows within ±5 percentage points. Higher is better.",
})
st.caption("pp = percentage points.")

st.markdown("### Grouped error snapshot")
grouped = build_grouped_error_summary()
if not grouped.empty:
    st.dataframe(grouped, width="stretch", hide_index=True)

st.markdown("### Featured visual evidence")
for fig, title, purpose, how, better, takeaway in [
    ("actual_vs_predicted.png", "Actual versus predicted", "Shows fit between held-out actual values and predictions.", "Points closer to the diagonal have smaller error.", "Closer to diagonal is better.", "SVR follows the broad target range but still has notable misses."),
    ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted error spread.", "Positive residuals mean underprediction.", "Centered near 0 with narrow spread is better.", "The distribution supports the underprediction-bias finding."),
    ("expanded_mae_comparison.png", "MAE comparison", "Compares average absolute error across SVR and baseline models.", "Lower bars are better.", "Lower is better.", "SVR improves MAE against tested baselines."),
    ("error_by_state.png", "Error by state", "Shows where held-out errors are larger or smaller by state.", "Higher bars mean larger error.", "Lower is better.", "State-level diagnostics identify where predictions need more caution."),
    ("permutation_importance.png", "Permutation importance", "Shows which features affected held-out error when perturbed.", "Larger bars mean stronger diagnostic influence.", "No performance direction; this is interpretation evidence.", "Feature influence is diagnostic, not causal."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Use detailed branch pages for full tables and all figures.")

st.markdown("### AI demonstrator snapshot")
demo = load_table("final_ai_demonstrator.csv")
if not demo.empty:
    show_table_with_guide(demo, "final_ai_demonstrator.csv", "Representative prediction row", max_rows=1)

st.markdown("### Output evidence status")
out = build_output_status_summary()
st.dataframe(out, width="stretch", hide_index=True)

render_page_discussion("svr_overview")
next_steps([
    "Open 2. Model Design for the SVR pipeline and feature-set setup.",
    "Open 4. Final Evaluation for exact held-out metrics and baseline comparison.",
    "Open 5. Error Diagnostics for residual, tolerance, and grouped-error behaviour.",
    "Open 8. AI Demonstrator for the user-facing prediction example.",
])
