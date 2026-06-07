import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, metric_cards, abbreviation_note, guided_figure, next_steps
from src.comparison_output_builders import load_row_level_prediction_comparison, load_row_level_winner_summary, load_largest_disagreements
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain

page_header("Supervised Model Comparison: Prediction Comparison", "Official row-level held-out prediction comparison.")
render_page_intro("comparison_predictions")

wins = load_row_level_winner_summary()
if not wins.empty:
    cards = {str(row["winner_by_row"]): f"{int(row['row_count'])} rows" for _, row in wins.iterrows()}
    metric_cards(cards, columns=3, help_map={"SVR": "Rows where SVR has lower absolute error.", "RF": "Rows where RF has lower absolute error."})

comp = load_row_level_prediction_comparison()
if comp.empty:
    st.error("Official row-level comparison output is unavailable.")
else:
    abbreviation_note()
    st.markdown("### Filter row-level predictions")
    c1, c2, c3 = st.columns(3)
    state = c1.selectbox("State", ["All"] + sorted(comp["state"].astype(str).unique().tolist()))
    stage = c2.selectbox("Stage", ["All"] + sorted(comp["stage"].astype(str).unique().tolist()))
    sex = c3.selectbox("Sex", ["All"] + sorted(comp["sex"].astype(str).unique().tolist()))
    view = comp.copy()
    if state != "All":
        view = view[view["state"].astype(str) == state]
    if stage != "All":
        view = view[view["stage"].astype(str) == stage]
    if sex != "All":
        view = view[view["sex"].astype(str) == sex]
    show_table_with_guide(view, "row_level_prediction_comparison.csv", "Filtered row-level prediction comparison", max_rows=20)

st.markdown("### Largest model disagreement rows")
disagree = load_largest_disagreements()
if not disagree.empty:
    show_table_with_guide(disagree, "largest_model_disagreement_rows.csv", "Largest disagreement rows", max_rows=20)

for fig, title in [("row_level_winner_summary.png", "Row-level winner summary")]:
    e = explain(fig)
    guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

render_page_discussion("comparison_predictions")
next_steps(["Open 4. Error Comparison for tolerance, residual, and grouped-error evidence."])
