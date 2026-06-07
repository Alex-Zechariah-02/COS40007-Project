import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, show_table, show_detail_table, why_not, metric_glossary, table_guide, next_steps
from src.summary_builders import build_supervised_system_overview
from src.data_loader import load_table
from src.content_blocks import WHY_REGRESSION, NO_CLUSTERING

page_header("Supervised Regression System: Overview", "Shared modelling scope for the completed SVR and RandomForestRegressor branches.")
render_page_intro("supervised_overview")

metric_cards({
    "Task type": "Regression",
    "Target": "next_year_completion_rate",
    "Model 1": "SVR",
    "Model 2": "RandomForestRegressor",
}, columns=4, help_map={
    "Task type": "The target is numeric, so regression metrics are used.",
    "Target": "Next-year school completion-rate value.",
    "Model 1": "Support Vector Regression branch is available.",
    "Model 2": "RandomForestRegressor branch is available and comparable against SVR.",
})

st.markdown("### Official comparison result")
st.info("The official comparison notebook validates both completed supervised-regression branches and selects Support Vector Regression as the stronger tested model on the current held-out outputs. The detailed evidence is available under Supervised Model Comparison.")

st.markdown("### One-screen methodology overview")
st.dataframe(build_supervised_system_overview(), width="stretch", hide_index=True)

st.markdown("### Metric and abbreviation guide")
metric_glossary()

why_not("Why classification metrics are excluded", WHY_REGRESSION)
why_not("Why clustering is not part of this app version", NO_CLUSTERING)

for fname, title in [
    ("project_context_summary.csv", "Project context summary"),
    ("supervised_regression_framing.csv", "Regression framing evidence"),
    ("excluded_scope.csv", "Excluded scope"),
    ("selected_public_sector_datasets.csv", "Selected dataset roles"),
]:
    df = load_table(fname)
    if not df.empty:
        show_detail_table(df, f"Detailed evidence: {title}")

render_page_discussion("supervised_overview")
next_steps([
    "Open 2. Shared Data Audit to inspect raw data and coverage.",
    "Open 3. Target and Row Unit to inspect the target construction.",
    "Open 6. Validation and Baselines before interpreting any model result.",
])
