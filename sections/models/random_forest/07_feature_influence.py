import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Feature Influence", "Native RF importance, permutation importance, and feature-group diagnostics.")
render_page_intro("rf_feature_influence")
st.warning("Feature importance is diagnostic evidence only. It does not prove causal impact on completion rates.")

for fname, title in [
    ("native_feature_importance.csv", "Native RF feature importance"),
    ("permutation_importance.csv", "RF permutation importance"),
    ("permutation_importance_with_groups.csv", "RF permutation importance with inferred groups"),
    ("feature_group_importance_summary.csv", "RF feature-group importance summary"),
]:
    df = load_rf_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=15)

for fig, title, purpose, how, better, takeaway in [
    ("native_feature_importance.png", "Native feature importance", "Shows RF split-based feature importance.", "Higher values mean greater tree-based importance.", "Not a performance metric.", "Completion-history features dominate native importance."),
    ("permutation_importance.png", "Permutation importance", "Shows score sensitivity when features are perturbed.", "Larger absolute importance means greater diagnostic influence.", "Not a performance metric.", "Stage and completion-history features are influential."),
    ("permutation_importance_grouped_by_feature_source.png", "Grouped permutation importance", "Groups feature influence by source/type.", "Higher total importance means stronger diagnostic influence.", "Not a performance metric.", "Completion-history and categorical groups dominate RF influence."),
]:
    guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Interpret RF education-capacity importance cautiously because current RF merge left education features missing for lower and upper secondary rows.")

render_page_discussion("rf_feature_influence")
next_steps(["Open 8. AI Demonstrator to inspect a representative RF prediction row."])
