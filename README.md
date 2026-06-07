# COS40007 Smart Government SVR Notebook System

This repository contains a Streamlit app that converts the completed Support Vector Regression notebook into an interactive notebook-as-system for COS40007 State Completion Rate Prediction.

Current status:

- SVR branch: complete and loaded from saved notebook outputs.
- RandomForestRegressor branch: pending.
- Supervised comparison: pending until Random Forest outputs are added.
- Clustering branch: intentionally excluded from this supervised-regression app.

Main target: `next_year_completion_rate`.

Main model: Support Vector Regression with RBF kernel.

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Deploy on Streamlit Community Cloud with main file path: `app.py`.
