import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import build_comparison_metric_cards, load_supervised_model_leaderboard, load_combined_final_metrics, load_final_model_selection
from src.data_loader import comparison_figure_path, load_comparison_table
from src.figure_explanations import explain

page_header("Supervised Model Comparison: Metric Leaderboard", "Official held-out metric comparison from the comparison notebook outputs.")
render_page_intro("comparison_metrics")

metric_cards(build_comparison_metric_cards(), columns=4, help_map={
    "Best MAE": "Lower Mean Absolute Error is better.",
    "Best RMSE": "Lower Root Mean Squared Error is better.",
    "Best R²": "Higher R² is better, but both models remain negative here.",
    "Best Median AE": "Lower Median Absolute Error is better.",
})
abbreviation_note()

tab_leader, tab_definitions, tab_figures, tab_details = st.tabs(["Leaderboard", "Metric definitions", "Figures", "Detailed tables"])

with tab_leader:
    leader = load_supervised_model_leaderboard()
    if not leader.empty:
        show_table_with_guide(leader, "supervised_model_leaderboard.csv", "Official supervised model leaderboard", max_rows=10)
    selection = load_final_model_selection()
    if not selection.empty:
        show_table_with_guide(selection, "final_model_selection.csv", "Final model selection", max_rows=1)

with tab_definitions:
    metric_direction_guide()

with tab_figures:
    for fig, title in [("model_metric_leaderboard.png", "Model metric leaderboard"), ("model_metric_leaderboard_mae.png", "MAE leaderboard"), ("model_metric_leaderboard_rmse.png", "RMSE leaderboard"), ("baseline_mae_improvement_comparison.png", "Baseline MAE improvement comparison")]:
        e = explain(fig)
        guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

with tab_details:
    for df, fname, title in [(load_combined_final_metrics(), "combined_final_metrics.csv", "Combined final metrics"), (load_comparison_table("model_vs_baseline_improvement.csv"), "model_vs_baseline_improvement.csv", "Model versus baseline improvement")]:
        if not df.empty:
            show_table_with_guide(df, fname, title, max_rows=25)

render_page_discussion("comparison_metrics")
next_steps(["Open 3. Prediction Comparison to inspect row-level wins and disagreements."])
