
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_jobs(resume_text, jobs_df, top_n=5):
    """Recommend jobs by comparing resume text with job information."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if jobs_df is None or jobs_df.empty:
        raise ValueError("The jobs dataset is empty.")

    required_columns = [
        "job_title",
        "company",
        "required_skills",
        "description",
    ]

    for column in required_columns:
        if column not in jobs_df.columns:
            raise ValueError(f"Missing required column: {column}")

    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    jobs = jobs_df.copy()

    for column in required_columns:
        jobs[column] = jobs[column].fillna("").astype(str)

    job_text = (
        jobs["job_title"] + " "
        + jobs["required_skills"] + " "
        + jobs["description"]
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    combined_text = [resume_text] + job_text.tolist()
    tfidf_matrix = vectorizer.fit_transform(combined_text)

    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    ).flatten()

    jobs["match_score"] = similarities * 100

    return (
        jobs.sort_values("match_score", ascending=False)
        .head(min(top_n, len(jobs)))
        .reset_index(drop=True)
    )


def analyze_skill_match(resume_skills, required_skills):
    """Compare resume skills with the skills required by a job."""

    if isinstance(resume_skills, str):
        resume_skills = [skill.strip() for skill in resume_skills.split(",")]

    if isinstance(required_skills, str):
        required_skills = [
            skill.strip() for skill in required_skills.split(",")
        ]

    resume_lookup = {
        skill.strip().casefold()
        for skill in resume_skills
        if isinstance(skill, str) and skill.strip()
    }

    required_list = list(dict.fromkeys(
        skill.strip()
        for skill in required_skills
        if isinstance(skill, str) and skill.strip()
    ))

    matched_skills = [
        skill for skill in required_list
        if skill.casefold() in resume_lookup
    ]

    missing_skills = [
        skill for skill in required_list
        if skill.casefold() not in resume_lookup
    ]

    if required_list:
        skill_match_percent = (
            len(matched_skills) / len(required_list)
        ) * 100
    else:
        skill_match_percent = 0.0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percent": round(skill_match_percent, 2),
    }
