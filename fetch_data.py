import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Replace with your actual values
SHEET_ID = "1f58eqLkFr5nJ6bm5PZ3TbfUAxeSd1hpBspW9693kXv8"
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def fetch_data():
    """Fetches data from Google Sheets and returns a Pandas DataFrame."""
    try:
        # Use service account credentials to access Google Sheets
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
        client = gspread.authorize(creds)

        # Open the Google Sheet by its ID
        sheet = client.open_by_key(SHEET_ID).sheet1

        # Get all data from the sheet
        data = sheet.get_all_values()

        # Convert data to pandas DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])  # Use headers from the first row

        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

# Example usage (optional)
if __name__ == "__main__":
    data = fetch_data()
    if not data.empty:
        print(data)
    else:
        print("Failed to fetch data.")