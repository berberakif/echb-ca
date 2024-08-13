import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

@st.cache_data
def load_satisfaction_data():
    # Load the satisfaction data from the provided JSON file
    SATISFACTION_DATA_FILENAME = Path(__file__).parent.parent / 'data' / 'Responses.json'
    return pd.read_json(SATISFACTION_DATA_FILENAME, lines=True)

def satisfaction_analysis():
    df = load_satisfaction_data()

    # Sidebar for selecting the section/module
    st.sidebar.header("Satisfaction Analysis Sections")
    section = st.sidebar.selectbox(
        "Choose the section/module to analyze:",
        [
            "Application Process",
            "Practice Weeks",
            "Lessons",
            "Exams",
            "Time Zones & Scheduling",
            "Content Quality",
            "Interaction Quality",
            "Overall Program"
        ]
    )

    # Dynamic content based on selected section/module
    if section == "Application Process":
        st.header('Satisfaction with Application Process')

        # Clarity of Application Instructions
        st.subheader('Clarity of Application Instructions')
        df_clarity = df['How satisfied were you with the clarity of the application instructions? '].dropna()
        st.bar_chart(df_clarity.value_counts().sort_index())

        # Smoothness of Registration Process
        st.subheader('Smoothness of Registration Process')
        df_registration = df['How smooth was the registration process?'].dropna()
        st.bar_chart(df_registration.value_counts().sort_index())

        # Helpfulness of Initial Contact with Academy Staff
        st.subheader('Helpfulness of Initial Contact with Academy Staff')
        df_helpfulness = df['How helpful was the initial contact with the academy’s staff? '].dropna()
        st.bar_chart(df_helpfulness.value_counts().sort_index())

        # Clarity and Convenience of Payment Options
        st.subheader('Clarity and Convenience of Payment Options')
        df_payment = df['Were the payment options and processes clear and convenient?'].dropna()
        st.bar_chart(df_payment.value_counts().sort_index())

        # Satisfaction with the Price of the Academy
        st.subheader('Satisfaction with the Price of the Academy')
        df_price_satisfaction = df['Were you satisfied with the price of the Academy?'].dropna()
        st.bar_chart(df_price_satisfaction.value_counts().sort_index())

        # Suggested Price for the 5th Generation
        st.subheader('Suggested Price for the 5th Gen')
        df_price_suggestions = df['What would be your suggested price for the 5ht Gen. considering 8 modules and practice weeks?'].dropna()
        st.dataframe(df_price_suggestions.describe())

        # Criteria/Screening for New Participants
        st.subheader('Criteria/Screening for New Participants')
        df_screening = df['What criteria/screening would you recommend while admitting new participants into the EHCB CA?'].dropna()
        st.dataframe(df_screening.value_counts())

    elif section == "Practice Weeks":
        st.header('Satisfaction with Practice Weeks')
        # Add similar analysis for Practice Weeks
        # Add your specific code here...

    elif section == "Lessons":
        st.header('Satisfaction with Lessons')
        # Add similar analysis for Lessons
        # Add your specific code here...

    elif section == "Exams":
        st.header('Satisfaction with Exams')
        # Add similar analysis for Exams
        # Add your specific code here...

    elif section == "Time Zones & Scheduling":
        st.header('Satisfaction with Time Zones & Scheduling')
        # Add similar analysis for Time Zones & Scheduling
        # Add your specific code here...

    elif section == "Content Quality":
        st.header('Satisfaction with Content Quality')
        # Add similar analysis for Content Quality
        # Add your specific code here...

    elif section == "Interaction Quality":
        st.header('Satisfaction with Interaction Quality')
        # Add similar analysis for Interaction Quality
        # Add your specific code here...

    elif section == "Overall Program":
        st.header('Satisfaction with Overall Program')
        # Add similar analysis for Overall Program
        # Add your specific code here...
