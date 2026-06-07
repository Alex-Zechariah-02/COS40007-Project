import streamlit as st
from src.data_loader import load_table, load_check, load_artifact_json, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, show_detail_table, metric_cards, guided_figure, next_steps, abbreviation_note
from src.summary_builders import build_svr_config_summary

page_header("SVR Branch: Training and Selection", "Chronological validation, hyperparameter selection, Ridge benchmark, and final SVR fitting.")
render_page_intro("svr_training")

cfg = build_svr_config_summary()
if not cfg.empty:
    st.markdown("### Selected SVR candidate")
    st.dataframe(cfg, width="stretch", hide_index=True)

params = load_artifact_json("best_svr_params.json")
if params:
    st.markdown("### Best-parameter artifact")
    st.json(params)

st.markdown("### Validation and tuning evidence")
for fname, title in [
    ("svr_validation_summary.csv", "SVR validation summary"),
    ("svr_validation_results.csv", "SVR validation results"),
    ("svr_tuning_audit.csv", "SVR tuning audit"),
    ("svr_fold_metric_variability.csv", "Fold metric variability"),
    ("ridge_benchmark_metrics.csv", "Ridge benchmark metrics"),
    ("final_svr_training_audit.csv", "Final SVR training audit"),
]:
    df = load_table(fname)
    if df.empty:
        df = load_check(fname)
    if not df.empty:
        show_table(df, title, max_rows=15)

st.markdown("### Training and selection visuals")
for fig, title, purpose, how, better, takeaway in [
    ("svr_validation_mae_by_feature_set.png", "Validation MAE by feature set", "Compares validation MAE across tested feature sets.", "Lower bars/points are better.", "Lower is better.", "Feature-set selection used validation error, not held-out test error."),
    ("selected_svr_vs_top_candidates.png", "Selected SVR versus top candidates", "Shows the selected candidate against strong alternatives.", "Compare validation metrics across candidates.", "Lower MAE/RMSE and higher R² are better.", "The selected candidate is traceable to validation evidence."),
    ("svr_fold_metric_variability.png", "Fold variability", "Shows how validation performance varies across chronological folds.", "Large spread means less stable validation performance.", "Lower variability is generally preferred.", "Few annual years make validation variability important."),
    ("ridge_validation_alpha_comparison.png", "Ridge benchmark", "Shows linear benchmark behaviour across alpha values.", "Use it as a simple-model sanity check.", "Lower validation error is better.", "Ridge is a benchmark, not the assigned main model."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Validation figures support selection but do not replace held-out testing.")

render_page_discussion("svr_training")
next_steps(["Open 4. Final Evaluation to inspect held-out test performance."])
