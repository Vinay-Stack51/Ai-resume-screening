import streamlit as st
import pandas as pd
import re
import PyPDF2
import google.generativeai as genai
import sqlite3
import base64
import spacy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------
# LOAD SPACY MODEL
# -------------------------
nlp = spacy.load("en_core_web_sm")

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Hybrid AI Recruitment Assistant",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>

.stTextArea > div > div {
    background-color: transparent !important;
}

.stTextArea textarea {
    background-color: transparent !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}

.stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.6) !important;
}

div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    backdrop-filter: blur(8px);
    color: white !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

div[role="listbox"] {
    background-color: transparent !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    color: white !important;
}

div[role="option"] {
    background-color: transparent !important;
    color: white !important;
}

div[role="option"]:hover {
    background-color: rgba(255,255,255,0.2) !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# BACKGROUND IMAGE
# -------------------------
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

# -------------------------
# GEMINI API
# -------------------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# DATABASE
# -------------------------
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

# -------------------------
# SAVE TO DATABASE
# -------------------------
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
        INSERT INTO candidates
        (
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

# -------------------------
# TITLE
# -------------------------
st.title("🤖 Hybrid AI-Powered Recruitment Assistant")

st.markdown("""
Rule-Based Filtering + NLP + Gemini AI + SQLite Storage
""")

# -------------------------
# SKILLS
# -------------------------
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

# -------------------------
# JOB REQUIREMENTS
# -------------------------
st.header("📋 Job Requirements")

required_skills = st.multiselect(
    "🧠 Required Skills",
    ALL_SKILLS
)

required_projects = st.multiselect(
    "📁 Required Project Domains",
    ALL_PROJECTS
)

min_cgpa = st.slider(
    "🎓 Minimum CGPA",
    0.0,
    10.0,
    6.0,
    0.1
)

# -------------------------
# JOB DESCRIPTION
# -------------------------
hr_description = st.text_area(
    "✍️ Full Job Description",
    height=150
)

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_files = st.file_uploader(
    "📄 Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# -------------------------
# PDF TEXT EXTRACTION
# -------------------------
def extract_text(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text.lower()

# -------------------------
# EXTRACT CGPA
# -------------------------
def extract_cgpa(text):

    matches = re.findall(r"(\d\.\d{1,2})", text)

    for m in matches:

        value = float(m)

        if value <= 10:
            return value

    return 0.0

# -------------------------
# EXTRACT PHONE
# -------------------------
def extract_phone(text):

    match = re.search(r'\+?\d[\d\s\-]{8,15}', text)

    return match.group(0) if match else "Not Found"

# -------------------------
# EXTRACT NAME USING SPACY
# -------------------------
def extract_name(text):

    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown"

# -------------------------
# NLP SKILL EXTRACTION
# -------------------------
def extract_skills_spacy(text):

    doc = nlp(text.lower())

    extracted_skills = set()

    tokens = [
        token.text.strip()
        for token in doc
    ]

    noun_chunks = [
        chunk.text.strip()
        for chunk in doc.noun_chunks
    ]

    combined = tokens + noun_chunks

    prompt = f"""
You are an intelligent HR skill analyzer.

HR REQUIRED SKILLS:
{required_skills}

RESUME TERMS:
{combined}

Determine which required skills are satisfied.

Example:
spaCy -> NLP
TensorFlow -> Machine Learning
AWS -> Cloud

Return ONLY comma separated matched skills.
"""

    try:

        response = model.generate_content(prompt)

        ai_output = response.text.strip()

        skills = [
            skill.strip()
            for skill in ai_output.split(",")
            if skill.strip()
        ]

        return list(set(skills))

    except:

        return []

# -------------------------
# PROJECT MATCH
# -------------------------
def extract_projects(text):

    matches = []

    text_lower = text.lower()

    for proj in required_projects:

        if proj.lower() in text_lower:
            matches.append(proj)

    return matches

# -------------------------
# HR KEYWORD FILTER
# -------------------------
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

# -------------------------
# TF-IDF SCORE
# -------------------------
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

# -------------------------
# GEMINI EVALUATION
# -------------------------
def gemini_evaluate(
    resume_text,
    job_description
):

    prompt = f"""
You are an expert HR recruiter.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text[:4000]}

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

    try:

        response = model.generate_content(prompt)

        result_text = response.text

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

# -------------------------
# MAIN SCREENING
# -------------------------
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

            if cgpa < min_cgpa:

                disqualified_reason += (
                    "Low CGPA | "
                )

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

            skill_match = extract_skills_spacy(text)

            project_match = extract_projects(text)

            hr_score = hr_description_score(
                text,
                hr_description
            )

            with st.spinner(
                f"Gemini analyzing {file.name}..."
            ):

                ai_result, ai_score = (
                    gemini_evaluate(
                        text,
                        hr_description
                    )
                )

            final_score = round(
                (
                    ai_score * 0.5
                    + hr_score * 0.3
                    + len(skill_match) * 5
                    + len(project_match) * 5
                ),
                2
            )

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

            name = extract_name(text)

            phone = extract_phone(text)

            save_to_db(
                name,
                phone,
                cgpa,
                final_score,
                ai_status,
                ai_score,
                hr_score
            )

            results.append({
                "Candidate": name,
                "Phone": phone,
                "CGPA": cgpa,
                "Skill Matches": ", ".join(skill_match) if skill_match else "None",
                "Project Matches": ", ".join(project_match) if project_match else "None",
                "HR Similarity %": hr_score,
                "AI Score": ai_score,
                "Final Score": final_score,
                "AI Decision": ai_status,
                "AI Report": ai_result
            })

        if not results:

            st.warning(
                "No resumes processed."
            )

        else:

            df = pd.DataFrame(results)

            df = df.sort_values(
                by="Final Score",
                ascending=False
            ).reset_index(drop=True)

            st.subheader(
                "🏆 Candidate Ranking"
            )

            st.dataframe(
                df.drop(columns=["AI Report"]),
                use_container_width=True
            )

            st.subheader(
                "🧠 Detailed AI Reports"
            )

            for index, row in df.iterrows():

                with st.expander(
                    f"{row['Candidate']} - "
                    f"{row['Final Score']}"
                ):

                    st.write(
                        f"📞 Phone: {row['Phone']}"
                    )

                    st.write(
                        f"🎓 CGPA: {row['CGPA']}"
                    )

                    st.write(
                        f"🤖 Decision: "
                        f"{row['AI Decision']}"
                    )

                    st.write(
                        row["AI Report"]
                    )

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "📥 Download Full Report",
                csv,
                "Candidate_Report.csv",
                "text/csv"
            )

# -------------------------
# VIEW DATABASE
# -------------------------
if st.button("📂 View Stored Candidates"):

    conn = sqlite3.connect(
        "candidates.db"
    )

    df_db = pd.read_sql_query(
        "SELECT * FROM candidates",
        conn
    )

    conn.close()

    st.subheader(
        "📊 Stored Candidates Database"
    )

    st.dataframe(
        df_db,
        use_container_width=True
    )

# -------------------------
# RESET DATABASE
# -------------------------
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
