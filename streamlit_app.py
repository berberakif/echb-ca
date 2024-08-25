import streamlit as st
from analysis.demographics import demographics
from analysis.summary import summary
from analysis.recommendations import recommendations
from analysis.pca_analysis import pca_analysis
from analysis.satisfaction_analysis import satisfaction_analysis
from analysis.comparative_analysis import comparative_analysis
from analysis.open_ended_viewer import open_ended_viewer

# Retrieve the username and passwords from Streamlit secrets
USERNAME = st.secrets["STREAMLIT_USERNAME"]
PASSWORD = st.secrets["STREAMLIT_PASSWORD"]
GUEST_USERNAME = st.secrets["STREAMLIT_GUEST_USERNAME"]
GUEST_PASSWORD = st.secrets["STREAMLIT_GUEST_PASSWORD"]

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
        st.session_state["is_guest"] = False
        st.sidebar.success("Logged in successfully")
        st.experimental_rerun()
    elif login_button and username == GUEST_USERNAME and password == GUEST_PASSWORD:
        st.session_state["logged_in"] = True
        st.session_state["is_guest"] = True
        st.sidebar.success("Logged in as Guest")
        st.experimental_rerun()
    elif login_button:
        st.sidebar.error("Invalid username or password")
else:
    # Add a toggle switch for one-page view vs. sectioned view
    st.sidebar.header("Display Options")
    one_page_view = st.sidebar.checkbox(
        "Show all sections on one page", value=False)

    if one_page_view:
        # Show all sections on one page
        st.header("Summary")
        summary()

        st.header("Demographics")
        demographics()

        st.header("PCA Analysis")
        pca_analysis()

        st.header("Satisfaction Details")
        satisfaction_analysis()

        # st.header("Comparative Analysis")
        # comparative_analysis()

        # st.header("Recommendations")
        # recommendations()

        st.header("Feedback Viewer")
        open_ended_viewer()

    else:
        # Sectioned view
        st.sidebar.header("Navigate")
        section = st.sidebar.radio("Go to", ["Summary", "Demographics", "PCA Analysis",
                                             "Satisfaction Details", "Feedback Viewer"])

        # Display the selected section
        if section == "Summary":
            st.header("Summary")
            summary()
        elif section == "Demographics":
            st.header("Demographics")
            demographics()
        elif section == "PCA Analysis":
            st.header("PCA Analysis")
            pca_analysis()
        elif section == "Satisfaction Details":
            st.header("Satisfaction Details")
            satisfaction_analysis()
        # elif section == "Comparative Analysis":
        #     st.header("Comparative Analysis")
        #     comparative_analysis()
        # elif section == "Recommendations":
        #     st.header("Recommendations")
        #     recommendations()
        elif section == "Feedback Viewer":
            st.header("Feedback Viewer")
            open_ended_viewer()

    # Add a logout button
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()
