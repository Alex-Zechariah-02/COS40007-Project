import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.rf_summary_builders import build_rf_metric_summary
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Final Evaluation", "Held-out test performance, baseline comparison, and RF interpretation.")
render_page_intro("rf_final_eval")

st.markdown("### Final held-out metrics")
metric_cards(build_rf_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()
metric_direction_guide()

for fname, title in [
    ("final_rf_metrics.csv", "Final RF metrics"),
    ("expanded_model_comparison_metrics.csv", "RF versus baselines leaderboard"),
    ("expanded_baseline_vs_rf_delta.csv", "RF improvement over compared models"),
    ("rf_vs_svr_comparison.csv", "Direct RF versus SVR metric comparison"),
    ("test_predictions.csv", "Held-out RF test predictions"),
]:
    df = load_rf_table(fname)
    if not df.empty:
        show_table_with_guide(df, fname, title, max_rows=12)

st.markdown("### Final evaluation visuals")
for fig, title, purpose, how, better, takeaway in [
    ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual completion rates against RF predictions.", "Points closer to the diagonal line have smaller errors.", "Closer to diagonal is better.", "RF has visible underprediction and larger errors than SVR."),
    ("actual_vs_predicted_with_error_bands.png", "Actual versus predicted with ±2 pp band", "Shows whether predictions fall inside a practical error band.", "Points inside the band are closer to actual values.", "More points inside the band is better.", "RF has lower practical tolerance coverage than SVR."),
    ("expanded_mae_comparison.png", "MAE comparison", "Compares Mean Absolute Error across RF and baselines.", "Lower bars are better.", "Lower is better.", "RF does not beat the strongest simple baselines by MAE."),
    ("rf_vs_svr_metric_comparison.png", "RF versus SVR comparison", "Compares the two supervised regression branches.", "Lower errors are better; higher R² is better.", "SVR is better on the current output metrics.", "Use row-level comparison for detailed case-level evidence."),
]:
    guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "This is held-out test evidence from Sam's RF output package.")

render_page_discussion("rf_final_eval")
next_steps(["Open 5. Error Diagnostics to inspect bias, tolerance coverage, and grouped errors."])
