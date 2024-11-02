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

# Create a concatenated column for the filter
df['Age_Gender'] = df['Age'].astype(str) + " " + df['Gender']

# Set up the page with title and subtitle
st.title("Kingsway Little Athletics Club")
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
filtered_df = filtered_df[['Age_Gender', 'Event', 'Marshall Area', 'Status']]

# Display the dataframe
st.dataframe(filtered_df, use_container_width=True)

# Add a refresh button that clears the cache and refreshes the page
if st.button("Refresh"):
    st.cache_data.clear()  # Clear cached data
    st.experimental_set_query_params()  # Refresh the pagez