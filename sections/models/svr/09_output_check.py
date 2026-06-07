import streamlit as st
import pandas as pd
from src.data_loader import load_table, load_check, model_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, show_table, show_detail_table, metric_cards, next_steps
from src.summary_builders import build_output_status_summary
from src.config import ARTIFACTS_DIR
from src.validators import app_readiness

page_header("SVR Branch: Output Check", "Saved evidence package, model artifact, parameter artifact, and output manifest status.")
render_page_intro("svr_output_check")

st.markdown("### Output evidence summary")
st.dataframe(build_output_status_summary(), width="stretch", hide_index=True)

summary = load_table("final_notebook_completion_summary.csv")
if not summary.empty:
    show_table(summary, "Completion summary", max_rows=10)

check = load_check("final_output_check.csv")
if not check.empty:
    show_table_with_guide(check, "final_output_check.csv", "Output status checks", max_rows=20)

missing = load_check("missing_output_files.csv")
if missing.empty:
    st.success("No missing required output files were reported.")
else:
    show_table(missing, "Missing output files", max_rows=20)

st.markdown("### Artifact status")
status = pd.DataFrame([
    {"Artifact": "SVR model artifact", "Status": "Present" if model_path("final_selected_svr_pipeline.joblib").exists() else "Missing"},
    {"Artifact": "Best parameter JSON", "Status": "Present" if (ARTIFACTS_DIR/"best_svr_params.json").exists() else "Missing"},
])
st.dataframe(status, width="stretch", hide_index=True)

with st.expander("Detailed evidence file status"):
    st.dataframe(app_readiness(), width="stretch", hide_index=True)

manifest = load_table("final_output_manifest.csv")
if not manifest.empty:
    with st.expander("Detailed output manifest"):
        st.dataframe(manifest, width="stretch", hide_index=True)

visual = load_table("visual_evidence_registry.csv")
if not visual.empty:
    with st.expander("Detailed visual evidence registry"):
        st.dataframe(visual, width="stretch", hide_index=True)

render_page_discussion("svr_output_check")
next_steps(["Open 10. Limitations and Reflection for the safe final interpretation."])
