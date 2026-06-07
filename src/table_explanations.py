DEFAULT_TABLE_EXPLANATION = {
    "how": "Read the column names first, then use the page discussion to connect the values to the supervised-regression workflow.",
    "better": "Depends on the table. For error metrics, lower is better; for coverage rates and pass statuses, higher/pass is better.",
    "takeaway": "Use this table as supporting evidence for the page interpretation.",
    "caveat": "Detailed tables are evidence records. Do not overinterpret individual rows without the page context.",
}

TABLE_EXPLANATIONS = {
    "raw_dataset_inventory.csv": {
        "how": "Each row is one raw CSV source. Use row count, column count, and filename to verify the data source inventory.",
        "better": "There is no model-performance direction; this is an audit table.",
        "takeaway": "The supervised workflow starts from the expected raw datasets before modelling.",
        "caveat": "Large row count does not automatically mean better model quality; merge compatibility and leakage control still matter.",
    },
    "final_feature_registry.csv": {
        "how": "Each row is a candidate or selected feature with its group, kind, and missingness profile.",
        "better": "Lower missingness is easier to model; valid feature kind and leakage-safe status matter more than raw feature count.",
        "takeaway": "The feature registry documents what predictors enter the supervised-regression workflow.",
        "caveat": "A feature being available does not prove causal importance.",
    },
    "leakage_audit.csv": {
        "how": "Each checked item is marked according to whether it is allowed, excluded, or controlled.",
        "better": "Allowed or pass statuses are expected for legitimate predictors; forbidden future-target fields must not be used.",
        "takeaway": "The modelling panel is designed to avoid future-year and target leakage.",
        "caveat": "Leakage control protects evaluation validity; it does not guarantee high predictive performance.",
    },
    "split_integrity_check.csv": {
        "how": "Read the check, value, and status columns to verify train/test/forecast split construction.",
        "better": "Pass status is required. Test rows must remain unseen during tuning.",
        "takeaway": "The workflow uses a chronological held-out test design instead of random row mixing.",
        "caveat": "Few annual years still limit generalisation confidence.",
    },
    "final_svr_metrics.csv": {
        "how": "This table summarises the selected SVR configuration and held-out test metrics.",
        "better": "Lower MAE, RMSE, and Median AE are better. Higher R² is better.",
        "takeaway": "The selected SVR achieved interpretable percentage-point errors but negative held-out R².",
        "caveat": "Do not judge the model without baseline comparison and residual diagnostics.",
    },
    "baseline_vs_svr_summary.csv": {
        "how": "Use the Boolean columns to see whether SVR beats the core baselines on MAE and RMSE.",
        "better": "True/pass on baseline improvement is better, but positive R² is also important.",
        "takeaway": "SVR improves MAE/RMSE versus tested baselines, but R² remains negative.",
        "caveat": "Improving error metrics does not make the model high-confidence forecasting.",
    },
    "residual_summary.csv": {
        "how": "Residual = actual minus predicted. Positive residuals mean underprediction; negative residuals mean overprediction.",
        "better": "Mean residual closer to 0 and higher tolerance coverage are better.",
        "takeaway": "The selected SVR has underprediction bias on the held-out rows.",
        "caveat": "Residual diagnostics are descriptive and should be read with row-level errors.",
    },
    "svr_metric_card_summary.csv": {
        "how": "This table condenses final SVR metrics, residual behaviour, practical tolerance coverage, and maximum error.",
        "better": "Lower error values are better; higher within-tolerance percentages are better; mean residual should be close to 0.",
        "takeaway": "Most held-out predictions are within ±5 percentage points, but underprediction bias remains.",
        "caveat": "Tolerance coverage is not a confidence interval.",
    },
    "error_by_state.csv": {
        "how": "Each state row summarises held-out prediction errors for that state.",
        "better": "Lower MAE/RMSE and higher within-tolerance percentage are better.",
        "takeaway": "State-level grouped errors identify where predictions were harder or easier.",
        "caveat": "Each state has limited test rows, so do not overgeneralise from one year.",
    },
    "error_by_stage.csv": {
        "how": "Compare MAE/RMSE across education stages.",
        "better": "Lower MAE/RMSE is better.",
        "takeaway": "Stage-level error helps show whether primary, lower-secondary, or upper-secondary rows are harder to predict.",
        "caveat": "Stage differences should be interpreted with row count and target distribution.",
    },
    "error_by_sex.csv": {
        "how": "Compare male and female held-out rows using the same error metrics.",
        "better": "Lower MAE/RMSE and higher within-tolerance percentage are better.",
        "takeaway": "Sex-level error checks whether model error differs between male and female rows.",
        "caveat": "This is an evaluation diagnostic, not a causal sex-effect analysis.",
    },
    "permutation_importance.csv": {
        "how": "Larger importance means shuffling that feature changed held-out prediction error more strongly.",
        "better": "No universal better direction; this is model interpretation, not performance ranking.",
        "takeaway": "Permutation importance shows which predictors the selected SVR is sensitive to.",
        "caveat": "It is not causal evidence and can be affected by correlated features.",
    },
    "final_ai_demonstrator.csv": {
        "how": "Read the representative state-stage-sex row, then compare current completion, predicted next-year completion, actual next-year completion, residual, and absolute error.",
        "better": "Smaller absolute error is better. Residual near 0 means closer prediction.",
        "takeaway": "This row demonstrates how the model output should be explained to a user.",
        "caveat": "One representative row is an example, not the whole model result.",
    },
    "final_output_check.csv": {
        "how": "Each check reports whether a required output or directory condition passed.",
        "better": "Pass status is required for completed evidence.",
        "takeaway": "The output evidence package is complete when checks pass and required files are present.",
        "caveat": "Output completeness does not prove model accuracy; it proves evidence availability.",
    },
}

