import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.rf_summary_builders import build_rf_diagnostic_summary, build_rf_grouped_error_summary
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Error Diagnostics", "Residuals, tolerance coverage, grouped errors, and worst-case rows.")
render_page_intro("rf_error_diag")

diag = build_rf_diagnostic_summary()
st.markdown("### Practical diagnostic cards")
metric_cards({
    "Mean residual": diag.get("Mean residual", "N/A"),
    "Bias": diag.get("Bias", "N/A"),
    "Underprediction": diag.get("Underprediction", "N/A"),
    "Within ±2 pp": diag.get("Within ±2 pp", "N/A"),
    "Within ±5 pp": diag.get("Within ±5 pp", "N/A"),
}, columns=5, help_map={
    "Mean residual": "Residual = actual minus predicted. Closer to 0 is better.",
    "Bias": "Dominant residual direction.",
    "Underprediction": "Percentage of rows where actual was higher than predicted.",
    "Within ±2 pp": "Higher is better.",
    "Within ±5 pp": "Higher is better.",
})
abbreviation_note()
metric_direction_guide()

st.markdown("### Grouped error snapshot")
grouped = build_rf_grouped_error_summary()
if not grouped.empty:
    st.dataframe(grouped, width="stretch", hide_index=True)

for fname, title in [
    ("residual_summary.csv", "RF residual summary"),
    ("rf_tolerance_summary.csv", "RF tolerance summary"),
    ("rf_residual_direction_summary.csv", "RF residual direction summary"),
    ("error_by_state.csv", "RF error by state"),
    ("error_by_stage.csv", "RF error by stage"),
    ("error_by_sex.csv", "RF error by sex"),
    ("error_by_state_stage_sex.csv", "RF detailed state-stage-sex errors"),
    ("worst_prediction_rows.csv", "Worst RF prediction rows"),
]:
    df = load_rf_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=12)

st.markdown("### Error diagnostic visuals")
for fig, title, purpose, how, better, takeaway in [
    ("residual_distribution.png", "Residual distribution", "Shows RF actual-minus-predicted error spread.", "Positive residuals mean underprediction.", "Centered near 0 is better.", "RF has underprediction bias."),
    ("rf_tolerance_coverage.png", "Tolerance coverage", "Shows percentage of predictions inside practical error bands.", "Higher bars are better.", "Higher is better.", "RF tolerance coverage is limited compared with SVR."),
    ("error_by_state.png", "Error by state", "Shows average RF error by state.", "Higher bars mean larger error.", "Lower is better.", "W.P. Putrajaya is the highest-error state in current RF output."),
    ("error_by_stage.png", "Error by stage", "Shows RF errors by education stage.", "Higher bars mean larger error.", "Lower is better.", "secondary_upper is the highest-error stage."),
    ("error_by_sex.png", "Error by sex", "Shows RF errors by sex group.", "Higher bars mean larger error.", "Lower is better.", "male rows have higher RF error than female rows."),
]:
    guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Grouped diagnostics describe this held-out test only.")

render_page_discussion("rf_error_diag")
next_steps(["Open 6. Visual Evidence for the full RF figure gallery."])
