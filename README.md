# AI-Powered Job Recommendation System

## Overview
This project recommends jobs based on resume content and identifies
matching and missing skills.

## Features
- Upload resumes in PDF or DOCX format
- Extract resume text
- Identify technical skills
- Recommend jobs using TF-IDF and cosine similarity
- Display text-similarity scores
- Analyze matching and missing skills
- Streamlit user interface

## Technologies
- Python
- Pandas
- Scikit-learn
- Streamlit
- PyPDF
- python-docx

## Project Structure
- app.py: Streamlit user interface
- src/resume_parser.py: Resume text extraction
- src/skill_extractor.py: Skill extraction
- src/recommender.py: Job recommendations and skill-gap analysis
- data/jobs.csv: Sample job dataset
- sample_resumes/: Sample resume files

## Run Locally
Install the dependencies:

    pip install -r requirements.txt

Start the application:

    streamlit run app.py

## Important Notes
The included jobs are fictional sample records.
Similarity scores are not probabilities of being hired.
The skill extractor recognizes only skills in its configured list.

## Future Improvements
- Add a larger, real job dataset
- Expand the skills dictionary
- Improve resume parsing
- Deploy the application online
