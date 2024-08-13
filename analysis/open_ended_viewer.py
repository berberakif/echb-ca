import streamlit as st
import pandas as pd
import os

def open_ended_viewer():
    st.header("Open-Ended Feedback Viewer")

    # Dictionary mapping questions to their respective CSV files
    questions = {
        "Application and Registration Process": "additional_comments_or_suggestions_about_Application_and_Registration_Process.csv",
        "Lecture Modules, Exam, Grading, and Certification": "additional_comments_or_suggestions_about_Lecture_Modules_exams.csv",
        "Networking": "additional_comments_or_suggestions_about_Networking.csv",
        "Bonus Lectures": "additional_comments_or_suggestions_about_the_Bonus_Lectures.csv",
        "Curriculum": "additional_comments_or_suggestions_about_the_Curriculum.csv",
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
    
    # Select question
    question = st.selectbox("Select a question", list(questions.keys()))
    
    # Load the selected CSV file
    if question:
        file_path = os.path.join('data', questions[question])
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            # Filter out generic responses
            generic_responses = ['/', 'yes', 'no', '-', 'na', 'none', 'N/A', 'Nothing', 'nothing']
            df = df[~df.iloc[:, 0].str.strip().str.lower().isin(generic_responses)]

            if not df.empty:
                st.markdown(f"### Responses for {question}")
                for index, row in df.iterrows():
                    st.markdown(f"- {row[0]}")
            else:
                st.write("No detailed responses available for this question.")
        else:
            st.write("File not found.")
