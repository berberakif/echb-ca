import streamlit as st
from analysis.demographics import demographics, additional_visualizations
from analysis.key_findings import key_findings
from analysis.recommendations import recommendations
from analysis.pca_analysis import pca_analysis  # Import the new PCA analysis module

# Set up the Streamlit app
st.set_page_config(page_title='Comprehensive Report', page_icon=':bar_chart:')

# Sidebar navigation
st.sidebar.header("Navigate")
section = st.sidebar.radio("Go to", ["Demographics", "Key Findings", "Recommendations", "PCA Analysis"])

# Display the selected section with filtering
if section == "Demographics":
    demographics()
    additional_visualizations()
elif section == "Key Findings":
    key_findings()
elif section == "Recommendations":
    recommendations()
elif section == "PCA Analysis":
    pca_analysis() 


