import streamlit as st
from analysis.demographics import demographics
from analysis.key_findings import key_findings
from analysis.recommendations import recommendations

# Set up the Streamlit app
st.set_page_config(page_title='Comprehensive Report', page_icon=':bar_chart:')

# Sidebar navigation
st.sidebar.header("Navigate")
section = st.sidebar.radio("Go to", ["Demographics", "Key Findings", "Recommendations"])

# Display the selected section with filtering
if section == "Demographics":
    demographics()
elif section == "Key Findings":
    key_findings()
elif section == "Recommendations":
    recommendations()
