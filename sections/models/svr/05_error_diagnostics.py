import streamlit as st
from src.data_loader import load_table, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, show_detail_table, metric_cards, guided_figure, metric_direction_guide, next_steps, abbreviation_note
from src.summary_builders import build_svr_diagnostic_summary, build_grouped_error_summary

page_header("SVR Branch: Error Diagnostics", "Residual direction, tolerance coverage, grouped errors, and worst-case rows.")
render_page_intro("svr_error_diag")

diag = build_svr_diagnostic_summary()
metric_cards({
    "Mean residual": diag.get("Mean residual", "N/A"),
    "Bias": diag.get("Bias", "N/A"),
    "Underprediction": diag.get("Underprediction", "N/A"),
    "Within ±2 pp": diag.get("Within ±2 pp", "N/A"),
    "Within ±5 pp": diag.get("Within ±5 pp", "N/A"),
    "P90 AE": diag.get("P90 AE", "N/A"),
}, columns=3, help_map={
    "Mean residual": "Residual = actual minus predicted. Closer to 0 is better.",
    "Bias": "Dominant residual direction. Underprediction means actual values were often higher than predictions.",
    "Underprediction": "Percentage of held-out rows where actual was higher than predicted.",
    "Within ±2 pp": "Percentage of rows within ±2 percentage points. Higher is better.",
    "Within ±5 pp": "Percentage of rows within ±5 percentage points. Higher is better.",
    "P90 AE": "90th percentile Absolute Error. Lower is better.",
})
abbreviation_note()
metric_direction_guide()

grouped = build_grouped_error_summary()
if not grouped.empty:
    st.markdown("### Highest-error grouped snapshot")
    st.dataframe(grouped, width="stretch", hide_index=True)

for fname, title in [
    ("residual_summary.csv", "Residual summary"),
    ("svr_metric_card_summary.csv", "Practical diagnostic metrics"),
    ("error_by_state.csv", "Error by state"),
    ("error_by_stage.csv", "Error by stage"),
    ("error_by_sex.csv", "Error by sex"),
    ("error_by_state_stage_sex.csv", "Detailed state-stage-sex errors"),
    ("worst_prediction_rows.csv", "Worst prediction rows"),
]:
    df = load_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=15)

st.markdown("### Diagnostic visuals")
for fig, title, purpose, how, better, takeaway in [
    ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted residual spread.", "Positive residuals mean underprediction; negative residuals mean overprediction.", "Centered near 0 with narrow spread is better.", "Supports the underprediction-bias interpretation."),
    ("underprediction_overprediction_bar.png", "Underprediction versus overprediction", "Shows the share of rows by residual sign.", "Compare the percentage of underpredicted and overpredicted rows.", "Balanced and low-bias behaviour is generally preferred.", "The model underpredicts most held-out rows."),
    ("svr_tolerance_coverage.png", "SVR tolerance coverage", "Shows percentage of predictions within practical error bands.", "Higher coverage means more predictions are close to actual values.", "Higher is better.", "Most rows are within ±5 percentage points."),
    ("error_by_state.png", "Error by state", "Shows state-level error magnitude.", "Higher bars mean larger errors.", "Lower is better.", "Some states require more cautious interpretation."),
    ("error_by_stage.png", "Error by stage", "Shows stage-level error magnitude.", "Compare bars across primary, lower secondary, and upper secondary.", "Lower is better.", "Stage diagnostics support targeted interpretation."),
    ("error_by_sex.png", "Error by sex", "Shows sex-group error magnitude.", "Compare male and female error bars.", "Lower is better.", "Sex-level diagnostics show whether errors differ by sex group."),
    ("worst_prediction_errors.png", "Worst prediction errors", "Shows rows with largest absolute errors.", "Higher bars are worse.", "Lower is better.", "Worst-case rows show where model caution is most needed."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Grouped diagnostics are descriptive and based on one held-out test year.")

render_page_discussion("svr_error_diag")
next_steps(["Open 6. Visual Evidence for the full figure gallery."])
