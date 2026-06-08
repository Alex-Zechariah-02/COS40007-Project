import streamlit as st
from src.data_loader import load_table, figure_path
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table_with_guide, metric_cards, guided_figure, metric_direction_guide, next_steps, abbreviation_note
from src.summary_builders import build_svr_metric_summary, build_baseline_summary

page_header("SVR Branch: Final Evaluation", "Held-out test performance, baseline comparison, and safe interpretation.")
render_page_intro("svr_final_eval")

metric_cards(build_svr_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()

tab_metrics, tab_baselines, tab_predictions, tab_figures = st.tabs(["Metrics", "Baselines", "Predictions", "Figures"])

with tab_metrics:
    metric_direction_guide()
    df = load_table("final_svr_metrics.csv")
    if not df.empty:
        show_table_with_guide(df, "final_svr_metrics.csv", "Final SVR metrics", max_rows=10)

with tab_baselines:
    base = build_baseline_summary()
    if not base.empty:
        st.markdown("### Baseline comparison conclusion")
        st.dataframe(base, width="stretch", hide_index=True)
    for fname, title in [("baseline_vs_svr_summary.csv", "Baseline versus SVR summary"), ("expanded_model_comparison_metrics.csv", "Expanded model and baseline comparison"), ("expanded_baseline_vs_svr_delta.csv", "SVR improvement over baselines")]:
        df = load_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=15)

with tab_predictions:
    df = load_table("test_predictions.csv")
    if not df.empty:
        show_table_with_guide(df, "test_predictions.csv", "Held-out test predictions", max_rows=20)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual completion rates against SVR predictions.", "Points closer to the diagonal line have smaller errors.", "Closer to the diagonal is better.", "Shows broad fit and visible misses."),
        ("actual_vs_predicted_with_error_bands.png", "Actual versus predicted with ±2 pp band", "Shows whether predictions fall inside a practical error band.", "Points inside the band are closer to actual values.", "More points inside the band is better.", "Helps translate error into practical tolerance language."),
        ("expanded_mae_comparison.png", "MAE comparison", "Compares Mean Absolute Error across SVR and baselines.", "Lower bars are better.", "Lower is better.", "SVR improves average absolute error versus tested baselines."),
        ("expanded_rmse_comparison.png", "RMSE comparison", "Compares Root Mean Squared Error across SVR and baselines.", "Lower bars are better.", "Lower is better.", "SVR also improves large-error penalty compared with tested baselines."),
        ("expanded_model_metric_heatmap.png", "Metric heatmap", "Compares models/baselines across several metrics.", "Use metric directions: lower error is better; higher R² is better.", "Depends on metric column.", "Shows mixed performance: error improves, R² remains weak."),
        ("svr_improvement_over_baselines.png", "Improvement over baselines", "Shows how much SVR improves over baseline errors.", "Positive values indicate improvement.", "Higher positive improvement is better.", "SVR adds value over simple baseline rules on MAE/RMSE."),
    ]:
        guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "This is held-out test evidence for SVR only. Open the comparison section for SVR versus RF evidence.")

render_page_discussion("svr_final_eval")
next_steps(["Open 5. Error Diagnostics to inspect bias, tolerance coverage, and grouped errors."])
