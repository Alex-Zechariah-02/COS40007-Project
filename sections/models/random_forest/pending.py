import pandas as pd
import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, show_table, next_steps
from src.rf_contract import RF_REQUIRED_OUTPUT_FILES, RF_REQUIRED_PREDICTION_COLUMNS, RF_INTEGRATION_RULES
from src.validators import rf_pending_status

page_header("RandomForestRegressor Branch Pending", "Reserved section for the second supervised-regression model branch.")
render_page_intro("rf_pending")

st.markdown("### Required output files")
st.dataframe(pd.DataFrame({"Required file": RF_REQUIRED_OUTPUT_FILES}), width="stretch", hide_index=True)

st.markdown("### Required prediction columns")
st.dataframe(pd.DataFrame({"Required column": RF_REQUIRED_PREDICTION_COLUMNS}), width="stretch", hide_index=True)

st.markdown("### Integration rules")
for rule in RF_INTEGRATION_RULES:
    st.markdown(f"- {rule}")

st.markdown("### Current RF file status")
st.dataframe(rf_pending_status(), width="stretch", hide_index=True)

st.warning("RandomForestRegressor results are pending. The app will not show RF metrics or comparisons until validated RF outputs are added.")
render_page_discussion("rf_pending")
next_steps(["After RF outputs are available, validate target, row unit, test rows, baselines, and metrics before enabling comparison."])
