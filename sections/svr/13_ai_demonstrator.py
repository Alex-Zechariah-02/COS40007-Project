import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, metric_row
from src.formatting import fmt_num, clean_label

page_header("13. AI Demonstrator", "Representative held-out prediction and forecast preview.")
purpose_box("This page is the AI demonstrator. It explains one representative held-out prediction and a non-evaluable forecast preview row.")
demo = load_csv(TABLES_DIR / "final_ai_demonstrator.csv")
if not demo.empty:
    r = demo.iloc[0]
    st.subheader("Representative held-out prediction")
    metric_row([
        ("State", clean_label(r.get("state")), None),
        ("Stage", clean_label(r.get("stage")), None),
        ("Sex", clean_label(r.get("sex")), None),
        ("Input → Target", f"{r.get('Input Year')} → {r.get('Target Year')}", None),
    ])
    metric_row([
        ("Current completion", fmt_num(r.get("Current Completion Rate"), 2) + "%", None),
        ("Predicted next-year", fmt_num(r.get("Predicted Next-Year Completion Rate"), 2) + "%", None),
        ("Actual next-year", fmt_num(r.get("Actual Next-Year Completion Rate"), 2) + "%", None),
        ("Absolute error", fmt_num(r.get("Absolute Error"), 2) + " pp", None),
    ])
show_dataframe(demo, "Representative row table", height=260)

forecast_preview = load_csv(TABLES_DIR / "forecast_demonstrator_preview.csv")
st.subheader("Forecast preview")
st.warning("Forecast-candidate rows are preview-only because actual next-year targets are unavailable.")
show_dataframe(forecast_preview, height=260)

with st.expander("All forecast-candidate predictions", expanded=False):
    show_dataframe(load_csv(TABLES_DIR / "forecast_candidate_predictions.csv"), height=420)

for name in ["representative_prediction_actual_vs_predicted.png", "representative_prediction_waterfall.png", "forecast_candidate_prediction_distribution.png", "forecast_candidate_by_stage_sex.png"]:
    show_image(SVR_FIGURES_DIR / name)
show_dataframe(load_csv(CHECKS_DIR / "ai_demonstrator_audit.csv"), "AI demonstrator audit", height=260)
