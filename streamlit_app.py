import pandas as pd
import streamlit as st  # Import Streamlit
import fetch_data  # Import your data fetching script

# Load data from Google Sheet using the separate script
data = fetch_data.fetch_data()

# Streamlit app logic
st.title("Ngee Ann Polytechnic Bus Arrival Information")
st.markdown("### Upcoming bus arrivals for the preselected bus stop:")

if not data.empty:
    # Sort data by EstimatedArrival
    data = data.sort_values(by='EstimatedArrival')

    # Format EstimatedArrival column
    if 'EstimatedArrival' in data.columns:  # Ensure column exists before formatting
        data['EstimatedArrival'] = pd.to_datetime(data['EstimatedArrival']).dt.strftime('%H:%M:%S')

    # Display data
    st.dataframe(data, use_container_width=True, height=400)
else:
    st.warning("No data available for the selected bus stop.")

st.markdown("---")
st.markdown("**Data refreshed periodically**")
