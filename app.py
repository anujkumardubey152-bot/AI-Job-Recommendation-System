
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

# Use the project folder for Streamlit Cloud and local deployment.
PROJECT_PATH = Path(__file__).resolve().parent
SRC_PATH = PROJECT_PATH / "src"
DATA_PATH = PROJECT_PATH / "data" / "jobs.csv"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from recommender import recommend_jobs, analyze_skill_match


st.set_page_config(
    page_title="CareerMatch AI | Job Recommendations",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- CUSTOM UI STYLING --------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #15243a;
    }

    .hero {
        background: linear-gradient(125deg, #101827 0%, #193b62 65%, #176b87 100%);
        padding: 2.4rem 2.2rem;
        border-radius: 22px;
        margin-bottom: 1.5rem;
        color: white;
    }

    .hero-tag {
        color: #9ee7f5;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.12;
        margin: 0 0 0.8rem 0;
    }

    .hero p {
        color: #d9e7f5;
        font-size: 1.05rem;
        line-height: 1.65;
        max-width: 720px;
        margin-bottom: 0;
    }

    .section-heading {
        font-size: 1.45rem;
        font-weight: 750;
        color: #15243a;
        margin-top: 1.4rem;
        margin-bottom: 0.3rem;
    }

    .section-subtitle {
        color: #607086;
        font-size: 0.96rem;
        margin-bottom: 1rem;
    }

    .upload-panel {
        background: white;
        border: 1px solid #dce5ef;
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .job-card {
        background: white;
        border: 1px solid #dce5ef;
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        margin: 0.7rem 0 1rem 0;
        box-shadow: 0 4px 15px rgba(20, 40, 70, 0.04);
    }

    .job-rank {
        color: #087e8b;
        font-weight: 750;
        font-size: 0.82rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .job-title {
        color: #15243a;
        font-size: 1.35rem;
        font-weight: 750;
        margin: 0.3rem 0;
    }

    .job-meta {
        color: #607086;
        font-size: 0.94rem;
        margin-bottom: 0.8rem;
    }

    .score-label {
        color: #607086;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .score-value {
        color: #15243a;
        font-size: 1.7rem;
        font-weight: 800;
    }

    .overall-score {
        background: #e4f7f3;
        border: 1px solid #b9e8dc;
        border-radius: 13px;
        padding: 0.8rem 1rem;
        margin: 0.6rem 0 1rem 0;
    }

    .overall-score .score-value {
        color: #087e68;
    }

    .skill-chip {
        display: inline-block;
        background: #e7f7f4;
        color: #086c60;
        border: 1px solid #c4e9e2;
        padding: 0.3rem 0.65rem;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 0.15rem 0.15rem 0.15rem 0;
    }

    .missing-chip {
        display: inline-block;
        background: #fff4e5;
        color: #915a12;
        border: 1px solid #f3d8ad;
        padding: 0.3rem 0.65rem;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 0.15rem 0.15rem 0.15rem 0;
    }

    .footer-note {
        color: #718096;
        font-size: 0.82rem;
        text-align: center;
        padding-top: 2rem;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #dce5ef;
        border-radius: 14px;
        padding: 1rem;
    }

    div[data-testid="stFileUploader"] {
        background: #f8fbff;
        border: 1px dashed #8baac8;
        border-radius: 14px;
        padding: 0.6rem;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HERO HEADER --------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">✦ Smart career discovery</div>
        <h1>Find the role that fits your skills.</h1>
        <p>
            Discover relevant opportunities, understand your strengths,
            and identify the skills that can help you move forward.
            Your next career step starts here.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "AI-powered job recommendations • Resume skill analysis • "
    "Personalized skill-gap insights"
)

# -------------------- LOAD JOB DATA --------------------

if not DATA_PATH.is_file():
    st.error(f"Job dataset not found: {DATA_PATH}")
    st.stop()

try:
    jobs_df = pd.read_csv(DATA_PATH)
except Exception as error:
    st.error(f"Could not read the job dataset: {error}")
    st.stop()

# -------------------- RESUME UPLOAD --------------------

st.markdown(
    '<div class="section-heading">Start with your resume</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">'
    'Upload a PDF or Word document to discover your best-matching jobs.'
    '</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX.",
    )

    top_n = st.slider(
        "How many jobs would you like to see?",
        min_value=1,
        max_value=min(10, max(1, len(jobs_df))),
        value=min(5, max(1, len(jobs_df))),
    )

st.info(
    "This project uses a small sample job dataset. Match scores are "
    "ranking estimates, not probabilities of being hired."
)

# -------------------- ANALYZE RESUME --------------------

if uploaded_file is not None:
    suffix = Path(uploaded_file.name).suffix.lower()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        with st.spinner("Analyzing your resume and matching jobs..."):
            resume_text = extract_resume_text(temp_path)

            if not resume_text.strip():
                st.error(
                    "No readable text was found. Please try another "
                    "PDF or DOCX resume."
                )
                st.stop()

            resume_skills = extract_skills(resume_text)
            recommendations = recommend_jobs(
                resume_text,
                jobs_df,
                top_n=top_n,
            )

        # -------------------- SKILLS SUMMARY --------------------

        st.markdown(
            '<div class="section-heading">Your skills snapshot</div>',
            unsafe_allow_html=True,
        )

        metric1, metric2, metric3 = st.columns(3)

        with metric1:
            st.metric("Skills detected", len(resume_skills))

        with metric2:
            st.metric("Jobs recommended", len(recommendations))

        with metric3:
            best_score = (
                float(recommendations.iloc[0]["overall_match_score"])
                if not recommendations.empty
                else 0.0
            )
            st.metric("Top overall match", f"{best_score:.1f}%")

        with st.container(border=True):
            st.markdown("**Skills detected in your resume**")

            if resume_skills:
                chips = "".join(
                    f'<span class="skill-chip">{skill}</span>'
                    for skill in resume_skills
                )
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.warning(
                    "No recognized skills were detected. Try a resume "
                    "that clearly lists your technical skills."
                )

        # -------------------- JOB RECOMMENDATIONS --------------------

        st.markdown(
            '<div class="section-heading">Your recommended jobs</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle">'
            'Ranked by your combined text similarity and required-skill coverage.'
            '</div>',
            unsafe_allow_html=True,
        )

        if recommendations.empty:
            st.warning(
                "No recommendations were returned. Please check your job dataset."
            )
        else:
            for rank, (_, job) in enumerate(
                recommendations.iterrows(),
                start=1,
            ):
                required_skills = job.get("required_skills", "")

                if pd.isna(required_skills):
                    required_skills = ""

                skill_result = analyze_skill_match(
                    resume_skills,
                    str(required_skills),
                )

                text_score = float(job.get("match_score", 0))
                skill_score = float(
                    skill_result["skill_match_percent"]
                )
                overall_score = float(
                    job.get("overall_match_score", 0)
                )

                job_title = str(
                    job.get("job_title", "Job title unavailable")
                )
                company = str(
                    job.get("company", "Not specified")
                )
                experience = str(
                    job.get("experience_level", "Not specified")
                )

                with st.container(border=True):
                    st.markdown(
                        f'<div class="job-rank">MATCH #{rank}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="job-title">{job_title}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="job-meta">🏢 {company} '
                        f'&nbsp; · &nbsp; 💼 {experience}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div class="overall-score">
                            <div class="score-label">OVERALL MATCH SCORE</div>
                            <div class="score-value">{overall_score:.1f}%</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    score1, score2 = st.columns(2)

                    with score1:
                        st.markdown("**Text similarity**")
                        st.progress(
                            max(0.0, min(1.0, text_score / 100))
                        )
                        st.caption(f"{text_score:.1f}%")

                    with score2:
                        st.markdown("**Skill coverage**")
                        st.progress(
                            max(0.0, min(1.0, skill_score / 100))
                        )
                        st.caption(f"{skill_score:.1f}%")

                    st.markdown("**Required skills**")
                    st.write(str(required_skills) or "Not specified")

                    matched = skill_result["matched_skills"]
                    missing = skill_result["missing_skills"]

                    with st.expander("View matched skills and skill gaps"):
                        st.markdown("**Skills you already have**")

                        if matched:
                            matched_html = "".join(
                                f'<span class="skill-chip">{skill}</span>'
                                for skill in matched
                            )
                            st.markdown(
                                matched_html,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.write("No required skills matched.")

                        st.markdown("**Skills you could develop**")

                        if missing:
                            missing_html = "".join(
                                f'<span class="missing-chip">{skill}</span>'
                                for skill in missing
                            )
                            st.markdown(
                                missing_html,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.success(
                                "All listed required skills were detected "
                                "in your resume."
                            )

    except Exception as error:
        st.error(
            "Something went wrong while analyzing the resume. "
            "Please check the file and try again."
        )
        st.exception(error)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

else:
    # Empty state before resume upload.
    with st.container(border=True):
        st.markdown("### ✨ Your next opportunity starts here")
        st.write(
            "Upload your resume above to see ranked job matches, "
            "your skill coverage, and areas you could develop."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🎯 Find relevant roles")
            st.caption("Explore jobs ranked against your resume.")

        with col2:
            st.markdown("#### 🧩 Understand your skills")
            st.caption("See which listed job requirements match.")

        with col3:
            st.markdown("#### 🚀 Plan your next step")
            st.caption("Discover potential skills to learn next.")

st.markdown(
    """
    <div class="footer-note">
        CareerMatch AI · Built for career exploration ·
        Scores are estimates and do not guarantee hiring outcomes.
    </div>
    """,
    unsafe_allow_html=True,
)

