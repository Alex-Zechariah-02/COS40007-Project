import streamlit as st
from src.data_loader import load_table, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, metric_cards, guided_figure, next_steps, abbreviation_note
from src.formatting import fmt_pp

page_header("SVR Branch: AI Demonstrator", "Representative held-out prediction and forecast-preview explanation.")
render_page_intro("svr_ai_demo")

demo = load_table("final_ai_demonstrator.csv")
if not demo.empty:
    r = demo.iloc[0]
    metric_cards({
        "State": str(r.get("state", "N/A")).title(),
        "Stage": str(r.get("stage", "N/A")).replace("_", " ").title(),
        "Sex": str(r.get("sex", "N/A")).title(),
        "Input → target": f"{r.get('Input Year', 'N/A')} → {r.get('Target Year', 'N/A')}",
        "Prediction": fmt_pp(r.get("Predicted Next-Year Completion Rate")),
        "Actual": fmt_pp(r.get("Actual Next-Year Completion Rate")),
        "Residual": fmt_pp(r.get("Residual")),
        "AE": fmt_pp(r.get("Absolute Error")),
    }, columns=4, help_map={
        "Prediction": "Predicted next-year completion rate.",
        "Actual": "Observed next-year completion rate in the held-out test set.",
        "Residual": "Actual minus predicted. Positive means underprediction; negative means overprediction.",
        "AE": "Absolute Error. Lower is better.",
    })
    abbreviation_note()
    show_table_with_guide(demo, "final_ai_demonstrator.csv", "Representative prediction row", max_rows=1)

forecast = load_table("forecast_candidate_predictions.csv")
if not forecast.empty:
    st.markdown("### Forecast-candidate preview")
    st.info("Forecast-candidate rows are preview-only unless actual future targets become available. They are not used for final evaluation.")
    show_table(forecast, "Forecast-candidate predictions", max_rows=20)

st.markdown("### Demonstrator visuals")
for fig, title, purpose, how, better, takeaway in [
    ("representative_prediction_actual_vs_predicted.png", "Representative actual versus predicted", "Shows the demonstrator row prediction against its actual target.", "Compare predicted and actual values.", "Smaller gap is better.", "The representative row shows how a model output is interpreted."),
    ("representative_prediction_waterfall.png", "Representative prediction waterfall", "Breaks down the demonstrator prediction information.", "Read the labelled value changes in sequence.", "Smaller final error is better.", "Helps explain one prediction in a user-facing way."),
    ("forecast_candidate_prediction_distribution.png", "Forecast preview distribution", "Shows predicted values for forecast candidates.", "Read as preview distribution only, not evaluated accuracy.", "No evaluation direction without actual targets.", "Forecast preview can support planning discussion but not final scoring."),
    ("forecast_candidate_by_stage_sex.png", "Forecast preview by stage and sex", "Groups forecast-preview predictions by stage and sex.", "Compare predicted values by group.", "No accuracy direction without actual targets.", "This helps review predicted patterns while clearly labelling them as non-evaluable."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Forecast previews are not final evaluation evidence without actual targets.")

render_page_discussion("svr_ai_demo")
next_steps(["Open 9. Output Check to verify saved evidence and artifacts."])
