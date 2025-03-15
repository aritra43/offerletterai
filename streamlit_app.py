from crewai import Agent
# from tools import yt_tool
# from dotenv import load_dotenv
from crewai import LLM
import litellm
import openai
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import FileReadTool, FileWriterTool
import streamlit as st

load_dotenv()

# Title
st.set_page_config(page_title="HRAI", layout="wide")

# Title and description
st.title("AI HR")

# Sidebar
with st.sidebar:
    st.header("Content Settings")
    candidate_name = st.text_input("Candidate Name", "John Doe")
    job_title = st.text_input("Job Title", "Data Scientist")
    company_name = st.text_input("Company Name", "ABC Inc.")
    salary = st.text_input("Salary")
    joining_date = st.date_input("Joining Date", value=None, min_value=None, max_value=None)
    work_location = st.text_input("Work Location", "New York")
    employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
    reporting_manager = st.text_input("Reporting Manager", "Jane Smith")
    st.markdown("-----")

    generate_button = st.button("Generate Content", type="primary", use_container_width=True)

def generate_content(candidate_name, job_title, company_name, salary, joining_date, work_location, employment_type, reporting_manager):

        # Create a senior blog content researcher
        hr_manager = Agent(
            role='Senior HR Manager',
            goal='Generate HR content for onboarding new employees',
            description='Generate offer letter content for onboarding new employees',
            verbose=True,
            memory=True,
            backstory=(
                 "Generate offer letter for new employees as per the given details {candidate_name}, {job_title}, {company_name}, {salary}, {joining_date}, {work_location}, {employment_type}, {reporting_manager}"
                 "The generated offer letter should comply with the industry standards and rules"
                 "The generated offer letter should be professional and welcoming and well strucrured without any error"
            ),
            allow_delegation=True,
        )

        # Create a reporting analyst agent
        hr_writer = Agent(
            role='Senior HR Writer',
            goal='Write the offer letter content for onboarding new employees',
            description='Write the offer letter content for onboarding new employees',
            verbose=True,
            memory=True,
            backstory=(
                "You're a meticulous analyst with a keen eye for detail."
                "Write the offer letter in official method"
                "It should comply with the industry standards"
                "It should be well structured and formatted"
            ),
            allow_delegation=True,
            tools=[FileWriterTool()]
        )

        research_task = Task(
            description=(
            "Generate a detailed and accurate offer letter for the new employee. "
            "Ensure that all provided details such as {candidate_name}, {job_title}, {company_name}, {salary}, {joining_date}, {work_location}, {employment_type}, {reporting_manager} are included."
            "The offer letter should be professional, welcoming, and comply with industry standards."
            "It should be very detailed"
            "For the date in the letter use the a date that is 15 days befiore the {joining_date}"
            "For the letterhead use IEMCS"
            "Do not keep the address just give the salutation"
            ),
            expected_output='A professionally written offer letter with all the provided details accurately included and well structured.',
            agent=hr_manager,
        )

        reporting_task = Task(
            description=(
            "Write a detailed and professional offer letter based on the provided details. "
            "Ensure the letter is well-structured, error-free, and adheres to industry standards. "
            "Include all necessary information such as {candidate_name}, {job_title}, {company_name}, {salary}, {joining_date}, {work_location}, {employment_type}, and {reporting_manager}."
            ),
            expected_output='A professionally written offer letter with all the provided details accurately included and well structured.',
            agent=hr_writer,
        )

        # Crew
        crew = Crew(
            agents=[hr_manager, hr_writer],
            tasks=[research_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        # Convert joining_date to string
        joining_date_str = joining_date.strftime('%Y-%m-%d')

        return crew.kickoff(inputs={
            "candidate_name": candidate_name,
            "job_title": job_title,
            "company_name": company_name,
            "salary": salary,
            "joining_date": joining_date_str,
            "work_location": work_location,
            "employment_type": employment_type,
            "reporting_manager": reporting_manager
        })

# Main content area
if generate_button:
    with st.spinner("Generating Content...This may take a moment.."):
        try:
            result = generate_content(candidate_name, job_title, company_name, salary, joining_date, work_location, employment_type, reporting_manager)
            if result:
                st.markdown("### Generated Content")
                st.markdown(result)

                # Add download button
                st.download_button(
                    label="Download Content",
                    data=result.raw,
                    file_name=f"article.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("----")
st.markdown("Built by AritraM")
