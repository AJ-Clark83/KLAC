# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:39:52 2024

@author: andrew.clark
"""

import streamlit as st

# Set page configuration to wide mode
st.set_page_config(layout="wide")

import pandas as pd
import requests

# Load the data from Google Sheets
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRBXEVC7gCD1n1JteAdB0I1JUbVCfH-vA6s8uJ1CHIJ4ALWF4dCh1NJk6oahJQlOGixibw3WlY21aIi/pub?gid=0&single=true&output=csv'
df = pd.read_csv(url)

# Display a logo at the top center of the page
st.markdown(
    """
    <style>
    .centered-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -50px; /* Adjusts the space above the logo */
    }
    </style>
    <div class="centered-logo">
        <img src="https://raw.githubusercontent.com/AJ-Clark83/KLAC/refs/heads/main/KLAC.jpg" alt="Kingsway Logo" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Create a concatenated column for the filter
df['Group'] = df['Age'].astype(str) + " " + df['Gender']

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

# Reorder columns to move Age_Gender to the first position and drop Age and Gender
filtered_df = filtered_df[['Group', 'Event', 'Marshalling Area', 'Status']]

# Display the dataframe
st.dataframe(filtered_df, hide_index=True, use_container_width=True)

# Custom CSS to style the button
st.markdown(
    """
    <style>
    /* Style the button */
    div.stButton > button {
        background-color: #A8CE3B;  /* Green color */
        color: black;  /* Black text */
        border: none;
        padding: 0.5em 1em;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
    }

    /* Button hover effect */
    div.stButton > button:hover {
        background-color: #082251;  /* Kingsway Blue hover */
        color: white;  /* white text */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add a refresh button that clears the cache and triggers a rerun
if st.button("Refresh"):
    st.cache_data.clear()  # Clear cached data
    st.session_state["refresh_trigger"] = not st.session_state.get("refresh_trigger", False)


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
if announcement and announcement.lower() != "hide":  # Check if content is not "hide"
    st.markdown("<hr style='border-top: 2px solid #082251; margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown(f"### 📢🍔 Canteen Specials\n{announcement}")
    st.markdown("<hr style='border-top: 2px solid #082251; margin: 20px 0;'>", unsafe_allow_html=True)
    
