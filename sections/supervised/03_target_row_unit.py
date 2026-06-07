import streamlit as st
from src.data_loader import load_table, load_check, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, show_detail_table, metric_cards, guided_figure, why_not, next_steps
from src.content_blocks import WHY_REGRESSION

page_header("Supervised Regression System: Target and Row Unit", "Numeric target, Malaysia benchmark, completion gap, and state-stage-sex-year row unit.")
render_page_intro("target_row_unit")

main = load_table("main_target_panel.csv")
both = load_table("both_only_target_panel.csv")
sup = load_table("main_supervised_target_panel.csv")
metric_cards({
    "Main target rows": f"{len(main):,}" if not main.empty else "N/A",
    "Both-only rows": f"{len(both):,}" if not both.empty else "N/A",
    "Supervised target rows": f"{len(sup):,}" if not sup.empty else "N/A",
    "Target": "next_year_completion_rate",
}, columns=4, help_map={
    "Main target rows": "Male/female state-stage-sex-year rows used by the main branch.",
    "Both-only rows": "Official aggregate rows kept separate because they combine male and female.",
    "Supervised target rows": "Rows with constructed next-year target for supervised modelling.",
    "Target": "Numeric next-year completion-rate value.",
})

why_not("Why this is regression", WHY_REGRESSION)

for fname, title in [
    ("main_supervised_target_panel.csv", "Main supervised target panel"),
    ("malaysia_benchmark.csv", "Malaysia benchmark rows"),
    ("both_only_target_panel.csv", "Both-only aggregate panel"),
]:
    df = load_table(fname)
    if not df.empty:
        show_table(df, title, max_rows=15)

rowval = load_check("row_unit_validation.csv")
if not rowval.empty:
    show_table_with_guide(rowval, "row_unit_validation.csv", "Row-unit validation", max_rows=20)

audit = load_check("target_construction_audit.csv")
if not audit.empty:
    show_detail_table(audit, "Detailed target construction audit")

st.markdown("### Key target and row-unit visuals")
for fig, title, purpose, how, better, takeaway in [
    ("target_distribution_histogram.png", "Target distribution", "Shows the numeric next-year completion-rate target distribution.", "Read the x-axis as completion-rate values and the y-axis as row frequency.", "No single better direction; this is a target-understanding figure.", "The target is numeric and suitable for regression."),
    ("target_by_stage_boxplot.png", "Target by stage", "Shows target variation across education stages.", "Compare median lines and spread by stage.", "No direct better direction; lower spread can be easier to predict.", "Stage differences justify including stage as a categorical feature."),
    ("target_by_sex_boxplot.png", "Target by sex", "Shows target variation between male and female rows.", "Compare medians and spread by sex.", "No direct better direction; this is a distribution check.", "Sex-specific rows preserve information that a both-only panel would hide."),
    ("main_vs_both_target_comparison.png", "Main versus both-only comparison", "Compares sex-specific main rows with official both-only aggregate rows.", "Read it as a row-unit evidence figure.", "No direct better direction.", "Both-only rows are useful for sensitivity/context but not mixed into the main model."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Distribution figures support target design, not final model performance.")

render_page_discussion("target_row_unit")
next_steps(["Open 4. Feature Engineering to see which predictors are built for this target."])
