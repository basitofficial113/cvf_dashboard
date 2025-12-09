import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# ------------------------------
# GOOGLE SHEETS CONNECTION
# ------------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("cvf_key.json", scopes=SCOPE)
client = gspread.authorize(creds)

# Load your Google Sheet
SHEET_NAME = "Python CVF"
WS_NAME = "Trade Sale"

sheet = client.open(SHEET_NAME).worksheet(WS_NAME)
rows = sheet.get_all_records()
df = pd.DataFrame(rows)

# ------------------------------
# DATA CLEANING
# ------------------------------
df["Visit Date"] = pd.to_datetime(df["Timestamp"]).dt.date
df["Weekday"] = pd.to_datetime(df["Visit Date"]).dt.weekday

# ------------------------------
# DASHBOARD TITLE
# ------------------------------
st.title("🎨 Paints CVF Dashboard (Live Google Sheets Data)")
st.write("Automatically updated dashboard for Sales Team CVF visits.")

# ------------------------------
# KPI 1 — Total Visits
# ------------------------------
st.subheader("📌 Total Visits per Salesperson")
visits = df.groupby("Salesperson")["Visit Date"].count()
st.bar_chart(visits)

# ------------------------------
# KPI 2 — Working Days
# ------------------------------
holidays = [
    "2025-01-01", "2025-03-23", "2025-05-01",
    "2025-08-14", "2025-12-25"
]
holidays = pd.to_datetime(holidays).date

df_work = df[~df["Visit Date"].isin(holidays)]
df_work = df_work[df_work["Weekday"] != 6]   # Remove Sundays

working_days = df_work.groupby("Salesperson")["Visit Date"].nunique()
st.subheader("📅 Working Days (Excluding Sundays & Holidays)")
st.dataframe(working_days)

# ------------------------------
# KPI 3 — Dealer Visit Counts
# ------------------------------
dealer_counts = df.groupby("Dealer Name")["Visit Date"].count()

st.subheader("🏪 Dealer Visit Frequency Categories")
st.write("Dealers visited Once, Twice, 3 times, 4 times, 5 times, >5 times")

once = dealer_counts[dealer_counts == 1]
twice = dealer_counts[dealer_counts == 2]
thrice = dealer_counts[dealer_counts == 3]
four = dealer_counts[dealer_counts == 4]
five = dealer_counts[dealer_counts == 5]
more_than_five = dealer_counts[dealer_counts > 5]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Once", len(once))
    st.metric("Thrice", len(thrice))
    st.metric(">5", len(more_than_five))
with col2:
    st.metric("Twice", len(twice))
with col3:
    st.metric("Four", len(four))
    st.metric("Five", len(five))

# ------------------------------
# KPI 4 — Fake Visits
# ------------------------------
st.subheader("⚠ Fake Visit Detection")
fake_visits = df[df["Geo Accuracy"] == "Low"]
st.write("Visits with low Geo accuracy:")
st.dataframe(fake_visits)

# ------------------------------
# KPI 5 — Non-visited Dealers
# ------------------------------
st.subheader("🚫 Non-Visited Dealers")

all_dealers = df["Dealer Name"].unique()
visited = df[df["Visit Type"] == "Dealer"]["Dealer Name"].unique()
non_visited = list(set(all_dealers) - set(visited))

st.write("Dealers never visited:")
st.write(non_visited)