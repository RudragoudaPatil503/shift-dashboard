import streamlit as st
import pandas as pd
from datetime import datetime

# Page settings
st.set_page_config(page_title="Employee Shift Dashboard", page_icon="🧭", layout="wide")
st.title("👷 Employee Shift Dashboard")

# Correct raw GitHub Excel file link
excel_url = "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/main/shifts.xlsx"

# Load Excel file
try:
    df = pd.read_excel(excel_url)
    st.success("✅ Data loaded successfully")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Optional: Filter by Status
status = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
if status != "All":
    df = df[df["Status"] == status]

# Display table
st.dataframe(df, use_container_width=True)

# Caption
st.caption("🔄 Data automatically updates whenever Excel file is updated on GitHub.")
