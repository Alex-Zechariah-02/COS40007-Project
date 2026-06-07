import streamlit as st
from src.config import CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image

page_header("2. Raw Data Audit", "Raw CSV availability, schema, coverage, missing values, and duplicate checks.")
purpose_box("This page proves the SVR branch starts from raw Malaysian public-sector CSV inputs and validates file structure before modelling.")

tabs = st.tabs(["Availability", "Inventory", "Schema", "Coverage", "Missing", "Duplicates", "Figures"])
with tabs[0]: show_dataframe(load_csv(CHECKS_DIR / "raw_file_availability.csv"), height=420)
with tabs[1]: show_dataframe(load_csv(CHECKS_DIR / "raw_dataset_inventory.csv"), height=420)
with tabs[2]: show_dataframe(load_csv(CHECKS_DIR / "raw_schema_audit.csv"), height=420)
with tabs[3]: show_dataframe(load_csv(CHECKS_DIR / "raw_coverage_audit.csv"), height=420)
with tabs[4]:
    show_dataframe(load_csv(CHECKS_DIR / "missing_values_audit.csv"), height=420)
    show_dataframe(load_csv(CHECKS_DIR / "raw_data_quality_summary.csv"), height=300)
with tabs[5]: show_dataframe(load_csv(CHECKS_DIR / "duplicate_key_audit.csv"), height=420)
with tabs[6]:
    show_image(SVR_FIGURES_DIR / "raw_dataset_row_count_bar.png")
    show_image(SVR_FIGURES_DIR / "raw_dataset_year_coverage_timeline.png")
    show_image(SVR_FIGURES_DIR / "missing_value_summary_heatmap.png")
