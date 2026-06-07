import streamlit as st
from src.data_loader import load_table, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, guided_figure, next_steps

page_header("SVR Branch: Feature Influence", "Permutation importance and feature-group interpretation for the selected SVR.")
render_page_intro("svr_feature_influence")

imp = load_table("permutation_importance.csv")
if not imp.empty:
    show_table_with_guide(imp, "permutation_importance.csv", "Permutation importance", max_rows=15)

grp = load_table("feature_group_importance_summary.csv")
if not grp.empty:
    show_table(grp, "Feature-group importance summary", max_rows=20, note="This groups model influence diagnostics by feature source. It is not causal evidence.")

for fname, title in [
    ("permutation_importance_with_groups.csv", "Permutation importance with feature groups"),
    ("feature_group_importance_summary.csv", "Feature group importance table"),
]:
    df = load_table(fname)
    if not df.empty:
        with st.expander(f"Detailed table: {title}"):
            st.dataframe(df, width="stretch", hide_index=True)

st.markdown("### Feature influence visuals")
for fig, title, purpose, how, better, takeaway in [
    ("permutation_importance.png", "Permutation importance", "Shows which features changed held-out error when perturbed.", "Larger bars mean stronger diagnostic influence.", "No performance direction; this is interpretation evidence.", "The trained SVR is sensitive to selected completion-history and contextual features."),
    ("permutation_importance_grouped_by_feature_source.png", "Grouped permutation importance", "Groups feature influence by source type.", "Higher grouped importance indicates larger combined diagnostic influence.", "No performance direction; use for interpretation.", "Shows which feature groups the model relies on most."),
    ("feature_group_importance_summary.png", "Feature-group importance summary", "Visualises group-level influence summary.", "Compare feature groups by importance magnitude.", "No universal better direction.", "Useful for explaining model behaviour without claiming causality."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Permutation importance is post-evaluation diagnostic evidence and not causal proof.")

render_page_discussion("svr_feature_influence")
next_steps(["Open 8. AI Demonstrator to see one prediction explained as a user-facing example."])
