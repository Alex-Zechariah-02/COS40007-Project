import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, metric_row, discussion
from src.formatting import fmt_num
from src.charts import scatter_actual_pred
from src import notebook_discussions as nd

page_header("9. Final Evaluation", "Held-out test prediction and model comparison.")
purpose_box("This page evaluates the final selected SVR on the held-out 2021 input year predicting 2022 completion rates. The held-out test set was not used for tuning.")
metrics = load_csv(TABLES_DIR / "final_svr_metrics.csv")
if not metrics.empty:
    r = metrics.iloc[0]
    metric_row([
        ("MAE", fmt_num(r.get("MAE"), 3), None),
        ("RMSE", fmt_num(r.get("RMSE"), 3), None),
        ("R²", fmt_num(r.get("R2"), 3), "Negative R² means weak held-out explanatory power"),
        ("Median AE", fmt_num(r.get("Median_AE"), 3), None),
    ])

tabs = st.tabs(["Final metrics", "Predictions", "Model comparison", "Baseline deltas", "Figures"])
with tabs[0]:
    show_dataframe(metrics, height=260)
    show_dataframe(load_csv(CHECKS_DIR / "heldout_evaluation_audit.csv"), height=260)
with tabs[1]:
    preds = load_csv(TABLES_DIR / "test_predictions.csv")
    show_dataframe(preds, height=460)
    fig = scatter_actual_pred(preds, "Actual Next-Year Completion Rate", "Predicted Next-Year Completion Rate", "stage")
    if fig: st.plotly_chart(fig, width="stretch")
with tabs[2]: show_dataframe(load_csv(TABLES_DIR / "expanded_model_comparison_metrics.csv"), height=420)
with tabs[3]: show_dataframe(load_csv(TABLES_DIR / "expanded_baseline_vs_svr_delta.csv"), height=420)
with tabs[4]:
    for name in ["actual_vs_predicted.png", "actual_vs_predicted_with_error_bands.png", "expanded_model_metric_heatmap.png", "expanded_mae_comparison.png", "expanded_rmse_comparison.png", "expanded_r2_comparison.png", "model_rank_by_metric.png", "svr_improvement_over_baselines.png", "svr_metric_card_summary.png"]:
        show_image(SVR_FIGURES_DIR / name)

discussion("Notebook discussion", nd.FINAL_EVALUATION)
