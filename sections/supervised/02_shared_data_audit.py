import streamlit as st
from src.config import RAW_DATASET_FILES
from src.data_loader import load_check, load_table, load_raw, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, show_detail_table, metric_cards, guided_figure, next_steps
from src.file_registry import RAW_AUDIT_FILES

page_header("Supervised Regression System: Shared Data Audit", "Raw dataset inventory, coverage, missingness, duplicate-key checks, and controlled raw-data preview.")
render_page_intro("shared_data_audit")

inventory = load_check("raw_dataset_inventory.csv")
if inventory.empty:
    inventory = load_table("raw_dataset_inventory.csv")
if not inventory.empty:
    show_table_with_guide(inventory, "raw_dataset_inventory.csv", "Raw dataset inventory", max_rows=20)

quality = load_check("raw_data_quality_summary.csv")
if not quality.empty:
    show_table(quality, "Raw data quality summary", max_rows=20, note="Use this table to identify missingness, duplicate, or coverage risks before feature engineering.")

st.markdown("### Raw data preview")
st.caption("Only sample rows are shown by default so large raw files remain readable.")
raw_file = st.selectbox("Select raw CSV", RAW_DATASET_FILES)
raw_df = load_raw(raw_file)
if raw_df.empty:
    st.warning("Raw file is not available in the app package.")
else:
    metric_cards({"Rows": f"{len(raw_df):,}", "Columns": f"{raw_df.shape[1]:,}", "File": raw_file}, columns=3)
    st.dataframe(raw_df.head(15), width="stretch", hide_index=True)
    with st.expander("Show column list"):
        st.write(list(raw_df.columns))

st.markdown("### Key audit visuals")
for fig, title, purpose, how, better, takeaway in [
    ("raw_dataset_row_count_bar.png", "Raw dataset row counts", "Shows how many rows each raw source contains.", "Compare bar heights across datasets.", "No performance direction; this describes source size.", "Population data is much larger, so previewing is more practical than full display."),
    ("raw_dataset_year_coverage_timeline.png", "Raw dataset year coverage", "Shows year coverage across raw sources.", "Read across each source timeline.", "More consistent coverage is easier for time-aware modelling.", "Coverage differences justify careful merge and as-of logic."),
    ("missing_value_summary_heatmap.png", "Missing-value overview", "Shows missingness patterns before modelling.", "Cells with stronger colouring indicate more missingness depending on the legend.", "Less missingness is easier to model.", "Missingness must be handled explicitly before training."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "These are audit figures, not model-performance figures.")

with st.expander("Detailed raw audit tables"):
    for f, purpose in RAW_AUDIT_FILES:
        df = load_check(f)
        if df.empty:
            df = load_table(f)
        if not df.empty:
            st.markdown(f"##### {purpose}")
            st.dataframe(df.head(50), width="stretch", hide_index=True)
            if len(df) > 50:
                st.caption(f"Showing first 50 of {len(df):,} rows.")

render_page_discussion("shared_data_audit")
next_steps(["Open 3. Target and Row Unit after confirming the raw sources."])
