import streamlit as st

def key_findings():
    st.header('Summary of Key Findings')

    st.subheader('Overall Satisfaction')
    st.write("""
    Participants generally expressed high satisfaction with the overall structure and content of the program.
    Specific components like practice weeks, lessons, and exams received positive feedback, particularly from certain roles.
    """)

    st.subheader('Practice Weeks')
    st.write("""
    Practice weeks such as those with Partizan and Bayern Munich were highly rated, particularly by participants who found 
    the interaction and organization beneficial for their development.
    """)

    st.subheader('Lessons and Exams')
    st.write("""
    Academic rigor and the effectiveness of lessons and exams were well-received, especially in key areas like Offensive 
    and Defensive Team Tactics. However, there was feedback about the need for clearer exam guidelines.
    """)

    st.subheader('Time Zones and Scheduling')
    st.write("""
    Satisfaction with scheduling varied across different time zones. Participants from certain time zones expressed 
    challenges in attending sessions, particularly those outside the Central European Time (CET) zone. 
    Weekday evenings (CET) were the most popular times for participants.
    """)

    st.subheader('Sentiment from Open-Ended Responses')
    st.write("""
    Participants were generally positive about the content and organization. However, there were suggestions for improving 
    practical content, enhancing communication, and ensuring that scheduling accommodates a broader range of time zones.
    """)
