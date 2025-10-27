import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Shift Dashboard", page_icon="🧭", layout="wide")
st.title("👷 Employee Shift Dashboard")

# 👇 Use your GitHub raw Excel file link here
excel_url = "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/refs/heads/main/shifts.xlsx"

try:
    df = pd.read_excel(excel_url)
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error("❌ Error loading data. Please check your Excel file link.")
    st.stop()

# Optional: Filter by Status
status = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
if status != "All":
    df = df[df["Status"] == status]

# Display the table
st.dataframe(df, use_container_width=True)

st.caption("🔄 Data
