# COS40007 State Completion Rate Prediction

This repository contains a Streamlit application for the supervised-regression component of the COS40007 Smart Government project.

Current status:

- Shared supervised-regression workflow: complete
- Support Vector Regression branch: complete
- RandomForestRegressor branch: complete
- Supervised model comparison: available

Main task:

- Predict next-year Malaysian state school completion rate using supervised regression.

Main target:

- `next_year_completion_rate`

Completed model branches:

- Support Vector Regression
- RandomForestRegressor

Main metrics:

- MAE = Mean Absolute Error
- RMSE = Root Mean Squared Error
- R² = R-squared
- Median AE = Median Absolute Error

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Hosted Streamlit main file path:

```text
app.py
```
