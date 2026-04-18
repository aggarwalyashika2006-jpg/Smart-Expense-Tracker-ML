import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range(start="2024-01-01", end="2024-03-31")
categories = ['Food', 'Travel', 'Rent', 'Shopping', 'Bills', 'Entertainment']
payment_methods = ['Cash', 'UPI', 'Card']

data = {
    "Date": np.random.choice(dates, 300),
    "Category": np.random.choice(categories, 300),
    "Amount": np.random.randint(100, 5000, 300),
    "Payment_Method": np.random.choice(payment_methods, 300)
}

df = pd.DataFrame(data)
df.to_csv("data/expenses.csv", index=False)

print("Data Generated Successfully!")