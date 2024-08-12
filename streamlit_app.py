import streamlit as st
import pandas as pd
import json
import altair as alt
from pathlib import Path

# Set up the Streamlit app
st.set_page_config(page_title='Participant Distribution Dashboard', page_icon=':globe_with_meridians:')

# Function to load JSON data
@st.cache_data
def load_json_data(filename):
    DATA_FILENAME = Path(__file__).parent / 'data' / filename
    with open(DATA_FILENAME, 'r') as f:
        return json.load(f)

# Load the data
data = load_json_data('final_combined_country_data.json')

# Convert the JSON data into DataFrames for easier handling
df_nationality = pd.DataFrame(list(data['nationality'].items()), columns=['Country', 'Count'])
df_residence = pd.DataFrame(list(data['residence'].items()), columns=['Country', 'Count'])
df_federation = pd.DataFrame(list(data['related_federation'].items()), columns=['Country', 'Count'])

# App title
st.title(':globe_with_meridians: Participant Distribution Dashboard')

st.write("""
This dashboard shows the distribution of participants by their nationality, country of residence, 
and related federation. Use the filters to explore the data.
""")

# Sidebar for selecting the data to view
st.sidebar.header("Select Data to View")
view_option = st.sidebar.selectbox(
    "Choose the data to display:",
    ("Nationality", "Residence", "Related Federation")
)

# Select the appropriate DataFrame based on the user's choice
if view_option == "Nationality":
    df = df_nationality
elif view_option == "Residence":
    df = df_residence
else:
    df = df_federation

# Display the data and visualization
st.header(f'{view_option} Distribution')

st.subheader('Data Table')
st.dataframe(df)

st.subheader('Bar Chart')
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Country', sort='-y'),
    y='Count',
    tooltip=['Country', 'Count']
).properties(
    width=700,
    height=400
)
st.altair_chart(chart, use_container_width=True)

st.markdown("""
## Conclusion

This dashboard provides an overview of the distribution of participants by different categories. 
Use the insights to understand the geographic diversity and federation affiliations of participants.
""")
