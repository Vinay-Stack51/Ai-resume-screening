# =========================================
# IMPORTS
# =========================================
import streamlit as st
import pandas as pd
import re
import sqlite3
import spacy

from PyPDF2 import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# LANGCHAIN + GEMINI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)

set_bg("background.png")

# =========================================
# LOAD SPACY MODEL SAFELY
# =========================================
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="AI Resume Screening",
    layout="wide"
)

# =========================================
# GEMINI MODEL
# =========================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=st.secrets["GOOGLE_API_KEY"],
    temperature=0.3
)

# =========================================
# DATABASE INIT
# =========================================
def init_db():

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            phone TEXT,
            cgpa REAL,
            final_score REAL,
            ai_decision TEXT,
            ai_score REAL,
            hr_similarity REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================================
# SAVE TO DATABASE
# =========================================
def save_to_db(
    name,
    phone,
    cgpa,
    final_score,
    ai_decision,
    ai_score,
    hr_similarity
):

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            candidate_name,
            phone,
            cgpa,
            final_score,
            ai_decision,
            ai_score,
            hr_similarity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        phone,
        cgpa,
        final_score,
        ai_decision,
        ai_score,
        hr_similarity
    ))

    conn.commit()
    conn.close()

# =========================================
# TITLE
# =========================================
st.title("🤖 AI Resume Screening System")

# =========================================
# SKILLS & PROJECTS
# =========================================
ALL_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Data Science",
    "Cloud",
    "Web Development",
    "AI",
    "Deep Learning",
    "NLP"
]

ALL_PROJECTS = [
    "AI",
    "Web Development",
    "Mobile App",
    "Data Science",
    "Cloud",
    "Cyber Security",
    "ML"
]

# =========================================
# JOB REQUIREMENTS
# =========================================
st.header("📋 Job Requirements")

required_skills = st.multiselect(
    "Required Skills",
    ALL_SKILLS
)

required_projects = st.multiselect(
    "Required Projects",
    ALL_PROJECTS
)

min_cgpa = st.slider(
    "Minimum CGPA",
    0.0,
    10.0,
    6.0,
    0.1
)

# =========================================
# JOB DESCRIPTION
# =========================================
hr_description = st.text_area(
    "Job Description",
    height=150
)

# =========================================
# FILE UPLOAD
# =========================================
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# =========================================
# EXTRACT PDF TEXT
# =========================================
def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text.lower()

# =========================================
# EXTRACT CGPA
# =========================================
def extract_cgpa(text):

    matches = re.findall(r"(\d\.\d{1,2})", text)

    for m in matches:

        value = float(m)

        if value <= 10:
            return value

    return 0.0

# =========================================
# EXTRACT PHONE
# =========================================
def extract_phone(text):

    match = re.search(
        r'\+?\d[\d\s\-]{8,15}',
        text
    )

    return match.group(0) if match else "Not Found"

# =========================================
# EXTRACT NAME
# =========================================
def extract_name(text):

    if nlp is None:
        return "Unknown"

    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown"

# =========================================
# AI SKILL EXTRACTION
# =========================================
def extract_skills_langchain(text):

    if nlp is None:
        return []

    doc = nlp(text.lower())

    tokens = [
        token.text.strip()
        for token in doc
    ]

    noun_chunks = [
        chunk.text.strip()
        for chunk in doc.noun_chunks
    ]

    combined = tokens + noun_chunks

    template = """
    You are an HR skill analyzer.

    REQUIRED SKILLS:
    {required_skills}

    RESUME TERMS:
    {resume_terms}

    Return ONLY matched skills separated by commas.
    """

    prompt = PromptTemplate(
        input_variables=[
            "required_skills",
            "resume_terms"
        ],
        template=template
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    try:

        response = chain.invoke({
            "required_skills": required_skills,
            "resume_terms": combined
        })

        response_text = response["text"]

        skills = [
            skill.strip()
            for skill in response_text.split(",")
            if skill.strip()
        ]

        return list(set(skills))

    except Exception as e:

        st.error(f"Skill Extraction Error: {e}")

        return []

# =========================================
# PROJECT MATCH
# =========================================
def extract_projects(text):

    matches = []

    text_lower = text.lower()

    for proj in required_projects:

        if proj.lower() in text_lower:
            matches.append(proj)

    return matches

# =========================================
# HR KEYWORD FILTER
# =========================================
def hr_keywords_filter_dynamic(
    resume_text,
    hr_desc,
    selected_projects
):

    resume_text_lower = resume_text.lower()

    hr_desc_lower = hr_desc.lower()

    hr_keywords = [
        w for w in re.findall(
            r'\b\w{3,}\b',
            hr_desc_lower
        )
    ]

    project_keywords = [
        p.lower()
        for p in selected_projects
    ]

    all_keywords = set(
        hr_keywords + project_keywords
    )

    for kw in all_keywords:

        if kw in resume_text_lower:
            return True

    return False

# =========================================
# TF-IDF SIMILARITY SCORE
# =========================================
def hr_description_score(
    resume_text,
    hr_desc
):

    if not hr_desc.strip():
        return 0

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        resume_text,
        hr_desc
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)

