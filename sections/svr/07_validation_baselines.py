import streamlit as st
from src.config import TABLES_DIR, CHECKS_DIR, SVR_FIGURES_DIR
from src.data_loader import load_csv
from src.ui_components import page_header, purpose_box, show_dataframe, show_image, discussion
from src import notebook_discussions as nd

page_header("7. Validation & Baselines", "Chronological split and rule-based comparison methods.")
purpose_box("The notebook uses chronological validation and a held-out future input year because the task is next-year completion-rate prediction. Shuffled K-Fold is intentionally not used.")

tabs = st.tabs(["Split integrity", "Validation folds", "Core baselines", "Additional baselines", "Baseline summary", "Figures"])
with tabs[0]:
    show_dataframe(load_csv(CHECKS_DIR / "split_integrity_check.csv"), height=320)
    show_dataframe(load_csv(TABLES_DIR / "train_panel.csv"), "Train panel", height=250)
    show_dataframe(load_csv(TABLES_DIR / "test_panel.csv"), "Held-out test panel", height=250)
    show_dataframe(load_csv(TABLES_DIR / "forecast_candidate_panel.csv"), "Forecast candidate panel", height=250)
with tabs[1]: show_dataframe(load_csv(TABLES_DIR / "chronological_validation_folds.csv"), height=320)
with tabs[2]:
    show_dataframe(load_csv(TABLES_DIR / "baseline_metrics.csv"), height=360)
    show_dataframe(load_csv(TABLES_DIR / "baseline_predictions.csv"), height=360)
with tabs[3]:
    show_dataframe(load_csv(TABLES_DIR / "additional_rule_baseline_metrics.csv"), height=360)
    show_dataframe(load_csv(TABLES_DIR / "additional_rule_baseline_definitions.csv"), height=360)
with tabs[4]: show_dataframe(load_csv(TABLES_DIR / "all_baseline_metrics_pre_svr.csv"), height=420)
with tabs[5]:
    for name in ["chronological_split_timeline.png", "train_test_forecast_row_count_bar.png", "all_baseline_mae_rmse_comparison.png", "all_baseline_r2_comparison.png", "expanded_baseline_mae_comparison.png", "expanded_baseline_rmse_comparison.png"]:
        show_image(SVR_FIGURES_DIR / name)

discussion("Notebook discussion", nd.VALIDATION)
