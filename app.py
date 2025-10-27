import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# -------------------------
# Page settings
# -------------------------
st.set_page_config(
    page_title="Employee Shift Dashboard",
    page_icon="🧭",
    layout="wide",
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.image(
    "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/main/team_logo.png", width=150
)
st.sidebar.markdown("## 🛠 Support Team Dashboard")
st.sidebar.markdown("**Instructions:**")
st.sidebar.markdown(
    "- 🟢 Green rows = currently on shift\n"
    "- 🟠 Orange rows = next upcoming employee\n"
    "- Data updates automatically based on Excel file and current IST time"
)
st.sidebar.markdown("---")

# Live clock in IST
india_tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(india_tz)
st.sidebar.markdown(f"### ⏰ Current Time (IST): {now.strftime('%H:%M:%S')}")

# -------------------------
# Header
# -------------------------
st.image(
    "https://raw.githubusercontent.com/RudragoudaPatil503/shift-dashboard/main/team_logo.png", width=180
)
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
# Clean column names and map to standard names
# -------------------------
df.columns = df.columns.str.strip().str.replace('\n','').str.replace('\r','')

expected_columns = {'Name': None, 'Shift Start': None, 'Shift End': None, 'Status': None}

for col in df.columns:
    for key in expected_columns:
        if key.lower() == col.lower():
            expected_columns[key] = col

missing_cols = [k for k,v in expected_columns.items() if v is None]
if missing_cols:
    st.error(f"❌ Required column(s) missing in Excel: {missing_cols}")
    st.stop()

# Rename to standard names
df = df.rename(columns={v:k for k,v in expected_columns.items()})

# -------------------------
# Convert times safely
# -------------------------
df['Shift Start'] = pd.to_datetime(df['Shift Start'], errors='coerce').dt.time
df['Shift End'] = pd.to_datetime(df['Shift End'], errors='coerce').dt.time
df = df.dropna(subset=['Shift Start','Shift End'])

# -------------------------
# Determine current and upcoming
# -------------------------
def is_on_shift(start, end, current_time):
    try:
        if start < end:
            return start <= current_time <= end
        else:  # overnight shift
            return current_time >= start or current_time <= end
    except:
        return False

df['Currently On Shift'] = df.apply(lambda x: is_on_shift(x['Shift Start'], x['Shift End'], now.time()), axis=1)

current_employees = df[df['Currently On Shift']]

upcoming_employees = pd.DataFrame()
if 'Shift Start' in df.columns:
    upcoming_employees = df[~df['Currently On Shift']].sort_values(by='Shift Start').head(1)

# -------------------------
# Display Current Employees
# -------------------------
st.subheader("🟢 Currently Available Employees")
if not current_employees.empty:
    st.dataframe(
        current_employees[['Name','Shift Start','Shift End','Status']].style.apply(
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
        upcoming_employees[['Name','Shift Start','Shift End','Status']].style.apply(
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
st.caption("🔄 Dashboard updates automatically based on current IST time and Excel data.")
