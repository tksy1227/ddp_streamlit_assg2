import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def extract_data_from_google_sheets(sheets_url, credentials, st=None):
    """
    Extracts data from a Google Sheets URL and saves each sheet as a CSV file.
    """
    try:
        # Define the scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Create credentials object
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)

        # Authorize the client
        client = gspread.authorize(creds)

        # Extract the Google Sheet ID from the URL
        sheet_id = sheets_url.split("/d/")[1].split("/")[0]

        # Open the Google Sheets document by ID
        spreadsheet = client.open_by_key(sheet_id)

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