import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_spending():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month

    monthly = df.groupby("Month")["Amount"].sum().reset_index()

    X = monthly[["Month"]]
    y = monthly["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    future_months = np.array([[4], [5], [6]])  # Predict next 3 months
    predictions = model.predict(future_months)

    result = pd.DataFrame({
        "Month": [4, 5, 6],
        "Predicted Spending": predictions
    })

    return result