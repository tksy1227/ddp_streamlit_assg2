import pandas as pd
import streamlit as st

# Load data
data = pd.read_csv('DATA/ddp_data.csv')

# Convert BusStopCode to string
data['BusStopCode'] = data['BusStopCode'].astype(str)

# Convert EstimatedArrival to datetime for formatting
data['EstimatedArrival'] = pd.to_datetime(data['EstimatedArrival'])

# Streamlit UI
st.title("🚌 Ngee Ann Polytechnic Bus Arrival Information")
st.markdown("### Enter a bus stop code to view upcoming bus arrivals:")

# Dropdown for bus stop codes
bus_stop_code = st.selectbox("Select Bus Stop Code:", options=[""] + data['BusStopCode'].unique().tolist())

# Filter data
if bus_stop_code:
    filtered_data = data[data['BusStopCode'] == bus_stop_code]
    if not filtered_data.empty:
        # Sort data by EstimatedArrival
        filtered_data = filtered_data.sort_values(by='EstimatedArrival')

        # Format the EstimatedArrival column
        filtered_data['EstimatedArrival'] = filtered_data['EstimatedArrival'].dt.strftime('%H:%M:%S')

        # Display data
        st.dataframe(
            filtered_data,
            use_container_width=True,
            height=400  # Optional: Adjust table height
        )
    else:
        st.warning("No data available for the selected bus stop code.")
else:
    st.info("Please select a bus stop code to display results.")

# Optional: Add footer or last update info
st.markdown("---")
st.markdown("🔄 **Data refreshed periodically**")
