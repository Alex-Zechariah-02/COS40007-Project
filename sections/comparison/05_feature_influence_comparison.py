import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import load_feature_influence_comparison, load_top_feature_influence_comparison
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain

page_header("Supervised Model Comparison: Feature Influence Comparison", "Official feature-influence diagnostics from the comparison notebook outputs.")
render_page_intro("comparison_features")
st.warning("Feature influence is diagnostic only. It does not prove causal impact on completion rates.")

all_inf = load_feature_influence_comparison()
if not all_inf.empty:
    show_table_with_guide(all_inf, "feature_influence_comparison.csv", "Feature influence comparison", max_rows=30)

top_inf = load_top_feature_influence_comparison()
if not top_inf.empty:
    show_table_with_guide(top_inf, "top_feature_influence_comparison.csv", "Top feature influence comparison", max_rows=30)

st.markdown("### Official feature-influence figures")
for fig, title in [
    ("top_feature_influence_comparison.png", "Top feature influence comparison"),
    ("feature_influence_support_vector_regression_permutation_importance.png", "SVR permutation importance"),
    ("feature_influence_randomforestregressor_native_feature_importance.png", "RF native feature importance"),
    ("feature_influence_randomforestregressor_permutation_importance.png", "RF permutation importance"),
]:
    e = explain(fig)
    guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

render_page_discussion("comparison_features")
next_steps(["Open 6. AI Demonstrator Comparison for a same-row example."])
