import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

@st.cache_data
def load_cleaned_data():
    # Load the main demographics data
    CLEANED_DATA_FILENAME = Path(__file__).parent.parent / 'data' / 'Responses.json'
    return pd.read_json(CLEANED_DATA_FILENAME, lines=True)

def demographics():
    df_cleaned = load_cleaned_data()

    # Sidebar option for selecting the type of demographic data to display
    st.sidebar.header("Demographics Filters")
    view_option = st.sidebar.selectbox(
        "Choose the data to display:",
        ("Nationality", "Residence", "Gender", "Years of Work", "Age", "Professional Experience")
    )

    # Handle country-related data
    if view_option == "Nationality":
        df_view = df_cleaned['Nationality'].value_counts().reset_index()
        df_view.columns = ['Country', 'Count']
        st.header('Nationality Distribution')

    elif view_option == "Residence":
        df_view = df_cleaned['Residence'].value_counts().reset_index()
        df_view.columns = ['Country', 'Count']
        st.header('Residence Distribution')

    # Handle other demographics data from Responses.json
    elif view_option == "Gender":
        df_view = df_cleaned['Gender'].value_counts().reset_index()
        df_view.columns = ['Gender', 'Count']
        st.header('Gender Distribution')

    elif view_option == "Years of Work":
        if 'Coaching Since' in df_cleaned.columns:
            df_cleaned['Coaching Since'] = pd.to_datetime(df_cleaned['Coaching Since'], unit='ms', errors='coerce')
            df_cleaned['Years of Work'] = (pd.to_datetime('today') - df_cleaned['Coaching Since']).dt.days // 365
            df_cleaned['Years of Work'] = df_cleaned['Years of Work'].fillna(0).astype(int)
            df_view = df_cleaned['Years of Work'].value_counts(bins=10, sort=False).reset_index()
            df_view.columns = ['Years of Work Range', 'Count']
            df_view['Years of Work Range'] = df_view['Years of Work Range'].astype(str)  # Convert intervals to strings
            st.header('Years of Work Distribution')
        else:
            st.error('Column "Coaching Since" not found.')

    elif view_option == "Age":
        if 'Birth Year' in df_cleaned.columns:
            df_cleaned['Age'] = pd.to_datetime('today').year - df_cleaned['Birth Year']
            df_cleaned['Age'] = df_cleaned['Age'].fillna(0).astype(int)
            df_view = df_cleaned['Age'].value_counts(bins=10, sort=False).reset_index()
            df_view.columns = ['Age Range', 'Count']
            df_view['Age Range'] = df_view['Age Range'].astype(str)  # Convert intervals to strings
            st.header('Age Distribution')
        else:
            st.error('Column "Birth Year" not found.')

    elif view_option == "Professional Experience":
        if 'Played professional basketball?' in df_cleaned.columns:
            df_cleaned['Played professional basketball?'] = df_cleaned['Played professional basketball?'].fillna("No")
            df_view = df_cleaned['Played professional basketball?'].value_counts().reset_index()
            df_view.columns = ['Professional Experience', 'Count']
            st.header('Professional Experience Distribution')
        else:
            st.error('Column "Played professional basketball?" not found.')

    # Display the selected data and visualization
    st.subheader('Data Table')
    st.dataframe(df_view)

    st.subheader('World Map Visualization' if view_option in ["Nationality", "Residence"] else 'Bar Chart Visualization')

    if view_option in ["Nationality", "Residence"]:
        # Create the choropleth map for Nationality and Residence
        fig = px.choropleth(
            df_view,
            locations="Country",
            locationmode="country names",
            color="Count",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.YlGn,
            labels={'Count': 'Participant Count'},
        )
        fig.update_geos(showcoastlines=True, coastlinecolor="Black")
        fig.update_layout(
            title_text=f'{view_option} Distribution by Country',
            title_x=0.5,
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Create a bar chart for other demographics
        fig = px.bar(
            df_view,
            x=df_view.columns[0],
            y="Count",
            color="Count",
            color_continuous_scale=px.colors.sequential.YlGn,
            labels={df_view.columns[0]: view_option},
        )
        st.plotly_chart(fig, use_container_width=True)

