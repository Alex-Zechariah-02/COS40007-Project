# Interview Guide

## Core explanation path

- Objective: Supervised Regression System → 1. Overview
- Data and target: Supervised Regression System → 2-3
- Leakage and validation: Supervised Regression System → 5-6
- SVR result: SVR Branch → 1 and 4
- RandomForestRegressor result: Random Forest Branch → 1 and 4
- Final comparison: Supervised Model Comparison → 2-4
- User-facing demo: Supervised Model Comparison → 6

## Key points

- The target is numeric, so the task is regression.
- Both branches predict next-year completion rate.
- The current saved outputs favour SVR over RandomForestRegressor.
- Both models have limitations and should be treated as planning-support evidence, not production forecasting systems.
