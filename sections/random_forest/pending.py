import streamlit as st
from src.ui_components import page_header, purpose_box

page_header("Random Forest Pending", "Placeholder for the future RandomForestRegressor branch.")
purpose_box("No RandomForestRegressor outputs are included yet. This page is intentionally pending and does not fabricate RF metrics.")

st.subheader("Required future files")
st.code("""data/random_forest/rf_final_metrics.csv
data/random_forest/rf_test_predictions.csv
data/random_forest/rf_baseline_comparison.csv
data/random_forest/rf_error_by_state.csv
data/random_forest/rf_error_by_stage.csv
data/random_forest/rf_error_by_sex.csv
data/random_forest/rf_feature_importance.csv
models/random_forest/rf_final_model.joblib""")

st.subheader("Required shared contract")
st.markdown("""
The RandomForestRegressor branch must use the same:

- target: `next_year_completion_rate`
- row unit: state-stage-sex-year
- train/test split
- baselines
- regression metrics
- prediction table schema

Only the model-specific training and interpretation should differ.
""")
