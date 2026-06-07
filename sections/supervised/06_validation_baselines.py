import streamlit as st
from src.data_loader import load_table, load_check, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, show_table_with_guide, show_detail_table, metric_cards, guided_figure, metric_direction_guide, next_steps

page_header("Supervised Regression System: Validation and Baselines", "Chronological split design and rule-based baseline models for fair supervised-regression evaluation.")
render_page_intro("validation_baselines")

split = load_check("split_integrity_check.csv")
if not split.empty:
    vals = {str(r["Check"]): str(r["Value"]) for _, r in split.iterrows() if "Check" in split.columns and "Value" in split.columns}
    metric_cards({
        "Train rows": vals.get("Train row count", "N/A"),
        "Test rows": vals.get("Test row count", "N/A"),
        "Forecast rows": vals.get("Forecast candidate row count", vals.get("Forecast-candidate row count", "N/A")),
        "Split status": "Pass" if "Pass" in split.get("Status", []).astype(str).tolist() else "Check",
    }, columns=4)
    show_table_with_guide(split, "split_integrity_check.csv", "Split integrity check", max_rows=20)

st.markdown("### Metric direction guide")
metric_direction_guide()

for fname, title in [
    ("chronological_validation_folds.csv", "Chronological validation folds"),
    ("baseline_metrics.csv", "Core baseline metrics"),
    ("additional_rule_baseline_metrics.csv", "Additional rule baseline metrics"),
    ("all_baseline_metrics_pre_svr.csv", "All baseline metrics before SVR"),
]:
    df = load_table(fname)
    if df.empty:
        df = load_check(fname)
    if not df.empty:
        show_table(df, title, max_rows=20)

st.markdown("### Validation and baseline visuals")
for fig, title, purpose, how, better, takeaway in [
    ("chronological_split_timeline.png", "Chronological split timeline", "Shows the time-aware train, validation, held-out test, and forecast-candidate structure.", "Training years occur before validation and held-out test years.", "Later validation/test years should not be used for training or tuning.", "The split avoids future-year leakage for next-year prediction."),
    ("all_baseline_mae_rmse_comparison.png", "Baseline MAE/RMSE comparison", "Compares simple baseline errors before SVR evaluation.", "Lower bars are better for MAE and RMSE.", "Lower is better.", "Baselines define the minimum performance standard."),
    ("all_baseline_r2_comparison.png", "Baseline R² comparison", "Compares baseline R² values.", "Higher values are better; negative values indicate weak held-out explanatory power.", "Higher is better.", "R² should be read with MAE/RMSE and not used alone."),
]:
    guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Baseline visuals support the shared validation context. Open the comparison section for SVR versus RF evidence.")

render_page_discussion("validation_baselines")
next_steps(["Open SVR Branch → 1. Overview for the completed model branch."])
