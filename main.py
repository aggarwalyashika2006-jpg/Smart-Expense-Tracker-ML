import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# -----------------------------
# 1. Generate Synthetic Data
# -----------------------------
categories = ['Food', 'Travel', 'Rent', 'Shopping', 'Bills', 'Entertainment']
payment_modes = ['Cash', 'UPI', 'Card']

data = []

start_date = datetime(2025, 1, 1)

for i in range(200):
    date = start_date + timedelta(days=random.randint(0, 180))
    category = random.choice(categories)
    amount = random.randint(100, 5000)
    payment = random.choice(payment_modes)
    
    data.append([date, category, amount, payment])

df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount', 'Payment_Mode'])

df.to_csv('data/expenses.csv', index=False)

# -----------------------------
# 2. Data Cleaning
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'])
df.dropna(inplace=True)

# -----------------------------
# 3. Feature Engineering
# -----------------------------
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day_name()

# -----------------------------
# 4. Analysis
# -----------------------------
category_spending = df.groupby('Category')['Amount'].sum()
monthly_spending = df.groupby('Month')['Amount'].sum()

# -----------------------------
# 5. Visualization
# -----------------------------
plt.figure(figsize=(8,5))
category_spending.plot(kind='bar')
plt.title('Category-wise Spending')
plt.savefig('outputs/category_spending.png')
plt.close()

plt.figure(figsize=(8,5))
monthly_spending.plot(kind='line', marker='o')
plt.title('Monthly Spending Trend')
plt.savefig('outputs/monthly_trend.png')
plt.close()

# -----------------------------
# 6. Insights
# -----------------------------
highest_category = category_spending.idxmax()
print(f"Highest spending category: {highest_category}")

if category_spending.max() > 30000:
    print("⚠️ Overspending detected!")

print("Project Completed Successfully!")