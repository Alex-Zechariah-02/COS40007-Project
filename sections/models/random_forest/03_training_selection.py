import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, guided_figure, next_steps
from src.data_loader import load_rf_table, load_rf_artifact_json, rf_figure_path
from src.rf_summary_builders import build_rf_config_summary, build_rf_validation_issue_summary

page_header("Random Forest Branch: Training and Selection", "Chronological validation, candidate selection, and tuning limitations.")
render_page_intro("rf_training")

tab_selected, tab_validation, tab_fit, tab_figures = st.tabs(["Selected candidate", "Validation", "Fit status", "Figures"])

with tab_selected:
    cfg = build_rf_config_summary()
    if not cfg.empty:
        st.markdown("### Selected RF candidate")
        st.dataframe(cfg, width="stretch", hide_index=True)
    params = load_rf_artifact_json("best_rf_params.json")
    if params:
        st.markdown("### Best-parameter artifact")
        st.json(params)
    else:
        st.info("Best RF parameter artifact is not available.")

with tab_validation:
    for fname, title in [("chronological_validation_folds.csv", "Chronological validation folds"), ("rf_validation_summary.csv", "RF validation summary"), ("rf_validation_results.csv", "RF fold-level validation results"), ("rf_fold_metric_variability.csv", "Fold metric variability")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=20)

with tab_fit:
    fit = build_rf_validation_issue_summary()
    if not fit.empty:
        st.dataframe(fit, width="stretch", hide_index=True)
        st.warning("The selected RF is valid among successful candidates, but failed fit rows mean the intended grid was not fully evaluated.")

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("rf_validation_mae_by_feature_set.png", "Validation MAE by feature set", "Compares RF feature sets during validation.", "Lower validation MAE is better.", "Lower is better.", "The selected feature set had the best validation MAE among successful candidates."),
        ("feature_set_validation_metric_panel.png", "Feature-set validation panel", "Shows validation metrics across feature sets.", "Use metric direction guide: lower errors are better; higher R² is better.", "Depends on metric.", "Feature-set comparison supports the selected RF branch configuration."),
        ("rf_fold_metric_variability.png", "Fold metric variability", "Shows validation variability across folds.", "Lower variation indicates more stable validation behaviour.", "Lower variability is generally better.", "The fold-level view helps avoid relying on only one validation year."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Missing figure means it was not exported by the notebook under this filename.")

render_page_discussion("rf_training")
next_steps(["Open 4. Final Evaluation to see held-out test performance."])
