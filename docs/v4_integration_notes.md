# V4 Integration Notes

V4 integrates the completed RandomForestRegressor branch into the supervised-regression Streamlit application.

## Scope

- The shared supervised-regression workflow remains unchanged.
- The SVR branch remains available as the first completed model branch.
- The RandomForestRegressor branch is now available as the second completed model branch.
- The supervised model comparison section is now active.

## Data source for V4

The RandomForestRegressor pages are built from Sam's saved notebook outputs under:

- `data/random_forest/checks/`
- `data/random_forest/tables/`
- `data/random_forest/artifacts/`
- `figures/random_forest/`
- `models/random_forest/`

The Streamlit application does not retrain the RandomForestRegressor model.

## Current comparison result

The current saved outputs favour Support Vector Regression over RandomForestRegressor on MAE, RMSE, R², and Median AE. The RandomForestRegressor branch is still useful because it provides the required second supervised-regression model and enables direct model comparison.

## Interpretation cautions

- RandomForestRegressor has negative held-out R² in the current output.
- RandomForestRegressor does not beat the strongest simple historical baselines in the current output.
- Several `max_depth` candidates failed during RF validation.
- Education-capacity features were missing for `secondary_lower` and `secondary_upper` rows in the current RF feature merge.
- Feature importance is diagnostic, not causal.
