import pandas as pd

def load_data():
    df = pd.read_csv("data/expenses.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    return df

def category_analysis(df):
    return df.groupby('Category')['Amount'].sum()

def monthly_analysis(df):
    return df.groupby('Month')['Amount'].sum()

def payment_analysis(df):
    return df.groupby('Payment_Method')['Amount'].sum()