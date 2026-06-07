import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import load_ai_demonstrator_comparison, load_row_level_prediction_comparison
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain

page_header("Supervised Model Comparison: AI Demonstrator Comparison", "Same-row prediction demonstrator from the official comparison notebook outputs.")
render_page_intro("comparison_ai_demo")

ai = load_ai_demonstrator_comparison()
if not ai.empty:
    r = ai.iloc[0]
    metric_cards({
        "State": str(r.get("state", "N/A")),
        "Stage": str(r.get("stage", "N/A")),
        "Sex": str(r.get("sex", "N/A")),
        "Actual": f"{float(r.get('actual_next_year_completion_rate')):.2f}%",
        "SVR prediction": f"{float(r.get('svr_prediction')):.2f}%",
        "RF prediction": f"{float(r.get('rf_prediction')):.2f}%",
        "Winner": str(r.get("winner_by_row", "N/A")),
    }, columns=4, help_map={"Winner": "Model with lower absolute error for this held-out row."})
    abbreviation_note()
    show_table_with_guide(ai, "combined_ai_demonstrator.csv", "Official comparison demonstrator row", max_rows=1)

comp = load_row_level_prediction_comparison()
if not comp.empty:
    st.markdown("### Inspect another held-out row")
    c1, c2, c3 = st.columns(3)
    state = c1.selectbox("State", sorted(comp["state"].astype(str).unique().tolist()))
    subset = comp[comp["state"].astype(str) == state]
    stage = c2.selectbox("Stage", sorted(subset["stage"].astype(str).unique().tolist()))
    subset = subset[subset["stage"].astype(str) == stage]
    sex = c3.selectbox("Sex", sorted(subset["sex"].astype(str).unique().tolist()))
    subset = subset[subset["sex"].astype(str) == sex]
    if not subset.empty:
        show_table_with_guide(subset.head(1), "row_level_prediction_comparison.csv", "Selected held-out row", max_rows=1)

fig = "ai_demonstrator_comparison.png"
e = explain(fig)
guided_figure(comparison_figure_path(fig), "AI demonstrator comparison", e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

render_page_discussion("comparison_ai_demo")
next_steps(["Open 7. Forecast Preview Comparison for non-evaluable 2022 to 2023 forecast candidates."])
