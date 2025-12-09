import gspread
from google.oauth2.service_account import Credentials

# Scopes give permission for Sheets + Drive
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Load API credentials
creds = Credentials.from_service_account_file("cvf_key.json", scopes=SCOPE)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open("Python CVF").worksheet("Trade Sale")

# Read data into Python
data = sheet.get_all_records()

print("Connected successfully! Total rows:", len(data))
