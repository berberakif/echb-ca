import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

@st.cache_data
def load_json_data(filename):
    with open(Path(__file__).parent.parent / filename, 'r') as f:
        return json.load(f)

def comparative_analysis():
    st.header('Comparative Analysis')

    # Load the comparative analysis data
    role_data = load_json_data('data/Role_Comparative_Analysis.json')
    age_group_data = load_json_data('data/Age_Group_Comparative_Analysis.json')
    continent_data = load_json_data('data/Continent_Comparative_Analysis.json')

    # Display Role Comparison
    st.subheader('Role-Based Satisfaction Comparison')
    df_role = pd.DataFrame(role_data)
    fig_role = px.bar(df_role, x=df_role.index, y=df_role.columns, barmode='group', title="Role-Based Satisfaction")
    st.plotly_chart(fig_role)

    # Display Age Group Comparison
    st.subheader('Age Group-Based Satisfaction Comparison')
    df_age_group = pd.DataFrame(age_group_data)
    fig_age_group = px.bar(df_age_group, x=df_age_group.index, y=df_age_group.columns, barmode='group', title="Age Group-Based Satisfaction")
    st.plotly_chart(fig_age_group)

    # Display Continent Comparison
    st.subheader('Continent-Based Satisfaction Comparison')
    df_continent = pd.DataFrame(continent_data)
    fig_continent = px.bar(df_continent, x=df_continent.index, y=df_continent.columns, barmode='group', title="Continent-Based Satisfaction")
    st.plotly_chart(fig_continent)
