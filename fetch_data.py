import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import io
import requests

# Replace with your actual values
SHEET_ID = "1f58eqLkFr5nJ6bm5PZ3TbfUAxeSd1hpBspW9693kXv8"
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def fetch_data():
  """Fetches data from Google Sheets and returns a Pandas DataFrame."""

  # Use service account credentials to access Google Sheets
  creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
  client = gspread.authorize(creds)

  sheet = client.open_by_key(SHEET_ID).sheet1

  # Get all data from the sheet
  data = sheet.get_all_values()

  # Convert data to pandas DataFrame
  df = pd.DataFrame(data[1:], columns=data[0])

  return df

# Example usage (optional)
if __name__ == "__main__":
  data = fetch_data()
  print(data)
