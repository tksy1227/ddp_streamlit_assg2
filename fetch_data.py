import gspread
import pandas as pd
import os
from oauth2client.service_account import ServiceAccountCredentials

def extract_data_from_google_sheets(sheets_url, st=None):
    """
    Extracts data from a Google Sheets URL and saves each sheet as a CSV file.
    """
    try:
        # Path to the service account credentials file
        creds_file = "service_credentials.json"

        if not os.path.exists(creds_file):
            raise ValueError(f"Service account credentials file '{creds_file}' not found.")

        # Define the scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Load the credentials into ServiceAccountCredentials
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)

        # Authorize the client
        client = gspread.authorize(creds)

        # Open the Google Sheets document by URL
        spreadsheet = client.open_by_url(sheets_url)

        # List of sheet names to extract
        sheet_names = ["NextBus", "NextBus2", "NextBus3"]

        # Extract data from each sheet and save as CSV
        all_data = []  # To store data from all sheets

        for sheet_name in sheet_names:
            try:
                # Access the sheet
                sheet = spreadsheet.worksheet(sheet_name)
                # Get all records from the sheet
                data = sheet.get_all_records()
                # Convert to DataFrame
                df = pd.DataFrame(data)
                # Save to CSV
                csv_filename = f"{sheet_name}.csv"
                df.to_csv(csv_filename, index=False)
                # Append to the list
                all_data.append(df)
            except gspread.exceptions.WorksheetNotFound:
                if st:
                    st.warning(f"Sheet '{sheet_name}' not found in the Google Sheets document.")
                else:
                    print(f"Sheet '{sheet_name}' not found in the Google Sheets document.")
            except Exception as e:
                if st:
                    st.error(f"Error processing sheet '{sheet_name}': {e}")
                else:
                    print(f"Error processing sheet '{sheet_name}': {e}")

        # Combine all DataFrames into one
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            return combined_df
        else:
            if st:
                st.error("No data was extracted from any sheet.")
            else:
                print("No data was extracted from any sheet.")
            return pd.DataFrame()  # Return an empty DataFrame

    except Exception as e:
        if st:
            st.error(f"Error accessing Google Sheets: {e}")
        else:
            print(f"Error accessing Google Sheets: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error