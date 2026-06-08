PAGE_NARRATIVES = {
    "home": {
        "key": "This application presents the supervised-regression workflow for State Completion Rate Prediction. The shared workflow, completed SVR branch, completed RandomForestRegressor branch, and active model comparison are available for review.",
        "answers": "Use this page to understand the app structure, current model status, and the recommended review path.",
        "read": [
            "Start with the Supervised Regression System pages to understand the shared data, target, features, leakage control, validation, and baselines.",
            "Then open the SVR Branch pages to review the completed model design, training, evaluation, diagnostics, demonstrator, and limitations.",
            "The RandomForestRegressor and comparison sections are now available using validated saved outputs.",
        ],
        "discussion": "The app is organised around a shared supervised-regression contract rather than a single-model story. The completed Support Vector Regression and RandomForestRegressor branches are compared using the same target, row unit, split, baselines, and metric contract.",
    },
    "supervised_overview": {
        "key": "The supervised task is regression because the output is a numeric next-year completion-rate value, not a class label.",
        "answers": "This page explains the shared supervised-regression objective and how the completed SVR and RandomForestRegressor branches fit the same modelling task.",
        "read": ["Read the task cards first.", "Then inspect the overview of data, target, feature, leakage, validation, and baseline decisions.", "Use the detailed shared pages for evidence behind each decision."],
        "discussion": "The supervised branch predicts next-year school completion rate. This requires regression metrics such as MAE, RMSE, R², and Median AE. Classification metrics are excluded because no categorical class label is used. The completed SVR and RandomForestRegressor branches are comparable because they follow the same target, row unit, split, baselines, and metric contract.",
    },
    "shared_data_audit": {
        "key": "The workflow starts from nine raw CSV datasets and audits schema, coverage, missing values, duplicates, and dataset role before modelling.",
        "answers": "This page shows what raw datasets exist, how they contribute to the supervised-regression workflow, and what data-quality checks were performed.",
        "read": ["Use the inventory table for source coverage.", "Use the preview selector only for sample raw rows, not full-data inspection.", "Open detailed audit expanders when checking schema, missingness, or duplicate risks."],
        "discussion": "The raw data audit reduces the risk of building a model from unexplained processed data or invalid merge assumptions. It also helps explain why some feature groups need aggregation, imputation, as-of logic, or exclusion from the final model.",
    },
    "target_row_unit": {
        "key": "The main supervised target is next-year completion rate at state-stage-sex-year level using male and female rows. The `both` category is kept separate because it aggregates male and female.",
        "answers": "This page explains the label, Malaysia benchmark, completion gap, target shifting, and row-unit decision.",
        "read": ["Confirm the numeric target first.", "Then check how Malaysia benchmark rows are separated from modelling rows.", "Finally, inspect row-unit validation and the main versus both-only panels."],
        "discussion": "The selected target directly matches State Completion Rate Prediction because it predicts `next_year_completion_rate`. Completion gap from Malaysia remains useful policy context, but the main model output is the numeric completion rate. The state-stage-sex-year row unit preserves state, education stage, sex, and year structure without mixing aggregate `both` rows into sex-specific training rows.",
    },
    "feature_engineering": {
        "key": "The shared feature set combines completion history, education capacity, demographic pressure, household context, and audited socioeconomic features while avoiding future-year information.",
        "answers": "This page explains how predictor groups were built before model-specific training.",
        "read": ["Review the feature group cards to understand the intended signal.", "Check feature tables only if you need detailed columns.", "Use the caveats to distinguish selected final SVR features from prepared but excluded features."],
        "discussion": "Feature engineering was designed to add legitimate predictive signal without inflating metrics through leakage. Completion-history features help capture temporal persistence, education-capacity features describe school system pressure, demographic and household features describe state context, and economic features are only valid when source-year logic prevents future values from entering earlier prediction rows.",
    },
    "panel_leakage": {
        "key": "The supervised panel is valid only if future target values, target-year information, and duplicated district-state targets are excluded from predictors.",
        "answers": "This page shows how the final modelling panel, feature registry, leakage audit, and forecast-candidate separation protect evaluation validity.",
        "read": ["Start with the leakage audit.", "Then inspect feature registry and panel integrity.", "Use forecast-candidate separation to confirm non-evaluable rows are not used for model selection."],
        "discussion": "Leakage control is more important than producing better-looking metrics. Current-year completion history is allowed for next-year prediction, but next-year target values, future socioeconomic data, and duplicated raw district rows against a state target are not valid predictors. The panel and leakage checks provide the credibility base for both SVR and future RandomForestRegressor evaluation.",
    },
    "validation_baselines": {
        "key": "Chronological validation is used because the task predicts a future year. Baselines are mandatory because SVR and RF are only useful if they improve on simple rules.",
        "answers": "This page explains the train, validation, held-out test, forecast-candidate split, and baseline models.",
        "read": ["Check the split timeline first.", "Then inspect baseline definitions and baseline metrics.", "Remember that the held-out test year must not be used for tuning."],
        "discussion": "The validation design uses earlier years for training and later years for validation/testing. This is more defensible than shuffled K-Fold for a next-year prediction task because shuffled splits can train on future years and validate on earlier years. Baselines such as training mean and persistence define the minimum standard that model branches must beat.",
    },
    "svr_overview": {
        "key": "The completed SVR branch implements a full supervised-regression model for next-year completion-rate prediction. It improves MAE and RMSE against tested baselines, but held-out R² is negative, so it should be interpreted as a planning-support prototype rather than a high-confidence forecasting system.",
        "answers": "This page gives the executive overview of the whole SVR branch before the detailed pages.",
        "read": ["Read the branch overview cards first.", "Use performance and diagnostics to understand the result.", "Open detailed pages if you need exact tables, figures, or model settings."],
        "discussion": "The SVR branch is complete and evidence-backed. It uses a leakage-controlled modelling panel, chronological validation, baseline comparison, final held-out evaluation, residual diagnostics, feature influence diagnostics, and a representative AI demonstrator. The safest conclusion is that the branch is methodologically complete and useful for planning-support demonstration, while still limited by small annual data and negative held-out R².",
    },
    "svr_model_design": {
        "key": "The SVR branch uses an RBF-kernel regression pipeline with numeric scaling and categorical encoding for state, stage, and sex.",
        "answers": "This page explains the model design, preprocessing, feature sets, and why SVR needs a pipeline.",
        "read": ["Review the model design cards.", "Check pipeline readiness and feature-set registry.", "Use candidate registry only for detailed tuning evidence."],
        "discussion": "SVR with an RBF kernel can model nonlinear relationships, but it is sensitive to feature scale. Numeric features therefore use imputation and scaling, while categorical identifiers are encoded safely. RandomForestRegressor uses model-specific preprocessing, but both completed branches follow the same target, split, baselines, and metric contract for fair comparison.",
    },
    "svr_training": {
        "key": "The selected SVR was chosen using chronological validation, not held-out test performance.",
        "answers": "This page explains the candidate search, selected feature set, selected hyperparameters, and final training evidence.",
        "read": ["Start with selected candidate and validation metrics.", "Then inspect candidate/fold evidence if needed.", "Do not treat held-out test performance as part of model selection."],
        "discussion": "The final SVR configuration was selected from training-period chronological validation. The selected candidate uses an RBF kernel, standard scaling, C = 1.0, epsilon = 0.1, gamma = 0.01, and the `full_without_economic` feature set. The held-out test set is reserved for final evaluation only.",
    },
    "svr_final_eval": {
        "key": "The selected SVR improves MAE and RMSE against tested baselines, but R² is negative, so the model is useful but limited.",
        "answers": "This page shows final held-out test metrics and baseline comparison.",
        "read": ["Use MAE as the primary error metric.", "Use RMSE to check large misses.", "Use R² as a guardrail against overclaiming.", "Use baseline comparison to decide whether SVR adds value."],
        "discussion": "The final evaluation is performed on held-out input year 2021 predicting target year 2022. MAE and RMSE are interpreted in completion-rate percentage points. The SVR reduces average error relative to tested baselines, but negative R² shows limited held-out explanatory performance. The result should be reported honestly as planning-support evidence, not high-accuracy forecasting.",
    },
    "svr_error_diag": {
        "key": "The SVR has underprediction bias, but most predictions fall within a broad ±5 percentage-point tolerance band.",
        "answers": "This page shows residual direction, tolerance coverage, grouped errors, and worst prediction rows.",
        "read": ["Residual = actual minus predicted.", "Positive residual means underprediction.", "Lower grouped MAE/RMSE is better.", "Higher within-tolerance percentage is better."],
        "discussion": "Error diagnostics translate model performance into practical planning terms. The model tends to underpredict, so actual completion rates are often higher than predicted. Tolerance coverage shows how often predictions are close enough under practical percentage-point thresholds. Grouped errors identify states, stages, or sex groups where model behaviour needs more caution.",
    },
    "svr_visuals": {
        "key": "The visual evidence supports the modelling workflow by showing fit, residuals, grouped errors, baseline comparison, feature influence, and forecast-preview outputs.",
        "answers": "This page lets reviewers inspect the saved visual evidence without scrolling through a notebook.",
        "read": ["Start with featured figures.", "Use the figure guide before interpreting a chart.", "Use the full gallery only when checking detailed evidence."],
        "discussion": "Figures are used as diagnostic and explanatory evidence. They help show prediction fit, error distribution, grouped error differences, baseline comparison, tuning behaviour, and feature influence. A figure is not a standalone conclusion; it should be read with the metric tables and page discussion.",
    },
    "svr_feature_influence": {
        "key": "Permutation importance identifies which features the trained SVR is sensitive to, but it does not prove causal impact.",
        "answers": "This page explains feature influence diagnostics for the selected SVR.",
        "read": ["Higher importance means the model error changed more when the feature was perturbed.", "Use group summaries to understand feature-source influence.", "Do not interpret this as causal ranking."],
        "discussion": "Permutation importance is useful for explaining model behaviour after evaluation. It helps identify which features mattered to the trained SVR, but correlated features and small held-out data can affect the ranking. These results should support interpretation, not causal claims.",
    },
    "svr_ai_demo": {
        "key": "The AI demonstrator shows how one held-out prediction should be read: selected row, current completion, predicted next-year completion, actual next-year completion, residual, and absolute error.",
        "answers": "This page demonstrates the user-facing interpretation of a model prediction.",
        "read": ["Compare prediction with actual target when available.", "Use residual sign meaning to identify overprediction or underprediction.", "Treat forecast preview rows as non-evaluable if actual targets are unavailable."],
        "discussion": "The demonstrator turns the model result into a practical example. It shows the input year, target year, selected state-stage-sex row, predicted value, actual target, residual, and absolute error. Forecast-candidate rows are preview-only and must not be used as final evaluation evidence.",
    },
    "svr_output_check": {
        "key": "The saved output package contains the required tables, figures, model artifact, and best-parameter artifact for the completed SVR branch.",
        "answers": "This page verifies output completeness and evidence availability.",
        "read": ["Check the output summary first.", "Then verify model artifact and best-parameter JSON.", "Use detailed expanders only when checking exact file lists."],
        "discussion": "Output completeness shows that the branch has saved evidence for review: audit files, tables, figures, model artifact, and parameter metadata. This does not prove model accuracy by itself; it proves that the modelling evidence package is complete and available for inspection.",
    },
    "svr_limitations": {
        "key": "The SVR branch is methodologically complete but should be interpreted as a planning-support prototype, not a production forecasting system.",
        "answers": "This page states what the completed SVR branch can and cannot support.",
        "read": ["Separate supported uses from unsupported claims.", "Read negative R² and underprediction bias as limitations.", "Use the final wording to avoid overclaiming."],
        "discussion": "The main limitations are small annual data, negative held-out R², underprediction bias, non-causal design, and non-evaluable forecast-preview rows. The branch is still useful because it demonstrates a complete supervised-regression workflow with transparent evidence and a clear path for RandomForestRegressor comparison.",
    },
    "rf_pending": {
        "key": "The RandomForestRegressor branch is reserved for a second supervised-regression model and will only be enabled after validated RF outputs match the shared target, split, baselines, and metric contract.",
        "answers": "This page defines what the RF teammate must provide before comparison is valid.",
        "read": ["Check required files.", "Check required columns.", "Do not compare models until alignment checks pass."],
        "discussion": "The RF branch is intentionally pending. This avoids fabricating results and protects the fairness of the final supervised model comparison.",
    },
    "comparison_pending": {
        "key": "The final SVR versus RandomForestRegressor comparison is intentionally pending until both branches have validated outputs on the same held-out rows.",
        "answers": "This page explains the future comparison contract.",
        "read": ["Current evidence supports SVR versus baselines.", "SVR versus RF requires matching target, test rows, actual targets, baselines, and metrics.", "The future comparison should rank by MAE first, RMSE second, and R² as a guardrail."],
        "discussion": "A fair comparison is only valid when both model branches are evaluated on the same prediction problem. Until the RF branch exists, the app must not imply that a final two-model decision has been made.",
    },
}

