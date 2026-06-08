import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps, metric_cards, abbreviation_note
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: AI Demonstrator", "Representative RF prediction and non-evaluable forecast preview.")
render_page_intro("rf_ai_demo")

tab_row, tab_explain, tab_forecast, tab_figures = st.tabs(["Representative row", "Prediction explanation", "Forecast preview", "Figures"])

demo = load_rf_table("final_ai_demonstrator.csv")
with tab_row:
    if not demo.empty:
        r = demo.iloc[0]
        metric_cards({
            "State": r.get("state", "N/A"),
            "Stage": r.get("stage", "N/A"),
            "Sex": r.get("sex", "N/A"),
            "Input → Target": f"{r.get('Input Year', 'N/A')} → {r.get('Target Year', 'N/A')}",
            "Prediction": f"{float(r.get('Predicted Next-Year Completion Rate')):.2f}%",
            "Actual": f"{float(r.get('Actual Next-Year Completion Rate')):.2f}%",
            "AE": f"{float(r.get('Absolute Error')):.2f} pp",
            "Outcome": r.get("Prediction Outcome Label", "N/A"),
        }, columns=4, help_map={"AE":"Absolute Error. Lower is better.", "Prediction":"Predicted next-year completion rate.", "Actual":"Observed next-year completion rate."})
        abbreviation_note()

with tab_explain:
    if not demo.empty:
        show_table_with_guide(demo, "final_ai_demonstrator.csv", "Representative RF prediction row", max_rows=1)

with tab_forecast:
    st.info("Forecast-candidate rows are preview-only because actual future targets are unavailable. They are not used for final RF evaluation.")
    for fname, title in [("forecast_candidate_predictions.csv", "RF forecast-candidate predictions"), ("forecast_candidate_2022_panel.csv", "RF forecast-candidate panel")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=10)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("representative_prediction_actual_vs_predicted.png", "Representative prediction", "Shows actual and predicted values for one RF held-out row.", "Smaller gap between actual and predicted is better.", "Closer values are better.", "The representative RF row is underpredicted."),
        ("representative_prediction_waterfall.png", "Prediction waterfall", "Shows current value, prediction, actual value, and error components for the representative row.", "Use labels to trace the prediction difference.", "Smaller absolute error is better.", "This supports user-facing interpretation."),
        ("forecast_candidate_prediction_distribution.png", "Forecast-candidate prediction distribution", "Shows RF preview predictions for non-evaluable future rows.", "Read as preview-only because actual targets are unavailable.", "No better direction; not evaluated.", "Forecast preview must not be used as final model performance."),
        ("forecast_candidate_by_stage_sex.png", "Forecast preview by stage and sex", "Shows RF forecast-candidate preview distribution by stage and sex.", "Compare group-level preview patterns only; actual targets are unavailable.", "No better direction; not evaluated.", "This is preview evidence, not held-out performance evidence."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Forecast-candidate rows are preview-only, not final evaluation evidence.")

render_page_discussion("rf_ai_demo")
next_steps(["Open 9. Output Check to inspect saved RF evidence files."])
