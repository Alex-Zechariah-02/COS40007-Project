import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.rf_summary_builders import build_rf_metric_summary, build_rf_baseline_summary
from src.data_loader import load_rf_table, rf_figure_path

page_header("Random Forest Branch: Final Evaluation", "Held-out test performance, baseline comparison, and RF interpretation.")
render_page_intro("rf_final_eval")

metric_cards(build_rf_metric_summary(), columns=4, help_map={
    "MAE": "Mean Absolute Error. Lower is better.",
    "RMSE": "Root Mean Squared Error. Lower is better.",
    "R²": "R-squared. Higher is better; negative indicates weak held-out explanatory power.",
    "Median AE": "Median Absolute Error. Lower is better.",
})
abbreviation_note()

tab_metrics, tab_baselines, tab_predictions, tab_figures = st.tabs(["Metrics", "Baselines", "Predictions", "Figures"])

with tab_metrics:
    metric_direction_guide()
    df = load_rf_table("final_rf_metrics.csv")
    if not df.empty:
        show_table_with_guide(df, "final_rf_metrics.csv", "Final RF metrics", max_rows=10)

with tab_baselines:
    base = build_rf_baseline_summary()
    if not base.empty:
        st.markdown("### Baseline comparison conclusion")
        st.dataframe(base, width="stretch", hide_index=True)
    st.info("The RF branch is valid as the second supervised-regression model branch, but the current held-out result does not support selecting RF as the best model because it does not beat the strongest simple baselines by MAE.")
    for fname, title in [("expanded_model_comparison_metrics.csv", "RF versus baselines summary"), ("expanded_baseline_vs_rf_delta.csv", "RF improvement over baselines"), ("rf_vs_svr_comparison.csv", "Direct RF versus SVR metric comparison")]:
        df = load_rf_table(fname)
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=20)

with tab_predictions:
    df = load_rf_table("test_predictions.csv")
    if not df.empty:
        show_table_with_guide(df, "test_predictions.csv", "Held-out RF test predictions", max_rows=20)

with tab_figures:
    for fig, title, purpose, how, better, takeaway in [
        ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual completion rates against RF predictions.", "Points closer to the diagonal line have smaller errors.", "Closer to diagonal is better.", "RF has visible underprediction and larger errors than SVR."),
        ("actual_vs_predicted_with_error_bands.png", "Actual versus predicted with ±2 pp band", "Shows whether predictions fall inside a practical error band.", "Points inside the band are closer to actual values.", "More points inside the band is better.", "RF has lower practical tolerance coverage than SVR."),
        ("expanded_mae_comparison.png", "MAE comparison", "Compares Mean Absolute Error across RF and baselines.", "Lower bars are better.", "Lower is better.", "RF does not beat the strongest simple baselines by MAE."),
        ("expanded_rmse_comparison.png", "RMSE comparison", "Compares large-error-sensitive performance across RF and baselines.", "Lower bars are better.", "Lower is better.", "RF reduces RMSE against some weak baselines but not the strongest baseline set."),
        ("rf_vs_svr_metric_comparison.png", "RF versus SVR comparison", "Compares the two supervised regression branches.", "Lower errors are better; higher R² is better.", "SVR is better on the current output metrics.", "Use the official comparison branch for final SVR-versus-RF evidence."),
    ]:
        guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "This is held-out test evidence from Sam's RF output package.")

render_page_discussion("rf_final_eval")
next_steps(["Open 5. Error Diagnostics to inspect bias, tolerance coverage, and grouped errors."])