def get_page_narrative(page_id: str) -> dict:
    return PAGE_NARRATIVES[page_id]

# ---- V4 RandomForestRegressor and comparison narratives ----
V4_NARRATIVES = {
    "rf_overview": {
        "key": "The RandomForestRegressor branch completed the same supervised-regression task as SVR, but its held-out performance is weaker than SVR and weaker than the best simple historical baselines.",
        "answers": "This page gives the executive overview of the RandomForestRegressor branch before the detailed RF pages.",
        "read": ["Start with the RF metric cards.", "Check the selected configuration and diagnostics.", "Use the comparison section to see how RF performs against SVR."],
        "discussion": "The RandomForestRegressor branch is a valid second supervised-regression branch for next-year completion-rate prediction. It uses the same broad target and chronological evaluation framing as the SVR branch. However, the current RF output has higher MAE/RMSE, more negative R², and stronger underprediction bias, so it should be used for comparison evidence rather than presented as the best model.",
    },
    "rf_model_design": {
        "key": "The RF branch uses RandomForestRegressor as a nonlinear tree-ensemble regression model, with imputation and categorical encoding to support the shared supervised-regression target.",
        "answers": "This page explains the RF model design, feature sets, preprocessing, and candidate grid.",
        "read": ["Review the selected feature set first.", "Then inspect the candidate registry and feature-set registry.", "Remember that RF does not require numeric scaling, but still needs valid missing-value and categorical handling."],
        "discussion": "RandomForestRegressor averages predictions from multiple decision-tree regressors. This can capture nonlinear feature interactions, but small annual public-sector panels can still produce weak generalisation. The selected RF feature set uses completion history, categorical context, and education-capacity variables.",
    },
    "rf_training": {
        "key": "The final RF was selected from chronological validation, but the intended max_depth grid was not fully evaluated because several candidates failed during fitting.",
        "answers": "This page shows the RF validation results, selected candidate, and tuning caveat.",
        "read": ["Check selected candidate first.", "Then check successful versus failed fit statuses.", "Treat the selected RF as valid among successful candidates, not as proof of a complete RF grid search."],
        "discussion": "The RF notebook records successful validation results and selects a final model from those results. A material caveat is that many max_depth candidates failed, likely because integer depth values were represented as floats after registry conversion. This limits how strongly the RF branch can claim fully completed hyperparameter tuning.",
    },
    "rf_final_eval": {
        "key": "RF achieved MAE = 3.18 pp and RMSE = 3.85 pp on the held-out test set, but it did not beat the strongest simple baselines and had negative R².",
        "answers": "This page evaluates the final RF model on held-out input year 2021 predicting target year 2022.",
        "read": ["Lower MAE/RMSE/Median AE is better.", "Higher R² is better.", "Use baseline comparison before deciding whether the model adds value."],
        "discussion": "The held-out RF result is weak compared with SVR and several simple baselines. The model is still useful as a second supervised branch because it enables a fair model comparison, but its current metrics do not support selecting RF as the final best model.",
    },
    "rf_error_diag": {
        "key": "The RF model has stronger underprediction bias than SVR and lower practical tolerance coverage, especially for some states and secondary_upper rows.",
        "answers": "This page shows RF residual direction, tolerance coverage, grouped errors, and worst predictions.",
        "read": ["Residual = actual minus predicted.", "Positive residual means underprediction.", "Lower grouped MAE/RMSE is better.", "Higher within-tolerance coverage is better."],
        "discussion": "RF underpredicts most held-out rows. Tolerance coverage is substantially lower than SVR, and grouped diagnostics show larger errors for W.P. Putrajaya, secondary_upper, and male rows in the current RF output.",
    },
    "rf_visuals": {
        "key": "RF visual evidence shows model fit, residual behaviour, grouped error patterns, tolerance coverage, feature influence, and comparison against SVR.",
        "answers": "This page presents the saved RF figures with short reading guidance.",
        "read": ["Start with featured figures.", "Use the figure guide before interpreting each chart.", "Use the full gallery only when checking detailed evidence."],
        "discussion": "The RF figures support the same evaluation story as the metric tables: the model runs and produces interpretable evidence, but its held-out performance is weaker than SVR and should be interpreted cautiously.",
    },
    "rf_feature_influence": {
        "key": "RF mostly relies on completion-history and categorical context; education-capacity importance must be interpreted cautiously because of current secondary-stage feature-mapping limitations.",
        "answers": "This page shows native RF feature importance and permutation importance diagnostics.",
        "read": ["Native RF importance is tree-based diagnostic evidence.", "Permutation importance measures score change when a feature is perturbed.", "Neither method proves causation."],
        "discussion": "The top RF features are mainly completion-history fields and stage/state/sex context. Education-capacity features appear in the selected feature set, but the notebook audit indicates missing education features for lower and upper secondary rows, so those importance values need caution.",
    },
    "rf_ai_demo": {
        "key": "The RF demonstrator shows how a single held-out prediction is interpreted using actual value, prediction, residual, absolute error, and underprediction status.",
        "answers": "This page demonstrates the RF model on one representative held-out row and previews non-evaluable forecast-candidate outputs.",
        "read": ["Compare predicted completion with actual completion when available.", "Use residual sign to identify overprediction or underprediction.", "Forecast preview rows are not final evaluation evidence."],
        "discussion": "The RF demonstrator helps translate model output into a user-facing prediction case. In the representative row, RF underpredicts actual next-year completion. Forecast-candidate rows should be read as preview-only because actual future targets are not available.",
    },
    "rf_output_check": {
        "key": "The RF branch output evidence is normalised into the same Streamlit status-check structure used by the SVR branch while still deriving every value from Sam's saved RF files.",
        "answers": "This page verifies RandomForestRegressor output evidence availability using a derived status view, artifact checks, manifest evidence, and detailed raw audit tables.",
        "read": ["Start with the derived output status checks, where Pass confirms that the required RF evidence is available.", "Then verify the model artifact and best-parameter JSON.", "Use the detailed expanders to inspect Sam's original RF file audit, output manifest, and visual registry."],
        "discussion": "The RF output-check page is a presentation-layer normalisation of the saved RF output package. It does not claim that the RF notebook produced the same status-table format as the SVR notebook. Output completeness means the RF branch has saved evidence for review; model quality must still be judged from metrics, baselines, diagnostics, and comparison pages.",
    },
    "rf_limitations": {
        "key": "The RF branch is usable as the second supervised-regression model branch, but the current results do not support selecting RF as the best model.",
        "answers": "This page states the limitations of the RF branch.",
        "read": ["Separate implementation completeness from model quality.", "Read tuning and education-stage limitations carefully.", "Use the comparison pages for final model selection."],
        "discussion": "The main RF limitations are negative R², weaker performance than SVR, failure to beat the strongest simple baselines, strong underprediction bias, failed max_depth candidates, and education-capacity feature missingness for secondary stages. These limitations should be disclosed rather than hidden.",
    },
    "comparison_overview": {
        "key": "SVR and RF can be compared because both target next-year completion rate on the same supervised-regression task. The current outputs show SVR performs better than RF on the main held-out metrics.",
        "answers": "This page explains the active supervised model comparison and validity checks.",
        "read": ["Check row alignment first.", "Then review metric leaderboard and error comparisons.", "Do not select a model from one metric alone."],
        "discussion": "The comparison section combines saved SVR and RF outputs. It does not retrain either model. It checks that both models are compared on the same held-out prediction problem and then evaluates metrics, residuals, grouped errors, feature influence, and demonstrator examples.",
    },
    "comparison_metrics": {
        "key": "SVR is the better supervised model in the current outputs because it has lower MAE, lower RMSE, better R², and lower Median AE than RF.",
        "answers": "This page ranks SVR and RF using the main regression metrics.",
        "read": ["Lower MAE, RMSE, and Median AE are better.", "Higher R² is better.", "MAE is the primary ranking metric because it is interpretable in percentage points."],
        "discussion": "Both models have negative R², so neither should be described as high-accuracy forecasting. SVR is still stronger than RF because it reduces average error and large-error penalty more effectively in the current held-out test.",
    },
    "comparison_predictions": {
        "key": "The row-level comparison shows whether SVR's overall advantage is consistent across individual state-stage-sex test rows.",
        "answers": "This page compares SVR and RF predictions row by row.",
        "read": ["Choose a row or inspect winner counts.", "A positive RF-minus-SVR error difference means RF was worse for that row.", "Winner by row uses lower absolute error."],
        "discussion": "Row-level comparison is useful because one model can win overall while another model wins specific rows. This page makes the comparison more transparent than only showing aggregate metrics.",
    },
    "comparison_errors": {
        "key": "SVR has better tolerance coverage and weaker underprediction bias than RF, although both models still require cautious interpretation.",
        "answers": "This page compares residual direction, tolerance coverage, and grouped errors between SVR and RF.",
        "read": ["Lower grouped MAE/RMSE is better.", "Higher tolerance coverage is better.", "Residuals near zero indicate less bias."],
        "discussion": "Error comparison shows how model differences appear across states, stages, sex groups, and practical tolerance bands. The current outputs favour SVR overall.",
    },
    "comparison_features": {
        "key": "Both models rely strongly on completion-history information, while RF also shows categorical and education-capacity importance with caveats.",
        "answers": "This page compares feature influence diagnostics from the SVR and RF branches.",
        "read": ["Treat feature influence as model diagnostics only.", "Do not interpret feature rankings causally.", "Compare feature groups rather than only individual columns."],
        "discussion": "Feature influence comparison helps explain what each model relied on, but it does not prove why completion rates change. Differences can come from model architecture, feature encoding, and feature missingness.",
    },
    "comparison_ai_demo": {
        "key": "The comparison demonstrator shows how both supervised models predict the same type of row and which model is closer to the actual completion rate for a selected case.",
        "answers": "This page provides a user-facing SVR versus RF prediction example.",
        "read": ["Select a state-stage-sex row if using the table.", "Compare actual value with both predictions.", "The lower absolute error wins for that row."],
        "discussion": "The demonstrator turns aggregate model comparison into a concrete case. It is useful for explaining how the same input row can produce different model predictions and why final model choice should be based on held-out evidence.",
    },
}
PAGE_NARRATIVES.update(V4_NARRATIVES)