# =========================================
# GEMINI AI EVALUATION
# =========================================
def gemini_evaluate(
    resume_text,
    job_description
):

    template = """
    You are an expert HR recruiter.

    JOB DESCRIPTION:
    {job_description}

    RESUME:
    {resume_text}

    Provide output in this format:

    Match Percentage: 0-100

    Strengths:
    - point1
    - point2

    Missing Skills:
    - point1
    - point2

    Final Recommendation:
    Strong Hire / Consider / Reject
    """

    prompt = PromptTemplate(
        input_variables=[
            "job_description",
            "resume_text"
        ],
        template=template
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    try:

        response = chain.invoke({
            "job_description": job_description,
            "resume_text": resume_text[:4000]
        })

        result_text = response["text"]

        match = re.search(
            r'Match Percentage:\s*(\d{1,3})',
            result_text
        )

        match_score = int(
            match.group(1)
        ) if match else 0

        return result_text, match_score

    except Exception as e:

        return f"Error: {str(e)}", 0

# =========================================
# MAIN SCREENING
# =========================================
if st.button("🚀 Screen Candidates"):

    if not hr_description.strip():

        st.warning(
            "Please enter Job Description."
        )

    elif not uploaded_files:

        st.warning(
            "Please upload resumes."
        )

    else:

        results = []

        for file in uploaded_files:

            text = extract_text(file)

            cgpa = extract_cgpa(text)

            disqualified_reason = ""

            # CGPA FILTER
            if cgpa < min_cgpa:

                disqualified_reason += (
                    "Low CGPA | "
                )

            # KEYWORD FILTER
            keyword_match = (
                hr_keywords_filter_dynamic(
                    text,
                    hr_description,
                    required_projects
                )
            )

            if not keyword_match:

                disqualified_reason += (
                    "HR Keywords Not Matched | "
                )

            # SKILL MATCH
            skill_match = extract_skills_langchain(text)

            # PROJECT MATCH
            project_match = extract_projects(text)

            # TF-IDF SCORE
            hr_score = hr_description_score(
                text,
                hr_description
            )

            # AI ANALYSIS
            with st.spinner(
                f"AI analyzing {file.name}..."
            ):

                ai_result, ai_score = (
                    gemini_evaluate(
                        text,
                        hr_description
                    )
                )

            # FINAL SCORE
            final_score = round(
                (
                    ai_score * 0.5
                    + hr_score * 0.3
                    + len(skill_match) * 5
                    + len(project_match) * 5
                ),
                2
            )

            # DECISION
            if disqualified_reason:

                ai_status = (
                    f"Disqualified ❌ "
                    f"({disqualified_reason})"
                )

            elif final_score < 40:

                ai_status = "Rejected ❌"

            elif final_score < 70:

                ai_status = "Consider 🤔"

            else:

                ai_status = "Strong Hire ✅"

            # NAME & PHONE
            name = extract_name(text)

            phone = extract_phone(text)

            # SAVE TO DB
            save_to_db(
                name,
                phone,
                cgpa,
                final_score,
                ai_status,
                ai_score,
                hr_score
            )

            # STORE RESULT
            results.append({
                "Candidate": name,
                "Phone": phone,
                "CGPA": cgpa,
                "Skill Matches": ", ".join(skill_match),
                "Project Matches": ", ".join(project_match),
                "HR Similarity %": hr_score,
                "AI Score": ai_score,
                "Final Score": final_score,
                "AI Decision": ai_status,
                "AI Report": ai_result
            })

        # CREATE DATAFRAME
        df = pd.DataFrame(results)

        # SORT
        df = df.sort_values(
            by="Final Score",
            ascending=False
        )

        # DISPLAY
        st.subheader("🏆 Candidate Ranking")

        st.dataframe(
            df.drop(columns=["AI Report"]),
            use_container_width=True
        )

        # AI REPORTS
        st.subheader("🧠 Detailed AI Reports")

        for index, row in df.iterrows():

            with st.expander(
                f"{row['Candidate']} - {row['Final Score']}"
            ):

                st.write(
                    f"📞 Phone: {row['Phone']}"
                )

                st.write(
                    f"🎓 CGPA: {row['CGPA']}"
                )

                st.write(
                    f"🤖 Decision: {row['AI Decision']}"
                )

                st.write(
                    row["AI Report"]
                )

# =========================================
# VIEW DATABASE
# =========================================
if st.button("📂 View Stored Candidates"):

    conn = sqlite3.connect(
        "candidates.db"
    )

    df_db = pd.read_sql_query(
        "SELECT * FROM candidates",
        conn
    )

    conn.close()

    st.dataframe(
        df_db,
        use_container_width=True
    )

# =========================================
# RESET DATABASE
# =========================================
if st.button("🗑 Reset Database"):

    conn = sqlite3.connect(
        "candidates.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM candidates"
    )

    conn.commit()

    conn.close()

    st.success(
        "Database cleared successfully ✅"
    )
