import pandas as pd
import streamlit as st

from src.ui_components import (
    page_header,
    render_page_intro,
    render_page_discussion,
    metric_cards,
    abbreviation_note,
    show_table_with_guide,
    guided_figure,
    next_steps,
)
from src.comparison_output_builders import (
    build_comparison_overview_cards,
    build_comparison_error_summary_cards,
    build_grouped_comparison_summary,
    build_ai_demo_cards,
    build_forecast_cards,
    load_comparison_validity_summary,
    load_supervised_model_leaderboard,
    build_comparison_metric_decision_table,
    format_metric_decision_table,
    load_row_level_winner_summary,
    load_tolerance_comparison,
    load_residual_bias_comparison,
    load_grouped_error_comparison,
    load_feature_influence_comparison,
    load_top_feature_influence_comparison,
    load_forecast_preview_comparison,
    load_ai_demonstrator_comparison,
    load_final_model_selection,
)
from src.data_loader import comparison_figure_path
from src.figure_explanations import explain


page_header(
    "Supervised Model Comparison: Overview",
    "Executive summary of the official SVR versus RandomForestRegressor comparison.",
)
render_page_intro("comparison_overview")

st.markdown("### Official comparison summary")
metric_cards(
    build_comparison_overview_cards(),
    columns=5,
    help_map={
        "Selected model": "Model selected using held-out comparison metrics.",
        "Compared rows": "Matched held-out rows used for both models.",
        "Validity checks": "Comparison checks passed in the comparison notebook.",
        "SVR row wins": "Rows where SVR had lower absolute error.",
        "RF row wins": "Rows where RF had lower absolute error.",
    },
)

st.markdown("### Final model decision")
decision_table = build_comparison_metric_decision_table()
if not decision_table.empty:
    st.dataframe(format_metric_decision_table(decision_table), width="stretch", hide_index=True)
    st.info(
        "Support Vector Regression is selected because it has lower MAE, lower RMSE, "
        "better R², lower Median Absolute Error, and more row-level wins than "
        "RandomForestRegressor. Both models still have negative R², so the result should be "
        "read as selecting the stronger tested model rather than proving high forecasting accuracy."
    )
abbreviation_note()

st.markdown("### Comparison validity")
validity = load_comparison_validity_summary()
if not validity.empty:
    show_table_with_guide(validity, "comparison_validity_summary.csv", "Validity checks", max_rows=20)

st.markdown("### Metric leaderboard summary")
leader = load_supervised_model_leaderboard()
if not leader.empty:
    show_table_with_guide(leader, "supervised_model_leaderboard.csv", "Official model leaderboard", max_rows=10)
    e = explain("model_metric_leaderboard.png")
    guided_figure(
        comparison_figure_path("model_metric_leaderboard.png"),
        "Model metric leaderboard",
        e["purpose"],
        e["how"],
        e["better"],
        e["takeaway"],
        e.get("caveat"),
    )

st.markdown("### Row-level prediction summary")
wins = load_row_level_winner_summary()
if not wins.empty:
    show_table_with_guide(wins, "row_level_winner_summary.csv", "Row-level winner summary", max_rows=10)
    e = explain("row_level_winner_summary.png")
    guided_figure(
        comparison_figure_path("row_level_winner_summary.png"),
        "Row-level winner summary",
        e["purpose"],
        e["how"],
        e["better"],
        e["takeaway"],
        e.get("caveat"),
    )

st.markdown("### Practical error summary")
metric_cards(
    build_comparison_error_summary_cards(),
    columns=3,
    help_map={
        "SVR within ±2 pp": "Higher tolerance coverage is better.",
        "RF within ±2 pp": "Higher tolerance coverage is better.",
        "SVR within ±5 pp": "Higher tolerance coverage is better.",
        "RF within ±5 pp": "Higher tolerance coverage is better.",
        "SVR mean residual": "Closer to zero indicates less average bias.",
        "RF mean residual": "Closer to zero indicates less average bias.",
    },
)
error_tabs = st.tabs(["Tolerance", "Residual bias"])
with error_tabs[0]:
    tol = load_tolerance_comparison()
    if not tol.empty:
        show_table_with_guide(tol, "tolerance_comparison.csv", "Tolerance coverage", max_rows=10)
with error_tabs[1]:
    resid = load_residual_bias_comparison()
    if not resid.empty:
        show_table_with_guide(resid, "residual_bias_comparison.csv", "Residual bias comparison", max_rows=10)

st.markdown("### Grouped error summary")
group_summary = build_grouped_comparison_summary()
if not group_summary.empty:
    st.dataframe(group_summary, width="stretch", hide_index=True)
for group, label in [("stage", "Stage"), ("sex", "Sex"), ("state", "State")]:
    df = load_grouped_error_comparison(group)
    if not df.empty:
        with st.expander(f"Detailed error comparison by {label.lower()}"):
            show_table_with_guide(df, f"error_comparison_by_{group}.csv", f"Error comparison by {label.lower()}", max_rows=20)

st.markdown("### Feature influence summary")
feature_tabs = st.tabs(["Top features", "All feature influence"])
with feature_tabs[0]:
    top_features = load_top_feature_influence_comparison()
    if not top_features.empty:
        show_table_with_guide(top_features, "top_feature_influence_comparison.csv", "Top feature influence comparison", max_rows=20)
with feature_tabs[1]:
    feature_table = load_feature_influence_comparison()
    if not feature_table.empty:
        show_table_with_guide(feature_table, "feature_influence_comparison.csv", "Feature influence comparison", max_rows=20)
st.caption("Feature influence is diagnostic model-behaviour evidence. It does not prove causal impact on completion rates.")

st.markdown("### AI demonstrator summary")
metric_cards(
    build_ai_demo_cards(),
    columns=4,
    help_map={
        "Winner": "Model with lower absolute error for the selected held-out row.",
        "Actual": "Actual target completion rate for the selected held-out row.",
        "SVR prediction": "SVR prediction for the same held-out row.",
        "RF prediction": "RandomForestRegressor prediction for the same held-out row.",
    },
)
ai = load_ai_demonstrator_comparison()
if not ai.empty:
    show_table_with_guide(ai, "combined_ai_demonstrator.csv", "Official AI demonstrator row", max_rows=1)

st.markdown("### Forecast preview summary")
metric_cards(
    build_forecast_cards(),
    columns=4,
    help_map={
        "Forecast rows": "Matched 2022 to 2023 forecast-candidate rows.",
        "SVR mean preview": "Mean SVR forecast preview prediction.",
        "RF mean preview": "Mean RF forecast preview prediction.",
        "Mean model difference": "Mean absolute difference between SVR and RF forecast preview predictions.",
    },
)
forecast = load_forecast_preview_comparison()
if not forecast.empty:
    st.warning("Forecast preview rows are non-evaluable because actual 2023 targets are unavailable. They are not used for final model selection.")
    show_table_with_guide(forecast, "forecast_preview_model_comparison.csv", "Forecast preview comparison", max_rows=10)

selection = load_final_model_selection()
if not selection.empty:
    st.markdown("### Final selection table")
    show_table_with_guide(selection, "final_model_selection.csv", "Final model selection", max_rows=1)

render_page_discussion("comparison_overview")
next_steps([
    "Open 2. Metric Leaderboard for the full metric and baseline comparison.",
    "Open 3. Prediction Comparison for row-level wins and disagreement rows.",
    "Open 4. Error Comparison for tolerance, residual, and grouped-error evidence.",
    "Open 6. AI Demonstrator Comparison for the same-row prediction example.",
])
