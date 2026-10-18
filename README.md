# 💼 CareerMatch AI — AI-Powered Job Recommendation System

An interactive resume-based job recommendation system that helps users discover relevant job roles, analyze their skills, and identify potential skill gaps.

## 🌟 Overview

CareerMatch AI analyzes an uploaded resume and compares it with a sample job dataset to recommend relevant positions. It combines text similarity with required-skill coverage to rank jobs and display insights through an interactive Streamlit dashboard.

## ✨ Features

- **Resume Parsing:** Upload resumes in PDF or DOCX format.
- **Skill Extraction:** Identify recognized technical skills from resume text.
- **Personalized Job Recommendations:** Rank jobs based on resume relevance.
- **Hybrid Matching:** Combine text similarity and skill coverage into an overall match score.
- **Skill Gap Analysis:** Display matched skills and skills that may need improvement.
- **Interactive Dashboard:** View detected skills, recommended jobs, and match scores.
- **Configurable Results:** Choose how many job recommendations to display.

## 🛠️ Tech Stack

- **Language:** Python
- **Data Processing:** Pandas
- **Machine Learning / NLP:** Scikit-learn, TF-IDF text similarity
- **Web Interface:** Streamlit
- **Resume Processing:** PDF and DOCX parsing libraries
- **Deployment:** Streamlit Community Cloud
- **Version Control:** Git and GitHub

## 🧠 How It Works

1. **Upload Resume:** The user uploads a PDF or Word resume.
2. **Extract Text:** The resume parser extracts readable text.
3. **Identify Skills:** The skill extractor detects supported skills.
4. **Compare Jobs:** The recommender compares resume text with job descriptions and required skills.
5. **Calculate Match Scores:** Text similarity and skill coverage contribute to the overall ranking.
6. **Display Results:** The dashboard presents recommended roles, scores, matched skills, and skill gaps.

### Matching Method

The current hybrid ranking uses the following weights:

- Text similarity: **30%**
- Required-skill coverage: **70%**

The overall score is calculated as:

`Overall Match Score = (0.30 × Text Similarity) + (0.70 × Skill Coverage)`

Both component scores are expressed as percentages.

**Note:** Match scores are algorithmic relevance estimates. They are not probabilities of getting hired.

## 📂 Project Structure

```text
AI_Job_Recommendation_System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── jobs.csv
│
├── src/
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   └── recommender.py
│
├── models/
│
└── sample_resumes/
    └── sample_resume.docx
```

## ⚙️ Installation and Setup

### 1. Clone the repository

Replace the placeholder URL with your actual public GitHub repository URL.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Job_Recommendation_System
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL to open the application in your browser.

## 🚀 Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project files to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select the appropriate branch.
5. Set `app.py` as the main application file.
6. Deploy the application.

Ensure that `requirements
