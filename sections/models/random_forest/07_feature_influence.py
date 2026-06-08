import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Feature Influence", "Native RF importance, permutation importance, and feature-group diagnostics.")
render_page_intro("rf_feature_influence")
st.warning("Feature importance is diagnostic evidence only. It does not prove causal impact on completion rates.")

tab_native, tab_perm, tab_groups, tab_figures = st.tabs(["Native importance", "Permutation importance", "Feature groups", "Figures"])

with tab_native:
    df = load_rf_table("native_feature_importance.csv")
    if not df.empty:
        show_table_with_guide(df, "native_feature_importance.csv", "Native RF feature importance", max_rows=20)

with tab_perm:
    for fname, title in [("permutation_importance.csv", "RF permutation importance"), ("permutation_importance_with_groups.csv", "RF permutation importance with inferred groups")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=20)

with tab_groups:
    df = load_rf_table("feature_group_importance_summary.csv")
    if not df.empty:
        show_table_with_guide(df, "feature_group_importance_summary.csv", "RF feature-group importance summary", max_rows=20)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("native_feature_importance.png", "Native feature importance", "Shows RF split-based feature importance.", "Higher values mean greater tree-based importance.", "Not a performance metric.", "Completion-history features dominate native importance."),
        ("permutation_importance.png", "Permutation importance", "Shows score sensitivity when features are perturbed.", "Larger absolute importance means greater diagnostic influence.", "Not a performance metric.", "Stage and completion-history features are influential."),
        ("permutation_importance_grouped_by_feature_source.png", "Grouped permutation importance", "Groups feature influence by source/type.", "Higher total importance means stronger diagnostic influence.", "Not a performance metric.", "Completion-history and categorical groups dominate RF influence."),
        ("feature_group_count_bar.png", "Feature-group count", "Shows how model inputs are distributed by feature group.", "Higher bars mean more features from that group.", "No performance direction.", "Feature-count context helps interpret the selected RF feature set."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Interpret RF education-capacity importance cautiously because current RF merge left education features missing for lower and upper secondary rows.")

render_page_discussion("rf_feature_influence")
next_steps(["Open 8. AI Demonstrator to inspect a representative RF prediction row."])
