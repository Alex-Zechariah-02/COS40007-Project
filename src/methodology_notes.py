NOTES = {
    "raw_data": "The raw data audit checks all input CSVs before modelling. This prevents the workflow from depending on unexplained processed files and makes data coverage, missingness, and duplicate-key risks visible.",
    "target": "The target construction step creates next_year_completion_rate from observed completion rates. Malaysia rows are used only as benchmark rows, while state rows become model rows. Male and female rows form the primary supervised dataset, while both-only rows are kept separate.",
    "features": "Feature engineering builds predictors from completion history, education capacity, population, household, fertility, and economic sources. Time-sensitive features are constructed from the input year or earlier only.",
    "panel": "The supervised panel combines target rows and feature blocks into a single row unit. The leakage audit checks that future target values and forbidden target-derived columns are not used as predictors.",
    "validation": "The validation design uses earlier input years for training and later input years for validation or testing. This matches the next-year prediction task more closely than shuffled random folds.",
    "svr_design": "The SVR branch uses a Pipeline with numeric imputation and scaling, categorical one-hot encoding, and an RBF-kernel SVR. This keeps preprocessing inside the model workflow and avoids fitting transformations on held-out rows.",
    "evaluation": "Final evaluation uses a held-out input year, not validation rows used for model selection. The result should be interpreted through MAE, RMSE, R², median absolute error, baseline comparison, and practical error diagnostics.",
    "diagnostics": "Error diagnostics explain where predictions are strong or weak. Residual direction, tolerance coverage, grouped errors, and worst rows make the model result easier to interpret for planning.",
    "importance": "Permutation importance is used as a diagnostic of trained-model sensitivity. It is not causal evidence and was not used to select the final model.",
    "demonstrator": "The AI demonstrator shows a representative held-out prediction and a forecast preview. Forecast candidates are labelled non-evaluable when the actual next-year target is unavailable.",
}
