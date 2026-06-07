import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, ARTIFACTS_DIR, SVR_MODELS_DIR, REQUIRED_CORE_FILES
from src.data_loader import load_csv, load_json
from src.ui_components import page_header, purpose_box, show_dataframe, file_status_table, success_box, caution_box

page_header("14. Output Check", "Final output manifest, model artifact, parameter JSON, and completeness checks.")
purpose_box("This page verifies that the notebook saved the expected evidence files and model artifacts.")
file_status_table(REQUIRED_CORE_FILES)

tabs = st.tabs(["Final output check", "Manifest", "Missing files", "Completion summary", "Best params"])
with tabs[0]: show_dataframe(load_csv(CHECKS_DIR / "final_output_check.csv"), height=360)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "final_output_manifest.csv"), height=460)
with tabs[2]: show_dataframe(load_csv(CHECKS_DIR / "missing_output_files.csv"), height=260)
with tabs[3]: show_dataframe(load_csv(TABLES_DIR / "final_notebook_completion_summary.csv"), height=300)
with tabs[4]: st.json(load_json(ARTIFACTS_DIR / "best_svr_params.json"))

missing = load_csv(CHECKS_DIR / "missing_output_files.csv")
if missing.empty:
    success_box("No missing-output rows are present in the missing output file table.")
else:
    caution_box("Review the missing output table above before submission.")
