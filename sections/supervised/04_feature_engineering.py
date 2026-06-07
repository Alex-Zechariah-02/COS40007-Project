import streamlit as st
import pandas as pd
from src.data_loader import load_table, load_check, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, show_detail_table, metric_cards, guided_figure, table_guide, next_steps, takeaway_box

page_header("Supervised Regression System: Feature Engineering", "Shared feature groups prepared for supervised completion-rate prediction.")
render_page_intro("feature_engineering")

feature_groups = [
    {"Feature group": "Completion history", "Purpose": "Captures persistence, lag, change, and rolling-history signals.", "Leakage note": "Allowed only when built from input year or earlier."},
    {"Feature group": "Education capacity", "Purpose": "Represents schools, students, teachers, and ratios.", "Leakage note": "District sources must be aggregated or use official state totals before merging."},
    {"Feature group": "Demographic pressure", "Purpose": "Represents population and school-age share context.", "Leakage note": "Future population values must not predict earlier targets."},
    {"Feature group": "Household context", "Purpose": "Represents household and living-quarter structure.", "Leakage note": "Merged by state-year only when available at input year."},
    {"Feature group": "Economic context", "Purpose": "Represents income and poverty context when source-year logic is valid.", "Leakage note": "Use as-of source years only; final SVR selected the feature set without economic features."},
]
st.dataframe(pd.DataFrame(feature_groups), width="stretch", hide_index=True)

reg = load_table("final_feature_registry.csv")
if not reg.empty:
    group_counts = reg.groupby("Feature Group").size().reset_index(name="Feature Count").sort_values("Feature Count", ascending=False)
    metric_cards({"Registered features": f"{len(reg):,}", "Feature groups": f"{group_counts['Feature Group'].nunique():,}", "Categorical features": f"{(reg.get('Feature Kind')=='categorical').sum() if 'Feature Kind' in reg.columns else 'N/A'}"}, columns=3)
    show_table_with_guide(reg, "final_feature_registry.csv", "Final feature registry", max_rows=15)
    show_detail_table(group_counts, "Feature counts by group")

for fname, title in [
    ("education_features.csv", "Education capacity features"),
    ("population_features.csv", "Population features"),
    ("household_features.csv", "Household features"),
    ("economic_features.csv", "Economic and poverty features"),
    ("fertility_features.csv", "Fertility features"),
    ("autoregressive_feature_panel.csv", "Autoregressive completion-history features"),
]:
    df = load_table(fname)
    if not df.empty:
        show_detail_table(df.head(100), title)

st.markdown("### Key feature visuals")
for fig, title, purpose, how, better, takeaway in [
    ("feature_group_count_bar.png", "Feature group counts", "Shows how many features come from each source group.", "Compare bar heights by group.", "No direct performance direction; compact and valid features are preferred over uncontrolled feature growth.", "The modelling panel combines several interpretable feature groups."),
    ("education_capacity_correlation_heatmap.png", "Education capacity correlation", "Shows relationships among education-capacity variables.", "Stronger colours indicate stronger relationships depending on the colour scale.", "No universal better direction; high correlation can indicate redundancy.", "Correlation review helps interpret feature overlap."),
    ("economic_data_age_by_year.png", "Economic data age", "Shows how old economic source data is after as-of merging.", "Lower data age means fresher economic evidence.", "Lower is better.", "Economic features must be handled cautiously if sparse or stale."),
    ("completion_lag_relationship_scatter.png", "Completion lag relationship", "Shows relationship between historical completion and next-year target.", "Look for patterns between previous/current completion history and future target.", "Clearer relationship can help prediction.", "Autoregressive features are legitimate only when based on current or prior years."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Feature visuals support understanding and do not prove causality.")

render_page_discussion("feature_engineering")
next_steps(["Open 5. Panel and Leakage Control to confirm these features are merged safely."])
