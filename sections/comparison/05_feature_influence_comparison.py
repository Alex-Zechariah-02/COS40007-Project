import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import load_feature_influence_comparison, load_top_feature_influence_comparison
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain

page_header("Supervised Model Comparison: Feature Influence Comparison", "Official feature-influence diagnostics from the comparison notebook outputs.")
render_page_intro("comparison_features")
st.warning("Feature influence is diagnostic only. It does not prove causal impact on completion rates.")

tab_summary, tab_svr, tab_rf, tab_figures = st.tabs(["Summary", "SVR importance", "RF importance", "Figures"])

all_inf = load_feature_influence_comparison()
top_inf = load_top_feature_influence_comparison()

with tab_summary:
    if not top_inf.empty:
        show_table_with_guide(top_inf, "top_feature_influence_comparison.csv", "Top feature influence comparison", max_rows=30)

with tab_svr:
    if not all_inf.empty:
        view = all_inf[all_inf.astype(str).apply(lambda s: s.str.contains("Support Vector|svr", case=False, na=False)).any(axis=1)]
        show_table_with_guide(view if not view.empty else all_inf, "feature_influence_comparison.csv", "SVR feature influence rows", max_rows=30)

with tab_rf:
    if not all_inf.empty:
        view = all_inf[all_inf.astype(str).apply(lambda s: s.str.contains("RandomForest|random forest|rf", case=False, na=False)).any(axis=1)]
        show_table_with_guide(view if not view.empty else all_inf, "feature_influence_comparison.csv", "RF feature influence rows", max_rows=30)

with tab_figures:
    for fig, title in [("top_feature_influence_comparison.png", "Top feature influence comparison"), ("feature_influence_support_vector_regression_permutation_importance.png", "SVR permutation importance"), ("feature_influence_randomforestregressor_native_feature_importance.png", "RF native feature importance"), ("feature_influence_randomforestregressor_permutation_importance.png", "RF permutation importance")]:
        e = explain(fig)
        guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

render_page_discussion("comparison_features")
next_steps(["Open 6. AI Demonstrator Comparison for a same-row example."])
