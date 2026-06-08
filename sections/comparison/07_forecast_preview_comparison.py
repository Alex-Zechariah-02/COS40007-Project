import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, show_table_with_guide, next_steps
from src.comparison_output_builders import load_forecast_preview_comparison, build_forecast_cards
from src.data_loader import load_comparison_check

page_header("Supervised Model Comparison: Forecast Preview Comparison", "Non-evaluable 2022 to 2023 forecast-candidate comparison.")
render_page_intro("comparison_forecast")

metric_cards(build_forecast_cards(), columns=4, help_map={
    "Forecast rows": "Matched non-evaluable forecast-candidate rows.",
    "SVR mean preview": "Mean SVR predicted completion rate for forecast candidates.",
    "RF mean preview": "Mean RF predicted completion rate for forecast candidates.",
    "Mean model difference": "Mean absolute difference between the two model previews in percentage points.",
})
abbreviation_note()
st.warning("Forecast preview rows are not used for final model selection because actual 2023 targets are not available in the current data.")

tab_summary, tab_forecast, tab_availability, tab_caveat = st.tabs(["Summary", "Forecast table", "Availability evidence", "Caveat"])

forecast = load_forecast_preview_comparison()
with tab_summary:
    if not forecast.empty:
        st.dataframe(forecast[["state", "stage", "sex", "svr_forecast_prediction", "rf_forecast_prediction", "absolute_forecast_prediction_difference"]].head(10), width="stretch", hide_index=True)

with tab_forecast:
    if not forecast.empty:
        c1, c2, c3 = st.columns(3)
        state = c1.selectbox("State", ["All"] + sorted(forecast["state"].astype(str).unique().tolist()))
        stage = c2.selectbox("Stage", ["All"] + sorted(forecast["stage"].astype(str).unique().tolist()))
        sex = c3.selectbox("Sex", ["All"] + sorted(forecast["sex"].astype(str).unique().tolist()))
        view = forecast.copy()
        if state != "All": view = view[view["state"].astype(str) == state]
        if stage != "All": view = view[view["stage"].astype(str) == stage]
        if sex != "All": view = view[view["sex"].astype(str) == sex]
        show_table_with_guide(view, "forecast_preview_model_comparison.csv", "Forecast preview model comparison", max_rows=20)

with tab_availability:
    availability = load_comparison_check("forecast_preview_availability.csv")
    if not availability.empty:
        display_availability = availability.copy()
        if "model_key" in display_availability.columns:
            display_availability["Model"] = display_availability["model_key"].astype(str).str.upper()
        elif "model_name" in display_availability.columns:
            display_availability["Model"] = display_availability["model_name"].astype(str)
        else:
            display_availability["Model"] = range(1, len(display_availability) + 1)
        exists_col = "exists" if "exists" in display_availability.columns else "file_exists" if "file_exists" in display_availability.columns else None
        display_availability["Forecast file exists"] = display_availability[exists_col].astype(bool) if exists_col else True
        display_availability["Status"] = display_availability["Forecast file exists"].map(lambda x: "Pass" if bool(x) else "Missing")
        show_table_with_guide(display_availability[["Model", "Forecast file exists", "Status"]], "forecast_preview_availability.csv", "Forecast file availability", max_rows=10)
        with st.expander("Detailed file availability evidence"):
            st.dataframe(availability, width="stretch", hide_index=True)

with tab_caveat:
    st.info("Forecast preview rows use input year 2022 to predict target year 2023. Because actual 2023 targets are unavailable in the current output files, this section previews model behaviour only and must not be used to select the final supervised model.")

render_page_discussion("comparison_forecast")
next_steps(["Return to 1. Overview for the full comparison summary.", "Open 2. Metric Leaderboard to review the final model ranking."])
