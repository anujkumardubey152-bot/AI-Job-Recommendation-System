
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skill_extractor import extract_skills


# Ranking weights: total must equal 1.0
TEXT_WEIGHT = 0.30
SKILL_WEIGHT = 0.70


def recommend_jobs(resume_text, jobs_df, top_n=5):
    """Rank jobs using text similarity and required-skill coverage."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if jobs_df is None or jobs_df.empty:
        raise ValueError("The jobs dataset is empty.")

    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    required_columns = [
        "job_title",
        "company",
        "required_skills",
        "description",
    ]

    for column in required_columns:
        if column not in jobs_df.columns:
            raise ValueError(f"Missing required column: {column}")

    jobs = jobs_df.copy()

    for column in required_columns:
        jobs[column] = jobs[column].fillna("").astype(str)

    # Combine job title, required skills, and description.
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

    tfidf_matrix = vectorizer.fit_transform(
        [resume_text] + job_text.tolist()
    )

    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:],
    ).flatten()

    # Keep text similarity as a separate score.
    jobs["match_score"] = similarities * 100

    # Extract skills from the resume.
    resume_skills = extract_skills(resume_text)

    # Calculate skill coverage for each job.
    skill_results = [
        analyze_skill_match(resume_skills, required)
        for required in jobs["required_skills"]
    ]

    jobs["skill_match_percent"] = [
        result["skill_match_percent"]
        for result in skill_results
    ]

    # Combine text similarity and skill coverage.
    jobs["overall_match_score"] = (
        TEXT_WEIGHT * jobs["match_score"]
        + SKILL_WEIGHT * jobs["skill_match_percent"]
    ).round(2)

    # Rank by overall score, then text similarity.
    jobs = jobs.sort_values(
        ["overall_match_score", "match_score"],
        ascending=[False, False],
    )

    return jobs.head(min(top_n, len(jobs))).reset_index(drop=True)


def analyze_skill_match(resume_skills, required_skills):
    """Compare resume skills with the skills required by a job."""

    if isinstance(resume_skills, str):
        resume_skills = resume_skills.split(",")

    if isinstance(required_skills, str):
        required_skills = required_skills.split(",")

    resume_lookup = {
        skill.strip().casefold()
        for skill in resume_skills
        if isinstance(skill, str) and skill.strip()
    }

    # Remove duplicate required skills, ignoring capitalization.
    unique_required = []
    seen = set()

    for skill in required_skills:
        if not isinstance(skill, str) or not skill.strip():
            continue

        skill = skill.strip()
        normalized = skill.casefold()

        if normalized not in seen:
            unique_required.append(skill)
            seen.add(normalized)

    matched_skills = [
        skill for skill in unique_required
        if skill.casefold() in resume_lookup
    ]

    missing_skills = [
        skill for skill in unique_required
        if skill.casefold() not in resume_lookup
    ]

    if unique_required:
        skill_match_percent = (
            len(matched_skills) / len(unique_required)
        ) * 100
    else:
        skill_match_percent = 0.0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percent": round(skill_match_percent, 2),
    }

