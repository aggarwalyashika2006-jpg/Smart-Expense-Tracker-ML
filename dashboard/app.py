import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Fix import path for deployment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.prediction import predict_future_spending

# -------------------------------
# 🎯 PAGE CONFIG + HEADER
# -------------------------------
st.set_page_config(page_title="Smart Expense Tracker", layout="wide")

st.title("💸 Smart Expense Tracker")
st.markdown("### Analyze • Visualize • Predict your spending")

# -------------------------------
# 📂 LOAD DATA
# -------------------------------
df = pd.read_csv("data/expenses.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month

# -------------------------------
# 🔍 SIDEBAR FILTERS
# -------------------------------
st.sidebar.title("🔍 Filter Data")

category = st.sidebar.selectbox(
    "Select Category",
    df["Category"].unique()
)

# Budget input (WOW feature)
budget = st.sidebar.number_input("Set your monthly budget", value=20000)

filtered_df = df[df["Category"] == category]

# -------------------------------
# 💰 KPI SECTION
# -------------------------------
total = filtered_df["Amount"].sum()
avg = filtered_df["Amount"].mean()
max_val = filtered_df["Amount"].max()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Spend", f"₹{int(total)}")
col2.metric("📊 Avg Spend", f"₹{int(avg)}")
col3.metric("🔥 Max Spend", f"₹{int(max_val)}")

# -------------------------------
# 💰 BUDGET STATUS (WOW FEATURE)
# -------------------------------
st.subheader("💰 Budget Status")

if total > budget:
    st.error("⚠️ You have exceeded your budget!")
else:
    st.success("✅ You are within your budget.")

# -------------------------------
# 📊 CATEGORY CHART
# -------------------------------
st.subheader("📂 Category Spending")

fig1 = px.bar(filtered_df, x="Category", y="Amount", color="Category")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 📅 MONTHLY TREND
# -------------------------------
st.subheader("📅 Monthly Trend")

monthly = filtered_df.groupby("Month")["Amount"].sum().reset_index()
fig2 = px.line(monthly, x="Month", y="Amount", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 💳 PAYMENT DISTRIBUTION
# -------------------------------
st.subheader("💳 Payment Distribution")

fig3 = px.pie(filtered_df, names="Payment_Method", values="Amount")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 🔮 ML PREDICTION
# -------------------------------
st.subheader("🔮 Future Spending Prediction")

st.info(
    "This prediction is generated using Machine Learning (Linear Regression) "
    "based on past monthly expenses. It estimates how your spending may behave in upcoming months."
)

pred_df = predict_future_spending()

fig4 = px.line(pred_df, x="Month", y="Predicted Spending", markers=True)
st.plotly_chart(fig4, use_container_width=True)

st.write("📈 The trend line shows expected spending growth or decline based on historical data.")

st.dataframe(pred_df)

# -------------------------------
# 📌 INSIGHTS SECTION
# -------------------------------
st.subheader("📌 Insights")

top_category = filtered_df.groupby("Category")["Amount"].sum().idxmax()
st.write(f"💡 You spend the most on: **{top_category}**")

st.write(f"🔥 Highest single expense: ₹{int(max_val)}")
st.write(f"📊 Average spending: ₹{avg:.2f}")
