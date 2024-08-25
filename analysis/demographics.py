import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


@st.cache_data
def load_cleaned_data():
    CLEANED_DATA_FILENAME = Path(
        __file__).parent.parent / 'data' / 'Responses.json'
    return pd.read_json(CLEANED_DATA_FILENAME, lines=True)


@st.cache_data
def load_country_data():
    COUNTRY_DATA_FILENAME = Path(
        __file__).parent.parent / 'data' / 'final_combined_country_data.json'
    return pd.read_json(COUNTRY_DATA_FILENAME)


def demographics():
    df_cleaned = load_cleaned_data()
    country_data = load_country_data()

    # Ensure missing values for "Played professional basketball?" are treated as "No"
    df_cleaned['Played professional basketball?'] = df_cleaned['Played professional basketball?'].fillna(
        "No")

    # 1. Nationality Distribution
    st.header('Nationality Distribution')
    df_view = pd.DataFrame(country_data['nationality'].items(), columns=[
                           'Country', 'Count'])
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
        title_text='Nationality Distribution by Country',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="lightgray",
            projection_type='equirectangular'
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 2. Residence Distribution
    st.header('Residence Distribution')
    df_view = pd.DataFrame(country_data['residence'].items(), columns=[
                           'Country', 'Count'])
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
        title_text='Residence Distribution by Country',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="lightgray",
            projection_type='equirectangular'
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 3. Federation Distribution
    st.header('Federation Distribution')
    df_view = pd.DataFrame(country_data['related_federation'].items(), columns=[
                           'Country', 'Count'])
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
        title_text='Federation Distribution by Country',
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="lightgray",
            projection_type='equirectangular'
        ),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 4. Gender Distribution
    st.header('Gender Distribution')
    df_view = df_cleaned['Gender'].value_counts().reset_index()
    df_view.columns = ['Gender', 'Count']
    fig = px.bar(
        df_view,
        x='Gender',
        y='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.YlGn,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 5. Years of Work Distribution
    st.header('Years of Work Distribution')
    if 'Coaching Since' in df_cleaned.columns:
        # Attempt to convert the 'Coaching Since' column from Unix timestamps
        df_cleaned['Coaching Since'] = pd.to_datetime(
            df_cleaned['Coaching Since'], unit='ms', errors='coerce')

        # Check if conversion was successful
        if df_cleaned['Coaching Since'].isnull().all():
            st.error(
                "Failed to convert any 'Coaching Since' values to dates. Please check the data format.")
        else:
            # Calculate years of work
            df_cleaned['Years of Work'] = (pd.to_datetime(
                'today') - df_cleaned['Coaching Since']).dt.days // 365

            # Handle any negative or erroneous values
            df_cleaned['Years of Work'] = df_cleaned['Years of Work'].where(
                df_cleaned['Years of Work'] >= 0, other=None)
            df_cleaned['Years of Work'] = df_cleaned['Years of Work'].fillna(
                0).astype(int)

            # Define custom bins for years of work
            bins = [0, 3, 5, 10, 15, 20, 30, 40, 50, 60, 70]
            labels = ['0-3 years', '3-5 years', '5-10 years', '10-15 years', '15-20 years',
                      '20-30 years', '30-40 years', '40-50 years', '50-60 years', '60-70 years']
            df_cleaned['Years of Work Range'] = pd.cut(
                df_cleaned['Years of Work'], bins=bins, labels=labels, include_lowest=True)

            # Count the occurrences in each range
            df_view = df_cleaned['Years of Work Range'].value_counts(
            ).reset_index()
            df_view.columns = ['Years of Work Range', 'Count']
            df_view = df_view.sort_values(by='Years of Work Range')

            # Create and display the bar chart
            fig = px.bar(
                df_view,
                x='Years of Work Range',
                y='Count',
                color='Count',
                color_continuous_scale=px.colors.sequential.YlGn,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_view)

    # 6. Age Distribution
    st.header('Age Distribution')
    if 'Birth Year' in df_cleaned.columns:
        df_cleaned['Age'] = pd.to_datetime(
            'today').year - df_cleaned['Birth Year']
        df_cleaned['Age'] = df_cleaned['Age'].fillna(0).astype(int)
        df_view = df_cleaned['Age'].value_counts(
            bins=10, sort=False).reset_index()
        df_view.columns = ['Age Range', 'Count']
        df_view['Age Range'] = df_view['Age Range'].astype(str)
        fig = px.bar(
            df_view,
            x='Age Range',
            y='Count',
            color='Count',
            color_continuous_scale=px.colors.sequential.YlGn,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df_view)

    # 7. Professional Experience Distribution
    st.header('Professional Experience Distribution')
    df_view = df_cleaned['Played professional basketball?'].value_counts(
    ).reset_index()
    df_view.columns = ['Professional Experience', 'Count']
    fig = px.bar(
        df_view,
        x='Professional Experience',
        y='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.YlGn,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 8. Coaching For Distribution
    st.header('Coaching For Distribution')
    df_view = df_cleaned['Coaching For'].value_counts().reset_index()
    df_view.columns = ['Coaching For', 'Count']
    fig = px.bar(
        df_view,
        x='Coaching For',
        y='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.YlGn,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 9. Roles Taken Distribution
    st.header('Roles Taken Distribution')
    df_view = df_cleaned['Role(s) Taken'].str.split(
        ',').explode().value_counts().reset_index()
    df_view.columns = ['Roles Taken', 'Count']
    fig = px.bar(
        df_view,
        x='Roles Taken',
        y='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.YlGn,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_view)

    # 10. Word Cloud for Other Professions
    st.header('Word Cloud for Other Professions')
    df_view = df_cleaned['Other Profession(s)'].dropna()
    text = ' '.join(df_view.tolist())
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
