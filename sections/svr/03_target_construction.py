import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, discussion
from src import notebook_discussions as nd

page_header("3. Target Construction", "Completion target, Malaysia benchmark, gap construction, and row-unit decision.")
purpose_box("This page shows how the notebook constructs the numeric regression target `next_year_completion_rate` and keeps Malaysia as a benchmark rather than a training state.")

tabs = st.tabs(["Completion panel", "Malaysia benchmark", "Main and both-only panels", "Target review", "Row unit", "Figures"])
with tabs[0]: show_dataframe(load_csv(TABLES_DIR / "completion_target_panel.csv"), height=420)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "malaysia_benchmark.csv"), height=420)
with tabs[2]:
    show_dataframe(load_csv(TABLES_DIR / "main_target_panel.csv"), "Main male/female target panel", height=300)
    show_dataframe(load_csv(TABLES_DIR / "both_only_target_panel.csv"), "Both-only official aggregate panel", height=300)
    show_dataframe(load_csv(TABLES_DIR / "main_supervised_target_panel.csv"), "Supervised rows with next-year target", height=300)
with tabs[3]:
    show_dataframe(load_csv(TABLES_DIR / "target_distribution_review.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "target_construction_audit.csv"), height=300)
with tabs[4]: show_dataframe(load_csv(CHECKS_DIR / "row_unit_validation.csv"), height=420)
with tabs[5]:
    for name in ["target_distribution_histogram.png", "target_by_stage_boxplot.png", "target_by_sex_boxplot.png", "main_vs_both_target_comparison.png", "row_unit_count_by_stage_sex.png"]:
        show_image(SVR_FIGURES_DIR / name)

discussion("Notebook discussion", nd.TARGET_CONSTRUCTION)
