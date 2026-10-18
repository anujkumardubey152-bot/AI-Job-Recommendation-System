
import re

SKILLS = [
    "Python",
    "SQL",
    "Excel",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Natural Language Processing",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "Power BI",
    "Data Visualization",
    "Statistics",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Git",
    "APIs",
    "Databases",
    "Data Structures",
    "Algorithms",
    "ETL",
    "Data Pipelines",
    "DAX",
    "Transformers",
    "LLMs",
    "Prompt Engineering"
]


def extract_skills(text):
    """Identify known skills in resume text."""

    if not isinstance(text, str) or not text.strip():
        return []

    found_skills = []
    normalized_text = text.lower()

    for skill in SKILLS:
        normalized_skill = skill.lower()

        # Match whole words or phrases, not partial words.
        pattern = (
            r"(?<!\w)"
            + re.escape(normalized_skill)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    # Avoid returning duplicate skills.
    return list(dict.fromkeys(found_skills))
