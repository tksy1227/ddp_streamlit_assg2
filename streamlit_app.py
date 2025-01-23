import pandas as pd 
import streamlit as st

data = pd.read_csv('DATA/ddp_data.csv')

# Create Streamlit UI
st.title("Ngee Ann Polytechnic Bus Arrival Information")
bus_stop_code = st.text_input("Enter Bus Stop Code (12101/12109):")

# Filter data
if bus_stop_code:
    filtered_data = data[data['BusStopCode'] == bus_stop_code]
else:
    filtered_data = data

# Display data
st.dataframe(filtered_data)