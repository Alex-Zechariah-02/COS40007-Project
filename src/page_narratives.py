PAGE_NARRATIVES = {
    "home": {
        "key": "This application presents the supervised-regression workflow for State Completion Rate Prediction. The shared workflow and completed Support Vector Regression branch are available; the RandomForestRegressor branch is reserved until validated outputs are added.",
        "answers": "Use this page to understand the app structure, current model status, and the recommended review path.",
        "read": [
            "Start with the Supervised Regression System pages to understand the shared data, target, features, leakage control, validation, and baselines.",
            "Then open the SVR Branch pages to review the completed model design, training, evaluation, diagnostics, demonstrator, and limitations.",
            "The RandomForestRegressor and comparison sections are intentionally pending until teammate outputs are validated.",
        ],
        "discussion": "The app is organised around a shared supervised-regression contract rather than a single-model story. This keeps the workflow ready for a later fair comparison between Support Vector Regression and RandomForestRegressor using the same target, row unit, split, baselines, and metrics.",
    },
    "supervised_overview": {
        "key": "The supervised task is regression because the output is a numeric next-year completion-rate value, not a class label.",
        "answers": "This page explains the shared supervised-regression objective and how the completed SVR branch and pending RandomForestRegressor branch fit the same modelling task.",
        "read": ["Read the task cards first.", "Then inspect the overview of data, target, feature, leakage, validation, and baseline decisions.", "Use the detailed shared pages for evidence behind each decision."],
        "discussion": "The supervised branch predicts next-year school completion rate. This requires regression metrics such as MAE, RMSE, R², and Median AE. Classification metrics are excluded because no categorical class label is used. A later RandomForestRegressor branch can only be compared against SVR if it follows the same target, row unit, split, baselines, and metric contract.",
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
        "discussion": "SVR with an RBF kernel can model nonlinear relationships, but it is sensitive to feature scale. Numeric features therefore use imputation and scaling, while categorical identifiers are encoded safely. RandomForestRegressor later may use different model-specific preprocessing, but it must still use the same target, split, baselines, and metrics.",
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
        "discussion": "The main limitations are small annual data, negative held-out R², underprediction bias, non-causal design, and non-evaluable forecast-preview rows. The branch is still useful because it demonstrates a complete supervised-regression workflow with transparent evidence and a clear path for future RandomForestRegressor comparison.",
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
