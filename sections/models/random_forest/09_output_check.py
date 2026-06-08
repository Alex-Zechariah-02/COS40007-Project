import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, next_steps
from src.rf_summary_builders import (
    build_rf_output_status_summary,
    build_rf_output_completion_summary,
    build_rf_normalized_output_check,
    build_rf_artifact_status,
    build_rf_missing_output_summary,
)
from src.data_loader import load_rf_table, load_rf_check

page_header("Random Forest Branch: Output Check", "Saved evidence package, model artifact, parameter artifact, and output manifest status.")
render_page_intro("rf_output_check")

st.markdown("### Output evidence summary")
st.dataframe(build_rf_output_status_summary(), width="stretch", hide_index=True)

tab_status, tab_artifacts, tab_files, tab_visuals = st.tabs(["Status", "Artifacts", "Detailed files", "Visual registry"])

with tab_status:
    summary = build_rf_output_completion_summary()
    if not summary.empty:
        show_table(summary, "Completion/output summary", max_rows=10)
    status_check = build_rf_normalized_output_check()
    if not status_check.empty:
        show_table_with_guide(status_check, "rf_normalized_output_check.csv", "Output status checks", max_rows=20)
    missing = build_rf_missing_output_summary()
    if missing.empty:
        st.success("No missing required RF output files were reported in the output audit.")
    else:
        show_table(missing, "Missing output files", max_rows=20)

with tab_artifacts:
    st.dataframe(build_rf_artifact_status(), width="stretch", hide_index=True)

with tab_files:
    raw_audit = load_rf_check("output_file_audit.csv")
    if not raw_audit.empty:
        st.caption("This is the original RF output file audit from the saved RF notebook outputs.")
        st.dataframe(raw_audit, width="stretch", hide_index=True)
    manifest = load_rf_table("final_output_manifest.csv")
    if not manifest.empty:
        with st.expander("Detailed output manifest"):
            st.dataframe(manifest, width="stretch", hide_index=True)

with tab_visuals:
    visual = load_rf_table("visual_evidence_registry.csv")
    if not visual.empty:
        st.dataframe(visual, width="stretch", hide_index=True)

render_page_discussion("rf_output_check")
next_steps(["Open 10. Limitations and Reflection for RF caveats."])
