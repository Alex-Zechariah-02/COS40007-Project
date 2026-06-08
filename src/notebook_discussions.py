PROJECT_SCOPE = """
This branch implements the Support Vector Regression part of the supervised-regression objective. The target is a numeric next-year school completion-rate value, so the notebook uses regression metrics rather than classification metrics. RandomForestRegressor is a completed separate supervised-regression branch and clustering is outside this supervised-only app.
"""
TARGET_CONSTRUCTION = """
The notebook constructs a clean target panel from observed completion-rate rows. Malaysia rows are used as benchmark rows, not as training states. The main model uses male and female rows while `both` rows are retained separately as official aggregate evidence. The target is `next_year_completion_rate`, created by shifting within each state-stage-sex series.
"""
FEATURE_ENGINEERING = """
Feature engineering combines current and historical completion features with education-capacity, demographic, household, and prepared economic features. The final selected SVR feature set is `full_without_economic`, so prepared income and poverty features are evidence of the workflow but are not used by the selected final SVR.
"""
VALIDATION = """
The notebook uses chronological validation because the task is next-year prediction. Shuffled K-Fold is not used because it can train on later years and validate on earlier years. The final held-out test uses input year 2021 to predict 2022.
"""
FINAL_EVALUATION = """
The final SVR improves MAE and RMSE against the tested baselines, but held-out R² remains negative. The result should be interpreted as planning-support evidence and not as a high-accuracy forecasting system.
"""
LIMITATIONS = """
This model uses a small annual public-sector panel, government-school completion data, and known-state categorical effects. It is not causal evidence, not a production policy engine, and forecast-preview rows are not evaluated without future actual targets.
"""
