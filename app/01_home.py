from datetime import datetime

import streamlit as st

current_date = datetime.today().strftime("%Y-%m-%d")
st.set_page_config(page_title="Home Page", page_icon=":lemon:", layout="wide")

hide_menu_style = "<style> footer {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("🏠 Home Page (placeholder)")
st.info("Ensure you read the SOPs before using this application", icon="ℹ️")

st.markdown("### Project Overview")
st.markdown("Name: **Incidents Management System**")
st.markdown(
    "Purpose: Automation of the process of identifying and resolving incidents in the production line, "
    "and to compensate the customer for the inconvenience caused."
)
st.markdown("Owner: Cameron Jones")
st.markdown("Emal: cameron.jones@hellofresh.co.uk")
st.markdown("StakeHolders: ")
st.markdown("* Ben Simmonds (Customer Experience Manager UK)")
st.markdown("* Stefan Platteau (Head of Customer Strategy & Analytics UK)")

st.markdown("## How to use this tool")
st.markdown("### 1. Production Data")
st.markdown(
    "This page allows you to query the production data from the DWH. You can select a date range and a recipe "
    "or addon number. The data will be displayed in a table and you can download it as a csv file."
)
st.markdown("### 2. Bulk Upload Tool")
