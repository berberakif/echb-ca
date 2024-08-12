import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Set up the Streamlit app
st.set_page_config(page_title='Feedback Descriptive Statistics', page_icon=':bar_chart:')

# Function to load the cleaned JSON data
@st.cache_data
def load_cleaned_data():
    DATA_FILENAME = Path(__file__).parent / 'Cleaned_Responses.json'
    with open(DATA_FILENAME, 'r') as f:
        data = [json.loads(line) for line in f]
    return pd.DataFrame(data)

# Load the data
df = load_cleaned_data()

# App title
st.title(':bar_chart: Feedback Descriptive Statistics')

# Sidebar for filtering options
st.sidebar.header("Filter Options")

# Filter by Role
roles = df['Role'].unique()
selected_roles = st.sidebar.multiselect("Select Roles:", roles, default=roles)

# Filter by Time Zone
time_zones = df['Which timezone do you live at?'].unique()
selected_time_zones = st.sidebar.multiselect("Select Time Zones:", time_zones, default=time_zones)

# Apply filters
filtered_df = df[df['Role'].isin(selected_roles) & df['Which timezone do you live at?'].isin(selected_time_zones)]

# Display filtered data
st.subheader('Filtered Data')
st.write(f"Number of responses: {len(filtered_df)}")
st.dataframe(filtered_df)

# Descriptive statistics
st.subheader('Descriptive Statistics')

# Numeric columns for descriptive stats
numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
selected_stat_cols = st.multiselect("Select Columns for Statistics:", numeric_cols, default=numeric_cols)

# Calculate and display descriptive stats
if selected_stat_cols:
    st.write(filtered_df[selected_stat_cols].describe())
else:
    st.write("Please select at least one numeric column to view descriptive statistics.")

# Visualize distribution of a selected column
st.subheader('Distribution of Selected Column')
selected_dist_col = st.selectbox("Select a Column for Distribution:", numeric_cols)

if selected_dist_col:
    st.bar_chart(filtered_df[selected_dist_col].value_counts())

st.markdown("""
## Conclusion

This section provides a quick overview of the data, allowing you to filter and explore descriptive statistics of participant feedback.
""")
