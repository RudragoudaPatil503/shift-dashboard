import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------
# Page settings
# -------------------------
st.set_page_config(
    page_title="Employee Shift Dashboard",
    page_icon="🧭",
    layout="wide",
)

# -------------------------
# Company Logo
# -------------------------
logo_url = "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/main/logo.png"
st.image(logo_url, width=180)

st.markdown("<h1 style='text-align: center; color: #003366;'>Employee Shift Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")  # horizontal line

# -------------------------
# Load Excel data
# -------------------------
excel_url = "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/main/shifts.xlsx"

try:
    df = pd.read_excel(excel_url)
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# -------------------------
# Convert times
# -------------------------
df['Shift Start'] = pd.to_datetime(df['Shift Start'], format='%H:%M').dt.time
df['Shift End'] = pd.to_datetime(df['Shift End'], format='%H:%M').dt.time
now = datetime.now().time()

# -------------------------
# Determine current and upcoming
# -------------------------
def is_on_shift(start, end, current_time):
    if start < end:
        return start <= current_time <= end
    else:
        # Overnight shift
        return current_time >= start or current_time <= end

df['Currently On Shift'] = df.apply(lambda x: is_on_shift(x['Shift Start'], x['Shift End'], now), axis=1)
current_employees = df[df['Currently On Shift']]
upcoming_employees = df[~df['Currently On Shift']].sort_values(by='Shift Start').head(1)

# -------------------------
# Display Current Employees
# -------------------------
st.subheader("🟢 Currently Available Employees")
if not current_employees.empty:
    st.dataframe(
        current_employees[['Name', 'Shift Start', 'Shift End', 'Status']].style.apply(
            lambda x: ['background-color: #90EE90' for _ in x], axis=1
        ),
        use_container_width=True
    )
else:
    st.info("No employees are currently on shift.")

# -------------------------
# Display Next Upcoming Employee
# -------------------------
st.subheader("⏳ Next Upcoming Employee")
if not upcoming_employees.empty:
    st.dataframe(
        upcoming_employees[['Name', 'Shift Start', 'Shift End', 'Status']].style.apply(
            lambda x: ['background-color: #FFA500' for _ in x], axis=1
        ),
        use_container_width=True
    )
else:
    st.info("No upcoming employees found.")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("🔄 Dashboard updates automatically based on current time and Excel data.")
