import streamlit as st
from pathlib import Path
from src.config import APP_TITLE, REQUIRED_CORE_FILES, TABLES_DIR, CHECKS_DIR
from src.data_loader import load_csv
from src.formatting import fmt_num

st.set_page_config(
    page_title="COS40007 SVR Notebook System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.markdown("### Branch status")
st.sidebar.success("SVR: complete")
st.sidebar.info("RandomForestRegressor: pending")
st.sidebar.warning("Clustering: excluded from this supervised app")

metrics_df = load_csv(TABLES_DIR / "final_svr_metrics.csv")
if not metrics_df.empty:
    row = metrics_df.iloc[0]
    st.sidebar.markdown("### Final SVR")
    st.sidebar.write(f"MAE: **{fmt_num(row.get('MAE'), 3)}**")
    st.sidebar.write(f"RMSE: **{fmt_num(row.get('RMSE'), 3)}**")
    st.sidebar.write(f"R²: **{fmt_num(row.get('R2'), 3)}**")

pages = {
    "Home": [
        st.Page("sections/home.py", title="Dashboard Home"),
    ],
    "SVR Notebook System": [
        st.Page("sections/svr/01_project_scope.py", title="1. Project Scope"),
        st.Page("sections/svr/02_raw_data_audit.py", title="2. Raw Data Audit"),
        st.Page("sections/svr/03_target_construction.py", title="3. Target Construction"),
        st.Page("sections/svr/04_trend_exploration.py", title="4. Trend Exploration"),
        st.Page("sections/svr/05_feature_engineering.py", title="5. Feature Engineering"),
        st.Page("sections/svr/06_supervised_panel.py", title="6. Supervised Panel"),
        st.Page("sections/svr/07_validation_baselines.py", title="7. Validation & Baselines"),
        st.Page("sections/svr/08_svr_training.py", title="8. SVR Training"),
        st.Page("sections/svr/09_final_evaluation.py", title="9. Final Evaluation"),
        st.Page("sections/svr/10_error_diagnostics.py", title="10. Error Diagnostics"),
        st.Page("sections/svr/11_visual_evidence.py", title="11. Visual Evidence"),
        st.Page("sections/svr/12_permutation_importance.py", title="12. Permutation Importance"),
        st.Page("sections/svr/13_ai_demonstrator.py", title="13. AI Demonstrator"),
        st.Page("sections/svr/14_output_check.py", title="14. Output Check"),
        st.Page("sections/svr/15_limitations_reflection.py", title="15. Limitations & Reflection"),
    ],
    "Random Forest": [
        st.Page("sections/random_forest/pending.py", title="Random Forest Pending"),
    ],
    "Supervised Comparison": [
        st.Page("sections/comparison/supervised_comparison_pending.py", title="SVR vs RF Pending"),
    ],
}

pg = st.navigation(pages, expanded=True)
pg.run()
