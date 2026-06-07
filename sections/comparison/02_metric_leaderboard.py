import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, metric_cards, abbreviation_note, metric_direction_guide, show_table_with_guide, guided_figure, next_steps
from src.comparison_output_builders import build_comparison_metric_cards, load_supervised_model_leaderboard, load_combined_final_metrics, load_final_model_selection
from src.data_loader import comparison_figure_path, load_comparison_table

page_header("Supervised Model Comparison: Metric Leaderboard", "Official held-out metric comparison from the comparison notebook outputs.")
render_page_intro("comparison_metrics")

st.markdown("### Selected model metric cards")
metric_cards(build_comparison_metric_cards(), columns=4, help_map={
    "Selected model": "Model selected by the comparison notebook.",
    "Best MAE": "Lower Mean Absolute Error is better.",
    "Best RMSE": "Lower Root Mean Squared Error is better.",
    "Best R²": "Higher R² is better, but both models remain negative here.",
})
abbreviation_note()
metric_direction_guide()

leader = load_supervised_model_leaderboard()
if not leader.empty:
    show_table_with_guide(leader, "supervised_model_leaderboard.csv", "Official supervised model leaderboard", max_rows=10)

metrics = load_combined_final_metrics()
if not metrics.empty:
    show_table_with_guide(metrics, "combined_final_metrics.csv", "Combined final metrics", max_rows=10)

baseline = load_comparison_table("model_vs_baseline_improvement.csv")
if not baseline.empty:
    show_table_with_guide(baseline, "model_vs_baseline_improvement.csv", "Model versus baseline improvement", max_rows=20)

st.markdown("### Official comparison figures")
for fig, title in [
    ("model_metric_leaderboard.png", "Model metric leaderboard"),
    ("model_metric_leaderboard_mae.png", "MAE leaderboard"),
    ("model_metric_leaderboard_rmse.png", "RMSE leaderboard"),
    ("baseline_mae_improvement_comparison.png", "Baseline MAE improvement comparison"),
]:
    from src.figure_explanations import explain
    e = explain(fig)
    guided_figure(comparison_figure_path(fig), title, e["purpose"], e["how"], e["better"], e["takeaway"], e.get("caveat"))

selection = load_final_model_selection()
if not selection.empty:
    show_table_with_guide(selection, "final_model_selection.csv", "Final model selection", max_rows=1)

render_page_discussion("comparison_metrics")
next_steps(["Open 3. Prediction Comparison to inspect row-level wins and disagreements."])
