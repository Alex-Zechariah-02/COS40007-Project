import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, next_steps

page_header("Random Forest Branch: Limitations and Reflection", "Model quality, tuning, feature-merge, and interpretation limitations.")
render_page_intro("rf_limitations")

st.markdown("### Main RF limitations")
st.warning("\n".join([
    "- RF held-out R² is negative, so held-out explanatory performance is weak.",
    "- RF does not beat the strongest simple historical baselines in the current outputs.",
    "- RF performs worse than SVR on MAE, RMSE, R², and Median AE.",
    "- RF has strong underprediction bias.",
    "- Several max_depth validation candidates failed during fitting, so the intended tuning grid was not fully evaluated.",
    "- Education-capacity features are missing for secondary_lower and secondary_upper rows in the current RF feature merge, so related importance values need caution.",
    "- Feature importance is diagnostic, not causal.",
    "- Forecast-candidate rows are preview-only and are not final evaluation evidence."
]))

st.markdown("### Supported use")
st.write("The RF branch is useful as a second supervised-regression model branch and as comparison evidence against SVR and baselines.")

st.markdown("### Unsupported claims")
st.write("The current RF output should not be described as the best model, high-accuracy forecasting, or causal evidence.")

render_page_discussion("rf_limitations")
next_steps(["Open the Supervised Model Comparison section to compare SVR and RF directly."])
