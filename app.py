# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 14:39:52 2024

@author: andrew.clark
"""

import streamlit as st
import pandas as pd

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
        margin-top: -60px; /* Adjusts the space above the logo */
    }
    </style>
    <div class="centered-logo">
        <img src="https://raw.githubusercontent.com/AJ-Clark83/KLAC/refs/heads/main/KLAC.jpg" alt="Kingsway Logo" width="150">
    </div>
    """,
    unsafe_allow_html=True
)


# Create a concatenated column for the filter
df['Age_Gender'] = df['Age'].astype(str) + " " + df['Gender']

# Set up the page with title and subtitle
st.title("Kingsway Little Athletics Centre")
st.subheader("Active Program")

# Multi-select filter
age_gender_options = df['Age_Gender'].unique()
selected_age_gender = st.multiselect("Select Age and Gender", age_gender_options)

# Filter the dataframe based on selection
if selected_age_gender:
    filtered_df = df[df['Age_Gender'].isin(selected_age_gender)].copy()
else:
    filtered_df = df.copy()  # Show all data if no filter is selected

# Reorder columns to move Age_Gender to the first position and drop Age and Gender
filtered_df = filtered_df[['Age_Gender', 'Event', 'Marshalling Area', 'Status']]

# Display the dataframe
st.dataframe(filtered_df, hide_index=True, use_container_width=True)

# Add a refresh button that clears the cache and triggers a rerun
if st.button("Refresh"):
    st.cache_data.clear()  # Clear cached data
    st.session_state["refresh_trigger"] = not st.session_state.get("refresh_trigger", False)  # Toggle state to force rerun