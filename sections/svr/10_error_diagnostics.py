import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, metric_row
from src.formatting import fmt_num

page_header("10. Error Diagnostics", "Residuals, tolerance coverage, grouped errors, and worst predictions.")
purpose_box("This page explains practical model behaviour beyond MAE/RMSE/R², including bias direction, tolerance coverage, and groups with higher error.")
resid = load_csv(TABLES_DIR / "residual_summary.csv")
if not resid.empty:
    r = resid.iloc[0]
    metric_row([
        ("Mean residual", fmt_num(r.get("Mean Residual"), 3), "Residual = actual minus predicted"),
        ("Underprediction %", fmt_num(r.get("Underprediction Percentage"), 1) + "%", None),
        ("Overprediction %", fmt_num(r.get("Overprediction Percentage"), 1) + "%", None),
        ("Within ±2pp", fmt_num(r.get("Within 2 Percentage Points"), 1) + "%", None),
    ])

tabs = st.tabs(["Residual summary", "Tolerance", "State", "Stage", "Sex", "Detailed groups", "Worst rows", "Figures"])
with tabs[0]: show_dataframe(resid, height=260)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "svr_tolerance_summary.csv"), height=260)
with tabs[2]: show_dataframe(load_csv(TABLES_DIR / "error_by_state.csv"), height=420)
with tabs[3]: show_dataframe(load_csv(TABLES_DIR / "error_by_stage.csv"), height=360)
with tabs[4]: show_dataframe(load_csv(TABLES_DIR / "error_by_sex.csv"), height=300)
with tabs[5]: show_dataframe(load_csv(TABLES_DIR / "error_by_state_stage_sex.csv"), height=460)
with tabs[6]: show_dataframe(load_csv(TABLES_DIR / "worst_prediction_rows.csv"), height=420)
with tabs[7]:
    for name in ["residual_distribution.png", "residuals_vs_predicted.png", "underprediction_overprediction_bar.png", "svr_tolerance_coverage.png", "model_tolerance_coverage_comparison.png", "error_by_state.png", "error_by_stage.png", "error_by_sex.png", "state_mae_ranked_bar.png", "state_rmse_ranked_bar.png", "state_within_2pp_rate_bar.png", "state_stage_mae_heatmap.png", "state_stage_rmse_heatmap.png", "state_sex_mae_heatmap.png", "sex_stage_mae_heatmap.png", "worst_prediction_errors.png", "prediction_error_lollipop_top_errors.png"]:
        show_image(SVR_FIGURES_DIR / name)
