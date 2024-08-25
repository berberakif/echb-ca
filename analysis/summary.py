import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from pathlib import Path


def load_json_data(filename):
    """Helper function to load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)


def summary():
    # Phrase Frequency Analysis and Word Cloud Visualization
    phrase_data = load_json_data('data/Phrase_Frequency_Summary.json')

    # Create a dictionary for word cloud
    phrase_dict = {item["Phrase"]: item["Count"]
                   for item in phrase_data["Most_Common_Phrases"]}

    # Generate and display the word cloud
    wordcloud = WordCloud(
        width=800, height=400, background_color='white').generate_from_frequencies(phrase_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.write("""
    Overall, participants expressed satisfaction with the EHCB Coaches Academy, appreciating the practical content and smooth interactions with staff. However, there are a few areas where improvements could make a difference:

    - **Scheduling Flexibility:** Offering more session times could better accommodate participants from various time zones, ensuring everyone can attend lessons conveniently.
    - **Enhancing Practical Components:** Expanding practical sessions and real-world interactions, especially during practice weeks, could further enrich the learning experience.
    - **Clarifying Exams:** Content and the way of exams should be re-considered in a way to make them more practical and efficient.
    - **Improving Communication:** Strengthening communication channels, particularly in WhatsApp groups, will ensure that all participants feel supported and informed.
    - **Maintaining High-Quality Content:** Continuing to deliver high-quality academic and practical content, while regularly gathering feedback, will keep the curriculum aligned with participants' needs.

    Addressing these areas could further elevate the overall experience for everyone involved.
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
    st.subheader('Overall Satisfaction')
    # Load overall satisfaction data
    overall_satisfaction_data = load_json_data(
        'data/Comparative_Analysis-2.json')

    # Overall Satisfaction by Role
    df_overall_satisfaction = pd.DataFrame.from_dict(
        overall_satisfaction_data['Role_Satisfaction_Comparison'], orient='index').reset_index()
    df_overall_satisfaction.columns = ['Role', 'Satisfaction Score']
    fig_overall_satisfaction = px.bar(df_overall_satisfaction, x='Role',
                                      y='Satisfaction Score', color='Role', title="Overall Satisfaction by Role")
    st.plotly_chart(fig_overall_satisfaction)

    # Nationality Satisfaction Comparison
    df_nationality_satisfaction = pd.DataFrame.from_dict(
        overall_satisfaction_data['Nationality_Satisfaction_Comparison'], orient='index').reset_index()
    df_nationality_satisfaction.columns = ['Country', 'Average Satisfaction']
    # Calculate the overall average satisfaction score
    overall_avg_satisfaction = df_nationality_satisfaction['Average Satisfaction'].mean(
    )

    # Create the bar chart
    fig_nationality_satisfaction = px.bar(df_nationality_satisfaction,
                                          x='Country',
                                          y='Average Satisfaction',
                                          color='Country',
                                          title="Nationality Satisfaction Comparison")

    # Add a horizontal line representing the overall average satisfaction
    fig_nationality_satisfaction.add_shape(
        type="line",
        # Extend the line across the entire x-axis
        x0=-0.5, x1=len(df_nationality_satisfaction)-0.5,
        # Set the y position at the average satisfaction
        y0=overall_avg_satisfaction, y1=overall_avg_satisfaction,
        # Style the line (color, thickness, dash pattern)
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add the average value as annotation
    fig_nationality_satisfaction.add_annotation(
        # Position it at the end of the plot
        x=len(df_nationality_satisfaction)-1,
        y=overall_avg_satisfaction,
        text=f"Overall Average: {overall_avg_satisfaction:.2f}",
        showarrow=False,
        yshift=10,
        font=dict(color="red")
    )

    # Show the plot in Streamlit
    st.plotly_chart(fig_nationality_satisfaction)

  # Load and prepare the data
    continent_comparative_data = load_json_data(
        'data/continent_component_analysis.json')
    df_continent_comparative = pd.DataFrame(continent_comparative_data)
    df_continent_comparative = df_continent_comparative.reset_index().melt(
        id_vars='index', var_name='Continent', value_name='Score')
    df_continent_comparative.rename(
        columns={'index': 'Component'}, inplace=True)

    # Calculate the overall average score
    overall_avg_score = df_continent_comparative['Score'].mean()

    # Create the bar chart
    fig_continent_comparative = px.bar(
        df_continent_comparative,
        x='Component',
        y='Score',
        color='Continent',
        barmode='group',
        hover_data=['Continent', 'Score'],
        labels={'Score': 'Average Score', 'Component': 'Component'},
        title="Component Scores by Continent"
    )

    # Add a horizontal line representing the overall average score
    fig_continent_comparative.add_shape(
        type="line",
        # Extend across the entire x-axis
        x0=-0.5, x1=len(df_continent_comparative['Component'].unique()) - 0.5,
        # Set the y position at the average score
        y0=overall_avg_score, y1=overall_avg_score,
        # Style the line (color, thickness, dash pattern)
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add the average value as annotation
    fig_continent_comparative.add_annotation(
        # Position at the end of the plot
        x=len(df_continent_comparative['Component'].unique()) - 1,
        y=overall_avg_score,
        text=f"Overall Average: {overall_avg_score:.2f}",
        showarrow=False,
        yshift=10,
        font=dict(color="red")
    )

    # Update layout settings
    fig_continent_comparative.update_layout(
        xaxis_title="Component",
        yaxis_title="Average Score",
        legend_title="Continent",
        xaxis_tickangle=-45,
        title_x=0.5,
        height=600,
        width=1000
    )

    # Display the chart
    st.plotly_chart(fig_continent_comparative, use_container_width=True)

    # Practice Weeks Visualization
    st.subheader('Practice Weeks')
    st.write("""
    Practice weeks such as those with Partizan and Bayern Munich were highly rated, particularly by participants who found 
    the interaction and organization beneficial for their development.
    """)
    practice_weeks_data = load_json_data(
        'data/Extended_Practice_Week_Ranking_By_Role.json')

    for role, data in practice_weeks_data.items():
        df = pd.DataFrame(data)

        # Calculate the overall average score
        average_score = df['Average_Score'].mean()

        # Create the bar chart
        fig = go.Figure(data=[
            go.Bar(name=role, x=df['Practice_Week'], y=df['Average_Score'])
        ])

        # Add a horizontal line representing the average score
        fig.add_shape(
            type="line",
            # full width of the x-axis
            x0=-0.5, x1=len(df['Practice_Week'])-0.5,
            y0=average_score, y1=average_score,
            line=dict(color="red", width=2, dash="dash"),
        )

        # Update the layout with title, y-axis range, and other settings
        fig.update_layout(
            title_text=f'Practice Weeks Satisfaction - {role}',
            barmode='group',
            yaxis=dict(range=[3.3, 4.8]),
            shapes=[dict(
                type="line",
                xref="paper", x0=0, x1=1,
                yref="y", y0=average_score, y1=average_score,
                line=dict(color="red", width=2, dash="dash"),
            )]
        )

        # Show the plot
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
   # Initialize a DataFrame to count preferences for each day/time slot
    all_days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_times = pd.date_range(
        "08:00", "22:00", freq="H").strftime('%H:%M').tolist()

    # Create an empty DataFrame to store the counts
    preference_counts = pd.DataFrame(0, index=all_times, columns=all_days)
    SATISFACTION_DATA_FILENAME = Path(
        __file__).parent.parent / 'data' / 'Responses.json'
    df_all = pd.read_json(SATISFACTION_DATA_FILENAME, lines=True)

    # Iterate over each row to update the counts
    for idx, row in df_all.iterrows():
        preferred_days = row['Which days did you prefer the lessons the most?']
        weekday_times = row.get(
            'On weekdays, which time period fitted you the most? [Central European Time]')
        weekend_times = row.get(
            'At weekends, which time period fitted you the most? [Central European Time]')

        # Split the days and times into lists
        if pd.notna(preferred_days):
            days_list = [day.strip() for day in preferred_days.split(',')]

            # Update weekday counts
            if weekday_times and any(day in all_days[:5] for day in days_list):
                times_list = [time.strip()
                              for time in weekday_times.split(',')]
                for day in days_list:
                    if day in all_days[:5]:  # Only consider weekdays
                        for time in times_list:
                            # Extract the start time (e.g., '19:00' from '19:00 - 21:00')
                            start_time = time.split('-')[0].strip()
                            if start_time in all_times and day in all_days:
                                preference_counts.at[start_time, day] += 1
                            # else:
                            #    st.write(
                            #        f"Skipped invalid time or day: {start_time} {day}")

            # Update weekend counts
            if weekend_times and any(day in all_days[5:] for day in days_list):
                times_list = [time.strip()
                              for time in weekend_times.split(',')]
                for day in days_list:
                    if day in all_days[5:]:  # Only consider weekends
                        for time in times_list:
                            start_time = time.split('-')[0].strip()
                            if start_time in all_times and day in all_days:
                                preference_counts.at[start_time, day] += 1
                            # else:
                            #     st.write(
                            #         f"Skipped invalid time or day: {start_time} {day}")

    # Plot the heatmap for the combined week
    fig_heatmap = px.imshow(preference_counts,
                            labels=dict(x="Day", y="Time Slot",
                                        color="Participants"),
                            x=preference_counts.columns,
                            y=preference_counts.index,
                            color_continuous_scale=["red", "yellow", "green"],
                            title="Heatmap of Most Convenient Time Slots/Days for Lessons")

    st.plotly_chart(fig_heatmap)

    # Load the time zone data
    timezone_data = load_json_data(
        'data/Time_Zone_Availability_Satisfaction_Analysis_v2.json')

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
            sum(sentiment_data[category]["polarity"]) /
            len(sentiment_data[category]["polarity"])
        )
        sentiment_summary["Average Subjectivity"].append(
            sum(sentiment_data[category]["subjectivity"]) /
            len(sentiment_data[category]["subjectivity"])
        )

    # Convert the summary to a DataFrame
    df_sentiment = pd.DataFrame(sentiment_summary)

    # Create a bar chart of the average polarity
    fig_polarity = px.bar(df_sentiment, x='Category', y='Average Polarity',
                          color='Category', title="Sentiment Analysis - Polarity of Open-Ended Responses")
    st.plotly_chart(fig_polarity)

    # Create a bar chart of the average subjectivity
    fig_subjectivity = px.bar(df_sentiment, x='Category', y='Average Subjectivity',
                              color='Category', title="Sentiment Analysis - Subjectivity of Open-Ended Responses")
    st.plotly_chart(fig_subjectivity)
    # Load the open-ended responses CSV file
    df_open_ended = pd.read_csv('data/open_ended_all_responses.csv')

    # Define questions with their corresponding column names
    questions = {
        "Application and Registration Process": "additional_comments_or_suggestions_about_Application_and_Registration_Process.csv",
        "Curriculum": "additional_comments_or_suggestions_about_the_Curriculum.csv",
        "Networking": "additional_comments_or_suggestions_about_Networking.csv",
        "Bonus Lectures": "additional_comments_or_suggestions_about_the_Bonus_Lectures.csv",
        "Operational and Technical Aspects": "additional_comments_or_suggestions_about_the_Operational_and_Technical_Aspects.csv",
        "Practice Weeks": "additional_comments_or_suggestions_about_the_Practice_Weeks.csv",
        "Schedule and Attendance": "additional_comments_or_suggestions_about_the_Schedule_and_Attandance.csv",
        "General Suggestions": "additional_comments_or_suggestions.csv",
        "Should Exams be Part of the Curriculum?": "should_exams_be_part_of_the_curriculum.csv",
        "Criteria/Screening for New Participants": "screening_criteria.csv",
        "What Helped You Decide to Sign Up?": "decision_to_sign.csv",
        "Preferred Content from EHCB Members": "members_content.csv",
        "Preferred Interactivity from Professors": "what-kind-of-interactivity.csv",
        "Suggested Price for 5th Gen": "suggested-price.csv",
        "Module/Lesson to Add to the Curriculum": "what-to-add-for-curriculum.csv"
    }

    # Perform sentiment analysis on each column
    sentiment_data = {}
    for question, column in questions.items():
        # Ensure only string values are processed
        df_open_ended['text'] = df_open_ended[column].astype(str)

        df_open_ended['polarity'] = df_open_ended['text'].apply(
            lambda x: TextBlob(x).sentiment.polarity if x.strip() else None)
        df_open_ended['subjectivity'] = df_open_ended['text'].apply(
            lambda x: TextBlob(x).sentiment.subjectivity if x.strip() else None)

        # Filter out None values before calculating the mean
        sentiment_data[question] = {
            "polarity": df_open_ended['polarity'].dropna().mean(),
            "subjectivity": df_open_ended['subjectivity'].dropna().mean()
        }

    # Convert the sentiment data to a DataFrame for visualization
    df_sentiment = pd.DataFrame(sentiment_data).T.reset_index()
    df_sentiment.columns = ['Category',
                            'Average Polarity', 'Average Subjectivity']

    # Visualize the sentiment polarity
    st.subheader('Sentiment Analysis - Polarity by Question')
    st.write("""
    This section presents the average polarity scores for specific open-ended questions, indicating how positive or negative the responses were.
    """)
    fig_polarity = px.bar(df_sentiment, x='Category', y='Average Polarity',
                          color='Category', title="Sentiment Polarity by Category")
    st.plotly_chart(fig_polarity)

    # Visualize the sentiment subjectivity
    st.subheader('Sentiment Analysis - Subjectivity by Question')
    st.write("""
    This section displays the average subjectivity scores for specific open-ended questions, indicating how much of the feedback is based on personal opinions.
    """)
    fig_subjectivity = px.bar(df_sentiment, x='Category', y='Average Subjectivity',
                              color='Category', title="Sentiment Subjectivity by Category")
    st.plotly_chart(fig_subjectivity)
