import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, guided_figure, next_steps, show_table_with_guide
from src.rf_summary_builders import build_rf_metric_summary, build_rf_config_summary, build_rf_diagnostic_summary, build_rf_grouped_error_summary, build_rf_output_status_summary, build_rf_validation_issue_summary, build_rf_baseline_summary
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Overview", "Executive overview of the completed RandomForestRegressor branch.")
render_page_intro("rf_overview")

st.markdown("### Branch overview")
metric_cards({
    "Task": "Regression",
    "Model": "RandomForestRegressor",
    "Target": "next_year_completion_rate",
    "Row unit": "state-stage-sex-year",
}, columns=4, help_map={
    "Task": "Numeric target, so regression metrics are used.",
    "Model": "Tree-ensemble regression model.",
    "Target": "Predicts next-year school completion rate.",
    "Row unit": "State, education stage, sex, and input year.",
})

st.markdown("### Methodology flow")
st.write("Raw CSVs → target construction → feature engineering → chronological validation → baselines → RF tuning → held-out evaluation → diagnostics → AI demonstrator")

st.markdown("### Selected RF configuration")
cfg = build_rf_config_summary()
if not cfg.empty:
    st.dataframe(cfg, width="stretch", hide_index=True)

st.markdown("### Final held-out performance")
metric_cards(build_rf_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()

st.markdown("### Baseline comparison summary")
base = build_rf_baseline_summary()
if not base.empty:
    st.dataframe(base, width="stretch", hide_index=True)

st.markdown("### Practical diagnostics")
diag = build_rf_diagnostic_summary()
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
grouped = build_rf_grouped_error_summary()
if not grouped.empty:
    st.dataframe(grouped, width="stretch", hide_index=True)

st.markdown("### Validation caveat snapshot")
fit = build_rf_validation_issue_summary()
if not fit.empty:
    st.dataframe(fit, width="stretch", hide_index=True)
    st.warning("Several RF validation candidates failed during fitting. The selected model is valid among successful candidates, but the full intended max_depth grid was not completely evaluated.")

st.markdown("### Featured visual evidence")
for fig, title, purpose, how, better, takeaway in [
    ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual values with RF predictions.", "Points closer to the diagonal line have smaller prediction error.", "Closer to diagonal is better.", "RF shows larger misses than the completed SVR branch."),
    ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted error spread.", "Positive residuals mean underprediction.", "Centered near 0 is better.", "RF has clear underprediction bias."),
    ("expanded_mae_comparison.png", "MAE comparison", "Compares RF error against the tested baseline set.", "Lower bars are better.", "Lower is better.", "RF does not beat the strongest simple baselines by MAE."),
    ("error_by_state.png", "Error by state", "Shows where held-out RF errors are larger or smaller by state.", "Higher bars mean larger error.", "Lower is better.", "State-level diagnostics identify where RF predictions need more caution."),
    ("native_feature_importance.png", "Native feature importance", "Shows RF split-based feature influence.", "Higher values mean greater tree-based importance.", "No performance direction; this is interpretation evidence.", "Completion-history features dominate RF importance."),
]:
    guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Use detailed RF pages and comparison pages for full evidence.")

st.markdown("### AI demonstrator snapshot")
demo = load_rf_table("final_ai_demonstrator.csv")
if not demo.empty:
    show_table_with_guide(demo, "final_ai_demonstrator.csv", "Representative RF prediction row", max_rows=1)

st.markdown("### Output evidence status")
out = build_rf_output_status_summary()
st.dataframe(out, width="stretch", hide_index=True)

render_page_discussion("rf_overview")
next_steps([
    "Open 2. Model Design for the RF pipeline and feature-set setup.",
    "Open 4. Final Evaluation for exact held-out metrics and baseline comparison.",
    "Open 5. Error Diagnostics for residual, tolerance, and grouped-error behaviour.",
    "Open 8. AI Demonstrator for the user-facing prediction example.",
    "Open the Supervised Model Comparison section to compare RF against SVR.",
])
