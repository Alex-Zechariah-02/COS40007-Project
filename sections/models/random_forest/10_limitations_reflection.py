import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, next_steps, metric_cards, abbreviation_note
from src.rf_summary_builders import build_rf_metric_summary, build_rf_diagnostic_summary

page_header("Random Forest Branch: Limitations and Reflection", "Safe interpretation of what the RandomForestRegressor branch can and cannot support.")
render_page_intro("rf_limitations")

st.markdown("### Result context")
metric_cards(build_rf_metric_summary(), columns=4, help_map={
    "MAE": "Lower is better.",
    "RMSE": "Lower is better.",
    "R²": "Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Lower is better.",
})
abbreviation_note()

diag = build_rf_diagnostic_summary()
metric_cards({
    "Bias": diag.get("Bias", "N/A"),
    "Underprediction": diag.get("Underprediction", "N/A"),
    "Within ±5 pp": diag.get("Within ±5 pp", "N/A"),
}, columns=3)

st.markdown("### What the Random Forest branch can support")
st.success("""
- Demonstrates a complete RandomForestRegressor branch for the same supervised completion-rate prediction task.
- Provides a second supervised-regression model for comparison against SVR and baselines.
- Shows tree-ensemble validation, held-out testing, diagnostics, feature-importance evidence, and a representative prediction example.
- Supports model-comparison discussion by showing where RF is weaker and where simple baselines remain competitive.
""")

st.markdown("### What the Random Forest branch cannot support")
st.warning("""
- It should not be described as the best supervised model because current comparison outputs select SVR.
- It should not be described as high-accuracy forecasting because held-out R² is negative.
- It does not beat the strongest simple historical baselines in the current outputs.
- It does not prove causal effects of completion-history, education-capacity, demographic, or household variables.
- It does not evaluate forecast-candidate rows unless actual future targets are available.
- Its education-capacity feature influence should be interpreted cautiously because the current RF merge leaves those fields missing for lower and upper secondary rows.
- The intended RF max_depth grid was not fully evaluated because several validation candidates failed during fitting.
""")

render_page_discussion("rf_limitations")
next_steps(["Open the Supervised Model Comparison section to compare SVR and RF directly."])
