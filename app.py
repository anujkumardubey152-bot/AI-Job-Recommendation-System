import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_PATH = Path(__file__).resolve().parent
SRC_PATH = PROJECT_PATH / "src"
DATA_PATH = PROJECT_PATH / "data" / "jobs.csv"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from recommender import recommend_jobs, analyze_skill_match

st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI-Powered Job Recommendation System")
st.write(
    "Upload your resume to discover relevant jobs, see matching skills, "
    "and identify skills you may want to learn."
)

st.info(
    "This demo uses a small sample dataset. Match scores are estimates, "
    "not probabilities of getting hired."
)

if not DATA_PATH.is_file():
    st.error(f"Job dataset not found: {DATA_PATH}")
    st.stop()

try:
    jobs_df = pd.read_csv(DATA_PATH)
except Exception as error:
    st.error(f"Could not read the job dataset: {error}")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

top_n = st.slider(
    "Number of job recommendations",
    min_value=1,
    max_value=10,
    value=5
)

if uploaded_file is not None:
    suffix = Path(uploaded_file.name).suffix.lower()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        with st.spinner("Reading your resume and finding suitable jobs..."):
            resume_text = extract_resume_text(temp_path)

            if not resume_text.strip():
                st.warning("No readable text was found in this resume.")
                st.stop()

            resume_skills = extract_skills(resume_text)
            recommendations = recommend_jobs(
                resume_text, jobs_df, top_n=top_n
            )

        st.subheader("Skills found in your resume")

        if resume_skills:
            st.write(", ".join(resume_skills))
        else:
            st.warning(
                "No skills from the app's current skill list were detected. "
                "Try a resume that clearly lists your technical skills."
            )

        st.subheader("Recommended jobs")

        if recommendations.empty:
            st.warning(
                "No recommendations were returned. Check your job dataset."
            )
        else:
            for rank, (_, job) in enumerate(
                recommendations.iterrows(), start=1
            ):
                required_skills = job.get("required_skills", "")

                if pd.isna(required_skills):
                    required_skills = ""

                skill_result = analyze_skill_match(
                    resume_skills, str(required_skills)
                )

                with st.container(border=True):
                    st.markdown(
                        f"### {rank}. {job.get('job_title', 'Job title unavailable')}"
                    )
                    st.write(
                        f"**Company:** {job.get('company', 'Not specified')}"
                    )
                    st.write(
                        f"**Experience level:** "
                        f"{job.get('experience_level', 'Not specified')}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Text similarity",
                            f"{float(job['match_score']):.1f}%"
                        )

                    with col2:
                        st.metric(
                            "Skill coverage",
                            f"{skill_result['skill_match_percent']:.1f}%"
                        )

                    st.write(
                        "**Required skills:**",
                        str(required_skills) or "Not specified"
                    )

                    matched = skill_result["matched_skills"]
                    missing = skill_result["missing_skills"]

                    st.write(
                        "**Skills you have:**",
                        ", ".join(matched) if matched else "None matched"
                    )
                    st.write(
                        "**Skills to develop:**",
                        ", ".join(missing) if missing else "None! You meet all requirements."
                    )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