def get_page_narrative(page_id: str) -> dict:  # override earlier definition with safe fallback
    return PAGE_NARRATIVES.get(page_id, {
        "key": "This page presents supervised-regression evidence for state completion-rate prediction.",
        "answers": "This page supports the supervised-regression review workflow.",
        "read": ["Read the key takeaway first.", "Then inspect the main table or figure.", "Use detailed expanders for supporting evidence."],
        "discussion": "Use this page together with the rest of the app to interpret the saved model outputs and limitations.",
    })

PAGE_NARRATIVES.update({
    "comparison_overview": {
        "key": "The official comparison notebook validates that SVR and RandomForestRegressor use the same held-out rows and target values. SVR is selected as the stronger supervised-regression model in the current outputs.",
        "answers": "This page summarises the official model-comparison evidence, including validity checks, selected model, row-level wins, and comparison scope.",
        "read": ["Start with the validity cards to confirm the comparison is fair.", "Use the leaderboard and row-level winner summary to understand why SVR is selected.", "Open the output evidence page to verify that the comparison notebook produced the required files."],
        "discussion": "The comparison section now uses the official comparison notebook outputs as the source of truth. This means the app displays saved comparison results rather than recomputing the main conclusion from separate branch outputs. The comparison is valid because both branches use the same target, held-out input year, target year, row keys, and actual target values.",
    },
    "comparison_metrics": {
        "key": "SVR ranks first because it has lower MAE, lower RMSE, better R², and lower Median AE than RandomForestRegressor on the same held-out test rows.",
        "answers": "This page shows the official supervised model leaderboard and the final model selection metrics.",
        "read": ["Use MAE as the primary metric because it is directly interpretable in percentage points.", "Use RMSE, R², and Median AE as supporting checks.", "Do not treat negative R² as high forecasting accuracy."],
        "discussion": "The leaderboard identifies Support Vector Regression as the stronger tested supervised-regression model. SVR achieves lower error than RandomForestRegressor across the main held-out metrics. However, both models have negative R² values, so the result should be described as a comparative model-selection result rather than as a high-accuracy forecasting claim.",
    },
    "comparison_predictions": {
        "key": "SVR wins 74 of 96 held-out row-level comparisons, while RandomForestRegressor wins 22 rows.",
        "answers": "This page compares SVR and RF predictions row by row using the same state, stage, sex, input year, and target year keys.",
        "read": ["A row winner is the model with the lower absolute error for that held-out row.", "Use the disagreement table to identify where the model choice matters most.", "Filter by state, stage, or sex to inspect specific subgroups."],
        "discussion": "The row-level comparison confirms that SVR's advantage is not limited to the aggregate leaderboard. It is closer to the actual target for most held-out rows, while the largest disagreements show where RandomForestRegressor diverges more strongly from the actual completion-rate target.",
    },
    "comparison_errors": {
        "key": "SVR has better tolerance coverage and lower underprediction bias than RandomForestRegressor.",
        "answers": "This page compares practical tolerance bands, residual bias, and grouped errors by state, stage, and sex.",
        "read": ["Higher tolerance coverage is better.", "Residual is actual minus predicted; positive residuals mean underprediction.", "Grouped errors show whether one model performs better across policy-relevant subgroups."],
        "discussion": "Both models tend to underpredict, but RandomForestRegressor underpredicts more strongly. SVR also has higher percentages of predictions within ±1, ±2, and ±5 percentage-point tolerance bands. Grouped errors further show that SVR performs better across all stages, both sex groups, and most states.",
    },
    "comparison_features": {
        "key": "Both models rely strongly on completion-history signals, but feature influence is diagnostic only and must not be interpreted as causal evidence.",
        "answers": "This page compares SVR permutation importance, RF native feature importance, and RF permutation importance from the official comparison outputs.",
        "read": ["Higher importance means stronger model sensitivity, not causal impact.", "Compare feature groups to understand model behaviour.", "Use the visual explanations before interpreting feature ranking charts."],
        "discussion": "The feature influence outputs show that both supervised models use recent completion behaviour as important predictive information. This is methodologically reasonable for next-year prediction. However, the importance results only describe trained-model behaviour and do not prove that the listed variables cause changes in completion rates.",
    },
    "comparison_ai_demo": {
        "key": "The comparison demonstrator uses one common held-out row where SVR is closer to the actual completion-rate target than RandomForestRegressor.",
        "answers": "This page shows a concrete same-row prediction example for both supervised models.",
        "read": ["Compare the actual value against both model predictions.", "The model with lower absolute error is closer for the selected row.", "Use this as a demonstration example, not as a replacement for the full held-out evaluation."],
        "discussion": "The demonstrator translates the model comparison into a concrete held-out prediction case. The selected row is Kelantan, secondary_lower, male, with input year 2021 and target year 2022. SVR has the lower absolute error for this example, matching the overall model-selection result.",
    },
    "comparison_forecast": {
        "key": "The forecast preview compares 96 future-candidate rows, but it is non-evaluable because actual 2023 targets are unavailable.",
        "answers": "This page shows how SVR and RF predictions differ for input year 2022 predicting target year 2023.",
        "read": ["Forecast preview rows are not used for model selection.", "Compare SVR and RF prediction distributions only as future-candidate behaviour.", "Use the evaluation-status column to confirm these rows are non-evaluable."],
        "discussion": "The forecast preview is useful for showing how the two models behave on future-candidate inputs. However, because actual 2023 completion-rate values are not available in the current data, these predictions cannot be scored and cannot be used to select the final model.",
    },
    "comparison_output_check": {
        "key": "The official comparison output package contains the required checks, tables, figures, and selection artifact for the comparison section.",
        "answers": "This page verifies that the comparison notebook output files exist and that the comparison validity checks passed.",
        "read": ["Start with the validity summary.", "Confirm missing comparison outputs is zero.", "Use the manifest only as an output inventory, not as model-performance evidence."],
        "discussion": "The output evidence check confirms that the Streamlit comparison section is backed by saved notebook outputs. It supports reproducibility and allows the comparison pages to display official results rather than manually typed values.",
    },
})