def explain_table(filename: str) -> dict:
    return TABLE_EXPLANATIONS.get(filename, DEFAULT_TABLE_EXPLANATION)

TABLE_EXPLANATIONS.update({
    "supervised_model_leaderboard.csv": {
        "how": "Ranks the supervised models using held-out regression metrics.",
        "better": "Lower MAE, RMSE, and Median AE are better; higher R² is better.",
        "takeaway": "SVR ranks first on the current held-out comparison.",
        "caveat": "Negative R² means the selected model should not be described as highly accurate.",
    },
    "combined_final_metrics.csv": {
        "how": "Shows final held-out metrics for SVR and RandomForestRegressor side by side.",
        "better": "Lower error metrics are better; higher R² is better.",
        "takeaway": "SVR has lower error than RandomForestRegressor.",
        "caveat": "Both rows must be interpreted using the same held-out test set.",
    },
    "row_level_prediction_comparison.csv": {
        "how": "Each row compares SVR and RF predictions for the same state-stage-sex-year held-out target.",
        "better": "Lower absolute error is better for each row.",
        "takeaway": "SVR wins most row-level comparisons.",
        "caveat": "A row-level win does not replace aggregate and grouped evaluation.",
    },
    "row_level_winner_summary.csv": {
        "how": "Counts how many held-out rows each model predicted more accurately.",
        "better": "More row wins is better.",
        "takeaway": "SVR wins 74 of 96 held-out rows.",
        "caveat": "Ties, if any, should be interpreted separately.",
    },
    "largest_model_disagreement_rows.csv": {
        "how": "Lists rows where the two models differ most in absolute error.",
        "better": "A larger RF minus SVR error difference favours SVR for that row.",
        "takeaway": "Large disagreements highlight where model selection matters most.",
        "caveat": "Disagreement is diagnostic and does not imply causality.",
    },
    "model_vs_baseline_improvement.csv": {
        "how": "Compares each model's held-out metrics against saved baseline methods.",
        "better": "Positive error improvement means the model has lower error than the baseline.",
        "takeaway": "SVR beats all compared baselines, while RF does not beat the strongest baseline set.",
        "caveat": "Baseline availability differs by branch and must be read from the table.",
    },
    "tolerance_comparison.csv": {
        "how": "Shows how many predictions fall within practical percentage-point error bands.",
        "better": "Higher percentages are better.",
        "takeaway": "SVR has higher tolerance coverage than RF at all displayed bands.",
        "caveat": "Tolerance bands are descriptive thresholds, not confidence intervals.",
    },
    "residual_bias_comparison.csv": {
        "how": "Compares mean residual, median residual, and underprediction or overprediction rate.",
        "better": "Mean residual closer to zero is better; lower systematic bias is better.",
        "takeaway": "Both models underpredict, but RF underpredicts more strongly.",
        "caveat": "Residual bias should be interpreted together with absolute error metrics.",
    },
    "error_comparison_by_state.csv": {
        "how": "Compares model error by state.",
        "better": "Lower MAE and RMSE are better.",
        "takeaway": "SVR has lower MAE in most states.",
        "caveat": "State-level results are from one held-out input year.",
    },
    "error_comparison_by_stage.csv": {
        "how": "Compares model error by school stage.",
        "better": "Lower MAE and RMSE are better.",
        "takeaway": "SVR performs better than RF across all stages.",
        "caveat": "Stage-level patterns should not be interpreted causally.",
    },
    "error_comparison_by_sex.csv": {
        "how": "Compares model error by sex group.",
        "better": "Lower MAE and RMSE are better.",
        "takeaway": "SVR performs better than RF for both sex groups.",
        "caveat": "This is an evaluation subgroup, not a causal sex-effect analysis.",
    },
    "feature_influence_comparison.csv": {
        "how": "Combines feature influence outputs from the two model branches.",
        "better": "Importance is not a performance score; use it to understand model sensitivity.",
        "takeaway": "Completion-history signals are important for both models.",
        "caveat": "Feature influence is diagnostic only and not causal evidence.",
    },
    "top_feature_influence_comparison.csv": {
        "how": "Shows top-ranked feature influence values by model and source type.",
        "better": "Higher importance means stronger diagnostic influence for that fitted model.",
        "takeaway": "Both models rely on recent completion-history information.",
        "caveat": "Native RF importance and permutation importance are not directly identical methods.",
    },
    "combined_ai_demonstrator.csv": {
        "how": "Shows one common held-out row with actual target, SVR prediction, RF prediction, absolute errors, and winner.",
        "better": "Lower absolute error is better.",
        "takeaway": "SVR wins the selected demonstrator row.",
        "caveat": "This is one example and should be read alongside the full held-out comparison.",
    },
    "forecast_preview_model_comparison.csv": {
        "how": "Compares SVR and RF forecast-candidate predictions for input year 2022 predicting target year 2023.",
        "better": "No model can be scored here because actual 2023 targets are unavailable.",
        "takeaway": "The table shows prediction differences only, not evaluation performance.",
        "caveat": "Forecast preview must not be used for final model selection.",
    },
    "comparison_validity_summary.csv": {
        "how": "Lists the checks that make the SVR and RF comparison valid.",
        "better": "All checks should pass.",
        "takeaway": "The current comparison is valid because row and target checks pass.",
        "caveat": "If any validity check fails, model ranking should not be trusted.",
    },
    "comparison_output_check.csv": {
        "how": "Checks whether expected comparison output files exist.",
        "better": "Every expected output should exist.",
        "takeaway": "The comparison output package is complete when no expected outputs are missing.",
        "caveat": "File existence does not itself prove model quality.",
    },
})
