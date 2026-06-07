import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, ARTIFACTS_DIR, SVR_FIGURES_DIR, SVR_MODELS_DIR
from src.data_loader import load_csv, load_json
from src.ui_components import page_header, purpose_box, show_dataframe, show_image

page_header("8. SVR Training", "Pipeline, feature sets, candidate registry, chronological tuning, and final selection.")
purpose_box("This page shows how the final RBF-SVR model was selected using validation evidence only, before held-out test evaluation.")

tabs = st.tabs(["Pipeline", "Feature sets", "Candidates", "Validation summary", "Ridge benchmark", "Selected SVR", "Artifacts", "Figures"])
with tabs[0]: show_dataframe(load_csv(CHECKS_DIR / "svr_pipeline_readiness.csv"), height=360)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "feature_set_registry.csv"), height=460)
with tabs[2]:
    show_dataframe(load_csv(TABLES_DIR / "svr_candidate_registry.csv"), height=460)
    show_dataframe(load_csv(TABLES_DIR / "svr_candidate_grid_summary.csv"), height=280)
with tabs[3]:
    show_dataframe(load_csv(TABLES_DIR / "svr_validation_summary.csv"), height=460)
    show_dataframe(load_csv(TABLES_DIR / "svr_fold_metric_variability.csv"), height=300)
with tabs[4]:
    show_dataframe(load_csv(TABLES_DIR / "ridge_benchmark_metrics.csv"), height=360)
    show_dataframe(load_csv(TABLES_DIR / "ridge_best_params.csv"), height=260)
with tabs[5]:
    show_dataframe(load_csv(TABLES_DIR / "final_selected_svr_config.csv"), height=460)
    show_dataframe(load_csv(CHECKS_DIR / "final_svr_training_audit.csv"), height=300)
with tabs[6]:
    params = load_json(ARTIFACTS_DIR / "best_svr_params.json")
    st.json(params)
    st.write("Model file exists:", (SVR_MODELS_DIR / "final_selected_svr_pipeline.joblib").exists())
with tabs[7]:
    for name in ["svr_validation_mae_by_feature_set.png", "svr_validation_rmse_by_feature_set.png", "svr_validation_r2_by_feature_set.png", "feature_set_validation_metric_panel.png", "svr_candidate_grid_summary.png", "svr_top_candidate_validation_mae.png", "selected_svr_vs_top_candidates.png", "svr_fold_metric_variability.png", "ridge_validation_alpha_comparison.png"]:
        show_image(SVR_FIGURES_DIR / name)
