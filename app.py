import streamlit as st
import pandas as pd

st.set_page_config(page_title="Employee Shift Dashboard", page_icon="🧭", layout="wide")

st.title("👷 Employee Shift Dashboard")

# 👇 Replace with your actual GitHub raw Excel file link
excel_url = "https://raw.githubusercontent.com/<your-username>/shift-dashboard/main/shifts.xlsx"

try:
    df = pd.read_excel(excel_url)
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error("❌ Error loading data. Please check your Excel file link.")
    st.stop()

# Filter dropdown
status = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
if status != "All":
    df = df[df["Status"] == status]

# Display data
st.dataframe(df, use_container_width=True)

st.caption("🔄 Updates automatically when you replace Excel file on GitHub.")
