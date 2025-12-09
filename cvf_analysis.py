import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file("cvf_key.json", scopes=SCOPE)
client = gspread.authorize(creds)

sheet = client.open("Python CVF").worksheet("Trade Sale")
rows = sheet.get_all_records()

df = pd.DataFrame(rows)

# Convert date column
df['Visit Date'] = pd.to_datetime(df['Timestamp']).dt.date

visits = df.groupby('Salesperson')['Visit Date'].count()
print(visits)

active_dealers = df[df['Select Visit Type'] == 'Dealers']

fake_visits = df[df['Geo Accuracy'] == 'Low']   # simple example

holidays = [
    "2025-01-01", "2025-03-23", "2025-05-01",
    "2025-08-14", "2025-12-25"
]
holidays = pd.to_datetime(holidays).date

df['Weekday'] = pd.to_datetime(df['Visit Date']).dt.weekday
df_work = df[~df['Visit Date'].isin(holidays)]
df_work = df_work[df_work['Weekday'] != 6]   # 6 = Sunday

working_days = df_work.groupby('Salesperson')['Visit Date'].nunique()
print(working_days)

all_dealers = df['Dealer Name'].unique()
visited = df[df['Visit Type'] == 'Dealer']['Dealer Name'].unique()
non_visited = list(set(all_dealers) - set(visited))

dealer_counts = df.groupby('Dealer Name')['Visit Date'].count()

once = dealer_counts[dealer_counts == 1]
twice = dealer_counts[dealer_counts == 2]
thrice = dealer_counts[dealer_counts == 3]
four = dealer_counts[dealer_counts == 4]
five = dealer_counts[dealer_counts == 5]
more_than_five = dealer_counts[dealer_counts > 5]

daily_visits = df.groupby('Salesperson')['Visit Date'].nunique()
missing_days = working_days - daily_visits

df_daily = df.groupby(['Salesperson', 'Visit Date']).size()
low_entries = df_daily[df_daily <= 3]
