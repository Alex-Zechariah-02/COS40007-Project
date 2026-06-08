import streamlit as st
from src.ui_components import page_header, render_page_intro, render_page_discussion, guided_figure, next_steps
from src.data_loader import figure_path, load_table
from src.figure_gallery import render_gallery

page_header("SVR Branch: Visual Evidence", "Guided figure review for model fit, validation, diagnostics, interpretation, and forecast preview.")
render_page_intro("svr_visuals")

tab_featured, tab_gallery, tab_registry = st.tabs(["Featured figures", "Full gallery", "Visual registry"])

with tab_featured:
    featured = [
        ("actual_vs_predicted.png", "Actual versus predicted", "Compares held-out actual values with SVR predictions.", "Closer to the diagonal line means smaller prediction error.", "Closer to the diagonal is better.", "Shows the overall prediction fit."),
        ("expanded_mae_comparison.png", "MAE comparison", "Compares Mean Absolute Error across SVR and baselines.", "Lower bars are better.", "Lower is better.", "Shows whether SVR improves average error."),
        ("residual_distribution.png", "Residual distribution", "Shows actual-minus-predicted error spread.", "Positive residuals mean underprediction.", "Centered near 0 is better.", "Shows bias and spread."),
        ("error_by_state.png", "Error by state", "Shows grouped errors by state.", "Higher bars mean larger errors.", "Lower is better.", "Shows where predictions are weaker."),
        ("permutation_importance.png", "Permutation importance", "Shows model sensitivity to features.", "Larger bars indicate stronger diagnostic influence.", "No performance direction.", "Supports interpretation but not causality."),
    ]
    for fig, title, purpose, how, better, takeaway in featured:
        guided_figure(figure_path(fig), title, purpose, how, better, takeaway, "Featured figures are a guided subset. Use the full gallery for all saved figures.")

with tab_gallery:
    render_gallery()

with tab_registry:
    registry = load_table("visual_evidence_registry.csv")
    if not registry.empty:
        st.dataframe(registry, width="stretch", hide_index=True)

render_page_discussion("svr_visuals")
next_steps(["Open 7. Feature Influence to inspect model sensitivity diagnostics."])
