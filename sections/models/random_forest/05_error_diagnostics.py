import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, show_table_with_guide, guided_figure, next_steps, metric_direction_guide
from src.rf_summary_builders import build_rf_diagnostic_summary, build_rf_grouped_error_summary
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Error Diagnostics", "Residuals, tolerance coverage, grouped errors, and worst RF prediction rows.")
render_page_intro("rf_error_diagnostics")

diag = build_rf_diagnostic_summary()
metric_cards({
    "Mean residual": diag.get("Mean residual", "N/A"),
    "Bias": diag.get("Bias", "N/A"),
    "Underprediction": diag.get("Underprediction", "N/A"),
    "Within ±2 pp": diag.get("Within ±2 pp", "N/A"),
    "Within ±5 pp": diag.get("Within ±5 pp", "N/A"),
    "P90 AE": diag.get("P90 AE", "N/A"),
}, columns=3, help_map={
    "Mean residual": "Residual = actual minus predicted. Closer to 0 is better.",
    "Bias": "Dominant residual direction.",
    "Underprediction": "Percentage of held-out rows where actual was higher than predicted.",
    "Within ±2 pp": "Percentage of rows within ±2 percentage points. Higher is better.",
    "Within ±5 pp": "Percentage of rows within ±5 percentage points. Higher is better.",
    "P90 AE": "90th percentile Absolute Error. Lower is better.",
})
abbreviation_note()

tab_metrics, tab_grouped, tab_worst, tab_figures = st.tabs(["Practical metrics", "Grouped errors", "Worst rows", "Figures"])

with tab_metrics:
    metric_direction_guide()
    for fname, title in [("residual_summary.csv", "Residual summary"), ("rf_metric_card_summary.csv", "Practical diagnostic metrics"), ("rf_tolerance_summary.csv", "RF tolerance summary"), ("rf_residual_direction_summary.csv", "RF residual direction summary")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=15)

with tab_grouped:
    grouped = build_rf_grouped_error_summary()
    if not grouped.empty:
        st.markdown("### Highest-error grouped snapshot")
        st.dataframe(grouped, width="stretch", hide_index=True)
    for fname, title in [("error_by_state.csv", "RF error by state"), ("error_by_stage.csv", "RF error by stage"), ("error_by_sex.csv", "RF error by sex"), ("error_by_state_stage_sex.csv", "RF detailed state-stage-sex errors")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=20)

with tab_worst:
    df = load_rf_table("worst_prediction_rows.csv")
    if not df.empty:
        show_table_with_guide(df, "worst_prediction_rows.csv", "Worst RF prediction rows", max_rows=20)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted residual spread.", "Positive residuals mean underprediction; negative residuals mean overprediction.", "Centered near 0 with narrow spread is better.", "RF residuals show underprediction tendency."),
        ("underprediction_overprediction_bar.png", "Underprediction versus overprediction", "Shows the share of rows by residual sign.", "Compare underprediction and overprediction percentages.", "Balanced and low-bias behaviour is generally preferred.", "RF underpredicts most held-out rows."),
        ("rf_tolerance_coverage.png", "RF tolerance coverage", "Shows percentage of predictions within practical error bands.", "Higher coverage means more predictions are close to actual values.", "Higher is better.", "RF has weaker tolerance coverage than SVR."),
        ("error_by_state.png", "Error by state", "Shows state-level RF error magnitude.", "Higher bars mean larger errors.", "Lower is better.", "State-level diagnostics show where RF is weaker."),
        ("error_by_stage.png", "Error by stage", "Shows stage-level RF error magnitude.", "Compare primary, lower secondary, and upper secondary bars.", "Lower is better.", "RF errors are largest for secondary_upper in comparison outputs."),
        ("error_by_sex.png", "Error by sex", "Shows sex-group RF error magnitude.", "Compare male and female error bars.", "Lower is better.", "Sex-level diagnostics support subgroup interpretation."),
        ("prediction_error_lollipop_top_errors.png", "Worst RF prediction errors", "Shows RF rows with largest absolute errors.", "Higher values are worse.", "Lower is better.", "Worst-case rows show where RF caution is most needed."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Grouped diagnostics are descriptive and based on one held-out test year.")

render_page_discussion("rf_error_diagnostics")
next_steps(["Open 6. Visual Evidence for the full RF figure gallery."])
