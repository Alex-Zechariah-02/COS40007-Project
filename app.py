import streamlit as st
from src.config import APP_TITLE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="COS40007",
    layout="wide",
    initial_sidebar_state="expanded",
)

def pg(path: str, title: str, url_path: str):
    return st.Page(path, title=title, url_path=url_path)

pages = {
    "Home": [
        pg("sections/home.py", "Dashboard Home", "home"),
    ],
    "Supervised Regression System": [
        pg("sections/supervised/01_overview.py", "1. Overview", "supervised-overview"),
        pg("sections/supervised/02_shared_data_audit.py", "2. Shared Data Audit", "shared-data-audit"),
        pg("sections/supervised/03_target_row_unit.py", "3. Target and Row Unit", "target-row-unit"),
        pg("sections/supervised/04_feature_engineering.py", "4. Feature Engineering", "shared-feature-engineering"),
        pg("sections/supervised/05_panel_leakage_control.py", "5. Panel and Leakage Control", "panel-leakage-control"),
        pg("sections/supervised/06_validation_baselines.py", "6. Validation and Baselines", "validation-baselines"),
    ],
    "SVR Branch": [
        pg("sections/models/svr/01_overview.py", "1. Overview", "svr-overview"),
        pg("sections/models/svr/02_model_design.py", "2. Model Design", "svr-model-design"),
        pg("sections/models/svr/03_training_selection.py", "3. Training and Selection", "svr-training-selection"),
        pg("sections/models/svr/04_final_evaluation.py", "4. Final Evaluation", "svr-final-evaluation"),
        pg("sections/models/svr/05_error_diagnostics.py", "5. Error Diagnostics", "svr-error-diagnostics"),
        pg("sections/models/svr/06_visual_evidence.py", "6. Visual Evidence", "svr-visual-evidence"),
        pg("sections/models/svr/07_feature_influence.py", "7. Feature Influence", "svr-feature-influence"),
        pg("sections/models/svr/08_ai_demonstrator.py", "8. AI Demonstrator", "svr-ai-demonstrator"),
        pg("sections/models/svr/09_output_check.py", "9. Output Check", "svr-output-check"),
        pg("sections/models/svr/10_limitations_reflection.py", "10. Limitations and Reflection", "svr-limitations-reflection"),
    ],
    "Random Forest Branch": [
        pg("sections/models/random_forest/pending.py", "RandomForestRegressor Pending", "rf-pending"),
    ],
    "Supervised Model Comparison": [
        pg("sections/comparison/supervised_comparison_pending.py", "Comparison Pending", "supervised-comparison-pending"),
    ],
}

page = st.navigation(pages, position="sidebar", expanded=True)
page.run()
