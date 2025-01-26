import pandas as pd
import streamlit as st
import fetch_data  # Import your data fetching script

# Streamlit app logic
st.title("Ngee Ann Polytechnic Bus Arrival Information")
st.markdown("### Upcoming bus arrivals for the preselected bus stop:")

# Load data from Google Sheet using the separate script
data = fetch_data.extract_data_from_google_sheets(
    "https://docs.google.com/spreadsheets/d/1f58eqLkFr5nJ6bm5PZ3TbfUAxeSd1hpBspW9693kXv8/edit?usp=sharing",
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

    # Display data
    st.dataframe(data, use_container_width=True, height=400)
else:
    st.warning("No data available for the selected bus stop.")

st.markdown("---")
st.markdown("**Data refreshed periodically**")