import streamlit as st
from src.ui_components import page_header, purpose_box, caution_box, discussion
from src import notebook_discussions as nd

page_header("15. Limitations & Reflection", "Required cautious interpretation before report or presentation use.")
purpose_box("This final SVR page states what the model can and cannot claim.")

st.subheader("Safe interpretation")
st.markdown("""
- The SVR branch is a leakage-controlled supervised-regression prototype.
- It predicts numeric next-year completion-rate values.
- It improves MAE and RMSE over tested baselines in the saved held-out evaluation.
- Its held-out R² is negative, so explanatory power remains limited.
- It is suitable as planning-support evidence, not as a production decision system.
""")

st.subheader("Do not claim")
st.markdown("""
- Do not claim classification performance.
- Do not use accuracy, precision, recall, or F1-score for this regression target.
- Do not claim causal feature effects.
- Do not claim forecast-preview rows were evaluated.
- Do not claim the app implements Random Forest yet.
- Do not claim the model generalizes to unseen states.
""")

discussion("Notebook limitation discussion", nd.LIMITATIONS)
