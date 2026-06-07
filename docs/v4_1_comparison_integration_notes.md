# V4.1 Comparison Integration Notes

V4.1 integrates the official SVR versus RandomForestRegressor comparison notebook outputs into the Streamlit application.

## Integration rule

The comparison pages use `data/comparison/` and `figures/comparison/` as the main source of comparison evidence. The SVR and RandomForestRegressor branch outputs remain available for branch-specific review.

## Added pages

- Forecast Preview Comparison
- Output evidence files

## Display rule

Forecast preview rows are displayed as non-evaluable because actual 2023 targets are unavailable. They are not used for model selection.
