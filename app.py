import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 E-commerce Analytics Dashboard")

# Connect DB
conn = sqlite3.connect("ecommerce.db")

df = pd.read_sql("SELECT * FROM sales", conn)

# 🔥 If empty
if df.empty:
    st.warning("No data available. Run stream.py")
    st.stop()

# -------------------------------
# 🧩 ADD FILTERS
# -------------------------------

st.sidebar.header("🔍 Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

filtered_df = df[df["category"].isin(categories)]

# -------------------------------
# 📊 KPIs
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", int(filtered_df['price'].sum()))
col2.metric("🛒 Orders", len(filtered_df))
col3.metric("📦 Avg Order Value", int(filtered_df['price'].mean()))
col4.metric("📈 Max Sale", int(filtered_df['price'].max()))

# -------------------------------
# 📈 CHARTS
# -------------------------------

st.subheader("📈 Sales Trend")
st.line_chart(filtered_df['price'])

st.subheader("📊 Category-wise Revenue")
st.bar_chart(filtered_df.groupby('category')['price'].sum())

st.subheader("🏆 Top Products")
st.dataframe(filtered_df['product'].value_counts().head(10))

# -------------------------------
# 💡 INSIGHTS
# -------------------------------

st.subheader("💡 Insights")

top_category = filtered_df.groupby('category')['price'].sum().idxmax()
top_product = filtered_df['product'].value_counts().idxmax()

st.write(f"🔥 Top Category: **{top_category}**")
st.write(f"🏆 Most Sold Product: **{top_product}**")