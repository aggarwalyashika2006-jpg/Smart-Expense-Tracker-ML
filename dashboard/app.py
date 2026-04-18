import streamlit as st
import pandas as pd
import plotly.express as px

from src.prediction import predict_future_spending

st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💸 Smart Expense Tracker Dashboard")

# Load data
df = pd.read_csv("data/expenses.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month

# -------------------------------
# 🎯 SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

month = st.sidebar.multiselect(
    "Month",
    df["Month"].unique(),
    default=df["Month"].unique()
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Month"].isin(month))
]

# -------------------------------
# 💰 KPI CARDS
# -------------------------------
total = int(filtered_df["Amount"].sum())
avg = int(filtered_df["Amount"].mean())
max_val = int(filtered_df["Amount"].max())

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Spend", f"₹{total}")
col2.metric("📊 Avg Spend", f"₹{avg}")
col3.metric("🔥 Max Spend", f"₹{max_val}")

# -------------------------------
# 📊 INTERACTIVE CHARTS (Plotly)
# -------------------------------

st.subheader("📂 Category Spending")
fig1 = px.bar(filtered_df, x="Category", y="Amount", color="Category")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📅 Monthly Trend")
monthly = filtered_df.groupby("Month")["Amount"].sum().reset_index()
fig2 = px.line(monthly, x="Month", y="Amount", markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("💳 Payment Distribution")
fig3 = px.pie(filtered_df, names="Payment_Method", values="Amount")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 🔮 ML PREDICTION
# -------------------------------
st.subheader("🔮 Future Spending Prediction")

pred_df = predict_future_spending()

fig4 = px.line(pred_df, x="Month", y="Predicted Spending", markers=True)
st.plotly_chart(fig4, use_container_width=True)

st.dataframe(pred_df)

# -------------------------------
# ⚠️ INSIGHTS
# -------------------------------
st.subheader("📌 Insights")

top_cat = filtered_df.groupby("Category")["Amount"].sum().idxmax()
st.write(f"👉 Top category: **{top_cat}**")

high_spend = filtered_df[filtered_df["Amount"] > 4000]
st.write("⚠️ High Spending Transactions:")
st.dataframe(high_spend.head())
