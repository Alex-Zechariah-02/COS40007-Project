import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_detail_table, next_steps, metric_cards
from src.data_loader import load_rf_table, load_rf_check
from src.rf_summary_builders import build_rf_config_summary

page_header("Random Forest Branch: Model Design", "Model architecture, preprocessing, feature sets, and candidate registry.")
render_page_intro("rf_model_design")

st.markdown("### Model design cards")
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

st.markdown("### Selected configuration")
cfg = build_rf_config_summary()
if not cfg.empty:
    st.dataframe(cfg, width="stretch", hide_index=True)

for fname, title in [
    ("rf_pipeline_readiness.csv", "Pipeline readiness check"),
    ("feature_set_registry.csv", "Feature-set registry"),
    ("rf_candidate_registry.csv", "RF candidate registry"),
    ("rf_feature_set_best_metric_summary.csv", "Best validation metric by feature set"),
]:
    df = load_rf_check(fname) if fname.endswith("readiness.csv") else load_rf_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=10)

render_page_discussion("rf_model_design")
next_steps(["Open 3. Training and Selection to inspect validation and selected candidate evidence."])
