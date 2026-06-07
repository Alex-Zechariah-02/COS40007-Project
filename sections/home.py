import streamlit as st
from src.config import APP_TITLE, TABLES_DIR, CHECKS_DIR, REQUIRED_CORE_FILES
from src.data_loader import load_csv, load_json
from src.formatting import fmt_num
from src.ui_components import page_header, purpose_box, metric_row, file_status_table, show_dataframe

page_header(APP_TITLE, "Interactive Streamlit replacement for the completed Support Vector Regression notebook.")
purpose_box("This app presents the completed SVR notebook as an interactive system: raw data audit, target construction, feature engineering, validation, model training, final evaluation, visual evidence, AI demonstrator, output checks, and limitations.")

metrics = load_csv(TABLES_DIR / "final_svr_metrics.csv")
summary = load_csv(TABLES_DIR / "final_notebook_completion_summary.csv")
if not metrics.empty:
    row = metrics.iloc[0]
    metric_row([
        ("MAE", fmt_num(row.get("MAE"), 3), "Mean absolute error in completion-rate percentage points"),
        ("RMSE", fmt_num(row.get("RMSE"), 3), "Large-error penalty metric"),
        ("R²", fmt_num(row.get("R2"), 3), "Can be negative on held-out data"),
        ("Median AE", fmt_num(row.get("Median_AE"), 3), "Robust typical error"),
    ])
    st.caption(f"Selected feature set: `{row.get('Selected Feature Set')}` | Candidate: `{row.get('Selected Candidate Name')}`")

st.subheader("System status")
file_status_table(REQUIRED_CORE_FILES)

if not summary.empty:
    st.subheader("Notebook completion summary")
    show_dataframe(summary, height=280)

st.subheader("How to read this system")
st.markdown("""
1. Start with **Project Scope** to understand the supervised-regression framing.
2. Move through **Raw Data Audit**, **Target Construction**, and **Feature Engineering** to verify the data pipeline.
3. Review **Validation & Baselines** and **SVR Training** to see how the model was selected.
4. Use **Final Evaluation**, **Error Diagnostics**, **Visual Evidence**, and **AI Demonstrator** for results.
5. Use **Output Check** and **Limitations** before presenting or submitting.
""")
