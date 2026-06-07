import streamlit as st
from src.data_loader import load_table, load_check, load_artifact_json, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, show_detail_table, metric_cards, guided_figure, next_steps, abbreviation_note
from src.summary_builders import build_svr_config_summary

page_header("SVR Branch: Model Design", "SVR pipeline, feature sets, preprocessing, and candidate design.")
render_page_intro("svr_model_design")

st.markdown("### Model design cards")
metric_cards({
    "Algorithm": "SVR",
    "Kernel": "RBF",
    "Numeric preprocessing": "Impute + scale",
    "Categorical preprocessing": "One-hot encode",
}, columns=4, help_map={
    "Algorithm": "Support Vector Regression for numeric prediction.",
    "Kernel": "Radial basis function kernel for nonlinear relationships.",
    "Numeric preprocessing": "Median imputation and StandardScaler are used before SVR.",
    "Categorical preprocessing": "State, stage, and sex are encoded as categorical inputs.",
})

cfg = build_svr_config_summary()
if not cfg.empty:
    st.markdown("### Selected design summary")
    st.dataframe(cfg, width="stretch", hide_index=True)

for fname, title in [
    ("svr_pipeline_readiness.csv", "Pipeline readiness"),
    ("feature_set_registry.csv", "Feature-set registry"),
    ("svr_candidate_registry.csv", "SVR candidate registry"),
    ("svr_candidate_grid_summary.csv", "SVR candidate grid summary"),
]:
    df = load_table(fname)
    if df.empty:
        df = load_check(fname)
    if not df.empty:
        show_table(df, title, max_rows=15)

st.markdown("### Model design visuals")
for fig, title, purpose, how, better, takeaway in [
    ("feature_set_size_comparison.png", "Feature-set size comparison", "Shows how many features were included in each tested feature set.", "Compare bar heights by feature set.", "No direct performance direction; compact but informative sets are preferred.", "Feature-set comparison supports transparent model design."),
    ("svr_candidate_grid_summary.png", "SVR candidate grid summary", "Shows the tested SVR candidate configuration space.", "Read candidate counts and parameter combinations.", "No universal better direction; validation selects candidates.", "Tuning is documented instead of hidden."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Candidate design evidence is not held-out test performance.")

render_page_discussion("svr_model_design")
next_steps(["Open 3. Training and Selection to see which candidate was selected and why."])
