import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, next_steps
from src.rf_summary_builders import build_rf_output_status_summary
from src.data_loader import load_rf_table, load_rf_check

page_header("Random Forest Branch: Output Check", "RF output completeness and artifact availability.")
render_page_intro("rf_output_check")

st.markdown("### RF output evidence summary")
st.dataframe(build_rf_output_status_summary(), width="stretch", hide_index=True)

for fname, title, kind in [
    ("output_file_audit.csv", "RF output file audit", "check"),
    ("final_output_manifest.csv", "RF final output manifest", "table"),
    ("visual_evidence_registry.csv", "RF visual evidence registry", "table"),
]:
    df = load_rf_check(fname) if kind == "check" else load_rf_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=20)

render_page_discussion("rf_output_check")
next_steps(["Open 10. Limitations and Reflection for RF caveats."])
