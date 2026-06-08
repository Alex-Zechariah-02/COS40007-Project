import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, next_steps, metric_cards, guided_figure
from src.data_loader import load_rf_table, load_rf_check, rf_figure_path
from src.rf_summary_builders import build_rf_config_summary

page_header("Random Forest Branch: Model Design", "Model architecture, preprocessing, feature sets, and candidate registry.")
render_page_intro("rf_model_design")

metric_cards({
    "Algorithm": "RandomForestRegressor",
    "Model type": "Tree ensemble",
    "Selected set": "autoregressive + categorical + education",
    "Target": "next_year_completion_rate",
}, columns=4, help_map={
    "Algorithm": "A regression ensemble made from multiple decision-tree regressors.",
    "Model type": "Captures nonlinear interactions, but can overfit small tabular panels.",
    "Selected set": "Selected from chronological validation among successful candidates.",
    "Target": "Numeric completion-rate prediction target.",
})

tab_pipeline, tab_features, tab_candidates, tab_figures = st.tabs(["Pipeline", "Features", "Candidate registry", "Figures"])

with tab_pipeline:
    cfg = build_rf_config_summary()
    if not cfg.empty:
        st.markdown("### Selected design summary")
        st.dataframe(cfg, width="stretch", hide_index=True)
    df = load_rf_check("rf_pipeline_readiness.csv")
    if not df.empty:
        show_table_with_guide(df, "rf_pipeline_readiness.csv", "Pipeline readiness", max_rows=10)

with tab_features:
    df = load_rf_table("feature_set_registry.csv")
    if not df.empty:
        show_table_with_guide(df, "feature_set_registry.csv", "Feature-set registry", max_rows=20)

with tab_candidates:
    for fname, title in [("rf_candidate_registry.csv", "RF candidate registry"), ("rf_feature_set_best_metric_summary.csv", "RF candidate grid / validation summary")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=20)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("feature_set_size_comparison.png", "Feature-set size comparison", "Shows the number of features in each tested RF feature set.", "Compare feature counts across the tested feature-set options.", "No direct better direction; compact sets can reduce noise while larger sets may add signal.", "The RF notebook tested multiple feature scopes before selecting a final set."),
        ("feature_group_count_bar.png", "Feature-group count", "Shows how the selected features are distributed by source group.", "Higher bars mean more features from that group.", "No direct performance direction.", "The RF design includes completion-history, categorical, and education-capacity information."),
        ("feature_set_validation_metric_panel.png", "Feature-set validation panel", "Shows validation metrics across RF feature sets.", "Lower error metrics are better; higher R² is better.", "Depends on the metric.", "Validation evidence supports the selected RF feature set among successful candidates."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Missing figure means it was not exported under this filename.")

render_page_discussion("rf_model_design")
next_steps(["Open 3. Training and Selection to inspect validation and selected candidate evidence."])
