import pandas as pd
import fetch_data  # Import your data fetching script

# Load data from Google Sheet using the separate script
data = fetch_data.fetch_data()

# ... rest of your Streamlit app logic using the loaded data 'df'

# old code
import streamlit as st
data = pd.read_csv('data/ddp_data.csv')
data['BusStopCode'] = data['Bus StopCode'].astype(str)
data['EstimatedArrival'] = pd.to_datetime(data['EstimatedArrival'])

st.title("Ngee Ann Polytechnic Bus Arrival Information")
st.markdown("### Enter a bus stop code to view upcoming bus arrivals:")
bus_stop_code = st.text_input("Enter Bus Stop Code:")

if bus_stop_code:
    filtered_data = data[data['BusStopCode'] == bus_stop_code]
    if not filtered_data.empty:
        # Sort data by EstimatedArrival
        filtered_data = filtered_data.sort_values(by='EstimatedArrival')

        # Format EstimatedArrival column
        filtered_data['EstimatedArrival'] = filtered_data['EstimatedArrival'].dt.strftime('%H:%M:%S')

        # Display data
        st.dataframe(filtered_data, use_container_width=True, height=400)
    else:
        st.warning("No data available for the selected bus stop code.")
else:
    st.info("Please enter a bus stop code to display results.")


st.markdown("---")
st.markdown("**Data refreshed periodically**")