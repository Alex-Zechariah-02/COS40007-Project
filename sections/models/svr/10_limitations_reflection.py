import streamlit as st
from src.data_loader import load_table
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, show_table, next_steps, abbreviation_note
from src.summary_builders import build_svr_metric_summary, build_svr_diagnostic_summary

page_header("SVR Branch: Limitations and Reflection", "Safe interpretation of what the completed SVR branch can and cannot support.")
render_page_intro("svr_limitations")

st.markdown("### Result context")
metric_cards(build_svr_metric_summary(), columns=4, help_map={
    "MAE": "Lower is better.",
    "RMSE": "Lower is better.",
    "R²": "Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Lower is better.",
})
abbreviation_note()

diag = build_svr_diagnostic_summary()
metric_cards({"Bias": diag.get("Bias", "N/A"), "Underprediction": diag.get("Underprediction", "N/A"), "Within ±5 pp": diag.get("Within ±5 pp", "N/A")}, columns=3)

st.markdown("### What the SVR branch can support")
st.success("""
- Demonstrates a complete supervised-regression workflow for next-year completion-rate prediction.
- Shows how Malaysian public-sector education and contextual data can support planning analysis.
- Compares SVR against baselines using held-out chronological test evidence.
- Provides residual, tolerance, grouped-error, feature-influence, and demonstrator evidence.
""")

st.markdown("### What the SVR branch cannot support")
st.warning("""
- It should not be described as high-accuracy forecasting because held-out R² is negative.
- It does not prove causal effects of socioeconomic, demographic, or education-capacity variables.
- It does not evaluate forecast-candidate rows unless actual future targets are available.
- It does not replace policy judgement, school-domain expertise, or future model validation.
""")

render_page_discussion("svr_limitations")
next_steps(["When RF outputs are ready, open Random Forest Branch and then Supervised Model Comparison."])
