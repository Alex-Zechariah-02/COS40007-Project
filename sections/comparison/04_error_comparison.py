import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import load_tolerance_comparison, load_residual_bias_comparison, load_grouped_error_comparison, build_tolerance_cards
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain

page_header("Supervised Model Comparison: Error Comparison", "Tolerance, residual, and grouped-error comparison from official comparison outputs.")
render_page_intro("comparison_errors")

metric_cards(build_tolerance_cards(), columns=4, help_map={
    "SVR within ±2 pp": "Higher is better.",
    "RF within ±2 pp": "Higher is better.",
    "SVR within ±5 pp": "Higher is better.",
    "RF within ±5 pp": "Higher is better.",
})
abbreviation_note()

tab_tolerance, tab_grouped, tab_figures, tab_guide = st.tabs(["Tolerance and bias", "Grouped errors", "Figures", "Metric guide"])

with tab_tolerance:
    tol = load_tolerance_comparison()
    if not tol.empty:
        show_table_with_guide(tol, "tolerance_comparison.csv", "Tolerance coverage", max_rows=10)
    resid = load_residual_bias_comparison()
    if not resid.empty:
        show_table_with_guide(resid, "residual_bias_comparison.csv", "Residual bias comparison", max_rows=10)

with tab_grouped:
    for group in ["state", "stage", "sex"]:
        df = load_grouped_error_comparison(group)
        if not df.empty:
            show_table_with_guide(df, f"error_comparison_by_{group}.csv", f"Error comparison by {group}", max_rows=20)

with tab_figures:
    for fig, title in [("tolerance_comparison.png", "Tolerance comparison"), ("residual_bias_comparison.png", "Residual bias comparison"), ("error_by_state_comparison.png", "Error by state comparison"), ("error_by_stage_comparison.png", "Error by stage comparison"), ("error_by_sex_comparison.png", "Error by sex comparison")]:
        e = explain(fig)
        guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

with tab_guide:
    metric_direction_guide()

render_page_discussion("comparison_errors")
next_steps(["Open 5. Feature Influence Comparison to inspect model behaviour diagnostics."])
