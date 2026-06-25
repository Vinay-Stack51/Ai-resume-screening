## Agentic AI Resume Screening System

## Overview

RecruitIQ is an AI-powered resume screening and candidate ranking platform designed to automate the initial stages of recruitment. The system uses a multi-agent architecture to analyze resumes, extract candidate information, evaluate skills, compare resumes against job descriptions, and generate AI-driven hiring recommendations.

The platform helps recruiters reduce manual screening effort while improving consistency and decision-making.

---

## Features

### Resume Parsing

* Extracts text from PDF resumes
* Identifies candidate details automatically
* Handles multiple resume uploads

### Candidate Information Extraction

* Name
* Email Address
* Phone Number
* Educational Qualifications
* Work Experience

### Skill Analysis

* Extracts technical skills from resumes
* Matches skills against job requirements
* Identifies missing skills
* Calculates skill relevance

### Project Evaluation

* Detects candidate projects
* Matches projects with role requirements
* Evaluates project relevance

### AI-Powered Candidate Assessment

* Uses Google Gemini for deep resume analysis
* Evaluates candidate strengths
* Identifies potential concerns
* Generates interview questions
* Provides hiring recommendations

### Candidate Ranking

* TF-IDF Job Description Matching
* AI Assessment Score
* Culture Fit Score
* Final Composite Ranking Score

### Reporting

* Detailed candidate reports
* Hiring recommendations
* Interview preparation insights
* Candidate comparison

---

## Multi-Agent Architecture

The system consists of nine specialized AI agents:

| Agent              | Responsibility                         |
| ------------------ | -------------------------------------- |
| ParserAgent        | Extracts text from resumes             |
| ContactAgent       | Identifies candidate contact details   |
| AcademicAgent      | Extracts education and experience      |
| SkillAgent         | Performs skill extraction and matching |
| ProjectAgent       | Analyzes candidate projects            |
| SimilarityAgent    | Calculates resume-job similarity       |
| GeminiAnalystAgent | Performs AI-based candidate evaluation |
| RankingAgent       | Computes final candidate ranking       |
| ReportAgent        | Generates recruitment reports          |

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* Google Gemini API
* LangChain
* TF-IDF Vectorization

### Database

* SQLite

### Libraries

* PyPDF / PyPDF2
* Pandas
* NumPy
* Scikit-Learn
* Regex
* JSON

---

## System Workflow

1. Recruiter enters Job Description
2. Recruiter uploads candidate resumes
3. Resume text is extracted
4. Candidate details are identified
5. Skills and projects are analyzed
6. Resume is compared against Job Description
7. Gemini performs deep candidate evaluation
8. Composite scores are calculated
9. Candidates are ranked
10. Detailed reports are generated

---

## Installation

### Clone Repository

```bash
git clone [https://github.com/yourusername/recruitiq.git](https://github.com/Vinay-Stack51/Ai-resume-screening)
cd Ai-resume-screening
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create Streamlit Secrets:

```toml
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
```

### Run Application

```bash
streamlit run temp.py
```

---

## Screenshots

Add screenshots of:

* Dashboard
* Resume Upload Interface
* Candidate Ranking Table
* AI Evaluation Report
* Final Hiring Recommendation

---

## Future Enhancements

* Interview Scheduling
* Resume Fraud Detection
* ATS Integration
* LinkedIn Profile Analysis
* Multi-language Resume Support
* Recruiter Analytics Dashboard

---

## Project Highlights

* Agentic AI Architecture
* Multi-Agent Decision Pipeline
* AI-Powered Candidate Evaluation
* Automated Resume Screening
* Intelligent Candidate Ranking
* Recruiter-Friendly Dashboard

