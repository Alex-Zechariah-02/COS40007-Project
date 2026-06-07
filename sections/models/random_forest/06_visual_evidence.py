import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, guided_figure, next_steps, show_detail_table
from src.data_loader import rf_figure_path, load_rf_table, list_files, RF_FIGURES_DIR

page_header("Random Forest Branch: Visual Evidence", "Guided figure review for RF fit, diagnostics, interpretation, and forecast preview.")
render_page_intro("rf_visuals")

st.markdown("### Featured figures")
featured = [
    ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual values with RF predictions.", "Closer to diagonal means smaller prediction error.", "Closer to diagonal is better.", "RF shows visible misses and underprediction."),
    ("rf_vs_svr_metric_comparison.png", "RF versus SVR metric comparison", "Compares the two supervised regression branches.", "Lower errors are better; higher R² is better.", "Depends on metric.", "SVR outperforms RF in current outputs."),
    ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted errors.", "Positive residuals mean underprediction.", "Centered near 0 is better.", "RF has underprediction bias."),
    ("error_by_state.png", "Error by state", "Shows grouped error by state.", "Higher bars mean larger error.", "Lower is better.", "Some states are much harder for RF."),
    ("permutation_importance.png", "Permutation importance", "Shows RF feature influence diagnostics.", "Larger absolute importance means larger score change when perturbed.", "No performance direction.", "Completion history and categorical context dominate."),
]
for fig, title, purpose, how, better, takeaway in featured:
    guided_figure(rf_figure_path(fig), title, purpose, how, better, takeaway, "Featured figures are a guided subset. Use the full gallery below for all saved figures.")

st.markdown("### Full RF figure gallery")
figs = list_files(RF_FIGURES_DIR, ".png")
if figs:
    names = [p.name for p in figs]
    selected = st.selectbox("Select a saved RF figure", names)
    guided_figure(rf_figure_path(selected), selected.replace("_", " ").replace(".png", "").title(), "Saved RF visual evidence from the notebook output.", "Read axes, legend, and table context before interpreting.", "Depends on the metric shown.", "Use this figure with the page discussion and saved tables.", "Figures are diagnostic evidence, not causal proof.")
else:
    st.info("No RF figures found.")

registry = load_rf_table("visual_evidence_registry.csv")
if not registry.empty:
    show_detail_table(registry, "Detailed RF visual evidence registry")

render_page_discussion("rf_visuals")
next_steps(["Open 7. Feature Influence to inspect RF feature importance diagnostics."])
