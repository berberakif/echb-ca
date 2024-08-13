import streamlit as st
from analysis.demographics import demographics
from analysis.summary import summary
from analysis.recommendations import recommendations
from analysis.pca_analysis import pca_analysis 
from analysis.satisfaction_analysis import satisfaction_analysis
from analysis.comparative_analysis import comparative_analysis

# Define your username and password
USERNAME = "bche"
PASSWORD = "good2Change"

# Create a login form
st.title("EHCB CA - Feedback Report")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button and username == USERNAME and password == PASSWORD:
        st.session_state["logged_in"] = True
        st.sidebar.success("Logged in successfully")
    elif login_button:
        st.sidebar.error("Invalid username or password")
else:
    # If logged in, display the rest of the app
    st.sidebar.header("Navigate")
    section = st.sidebar.radio("Go to", ["Summary", "Demographics", "PCA Analysis", "Satisfaction Details", "Comparative Analysis", "Recommendations"])

    # Display the selected section with filtering
    if section == "Summary":
        summary()
    elif section == "Demographics":
        demographics()
    elif section == "PCA Analysis":
        pca_analysis() 
    elif section == "Satisfaction Details":
        satisfaction_analysis()
    elif section == "Comparative Analysis":
        comparative_analysis()
    elif section == "Recommendations":
        recommendations()

    # Add a logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.sidebar.empty()
