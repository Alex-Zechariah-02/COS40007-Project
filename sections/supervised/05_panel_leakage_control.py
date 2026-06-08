import streamlit as st
from src.data_loader import load_table, load_check, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_detail_table, metric_cards, guided_figure, next_steps

page_header("Supervised Regression System: Panel and Leakage Control", "Final modelling panel, feature registry, leakage audit, and forecast-candidate separation.")
render_page_intro("panel_leakage")

panel = load_table("supervised_modelling_panel.csv")
feat = load_table("final_feature_registry.csv")
forecast = load_table("forecast_candidate_panel.csv")
metric_cards({
    "Panel rows": f"{len(panel):,}" if not panel.empty else "N/A",
    "Panel columns": f"{panel.shape[1]:,}" if not panel.empty else "N/A",
    "Registered features": f"{len(feat):,}" if not feat.empty else "N/A",
    "Forecast-candidate rows": f"{len(forecast):,}" if not forecast.empty else "N/A",
}, columns=4)

tab_panel, tab_leakage, tab_checks, tab_figures = st.tabs(["Panel summary", "Leakage rules", "Integrity checks", "Figures"])

with tab_panel:
    if not feat.empty:
        show_table_with_guide(feat, "final_feature_registry.csv", "Final feature registry", max_rows=20)

with tab_leakage:
    leak = load_check("leakage_audit.csv")
    if not leak.empty:
        show_table_with_guide(leak, "leakage_audit.csv", "Leakage audit", max_rows=20)

with tab_checks:
    for fname, title in [("panel_integrity_check.csv", "Panel integrity check"), ("split_integrity_check.csv", "Split integrity check"), ("missing_values_audit.csv", "Missing values audit")]:
        df = load_check(fname)
        if not df.empty:
            show_detail_table(df, title)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("modelling_panel_row_flow.png", "Modelling panel row flow", "Shows how rows move from raw/target panels into train, test, and forecast-candidate groups.", "Read left to right as row filtering and separation steps.", "No performance direction; pass means row separation is clear.", "Forecast-candidate rows are kept separate from supervised evaluation."),
        ("train_test_forecast_row_count_bar.png", "Train, test, and forecast row counts", "Shows number of rows in train, held-out test, and forecast candidate sets.", "Compare bar heights across split groups.", "No direct better direction; this verifies split size.", "The held-out test and forecast candidate sets are distinct."),
    ]:
        guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Split figures explain evaluation design rather than model accuracy.")

render_page_discussion("panel_leakage")
next_steps(["Open 6. Validation and Baselines before reviewing the SVR model branch."])
