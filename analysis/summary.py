import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def summary():
    st.header('Summary')

   
    # Load word frequency data
    word_data = load_json_data('data/Word_Frequency_Summary_Alt.json')

    # Create a dictionary for word cloud
    word_dict = {item["Word"]: item["Count"] for item in word_data["Most_Common_Words"]}

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_dict)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
 # Overall Satisfaction
    st.subheader('Overall Satisfaction')
     # Overall Satisfaction Visualization
    overall_satisfaction_data = load_json_data('data/Comparative_Analysis-2.json')
    df_overall_satisfaction = pd.DataFrame.from_dict(overall_satisfaction_data['Role_Satisfaction_Comparison'], orient='index').reset_index()
    df_overall_satisfaction.columns = ['Role', 'Satisfaction Score']
    fig_overall_satisfaction = px.bar(df_overall_satisfaction, x='Role', y='Satisfaction Score', color='Role', title="Overall Satisfaction by Role")
    st.plotly_chart(fig_overall_satisfaction)

    # Role Satisfaction Comparison
    role_satisfaction_data = load_json_data('data/Comparative_Analysis-2.json')
    df_role_satisfaction = pd.DataFrame.from_dict(role_satisfaction_data['Role_Satisfaction_Comparison'], orient='index').reset_index()
    df_role_satisfaction.columns = ['Role', 'Average Satisfaction']
    fig_role_satisfaction = px.bar(df_role_satisfaction, x='Role', y='Average Satisfaction', color='Role', title="Role Satisfaction Comparison")
    st.plotly_chart(fig_role_satisfaction)

    # Nationality Satisfaction Comparison
    nationality_satisfaction_data = load_json_data('data/Comparative_Analysis-2.json')
    df_nationality_satisfaction = pd.DataFrame.from_dict(nationality_satisfaction_data['Nationality_Satisfaction_Comparison'], orient='index').reset_index()
    df_nationality_satisfaction.columns = ['Country', 'Average Satisfaction']
    fig_nationality_satisfaction = px.bar(df_nationality_satisfaction, x='Country', y='Average Satisfaction', color='Country', title="Nationality Satisfaction Comparison")
    st.plotly_chart(fig_nationality_satisfaction)

    # Continent Comparative Analysis
    continent_comparative_data = load_json_data('data/Continent_Comparative_Analysis.json')
    df_continent_comparative = pd.DataFrame.from_dict(continent_comparative_data['Residence_Continent'])
    fig_continent_comparative = px.line(df_continent_comparative, title="Continent Comparative Analysis")
    st.plotly_chart(fig_continent_comparative)

    # # Correlation Insights
    # correlation_insights_data = load_json_data('data/Correlation_Insights.json')
    # df_correlation_insights = pd.DataFrame(correlation_insights_data)
    # fig_correlation_insights = px.imshow(df_correlation_insights, title="Correlation Insights", color_continuous_scale='RdBu_r', aspect="auto")
    # st.plotly_chart(fig_correlation_insights)

    phrase_data = load_json_data('data/Phrase_Frequency_Summary.json')

    # Load phrase frequency data
    phrase_data = load_json_data('data/Phrase_Frequency_Summary.json')

    # Create a dictionary for word cloud
    phrase_dict = {item["Phrase"]: item["Count"] for item in phrase_data["Most_Common_Phrases"]}

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(phrase_dict)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.write("""Participants showed a high level of satisfaction with various aspects of the program's structure and content. Key components (after PCA analysis) such as technical accessibility, operational satisfaction, and the effectiveness of practical elements were especially well-received. However, satisfaction with the assessment of knowledge and academic rigor was slightly lower, particularly among some roles. While the overall feedback was positive, these areas highlight opportunities for further improvement to better meet the diverse needs of all participants.
             """)
    # Load the PCA Components Ranking by Role data
    pca_data = load_json_data('data/PCA_Components_Ranking_By_Role.json')
    
    # Prepare the DataFrame
    pca_records = []
    for role, components in pca_data.items():
        for component in components:
            pca_records.append({
                "Role": role,
                "PCA_Component": component["PCA_Component"],
                "Average_Score": component["Average_Score"],
                "Participant_Count": component["Participant_Count"]
            })
    
    df_pca = pd.DataFrame(pca_records)
    
    # Create the bar chart
    fig_pca = px.bar(
        df_pca,
        x="PCA_Component",
        y="Average_Score",
        color="Role",
        barmode="group",
        title="PCA Components Ranking by Role",
        hover_data=["Participant_Count"]
    )
    
    st.plotly_chart(fig_pca)

    # Practice Weeks Visualization
    st.subheader('Practice Weeks')
    st.write("""
    Practice weeks such as those with Partizan and Bayern Munich were highly rated, particularly by participants who found 
    the interaction and organization beneficial for their development.
    """)
    practice_weeks_data = load_json_data('data/Extended_Practice_Week_Ranking_By_Role.json')
    for role, data in practice_weeks_data.items():
        df = pd.DataFrame(data)
        fig = go.Figure(data=[
            go.Bar(name=role, x=df['Practice_Week'], y=df['Average_Score'])
        ])
        fig.update_layout(title_text=f'Practice Weeks Satisfaction - {role}', barmode='group')
        st.plotly_chart(fig)

    # Lessons and Exams Visualization
    st.subheader('Lessons and Exams')
    st.write("""
    Academic rigor and the effectiveness of lessons and exams were well-received, especially in key areas like Offensive 
    and Defensive Team Tactics. However, there was feedback about the need for clarity on the exams.
    """)
    data = load_json_data('data/Lessons_Exams_Ranking_By_Role.json')
    roles = list(data.keys())

    fig = go.Figure()

    for role in roles:
        df = pd.DataFrame(data[role])
        fig.add_trace(go.Bar(
            x=df['Lesson_Exam'],
            y=df['Average_Score'],
            name=role,
        ))

    fig.update_layout(
        title="Lessons and Exams Satisfaction by Role",
        xaxis_title="Lesson/Exam",
        yaxis_title="Average Satisfaction Score",
        barmode='group'
    )

    st.plotly_chart(fig)

    # Time Zones and Scheduling Visualization
    st.subheader('Time Zones and Scheduling')
    st.write("""
    Satisfaction with scheduling varied across different time zones. Participants from certain time zones expressed 
    challenges in attending sessions, particularly those outside the Central European Time (CET) zone. 
    Weekday evenings (CET) were the most popular times for participants.
    """)
    # Load the time zone data
    timezone_data = load_json_data('data/Time_Zone_Availability_Satisfaction_Analysis_v2.json')

    # Prepare the DataFrame
    df_timezones = pd.DataFrame({
        "Time Zone": list(timezone_data["Average_Satisfaction_By_Time_Zone"].keys()),
        "Satisfaction": list(timezone_data["Average_Satisfaction_By_Time_Zone"].values()),
        "Participants": [timezone_data["Time_Zone_Distribution"].get(zone, 0) for zone in timezone_data["Average_Satisfaction_By_Time_Zone"].keys()]
    })

    # Create the scatter plot
    fig_timezones = px.scatter(
        df_timezones, 
        x="Time Zone", 
        y="Satisfaction", 
        size="Participants", 
        color="Time Zone",
        title="Time Zone and Scheduling Satisfaction"
    )

    st.plotly_chart(fig_timezones)

    # Sentiment from Open-Ended Responses Visualization
    # st.subheader('Sentiment from Open-Ended Responses')
    # st.write("""
    # Participants were generally positive about the content and organization. However, there were suggestions for improving 
    # practical content, enhancing communication, and ensuring that scheduling accommodates a broader range of time zones.
    # """)
    # feedback_data = load_json_data('data/Expanded_Feedback_Summary_Final_v2.json')
    # df_feedback = pd.DataFrame(feedback_data)
    # fig_feedback = px.bar(df_feedback, x="Feedback Type", y="Count", color="Feedback Type", title="Feedback Summary")
    # st.plotly_chart(fig_feedback)

    # Sentiment from Open-Ended Responses Visualization
    st.subheader('Sentiment from Open-Ended Responses')
    st.write("""
    Participants' open-ended responses were generally positive, as indicated by the high polarity scores across most comments. However, there were some responses with neutral or slightly negative polarity, indicating areas where participants felt there could be improvements. The subjectivity scores show that most responses were personal opinions rather than objective statements, which is typical for feedback.
       """)

    # Load the sentiment analysis data
    sentiment_data = load_json_data('data/Sentiment_Analysis.json')

    # Create a summary of the average polarity and subjectivity for each category
    sentiment_summary = {
        "Category": [],
        "Average Polarity": [],
        "Average Subjectivity": []
    }

    categories = [
        "Please share any additional comments or suggestions about Application and Registration Process. ",
        "Please share any additional comments or suggestions about the Curriculum. ",
        "Please share any additional comments or suggestions about the Operational and Technical Aspects. ",
        "Please share any additional comments or suggestions about the Practice Weeks. ",
        "Please share any additional comments or suggestions about Networking. ",
        "Please share any additional comments or suggestions. "
    ]

    category_names = [
        "Application and Registration Process",
        "Curriculum",
        "Operational and Technical Aspects",
        "Practice Weeks",
        "Networking",
        "General Comments"
    ]

    for category, name in zip(categories, category_names):
        sentiment_summary["Category"].append(name)
        sentiment_summary["Average Polarity"].append(
            sum(sentiment_data[category]["polarity"]) / len(sentiment_data[category]["polarity"])
        )
        sentiment_summary["Average Subjectivity"].append(
            sum(sentiment_data[category]["subjectivity"]) / len(sentiment_data[category]["subjectivity"])
        )

    # Convert the summary to a DataFrame
    df_sentiment = pd.DataFrame(sentiment_summary)

    # Create a bar chart of the average polarity
    fig_polarity = px.bar(df_sentiment, x='Category', y='Average Polarity', color='Category', title="Sentiment Analysis - Polarity of Open-Ended Responses")
    st.plotly_chart(fig_polarity)

    # Create a bar chart of the average subjectivity
    fig_subjectivity = px.bar(df_sentiment, x='Category', y='Average Subjectivity', color='Category', title="Sentiment Analysis - Subjectivity of Open-Ended Responses")
    st.plotly_chart(fig_subjectivity)
