import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache_data
def load_cleaned_data():
    # Load the main demographics data
    CLEANED_DATA_FILENAME = Path(__file__).parent.parent / 'data' / 'Responses.json'
    return pd.read_json(CLEANED_DATA_FILENAME, lines=True)

@st.cache_data
def load_country_data():
    # Load the combined country-related data
    COUNTRY_DATA_FILENAME = Path(__file__).parent.parent / 'data' / 'final_combined_country_data.json'
    return pd.read_json(COUNTRY_DATA_FILENAME)

def demographics():
    df_cleaned = load_cleaned_data()
    country_data = load_country_data()

    # Handle empty "Played professional basketball?" as "No"
    df_cleaned['Played professional basketball?'] = df_cleaned['Played professional basketball?'].fillna("No")

    # Sidebar option for selecting the type of demographic data to display
    st.sidebar.header("Demographics Filters")
    view_option = st.sidebar.selectbox(
        "Choose the data to display:",
        ("Nationality", "Residence", "Federation", "Gender", "Years of Work", "Age", "Professional Experience", 
         "Coaching For", "Roles Taken", "Other Professions")
    )

    # Handle country-related data from final_combined_country_data.json
    if view_option in ["Nationality", "Residence", "Federation"]:
        if view_option == "Nationality":
            df_view = pd.DataFrame(country_data['nationality'].items(), columns=['Country', 'Count'])
            st.header('Nationality Distribution')
        elif view_option == "Residence":
            df_view = pd.DataFrame(country_data['residence'].items(), columns=['Country', 'Count'])
            st.header('Residence Distribution')
        elif view_option == "Federation":
            df_view = pd.DataFrame(country_data['related_federation'].items(), columns=['Country', 'Count'])
            st.header('Federation Distribution')

        # Display the world map visualization
        st.subheader('World Map Visualization')
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
                showcoastlines=True,  # Show coastlines
                showland=True,        # Show land even if no data
                landcolor="lightgray",
                projection_type='equirectangular'
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    elif view_option == "Gender":
        df_view = df_cleaned['Gender'].value_counts().reset_index()
        df_view.columns = ['Gender', 'Count']
        st.header('Gender Distribution')

    elif view_option == "Years of Work":
        if 'Coaching Since' in df_cleaned.columns:
            df_cleaned['Coaching Since'] = pd.to_datetime(df_cleaned['Coaching Since'], errors='coerce')
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
        df_view = df_cleaned['Played professional basketball?'].value_counts().reset_index()
        df_view.columns = ['Professional Experience', 'Count']
        st.header('Professional Experience Distribution')

    elif view_option == "Coaching For":
        df_view = df_cleaned['Coaching For'].value_counts().reset_index()
        df_view.columns = ['Coaching For', 'Count']
        st.header('Coaching For Distribution')

    elif view_option == "Roles Taken":
        df_view = df_cleaned['Role(s) Taken'].str.split(',').explode().value_counts().reset_index()
        df_view.columns = ['Roles Taken', 'Count']
        st.header('Roles Taken Distribution')

    elif view_option == "Other Professions":
        df_view = df_cleaned['Other Profession(s)'].dropna()
        text = ' '.join(df_view.tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        st.header('Word Cloud for Other Professions')
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    # Display the data table if it's not the Word Cloud visualization
    if view_option != "Other Professions":
        st.subheader('Data Table')
        st.dataframe(df_view)

    if view_option not in ["Nationality", "Residence", "Federation", "Other Professions"]:
        # Create a bar chart for other demographics
        st.subheader('Bar Chart Visualization')
        fig = px.bar(
            df_view,
            x=df_view.columns[0],
            y="Count",
            color="Count",
            color_continuous_scale=px.colors.sequential.YlGn,
            labels={df_view.columns[0]: view_option},
        )
        st.plotly_chart(fig, use_container_width=True)