PAGE_NARRATIVES.update({
    "comparison_overview": {
        "key": "Support Vector Regression is selected as the stronger supervised-regression model because it outperforms RandomForestRegressor on MAE, RMSE, R², Median AE, row-level wins, tolerance coverage, and most grouped-error comparisons.",
        "answers": "This page summarises the official comparison notebook outputs from the metric leaderboard, prediction comparison, error comparison, feature influence diagnostics, AI demonstrator, and forecast preview pages.",
        "read": [
            "Start with the validity cards to confirm that both models were compared on the same held-out rows and actual target values.",
            "Use the model-decision cards and leaderboard to understand why SVR is selected.",
            "Use the row-level, error, feature, demonstrator, and forecast summaries to understand the result beyond one metric.",
            "Treat forecast preview rows as non-evaluable because actual 2023 targets are unavailable.",
        ],
        "discussion": "The comparison overview consolidates the official comparison notebook outputs into one branch-level summary. The comparison is valid because SVR and RandomForestRegressor use the same target, row unit, input test year, target year, row keys, and actual target values. The current outputs select Support Vector Regression as the stronger supervised-regression model. The conclusion should still be stated carefully because both models have negative held-out R² values, so the result is a comparative model-selection finding rather than a high-accuracy forecasting claim.",
    },
    "comparison_forecast": {
        "key": "The forecast preview compares 96 future-candidate rows, but it is non-evaluable because actual 2023 targets are unavailable.",
        "answers": "This page shows how SVR and RF predictions differ for input year 2022 predicting target year 2023.",
        "read": ["Forecast preview rows are not used for model selection.", "Compare SVR and RF prediction distributions only as future-candidate behaviour.", "Use the evaluation-status column to confirm these rows are non-evaluable."],
        "discussion": "The forecast preview is useful for showing how the two models behave on future-candidate inputs. However, because actual 2023 completion-rate values are not available in the current data, these predictions cannot be scored and cannot be used to select the final model.",
    },
})


PAGE_NARRATIVES.update({
    "rf_error_diagnostics": PAGE_NARRATIVES.get("rf_error_diag", {
        "key": "The RF model has stronger underprediction bias than SVR and lower practical tolerance coverage.",
        "answers": "This page shows RF residual direction, tolerance coverage, grouped errors, and worst predictions.",
        "read": ["Residual = actual minus predicted.", "Positive residual means underprediction.", "Lower grouped MAE/RMSE is better.", "Higher within-tolerance coverage is better."],
        "discussion": "RF underpredicts most held-out rows. Tolerance coverage is lower than SVR, and grouped diagnostics show larger errors for W.P. Putrajaya, secondary_upper, and male rows in the current RF output.",
    })
})
