import pandas as pd
import streamlit as st
import time
import fetch_data

# Set page configuration
st.set_page_config(
    page_title="Ngee Ann Polytechnic Bus Arrival",
    page_icon="🚌",
    layout="wide"
)

# Initialize session state for auto-refresh
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    refresh_button = st.button("🔄 Refresh Data")
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("This app provides real-time bus arrival information for Ngee Ann Polytechnic.")

# Main content
st.title("🚌 Ngee Ann Polytechnic Bus Arrival Information")

# Image URLs
double_decker_image_url = "https://as2.ftcdn.net/v2/jpg/04/14/06/59/1000_F_414065974_Za4pTrRFns0pRqMAQKWoawFOCiE4Xs8w.jpg"
single_decker_image_url = "https://i.pinimg.com/originals/ef/e3/ba/efe3bae32ee3374180c6031a898a7f6b.jpg"
logo_url = "https://www.np.edu.sg/images/default-source/default-album/logo.png"

# Define the size for the bus images
image_width = 30
image_height = 30

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

    # Load data from Google Sheet
    data = fetch_data.extract_data_from_google_sheets(
        "https://docs.google.com/spreadsheets/d/1f58eqLkFr5nJ6bm5PZ3TbfUAxeSd1hpBspW9693kXv8/edit?usp=sharing",
        credentials,
        st
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

        # Validate the 'Type' column
        valid_bus_types = ["Single Deck", "Double Deck"]
        data['Type'] = data['Type'].apply(lambda x: x if x in valid_bus_types else "Single Deck")

        # Group data by ServiceNo
        grouped_data = data.groupby('ServiceNo')

        # Display data in cards
        st.markdown("---")
        for bus_number, group in grouped_data:
            # Get the next 3 arrivals for this bus
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
                    # Determine the color based on On Time status
                    color = "green" if row['On Time'] == 1 else "yellow"

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
                    # Create columns for horizontal layout
                    col1, col2, col3 = st.columns(3)
                    
                    for i, (_, row) in enumerate(next_arrivals.iterrows()):
                        # Determine which column to use based on the index
                        with col1 if i == 0 else col2 if i == 1 else col3:
                            # Determine the correct bus image URL based on the Type
                            current_bus_image = double_decker_image_url if row['Type'] == "Double Deck" else single_decker_image_url
                            
                            # Create a card for additional details
                            st.markdown(
                                f"""
                                <div style="
                                    border: 1px solid #ddd;
                                    border-radius: 10px;
                                    padding: 15px;
                                    margin: 10px 0;
                                    background-color: #f9f9f9;
                                ">
                                    <div style="
                                        border: 1px solid #ddd;
                                        border-radius: 10px;
                                        padding: 10px;
                                        margin: 5px 0;
                                        background-color: #fff;
                                    ">
                                        <h4>🚌 Arrival {i+1}</h4>
                                        <p><b>Feature:</b> {row['Feature']}</p>
                                        <p><b>Load:</b> {row['Load']}</p>
                                        <p><b>On Time:</b> {"✅ Yes" if row['On Time'] == 1 else "❌ No"}</p>
                                        <p><b>Type:</b> {row['Type']} <img src="{current_bus_image}" alt="Bus Icon" style="width:{image_width}px;height:{image_height}px;vertical-align:middle;margin-left:10px;"></p>
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
if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.rerun()