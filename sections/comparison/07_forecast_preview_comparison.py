import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, show_table_with_guide, next_steps
from src.comparison_output_builders import load_forecast_preview_comparison, build_forecast_cards
from src.data_loader import load_comparison_check

page_header("Supervised Model Comparison: Forecast Preview Comparison", "Non-evaluable 2022 to 2023 forecast-candidate comparison.")
render_page_intro("comparison_forecast")

st.markdown("### Forecast preview summary")
metric_cards(build_forecast_cards(), columns=4, help_map={
    "Forecast rows": "Matched non-evaluable forecast-candidate rows.",
    "SVR mean preview": "Mean SVR prediction for forecast candidates.",
    "RF mean preview": "Mean RF prediction for forecast candidates.",
    "Mean model difference": "Mean absolute difference between the two model previews.",
})
abbreviation_note()
st.warning("Forecast preview rows are not used for final model selection because actual 2023 targets are not available in the current data.")

availability = load_comparison_check("forecast_preview_availability.csv")
if not availability.empty:
    show_table_with_guide(availability, "forecast_preview_availability.csv", "Forecast file availability", max_rows=10)

forecast = load_forecast_preview_comparison()
if not forecast.empty:
    st.markdown("### Filter forecast-candidate rows")
    c1, c2, c3 = st.columns(3)
    state = c1.selectbox("State", ["All"] + sorted(forecast["state"].astype(str).unique().tolist()))
    stage = c2.selectbox("Stage", ["All"] + sorted(forecast["stage"].astype(str).unique().tolist()))
    sex = c3.selectbox("Sex", ["All"] + sorted(forecast["sex"].astype(str).unique().tolist()))
    view = forecast.copy()
    if state != "All":
        view = view[view["state"].astype(str) == state]
    if stage != "All":
        view = view[view["stage"].astype(str) == stage]
    if sex != "All":
        view = view[view["sex"].astype(str) == sex]
    show_table_with_guide(view, "forecast_preview_model_comparison.csv", "Forecast preview model comparison", max_rows=20)

render_page_discussion("comparison_forecast")
next_steps(["Return to 1. Overview for the full comparison summary.", "Open 2. Metric Leaderboard to review the final model ranking."])
