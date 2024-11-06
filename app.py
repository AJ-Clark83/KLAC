# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:39:52 2024

@author: andrew.clark
"""

from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import requests

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Set the refresh interval in milliseconds
refresh_interval_ms = 10000  # 10 seconds

# Load the data from Google Sheets
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRBXEVC7gCD1n1JteAdB0I1JUbVCfH-vA6s8uJ1CHIJ4ALWF4dCh1NJk6oahJQlOGixibw3WlY21aIi/pub?gid=0&single=true&output=csv'
df = pd.read_csv(url)

# Create a concatenated "Group" column immediately
df['Group'] = df['Age'].astype(str) + " " + df['Gender']

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Program", "Display"])

if page == "Program":
    # Display a logo at the top center of the page
    st.markdown(
        """
        <style>
        .centered-logo {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: -50px;
        }
        </style>
        <div class="centered-logo">
            <img src="https://raw.githubusercontent.com/AJ-Clark83/KLAC/refs/heads/main/KLAC.jpg" alt="Kingsway Logo" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Set up the page with title and subtitle
    st.title("Kingsway Little Athletics Centre")
    st.subheader("Active Program")

    # Multi-select filter
    age_gender_options = df['Group'].unique()
    selected_age_gender = st.multiselect("Filter Events by Age and Gender (Group)", age_gender_options)

    # Filter the dataframe based on selection
    if selected_age_gender:
        filtered_df = df[df['Group'].isin(selected_age_gender)].copy()
    else:
        filtered_df = df.copy()  # Show all data if no filter is selected

    # Reorder columns to move Group to the first position
    filtered_df = filtered_df[['Group', 'Event', 'Marshalling Area', 'Status']]

    # Display the dataframe
    st.dataframe(filtered_df, hide_index=True, use_container_width=True)

    # Custom CSS to style the button
    st.markdown(
        """
        <style>
        /* Style the button */
        div.stButton > button {
            background-color: #A8CE3B;
            color: black;
            border: none;
            padding: 0.5em 1em;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color: #082251;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a refresh button that clears the cache and triggers a rerun
    if st.button("Refresh"):st.session_state["refresh_trigger"] = not st.session_state.get("refresh_trigger", False)

    # URL to the raw text file on GitHub
    text_file_url = "https://pastebin.com/raw/74635ARb"

    # Fetch announcement text from GitHub
    def fetch_announcement(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text.strip()  # Remove any surrounding whitespace
        except requests.exceptions.RequestException:
            st.error("Error fetching the announcement.")
            return None

    # Display the announcement if content is not "hide" (case-insensitive)
    announcement = fetch_announcement(text_file_url)
    if announcement and announcement.lower() != "hide":
        st.markdown("<hr style='border-top: 2px solid #082251; margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown(f"### 📢 Live Information:\n{announcement}")
        st.markdown("<hr style='border-top: 2px solid #082251; margin: 20px 0;'>", unsafe_allow_html=True)

elif page == "Display":
        
    # Autorefresh mechanism
    st_autorefresh(interval=refresh_interval_ms, key="display_autorefresh")
    
    # Refresh count logic for looping and data refresh
    if 'refresh_count' not in st.session_state:
        st.session_state['refresh_count'] = 0
    
    # Filter and process your DataFrame
    filtered_df = df[['Group', 'Event', 'Marshalling Area', 'Status']]
    display_df = filtered_df.copy()
    display_df['Marshalling Area'] = display_df['Marshalling Area'].str.replace('Marshalling', '')
    display_df['Status'] = display_df['Status'].str.replace('Event', '')
    display_df['Group'] = display_df['Group'].str.replace('Female', 'F')
    display_df['Group'] = display_df['Group'].str.replace('Male', 'M')
    display_df = display_df.rename(columns={"Marshalling Area": "Area"})
    
    # Split DataFrame into chunks of 6 rows
    chunk_size = 6
    chunks = [display_df[i:i + chunk_size] for i in range(0, len(display_df), chunk_size)]
    num_chunks = len(chunks)
    
    # Determine which chunk to display based on the refresh count
    current_chunk = st.session_state['refresh_count'] % num_chunks  # Cycle through chunks
    
    # Display the current chunk
    current_df = chunks[current_chunk]
    
    # Define custom CSS for the table
    st.markdown(
        """
        <style>
        .custom-table {
            font-family: 'Roboto', sans-serif;
            font-size: 55px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #082251;
            border-collapse: collapse;
            width: 75%;
            margin-top: -40px;
        }
        .custom-table th, .custom-table td {
            padding: 3px;
            border: 1px solid #A8CE3B;
        }
        .custom-table th {
            background-color: #A8CE3B;
            color: #082251;
            text-align: left;
        }
        .custom-table tr:nth-child(even) td {
            background-color: #0A2E47;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Convert current DataFrame chunk to HTML
    table_html = current_df.to_html(index=False, classes="custom-table")
    
    # Display styled table as HTML in Streamlit
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Update refresh count and reload data when loop completes
    st.session_state['refresh_count'] += 1
    
    # Reset refresh count to reload data at the start of a new loop
    if current_chunk == num_chunks - 1:
        st.session_state['refresh_count'] = 0



