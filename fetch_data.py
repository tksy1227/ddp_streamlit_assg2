import gspread
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def extract_data_from_google_sheets(sheets_url, st=None):
    """
    Extracts data from a Google Sheets URL and saves each sheet as a CSV file.
    """
    try:
        # Define the scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Load credentials from Streamlit secrets
        credentials = {
            "type": st.secrets["google_credentials"]["type"],
            "project_id": st.secrets["google_credentials"]["project_id"],
            "private_key_id": st.secrets["google_credentials"]["private_key_id"],
            "private_key": st.secrets["google_credentials"]["private_key"],
            "client_email": st.secrets["google_credentials"]["client_email"],
            "client_id": st.secrets["google_credentials"]["client_id"],
            "auth_uri": st.secrets["google_credentials"]["auth_uri"],
            "token_uri": st.secrets["google_credentials"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["google_credentials"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["google_credentials"]["client_x509_cert_url"],
        }

        # Create credentials object
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)

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