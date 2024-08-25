import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json


@st.cache_data
def load_satisfaction_data():
    # Load the satisfaction data from the provided JSON file
    SATISFACTION_DATA_FILENAME = Path(
        __file__).parent.parent / 'data' / 'Responses.json'
    return pd.read_json(SATISFACTION_DATA_FILENAME, lines=True)


def satisfaction_analysis():
    df = load_satisfaction_data()

    # 1. Application Process
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
    df_price_satisfaction = df['Were you satisfied with the price of the Academy?'].dropna(
    )
    st.bar_chart(df_price_satisfaction.value_counts().sort_index())

    # Suggested Price for the 5th Generation
    st.subheader('Suggested Price for the 5th Gen')
    df_price_suggestions = df['What would be your suggested price for the 5ht Gen. considering 8 modules and practice weeks?'].dropna()

    # Visualizing the distribution with a box plot
    fig_price_box = px.box(df_price_suggestions, y=df_price_suggestions, title="Distribution of Suggested Prices for 5th Gen",
                           labels={"y": "Suggested Price"}, points="all")
    st.plotly_chart(fig_price_box)

    # Displaying summary statistics
    st.write("Summary Statistics:")
    st.write(df_price_suggestions.describe())

    # Criteria/Screening for New Participants
    st.subheader('Criteria/Screening for New Participants')
    df_screening = df['What criteria/screening would you recommend while admitting new participants into the EHCB CA?'].dropna()

    # Visualizing the counts with a horizontal bar chart
    df_screening_count = df_screening.value_counts().reset_index()
    df_screening_count.columns = ['Criteria', 'Count']

    fig_screening_bar = px.bar(df_screening_count, x='Count', y='Criteria',
                               orientation='h', title="Recommended Criteria for Screening New Participants")
    st.plotly_chart(fig_screening_bar)

    # 2. Practice Weeks
    # Satisfaction with Practice Weeks
    st.header('Satisfaction with Practice Weeks')

    # Practice Weeks Joined
    st.subheader('Which Practice Week Have You Joined?')
    df_practice_weeks = df['Which practice week have you joined'].dropna()
    st.bar_chart(df_practice_weeks.value_counts().sort_index())

    # Organization of Practice Week with EuroLeague Teams
    st.subheader(
        'How well-organized was the practice week with EuroLeague teams?')
    df_organization = df['How well-organized was the practice week with EuroLeague teams?'].dropna()
    st.bar_chart(df_organization.value_counts().sort_index())

    # Benefit for Coaching Development
    st.subheader(
        'How beneficial was the practice week for your coaching development?')
    df_benefit = df['How beneficial was the practice week for your coaching development?'].dropna()
    st.bar_chart(df_benefit.value_counts().sort_index())

    # Interaction with Coaches
    st.subheader(
        'How satisfactory was your interaction with the coaches of the practice week team?')
    df_interaction = df['How satisfactory was your interaction with the coaches of the practice week team? '].dropna()
    st.bar_chart(df_interaction.value_counts().sort_index())

    # Effectiveness of Practice Week Presentations
    st.subheader('How effective were the practice week presentations?')
    df_presentations = df['How effective were the practice week presentations?'].dropna(
    )
    st.bar_chart(df_presentations.value_counts().sort_index())

    # Out-of-Court Experiences in the City of the Practice Week
    st.subheader(
        'How would you rate the out-of-court experiences in the city of the practice week?')
    df_out_of_court = df['How would you rate the out-of-court experiences in the city of the practice week?'].dropna()
    st.bar_chart(df_out_of_court.value_counts().sort_index())

    # # Support for Operational Aspects of the Practice Week
    # st.subheader(
    #     'Please rate the support provided for operational aspects of the practice week (travel, accommodation, guidance etc.)')
    # df_operational_support = df['Please rate the support provided for operational aspects of the practice week (travel, accommodation, guidance etc.)'].dropna(
    # )
    # st.bar_chart(df_operational_support.value_counts().sort_index())
    st.header('Satisfaction with Lessons')

    # 4. Lessons
    st.header('Satisfaction with Lessons')

    # Question-by-Question Details
    st.subheader('Effectiveness of Lessons by Module')
    lessons_columns = [
        'How effective were the lessons on Offensive Team Tactic?',
        'How effective were the lessons on Defensive Team Tactic? ',
        'How effective were the lessons on Individual and Group Tactics? ',
        'How effective were the lessons on Basketball Technique? ',
        'How effective were the lessons on Planning & Programming and S&C?',
        'How effective were the lessons on Selection and Training of Young Players?',
        'How effective were the lessons on Basketball History and Factors? ',
        'How effective were the lessons on Theory of Sports Training and S&C? ',
        'How effective were the lessons on Sociology & Psychology?',
        'How effective were the lessons on Human Motoric? ',
        'How effective were the lessons on Biomedicine Subjects?'
    ]

    for lesson in lessons_columns:
        st.subheader(lesson)
        lesson_counts = df[lesson].value_counts().sort_index()
        fig_lesson = px.bar(lesson_counts, x=lesson_counts.index, y=lesson_counts.values,
                            labels={'x': 'Rating', 'y': 'Count'}, title=f'Distribution of Ratings for {lesson}')
        st.plotly_chart(fig_lesson)

    # Suggested Modules
    st.subheader('Suggested Modules to Add')
    df_suggestions = df['Which module/lesson would you like to add to the curriculum?'].dropna()
    suggestions_wordcloud = WordCloud(
        background_color='white').generate(' '.join(df_suggestions))
    plt.figure(figsize=(10, 5))
    plt.imshow(suggestions_wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # 5. Exams
    st.header('Satisfaction with Exams')

    # Question-by-Question Details
    st.subheader('Adequacy of Exams in Assessing Knowledge')
    exams_columns = [
        'Did the exam adequately assess your knowledge in Offensive Team Tactic?',
        'Did the exam adequately assess your knowledge in Defensive Team Tactic?',
        'Did the exam adequately assess your knowledge in Individual and Group Tactics?',
        'Did the exam adequately assess your knowledge in Basketball Technique?',
        'Did the exam adequately assess your knowledge in Planning & Programming and S&C?',
        'Did the exam adequately assess your knowledge in Selection and Training of Young Players?',
        'Did the exam adequately assess your knowledge in Basketball History and Factors? ',
        'Did the exam adequately assess your knowledge in Theory of Sports Training and S&C? ',
        'Did the exam adequately assess your knowledge in Sociology & Psychology?',
        'Did the exam adequately assess your knowledge in Human Motoric? ',
        'Did the exam adequately assess your knowledge in Biomedicine Subjects?'
    ]

    for exam in exams_columns:
        st.subheader(exam)
        exam_counts = df[exam].value_counts().sort_index()
        fig_exam = px.bar(exam_counts, x=exam_counts.index, y=exam_counts.values,
                          labels={'x': 'Rating', 'y': 'Count'}, title=f'Distribution of Ratings for {exam}')
        st.plotly_chart(fig_exam)

   # 6. Lessons - Overall Satisfaction Analysis
    st.subheader('Overall Satisfaction with Lessons')
    low_rating_counts = {}
    mean_ratings = {}

    for lesson in lessons_columns:
        low_rating_counts[lesson] = (df[lesson] < 4).sum()
        mean_ratings[lesson] = df[lesson].mean()

    df_lessons_ratings = pd.DataFrame({
        'Lesson': lessons_columns,
        'Low Ratings (<4)': low_rating_counts.values(),
        'Mean Rating': mean_ratings.values()
    }).sort_values(by='Mean Rating', ascending=False)

    # Calculate the overall average rating across all lessons
    overall_mean_lesson_rating = df_lessons_ratings['Mean Rating'].mean()

    # Create the bar chart with the average line
    fig_lessons_mean = px.bar(df_lessons_ratings, x='Lesson', y='Mean Rating',
                              title="Average Ratings of Lessons", labels={'Mean Rating': 'Average Rating'},
                              range_y=[4, 4.5])

    # Add a horizontal line for the overall average rating
    fig_lessons_mean.add_shape(
        type="line",
        x0=-0.5, x1=len(df_lessons_ratings)-0.5,  # X-axis spans the whole plot
        # Y-axis fixed at the mean value
        y0=overall_mean_lesson_rating, y1=overall_mean_lesson_rating,
        line=dict(color="red", width=2, dash="dash"),  # Line style
    )

    # Add annotation for the average line
    fig_lessons_mean.add_annotation(
        text=f"Overall Avg: {overall_mean_lesson_rating:.2f}",
        x=len(df_lessons_ratings)-1, y=overall_mean_lesson_rating,
        showarrow=False,
        yshift=10,  # Position adjustment
        font=dict(color="blue")
    )

    st.plotly_chart(fig_lessons_mean)

    fig_low_ratings_lessons = px.bar(df_lessons_ratings, x='Lesson', y='Low Ratings (<4)',
                                     title="Count of Low Ratings for Lessons", labels={'Low Ratings (<4)': 'Count of Low Ratings'})
    overall_avg_low_ratings_lessons = df_lessons_ratings['Low Ratings (<4)'].mean(
    )

    # Add a horizontal line for the overall average count of low ratings
    fig_low_ratings_lessons.add_shape(
        type="line",
        x0=-0.5, x1=len(df_lessons_ratings)-0.5,
        y0=overall_avg_low_ratings_lessons, y1=overall_avg_low_ratings_lessons,
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add annotation for the average line
    fig_low_ratings_lessons.add_annotation(
        text=f"Overall Avg Low Ratings: {overall_avg_low_ratings_lessons:.2f}",
        x=len(df_lessons_ratings)-1, y=overall_avg_low_ratings_lessons,
        showarrow=False,
        yshift=10,
        font=dict(color="blue")
    )
    st.plotly_chart(fig_low_ratings_lessons)

    # 7. Exams - Overall Satisfaction Analysis
    st.subheader('Overall Satisfaction with Exams')
    low_rating_counts_exams = {}
    mean_ratings_exams = {}

    for exam in exams_columns:
        low_rating_counts_exams[exam] = (df[exam] < 4).sum()
        mean_ratings_exams[exam] = df[exam].mean()

    df_exams_ratings = pd.DataFrame({
        'Exam': exams_columns,
        'Low Ratings (<4)': low_rating_counts_exams.values(),
        'Mean Rating': mean_ratings_exams.values()
    }).sort_values(by='Mean Rating', ascending=False)

    # Calculate the overall average rating across all exams
    overall_mean_exam_rating = df_exams_ratings['Mean Rating'].mean()

    # Create the bar chart with the average line
    fig_exams_mean = px.bar(df_exams_ratings, x='Exam', y='Mean Rating',
                            title="Average Ratings of Exams", labels={'Mean Rating': 'Average Rating'},
                            range_y=[4, 4.15])

    # Add a horizontal line for the overall average rating
    fig_exams_mean.add_shape(
        type="line",
        x0=-0.5, x1=len(df_exams_ratings)-0.5,
        y0=overall_mean_exam_rating, y1=overall_mean_exam_rating,
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add annotation for the average line
    fig_exams_mean.add_annotation(
        text=f"Overall Avg: {overall_mean_exam_rating:.2f}",
        x=len(df_exams_ratings)-1, y=overall_mean_exam_rating,
        showarrow=False,
        yshift=10,
        font=dict(color="blue")
    )

    st.plotly_chart(fig_exams_mean)

    fig_low_ratings_exams = px.bar(df_exams_ratings, x='Exam', y='Low Ratings (<4)',
                                   title="Count of Low Ratings for Exams", labels={'Low Ratings (<4)': 'Count of Low Ratings'})
    overall_avg_low_ratings = df_exams_ratings['Low Ratings (<4)'].mean()

    # Add a horizontal line for the overall average count of low ratings
    fig_low_ratings_exams.add_shape(
        type="line",
        x0=-0.5, x1=len(df_exams_ratings)-0.5,
        y0=overall_avg_low_ratings, y1=overall_avg_low_ratings,
        line=dict(color="red", width=2, dash="dash"),
    )

    # Add annotation for the average line
    fig_low_ratings_exams.add_annotation(
        text=f"Overall Avg Low Ratings: {overall_avg_low_ratings:.2f}",
        x=len(df_exams_ratings)-1, y=overall_avg_low_ratings,
        showarrow=False,
        yshift=10,
        font=dict(color="blue")
    )
    st.plotly_chart(fig_low_ratings_exams)

    # 8. Time Zones & Scheduling
    st.header('Satisfaction with Time Zones & Scheduling')
    # Preferred Days for Lessons
    st.subheader('Preferred Days for Lessons')
    df_days = df['Which days did you prefer the lessons the most?'].dropna()
    fig_days = px.bar(df_days.value_counts().sort_index(), x=df_days.value_counts().sort_index().index,
                      y=df_days.value_counts().sort_index().values,
                      labels={'x': 'Preferred Day', 'y': 'Count'},
                      title="Preferred Days for Lessons")
    st.plotly_chart(fig_days)

    # Preferred Times for Weekdays
    st.subheader('Preferred Times for Weekdays (Central European Time)')
    df_weekday_times = df['On weekdays, which time period fitted you the most? [Central European Time]'].dropna()
    fig_weekday_times = px.bar(df_weekday_times.value_counts().sort_index(), x=df_weekday_times.value_counts().sort_index().index,
                               y=df_weekday_times.value_counts().sort_index().values,
                               labels={'x': 'Preferred Time', 'y': 'Count'},
                               title="Preferred Times for Lessons on Weekdays (CET)")
    st.plotly_chart(fig_weekday_times)

    # Preferred Times for Weekends
    st.subheader('Preferred Times for Weekends (Central European Time)')
    df_weekend_times = df['At weekends, which time period fitted you the most? [Central European Time]'].dropna()
    fig_weekend_times = px.bar(df_weekend_times.value_counts().sort_index(), x=df_weekend_times.value_counts().sort_index().index,
                               y=df_weekend_times.value_counts().sort_index().values,
                               labels={'x': 'Preferred Time', 'y': 'Count'},
                               title="Preferred Times for Lessons on Weekends (CET)")
    st.plotly_chart(fig_weekend_times)

    # Ability to Attend Lessons
    st.subheader('Ability to Attend Lessons')
    df_attendance = df['Were you able to attend most of the lessons as per your personal schedule?'].dropna()
    fig_attendance = px.pie(df_attendance.value_counts(), values=df_attendance.value_counts().values,
                            names=df_attendance.value_counts().index,
                            title="Ability to Attend Lessons as per Personal Schedule")
    st.plotly_chart(fig_attendance)

    # Satisfaction with Peer Attendance
    st.subheader('Satisfaction with Peer Attendance')
    df_peer_attendance = df['How satisfied were you with the general attendance of your peers in the lessons? '].dropna()
    fig_peer_attendance = px.bar(df_peer_attendance.value_counts().sort_index(), x=df_peer_attendance.value_counts().sort_index().index,
                                 y=df_peer_attendance.value_counts().sort_index().values,
                                 labels={'x': 'Satisfaction Level',
                                         'y': 'Count'},
                                 title="Satisfaction with Peer Attendance")
    st.plotly_chart(fig_peer_attendance)

    # Overall Scheduling Satisfaction
    st.subheader('Overall Scheduling Satisfaction')
    df_overall_scheduling = df['How would you rate the overall scheduling of the lessons?'].dropna(
    )
    fig_overall_scheduling = px.bar(df_overall_scheduling.value_counts().sort_index(), x=df_overall_scheduling.value_counts().sort_index().index,
                                    y=df_overall_scheduling.value_counts().sort_index().values,
                                    labels={'x': 'Rating', 'y': 'Count'},
                                    title="Overall Satisfaction with Lesson Scheduling")
    st.plotly_chart(fig_overall_scheduling)

    # # Additional Comments on Scheduling
    # st.subheader('Additional Comments on Scheduling')
    # additional_comments = df['Please share any additional comments or suggestions about the Schedule and Attandance. '].dropna()
    # st.write(additional_comments.tolist())

    # 9. Content Quality
    st.header('Satisfaction with Content Quality')
    # 1. Satisfaction with Collaboration with University of Belgrade
    st.header('Satisfaction with Collaboration with University of Belgrade')
    if 'How satisfied were you about the collaboration with University of Belgrade?' in df.columns:
        df_collab_belgrade = df['How satisfied were you about the collaboration with University of Belgrade?'].dropna(
        )
        st.bar_chart(df_collab_belgrade.value_counts().sort_index())

    # 2. Satisfaction with Professors of University of Belgrade
    st.header('Satisfaction with Professors of University of Belgrade')
    if 'How satisfied were you with the professors of the University of Belgrade?' in df.columns:
        df_professors_belgrade = df['How satisfied were you with the professors of the University of Belgrade?'].dropna(
        )
        st.bar_chart(df_professors_belgrade.value_counts().sort_index())

    # 3. Satisfaction with Exams in General
    st.header('Satisfaction with Exams in General')
    if 'How satisfied were you with the exams in general?' in df.columns:
        df_exams_general = df['How satisfied were you with the exams in general?'].dropna(
        )
        st.bar_chart(df_exams_general.value_counts().sort_index())

    # 4. Effectiveness of EHCB Members Online Lectures
    st.header("Effectiveness of EHCB Members Online Lectures")
    df_online_lectures = pd.read_json('data/EHCB_Members_Online.json')
    # Load the JSON file
    with open('data/EHCB_Members_Online.json', 'r') as file:
        json_online_lectures = json.load(file)

    # Convert the JSON data into a DataFrame
    df_online_lectures = pd.DataFrame(json_online_lectures)

    # Display the data as a bar chart
    st.bar_chart(
        df_online_lectures['EHCB_Members_Online_Lectures'].value_counts().sort_index())

    # # 5. Effectiveness of EHCB Coaches Congress
    # st.header("Effectiveness of EHCB Coaches Congress")
    # if "How effective was the EHCB Coaches Congress in providing valuable learning experiences?" in df.columns:
    #     df_coaches_congress = df["How effective was the EHCB Coaches Congress in providing valuable learning experiences?"].dropna()
    #     st.bar_chart(df_coaches_congress.value_counts().sort_index())

    # # 6. Effectiveness of Panels and Masterclasses at the Congress
    # st.header("Effectiveness of Panels and Masterclasses at the Congress")
    # if "How effective were the panels and masterclasses at the Congress?" in df.columns:
    #     df_panels_masterclasses = df["How effective were the panels and masterclasses at the Congress?"].dropna()
    #     st.bar_chart(df_panels_masterclasses.value_counts().sort_index())

    # # 7. Value of Networking Opportunity at the Congress
    # st.header("Value of Networking Opportunity at the Congress")
    # if "How valuable was the networking opportunity provided at the Congress?" in df.columns:
    #     df_networking_congress = df["How valuable was the networking opportunity provided at the Congress?"].dropna()
    #     st.bar_chart(df_networking_congress.value_counts().sort_index())

    # 8. Satisfaction with General Attendance of Peers
    st.header("Satisfaction with General Attendance of Peers")
    if "How satisfied were you with the general attendance of your peers in the lessons? " in df.columns:
        df_attendance_peers = df["How satisfied were you with the general attendance of your peers in the lessons? "].dropna(
        )
        st.bar_chart(df_attendance_peers.value_counts().sort_index())

    # 9. Overall Scheduling of Lessons
    st.header("Overall Scheduling of Lessons")
    if "How would you rate the overall scheduling of the lessons?" in df.columns:
        df_scheduling_lessons = df["How would you rate the overall scheduling of the lessons?"].dropna(
        )
        st.bar_chart(df_scheduling_lessons.value_counts().sort_index())

    # 10. Value of Bonus Lectures
    st.header("Value of Bonus Lectures")
    if "How valuable did you find the Bonus Lectures?" in df.columns:
        df_bonus_lectures_value = df["How valuable did you find the Bonus Lectures?"].dropna(
        )
        st.bar_chart(df_bonus_lectures_value.value_counts().sort_index())

    # 11. Relevance of Bonus Lecture Topics
    st.header("Relevance of Bonus Lecture Topics")
    if "Were the topics covered in the Bonus Lectures relevant to your coaching needs / expectations? " in df.columns:
        df_bonus_lectures_relevance = df["Were the topics covered in the Bonus Lectures relevant to your coaching needs / expectations? "].dropna()
        st.bar_chart(df_bonus_lectures_relevance.value_counts().sort_index())

    # 12. User-Friendliness of Zoom
    st.header("User-Friendliness of Zoom")
    if "How user-friendly was Zoom?" in df.columns:
        df_zoom_user_friendly = df["How user-friendly was Zoom?"].dropna()
        st.bar_chart(df_zoom_user_friendly.value_counts().sort_index())

    # 13. User-Friendliness of MS Teams
    st.header("User-Friendliness of MS Teams")
    if "How user-friendly was MS Teams?" in df.columns:
        df_ms_teams_user_friendly = df["How user-friendly was MS Teams?"].dropna()
        st.bar_chart(df_ms_teams_user_friendly.value_counts().sort_index())

    # # 14. Effectiveness of Communication Channels
    # st.header("Effectiveness of Communication Channels")
    # if "How effective were the communication channels (WhatsApp, email, etc.)?" in df.columns:
    #     df_communication_channels = df["How effective were the communication channels (WhatsApp, email, etc.)?"].dropna(
    #     )
    #     st.bar_chart(df_communication_channels.value_counts().sort_index())

    # 15. Accessibility of Recorded Lectures and Materials
    st.header("Accessibility of Recorded Lectures and Materials")
    if "How accessible were the recorded lectures and materials? " in df.columns:
        df_accessibility_materials = df["How accessible were the recorded lectures and materials? "].dropna(
        )
        st.bar_chart(df_accessibility_materials.value_counts().sort_index())

    # # 16. Overall Technical Support
    # st.header("Overall Technical Support")
    # if "Please rate the overall technical support provided during the courses." in df.columns:
    #     df_technical_support = df["Please rate the overall technical support provided during the courses."].dropna(
    #     )
    #     st.bar_chart(df_technical_support.value_counts().sort_index())

    # 17. Support for Operational Aspects of the Academy
    st.header("Support for Operational Aspects of the Academy")
    if "Please rate the support provided for operational aspects of the academy" in df.columns:
        df_operational_support = df["Please rate the support provided for operational aspects of the academy"].dropna(
        )
        st.bar_chart(df_operational_support.value_counts().sort_index())

    # 10. Overall Program
    st.header('Satisfaction with Overall Program')
    # Example columns for overall program satisfaction
    overall_program_columns = [
        "How likely are you to recommend the EHCB Coaches Academy to other coaches? ",
        "To what extent has the academy helped you become a better coach?",
        "Did the academy meet your expectations for professional networking? ",
    ]

    for column in overall_program_columns:
        if column in df.columns:
            st.subheader(f'{column}')
            df_overall_program = df[column].dropna()
            st.bar_chart(df_overall_program.value_counts().sort_index())
        else:
            st.write(f"Column '{column}' not found in the dataset.")

    # Load the JSON file
    with open('data/How_much_knowledge_did_you_gain_from_the_modules.json', 'r') as f:
        data = json.load(f)

    # Extract the data
    df_knowledge_gained = pd.DataFrame(data)

    # Display the bar chart
    st.header("Knowledge Gained from EHCB Coaches Academy's Modules")
    st.bar_chart(
        df_knowledge_gained['How_much_knowledge_did_you_gain_from_the_modules'].value_counts().sort_index())
