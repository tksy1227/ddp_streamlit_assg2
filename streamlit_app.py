import pandas as pd
import streamlit as st
import time  # Import the time module
import fetch_data  # Import your data fetching script

# Set page configuration
st.set_page_config(
    page_title="Ngee Ann Polytechnic Bus Arrival",
    page_icon="🚌",
    layout="wide"
)

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    refresh_button = st.button("🔄 Refresh Data")
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("This app provides real-time bus arrival information for Ngee Ann Polytechnic.")

# Main content
st.title("🚌 Ngee Ann Polytechnic Bus Arrival Information")
st.markdown("### Upcoming bus arrivals for the preselected bus stop:")

# Access Google Sheets credentials from Streamlit secrets
try:
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
        "universe_domain": st.secrets["google_credentials"]["universe_domain"],
    }

    # Load data from Google Sheet using the separate script
    data = fetch_data.extract_data_from_google_sheets(
        "https://docs.google.com/spreadsheets/d/1f58eqLkFr5nJ6bm5PZ3TbfUAxeSd1hpBspW9693kXv8/edit?usp=sharing",
        credentials,  # Pass the credentials
        st  # Pass the Streamlit object
    )

    # Display the data
    if not data.empty:
        # Convert 'EstimatedArrival' to datetime format
        if 'EstimatedArrival' in data.columns:
            data['EstimatedArrival'] = pd.to_datetime(data['EstimatedArrival'], format='%d/%m/%Y %H:%M')

        # Sort data by EstimatedArrival
        data = data.sort_values(by='EstimatedArrival')

        # Format EstimatedArrival column to display only time
        if 'EstimatedArrival' in data.columns:
            data['EstimatedArrival'] = data['EstimatedArrival'].dt.strftime('%H:%M:%S')

        # Group data by ServiceNo (bus number)
        grouped_data = data.groupby('ServiceNo')

        # Display data in cards with improved formatting
        st.markdown("---")
        for bus_number, group in grouped_data:
            # Get the next 3 arrivals for this bus (current + next 2)
            next_arrivals = group.head(3)

            # Create a card-like container for each bus
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 15px;
                        margin: 10px 0;
                        background-color: #f9f9f9;
                    ">
                        <h3>🚏 Bus {bus_number} - {next_arrivals.iloc[0]['Description']}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Display minutes left for the next 3 arrivals
                col1, col2, col3 = st.columns(3)
                for i, (_, row) in enumerate(next_arrivals.iterrows()):
                    # Determine the color based on Monitored status
                    color = "green" if row['Monitored'] == 1 else "yellow"

                    # Display minutes left for each arrival
                    with col1 if i == 0 else col2 if i == 1 else col3:
                        st.markdown(
                            f"""
                            <div style="
                                border: 1px solid #ddd;
                                border-radius: 10px;
                                padding: 10px;
                                margin: 5px;
                                background-color: #fff;
                            ">
                                <h4>Next Arrival {i+1}</h4>
                                <p><b>Minutes Left:</b> <span style='color:{color};'>{row['MinutesLeft']}</span></p>
                                <p><b>Arrival Time:</b> {row['EstimatedArrival']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                # Add a dropdown for additional details
                with st.expander(f"📄 View Additional Details for Bus {bus_number}"):
                    for _, row in next_arrivals.iterrows():
                        # Create a card for additional details
                        st.markdown(
                            f"""
                            <div style="
                                border: 1px solid #ddd;
                                border-radius: 10px;
                                padding: 10px;
                                margin: 5px 0;
                                background-color: #fff;
                            ">
                                <h4>🚌 Arrival Details</h4>
                                <div style="display: flex; justify-content: space-between;">
                                    <div style="flex: 1;">
                                        <p><b>Arrival Time:</b> {row['EstimatedArrival']}</p>
                                        <p><b>Feature:</b> {row['Feature']}</p>
                                    </div>
                                    <div style="flex: 1;">
                                        <p><b>Load:</b> {row['Load']}</p>
                                        <p><b>Monitored:</b> {"✅ Yes" if row['Monitored'] == 1 else "❌ No"}</p>
                                    </div>
                                    <div style="flex: 1;">
                                        <p><b>Type:</b> {row['Type']}</p>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            st.markdown("---")
    else:
        st.warning("No data available for the selected bus stop.")

except KeyError as e:
    st.error(f"Error accessing Google Sheets credentials: {e}")
except Exception as e:
    st.error(f"Error accessing Google Sheets: {e}")

# Footer
st.markdown("---")
st.markdown("**Data refreshed periodically**")
st.markdown("© 2023 Ngee Ann Polytechnic. All rights reserved.")

# Auto-refresh every 30 seconds
time.sleep(30)  # Wait for 30 seconds
st.experimental_rerun()  # Rerun the app to refresh the data