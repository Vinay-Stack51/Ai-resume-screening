# =========================================
# AGENTIC AI RESUME SCREENING SYSTEM
# Multi-Agent Pipeline with Tool Use
# =========================================

import streamlit as st

st.set_page_config(
    page_title="Resume Screening",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS: Clean dark-blue professional theme ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: #0A0E1A;
    color: #E2E8F0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0F1629 !important;
    border-right: 1px solid #1E2A4A;
}

/* Cards */
.agent-card {
    background: #111827;
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
    transition: border-color 0.3s;
}
.agent-card:hover { border-color: #3B82F6; }

.agent-card.running {
    border-color: #F59E0B;
    box-shadow: 0 0 20px rgba(245,158,11,0.15);
}
.agent-card.done {
    border-color: #10B981;
    box-shadow: 0 0 20px rgba(16,185,129,0.10);
}
.agent-card.failed {
    border-color: #EF4444;
}

/* Agent header */
.agent-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}
.agent-name {
    font-weight: 600;
    font-size: 15px;
    color: #93C5FD;
}
.agent-status {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 500;
    letter-spacing: 0.5px;
}
.status-idle     { background:#1E293B; color:#64748B; }
.status-running  { background:#7C2D12; color:#FCD34D; }
.status-done     { background:#064E3B; color:#6EE7B7; }
.status-failed   { background:#7F1D1D; color:#FCA5A5; }

/* Metrics row */
.metrics-row {
    display: flex;
    gap: 16px;
    margin: 20px 0;
    flex-wrap: wrap;
}
.metric-box {
    flex: 1;
    min-width: 140px;
    background: #111827;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #60A5FA;
}
.metric-label {
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Pipeline trace log */
.trace-log {
    background: #050810;
    border: 1px solid #1E2A4A;
    border-radius: 8px;
    padding: 14px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    max-height: 260px;
    overflow-y: auto;
    color: #94A3B8;
}
.trace-log .log-info    { color: #60A5FA; }
.trace-log .log-success { color: #34D399; }
.trace-log .log-warn    { color: #FBBF24; }
.trace-log .log-error   { color: #F87171; }

/* Candidate card */
.candidate-card {
    background: #111827;
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 22px;
    margin: 14px 0;
}
.candidate-name {
    font-size: 18px;
    font-weight: 700;
    color: #F0F4FF;
}
.score-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
    margin-left: 12px;
}
.badge-hire    { background:#064E3B; color:#6EE7B7; }
.badge-consider{ background:#78350F; color:#FDE68A; }
.badge-reject  { background:#7F1D1D; color:#FCA5A5; }

/* Section titles */
.section-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 16px 0 8px;
}

/* Skill chip */
.chip {
    display: inline-block;
    background: #1E3A5F;
    color: #93C5FD;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    margin: 3px;
}
.chip.matched { background:#064E3B; color:#6EE7B7; }
.chip.missing { background:#7F1D1D; color:#FCA5A5; }

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E3A5F, transparent);
    margin: 24px 0;
}

/* Top header */
.top-header {
    background: linear-gradient(135deg, #0F1629 0%, #1a1f3a 100%);
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 30px 36px;
    margin-bottom: 28px;
}
.top-header h1 {
    font-size: 32px;
    font-weight: 700;
    color: #F0F4FF;
    margin: 0;
}
.top-header p {
    color: #64748B;
    font-size: 14px;
    margin: 6px 0 0;
}
.top-header .tag {
    display: inline-block;
    background: #1E3A5F;
    color: #60A5FA;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

/* Progress bar */
.progress-outer {
    background: #1E293B;
    border-radius: 4px;
    height: 6px;
    margin: 8px 0;
    overflow: hidden;
}
.progress-inner {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
    transition: width 0.5s ease;
}

/* AI reasoning box */
.reasoning-box {
    background: #050810;
    border-left: 3px solid #3B82F6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #94A3B8;
    white-space: pre-wrap;
    line-height: 1.7;
}

.stButton > button {
    background: linear-gradient(135deg, #3B82F6, #6366F1);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 24px;
    font-size: 14px;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid #1E3A5F !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
}

.stSlider [data-testid="stThumbValue"] { color: #60A5FA !important; }

h1,h2,h3 { color: #F0F4FF !important; }
label { color: #94A3B8 !important; }
</style>
""", unsafe_allow_html=True)


import pandas as pd
import re
import sqlite3
import json
import time
import base64
from datetime import datetime
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

# ─── GEMINI LLM ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    import asyncio

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=0.2
    )
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
llm = get_llm()

# ─── DATABASE ──────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("recruitiq.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            screened_at TEXT,
            candidate_name TEXT,
            phone TEXT,
            email TEXT,
            cgpa REAL,
            years_exp REAL,
            education_level TEXT,
            extracted_skills TEXT,
            matched_skills TEXT,
            missing_skills TEXT,
            project_matches TEXT,
            tfidf_score REAL,
            ai_score INTEGER,
            culture_score INTEGER,
            final_score REAL,
            decision TEXT,
            strengths TEXT,
            red_flags TEXT,
            interview_questions TEXT,
            salary_estimate TEXT,
            agent_trace TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_screening(data: dict):
    conn = sqlite3.connect("recruitiq.db")
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO screenings (
                session_id, screened_at, candidate_name, phone, email,
                cgpa, years_exp, education_level,
                extracted_skills, matched_skills, missing_skills, project_matches,
                tfidf_score, ai_score, culture_score, final_score, decision,
                strengths, red_flags, interview_questions, salary_estimate, agent_trace
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            str(data.get("session_id","")),
            str(data.get("screened_at","")),
            str(data.get("name","")),
            str(data.get("phone","")),
            str(data.get("email","")),

            float(data.get("cgpa",0) or 0),
            float(data.get("years_exp",0) or 0),

            str(data.get("education_level","")),

            json.dumps(data.get("extracted_skills", [])),
            json.dumps(data.get("matched_skills", [])),
            json.dumps(data.get("missing_skills", [])),
            json.dumps(data.get("project_matches", [])),

            float(data.get("tfidf_score",0) or 0),
            int(data.get("ai_score",0) or 0),
            int(data.get("culture_score",0) or 0),
            float(data.get("final_score",0) or 0),

            str(data.get("decision","")),

            json.dumps(data.get("strengths", [])),
            json.dumps(data.get("red_flags", [])),
            json.dumps(data.get("interview_questions", [])),

            str(data.get("salary_estimate","")),

            json.dumps(data.get("agent_trace", []))
        ))

        conn.commit()

    except Exception as e:
        st.error(f"Database Error: {e}")
        raise

    finally:
        conn.close()

# ─── TOOL DEFINITIONS (for agent to "use") ─────────────────────────────────────
ALL_SKILLS = [
    "Python","Java","C++","C","JavaScript","TypeScript","Go","Rust","R","Scala",
    "SQL","NoSQL","MongoDB","PostgreSQL","MySQL","Redis",
    "Machine Learning","Deep Learning","NLP","Computer Vision","Reinforcement Learning",
    "Data Science","Data Engineering","MLOps","LLMOps",
    "TensorFlow","PyTorch","Keras","Scikit-learn","Hugging Face","LangChain","OpenAI",
    "AWS","Azure","GCP","Docker","Kubernetes","CI/CD","Git","Linux",
    "React","Node.js","FastAPI","Flask","Django","Spring Boot",
    "Web Development","Mobile App","Cloud","Cyber Security",
    "AI","Generative AI","RAG","Vector Databases","Transformers","BERT","GPT"
]

ALL_PROJECTS = [
    "AI","Machine Learning","Deep Learning","NLP","Computer Vision",
    "Web Development","Mobile App","Data Science","Cloud",
    "Cyber Security","ML","Generative AI","RAG","Chatbot","LLM"
]

# ─── AGENT TOOLS ───────────────────────────────────────────────────────────────

def tool_extract_pdf_text(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + " "
    return text.strip()

def tool_extract_contact_info(text: str) -> dict:
    """Agent Tool: Extract name, phone, email from resume text."""
    phone_match = re.search(r'(\+?\d[\d\s\-]{8,15}\d)', text)
    phone = phone_match.group(0).strip() if phone_match else "Not Found"
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else "Not Found"
    name = "Unknown"
    lines = text.split("\n")
    for line in lines[:15]:
        line = line.strip()
        if not line or "@" in line or re.search(r'\d{4,}', line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() if w else True for w in words):
            name = line.title()
            break
    if name == "Unknown" and nlp:
        doc = nlp(text[:1000])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.title()
                break
    return {"name": name, "phone": phone, "email": email}

def tool_extract_academic_info(text: str) -> dict:
    """Agent Tool: Extract CGPA, education level, years of experience."""
    cgpa = 0.0
    matches = re.findall(r'(\d\.\d{1,2})', text)
    for m in matches:
        v = float(m)
        if 5.0 <= v <= 10.0:
            cgpa = v
            break

    education_level = "Unknown"
    text_lower = text.lower()
    if any(w in text_lower for w in ["phd","ph.d","doctorate"]):
        education_level = "PhD"
    elif any(w in text_lower for w in ["m.tech","m.e.","mtech","msc","m.sc","master"]):
        education_level = "Masters"
    elif any(w in text_lower for w in ["b.tech","btech","b.e.","bsc","bachelor"]):
        education_level = "Bachelors"
    elif "diploma" in text_lower:
        education_level = "Diploma"

    exp_match = re.findall(r'(\d+\.?\d*)\s*\+?\s*years?\s*(of\s+)?experience', text_lower)
    years_exp = float(exp_match[0][0]) if exp_match else 0.0

    return {"cgpa": cgpa, "education_level": education_level, "years_exp": years_exp}

import re
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def tool_skill_matcher(text: str, required_skills: list) -> dict:

    text_lower = text.lower()

    # Existing keyword extraction
    found_skills = []

    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    # spaCy NLP extraction
    doc = nlp(text)

    candidate_terms = set()

    # nouns & proper nouns
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if len(token.text.strip()) > 2:
                candidate_terms.add(token.text.lower())

    # noun chunks
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()

        if len(phrase) > 2:
            candidate_terms.add(phrase)

    candidate_terms.update(
        [s.lower() for s in found_skills]
    )

    # keyword matches (Gemini will improve later)
    matched = [
        skill
        for skill in required_skills
        if skill in found_skills
    ]

    missing = [
        skill
        for skill in required_skills
        if skill not in found_skills
    ]

    extra = [
        skill
        for skill in found_skills
        if skill not in required_skills
    ]

    return {
        "extracted_skills": found_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "candidate_terms": sorted(list(candidate_terms))
    }

def tool_project_analyzer(text: str, required_projects: list) -> dict:
    """Agent Tool: Find relevant projects in resume."""
    text_lower = text.lower()
    found = []
    for proj in ALL_PROJECTS:
        if proj.lower() in text_lower:
            found.append(proj)
    matched = [p for p in required_projects if p in found]
    return {"found_projects": found, "matched_required": matched}

def tool_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """Agent Tool: Cosine similarity between resume and JD."""
    if not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    vecs = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
    return round(score * 100, 2)

def tool_gemini_deep_analyze(
    resume_text: str,
    jd: str,
    role: str,
    extracted_skills: list,
    candidate_terms: list
) -> dict:

    template = """
You are an expert AI recruiter and technical hiring specialist.

ROLE:
{role}

JOB DESCRIPTION:
{jd}

EXTRACTED SKILLS:
{skills}

EXTRACTED CANDIDATE CONCEPTS:
{candidate_terms}

RESUME:
{resume}

Instructions:

- Use semantic reasoning, not just keyword matching.
- Consider related technologies as relevant.
- Evaluate technical depth.
- Infer transferable skills.
- Compare candidate concepts against job requirements.

Return ONLY valid JSON.

{{
"match_score": <0-100 integer>,
"culture_fit_score": <0-100 integer>,
"strengths": ["point1","point2","point3"],
"red_flags": ["flag1","flag2"],
"missing_skills": ["skill1","skill2"],
"related_skills": ["skill1","skill2"],
"recommendation": "Strong Hire" | "Consider" | "Reject",
"reasoning": "2-3 sentence explanation",
"salary_estimate": "range like 6-9 LPA or N/A",
"interview_questions": [
    "q1",
    "q2",
    "q3",
    "q4",
    "q5"
]
}}
"""

    prompt = PromptTemplate(
        input_variables=[
            "role",
            "jd",
            "skills",
            "candidate_terms",
            "resume"
        ],
        template=template
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    try:

        response = chain.invoke({
            "role": role,
            "jd": jd,
            "skills": json.dumps(extracted_skills),
            "candidate_terms": json.dumps(candidate_terms[:300]),
            "resume": resume_text[:5000]
        })

        text = (
            response.get("text", "")
            if isinstance(response, dict)
            else response.content
        )

        text = text.strip()

        text = re.sub(
            r"```json|```",
            "",
            text
        ).strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        return json.loads(text)

    except Exception as e:

        return {
            "match_score": 0,
            "culture_fit_score": 0,
            "strengths": [],
            "red_flags": [str(e)],
            "missing_skills": [],
            "related_skills": [],
            "recommendation": "Reject",
            "reasoning": f"Analysis failed: {e}",
            "salary_estimate": "N/A",
            "interview_questions": []
        }

def tool_rank_candidates(candidates: list) -> list:
    """Agent Tool: Rank candidates by weighted final score."""
    def compute_score(c):
        return round(
            c.get("ai_score", 0) * 0.40 +
            c.get("culture_score", 0) * 0.15 +
            c.get("tfidf_score", 0) * 0.20 +
            min(len(c.get("matched_skills",[])) * 5, 20) * 0.15 +
            min(c.get("cgpa", 0) * 5, 50) * 0.10,
            2
        )
    for c in candidates:
        c["final_score"] = compute_score(c)
    return sorted(candidates, key=lambda x: x["final_score"], reverse=True)

def tool_generate_screening_report(candidate: dict) -> str:
    """Agent Tool: Generate structured screening summary."""
    return f"""
CANDIDATE SCREENING REPORT
══════════════════════════════════
Name      : {candidate.get('name')}
Decision  : {candidate.get('decision')}
Final Score: {candidate.get('final_score')} / 100

SCORES BREAKDOWN
  AI Match      : {candidate.get('ai_score',0)}/100
  Culture Fit   : {candidate.get('culture_score',0)}/100
  JD Similarity : {candidate.get('tfidf_score',0)}/100
  CGPA          : {candidate.get('cgpa',0)}/10
  Experience    : {candidate.get('years_exp',0)} years

SKILLS
  Matched : {', '.join(candidate.get('matched_skills',[]))}
  Missing : {', '.join(candidate.get('missing_skills',[]))}

STRENGTHS
{chr(10).join('  • ' + s for s in candidate.get('strengths',[]))}

RED FLAGS
{chr(10).join('  ⚠ ' + r for r in candidate.get('red_flags',[])) or '  None'}

AI REASONING
  {candidate.get('reasoning','')}
══════════════════════════════════
"""

# ─── ORCHESTRATOR AGENT ───────────────────────────────────────────────────────

class RecruitIQOrchestrator:
    """
    Multi-step agentic pipeline:
    Agent 0 → Parsing Agent     (PDF extraction)
    Agent 1 → Contact Agent     (name, phone, email)
    Agent 2 → Academic Agent    (CGPA, education, experience)
    Agent 3 → Skill Agent       (skill matching)
    Agent 4 → Project Agent     (project matching)
    Agent 5 → Similarity Agent  (TF-IDF JD match)
    Agent 6 → AI Deep Analyst   (Gemini LLM evaluation)
    Agent 7 → Ranking Agent     (score & rank all candidates)
    Agent 8 → Report Agent      (final screening reports)
    """

    def __init__(self, jd: str, role: str, required_skills: list,
                 required_projects: list, min_cgpa: float):
        self.jd = jd
        self.role = role
        self.required_skills = required_skills
        self.required_projects = required_projects
        self.min_cgpa = min_cgpa
        self.trace = []
        self.candidates = []

    def log(self, level: str, agent: str, message: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.trace.append({"ts": ts, "level": level, "agent": agent, "msg": message})

    def run(self, uploaded_files, status_containers: dict):
        """Execute the full agentic pipeline."""

        # ── PHASE 1: PER-RESUME AGENTS ───────────────────────────────────────
        for file in uploaded_files:
            candidate_data = {"agent_trace": [], "session_id": st.session_state.get("session_id","")}

            # ── Agent 0: Parsing Agent ─────────────────────────────────────────
            self._set_status(status_containers, "parser", "running")
            self.log("info","ParserAgent",f"Extracting text from: {file.name}")
            text = tool_extract_pdf_text(file)
            candidate_data["raw_text"] = text
            candidate_data["filename"] = file.name
            self.log("success","ParserAgent",f"Extracted {len(text)} chars")
            self._set_status(status_containers, "parser", "done")

            # ── Agent 1: Contact Agent ─────────────────────────────────────────
            self._set_status(status_containers, "contact", "running")
            self.log("info","ContactAgent","Extracting contact information")
            contact = tool_extract_contact_info(text)
            candidate_data.update(contact)
            self.log("success","ContactAgent",f"Found: {contact['name']} | {contact['email']}")
            self._set_status(status_containers, "contact", "done")

            # ── Agent 2: Academic Agent ────────────────────────────────────────
            self._set_status(status_containers, "academic", "running")
            self.log("info","AcademicAgent","Extracting academic & experience info")
            academic = tool_extract_academic_info(text)
            candidate_data.update(academic)
            disqualified = ""
            if academic["cgpa"] < self.min_cgpa and academic["cgpa"] > 0:
                disqualified += "Low CGPA | "
                self.log("warn","AcademicAgent",f"CGPA {academic['cgpa']} below threshold {self.min_cgpa}")
            else:
                self.log("success","AcademicAgent",f"CGPA: {academic['cgpa']} | Education: {academic['education_level']} | Exp: {academic['years_exp']}y")
            self._set_status(status_containers, "academic", "done")

            # ── Agent 3: Skill Matching Agent ──────────────────────────────────
            self._set_status(status_containers, "skills", "running")
            self.log("info","SkillAgent",f"Matching against {len(self.required_skills)} required skills")
            skill_data = tool_skill_matcher(text, self.required_skills)
            candidate_data.update(skill_data)
            self.log("success","SkillAgent",
                f"Matched {len(skill_data['matched_skills'])}/{len(self.required_skills)} | "
                f"Also found: {', '.join(skill_data['extra_skills'][:5])}")
            self._set_status(status_containers, "skills", "done")

            # ── Agent 4: Project Analysis Agent ───────────────────────────────
            self._set_status(status_containers, "projects", "running")
            self.log("info","ProjectAgent","Scanning resume for relevant projects")
            project_data = tool_project_analyzer(text, self.required_projects)
            candidate_data["found_projects"] = project_data["found_projects"]
            candidate_data["project_matches"] = project_data["matched_required"]
            self.log("success","ProjectAgent",f"Found projects: {', '.join(project_data['found_projects'][:5])}")
            self._set_status(status_containers, "projects", "done")

            # ── Agent 5: Similarity Agent ──────────────────────────────────────
            self._set_status(status_containers, "similarity", "running")
            self.log("info","SimilarityAgent","Computing TF-IDF cosine similarity with JD")
            tfidf = tool_tfidf_similarity(text, self.jd)
            candidate_data["tfidf_score"] = tfidf
            self.log("success","SimilarityAgent",f"JD Similarity: {tfidf}%")
            self._set_status(status_containers, "similarity", "done")

            # ── Agent 6: AI Deep Analyst ───────────────────────────────────────
            self._set_status(status_containers, "llm", "running")
            self.log("info","GeminiAnalystAgent",f"Running deep LLM analysis for {candidate_data['name']}")
            ai_result = tool_gemini_deep_analyze(text, self.jd, self.role,candidate_data["extracted_skills"],candidate_data["candidate_terms"])
            candidate_data["ai_score"] = ai_result.get("match_score", 0)
            candidate_data["culture_score"] = ai_result.get("culture_fit_score", 0)
            candidate_data["strengths"] = ai_result.get("strengths", [])
            candidate_data["red_flags"] = ai_result.get("red_flags", [])
            candidate_data["missing_skills"] += [
                s for s in ai_result.get("missing_skills", [])
                if s not in candidate_data["missing_skills"]
            ]
            candidate_data["recommendation"] = ai_result.get("recommendation","Reject")
            candidate_data["reasoning"] = ai_result.get("reasoning","")
            candidate_data["salary_estimate"] = ai_result.get("salary_estimate","N/A")
            candidate_data["interview_questions"] = ai_result.get("interview_questions",[])
            if disqualified:
                candidate_data["decision"] = f"Disqualified ❌ ({disqualified.strip('| ')})"
            else:
                candidate_data["decision"] = {
                    "Strong Hire": "Strong Hire ✅",
                    "Consider": "Consider 🤔",
                    "Reject": "Rejected ❌"
                }.get(ai_result.get("recommendation","Reject"), "Rejected ❌")
            self.log("success","GeminiAnalystAgent",
                f"Match: {ai_result.get('match_score')}% | Rec: {ai_result.get('recommendation')}")
            self._set_status(status_containers, "llm", "done")

            candidate_data["agent_trace"] = self.trace.copy()
            candidate_data["screened_at"] = datetime.now().isoformat()
            self.candidates.append(candidate_data)

        # ── PHASE 2: RANKING AGENT ────────────────────────────────────────────
        self._set_status(status_containers, "ranking", "running")
        self.log("info","RankingAgent",f"Ranking {len(self.candidates)} candidates")
        self.candidates = tool_rank_candidates(self.candidates)
        self.log("success","RankingAgent","Candidates ranked by weighted composite score")
        self._set_status(status_containers, "ranking", "done")

        # ── PHASE 3: REPORT AGENT ─────────────────────────────────────────────
        self._set_status(status_containers, "report", "running")
        self.log("info","ReportAgent","Generating structured screening reports")
        for c in self.candidates:
            c["report"] = tool_generate_screening_report(c)
            save_screening(c)
        self.log("success","ReportAgent","All reports generated and saved to database")
        self._set_status(status_containers, "report", "done")

        return self.candidates

    def _set_status(self, containers, key, status):
        if key in containers and containers[key] is not None:
            icons = {"running":"⚡","done":"✓","idle":"○","failed":"✗"}
            labels = {
                "parser":"Parsing Agent","contact":"Contact Agent",
                "academic":"Academic Agent","skills":"Skill Matching Agent",
                "projects":"Project Analysis Agent","similarity":"Similarity Agent",
                "llm":"Gemini Analyst Agent","ranking":"Ranking Agent","report":"Report Agent"
            }
            css = {"running":"running","done":"done","idle":"","failed":"failed"}
            status_map = {
                "running": '<span class="agent-status status-running">⚡ RUNNING</span>',
                "done":    '<span class="agent-status status-done">✓ DONE</span>',
                "failed":  '<span class="agent-status status-failed">✗ FAILED</span>',
            }
            containers[key].markdown(f"""
<div class="agent-card {css.get(status,'')}">
  <div class="agent-header">
    <span class="agent-name">{labels.get(key,key)}</span>
    {status_map.get(status,'')}
  </div>
</div>""", unsafe_allow_html=True)


# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"
if "results" not in st.session_state:
    st.session_state.results = []
if "trace" not in st.session_state:
    st.session_state.trace = []

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px">
      <div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:2px;margin-bottom:4px">Resume Screening</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**📋 Job Configuration**")
    role_name = st.text_input("Role Title", placeholder="e.g. ML Engineer, Data Scientist")

    required_skills = st.multiselect(
        "Required Skills",
        sorted(ALL_SKILLS),
        default=["Python","Machine Learning"]
    )
    required_projects = st.multiselect(
        "Required Project Areas",
        ALL_PROJECTS
    )
    min_cgpa = st.slider("Minimum CGPA", 0.0, 10.0, 6.5, 0.1)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    # st.markdown("**🤖 Pipeline Agents**")
    # agents_info = [
    #     ("ParserAgent","PDF text extraction"),
    #     ("ContactAgent","Name, phone, email"),
    #     ("AcademicAgent","CGPA, education, exp"),
    #     ("SkillAgent","Skill matching & gap"),
    #     ("ProjectAgent","Project analysis"),
    #     ("SimilarityAgent","TF-IDF JD match"),
    #     ("GeminiAnalystAgent","LLM deep evaluation"),
    #     ("RankingAgent","Composite scoring"),
    #     ("ReportAgent","Report generation"),
    # ]
    # for name, desc in agents_info:
    #     st.markdown(f"""
    #     <div style="display:flex;justify-content:space-between;align-items:center;
    #                 padding:6px 0;border-bottom:1px solid #1E2A4A">
    #       <span style="font-size:12px;color:#93C5FD;font-weight:500">{name}</span>
    #       <span style="font-size:11px;color:#64748B">{desc}</span>
    #     </div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.button("🗑 Clear Database"):
        conn = sqlite3.connect("recruitiq.db")
        conn.execute("DELETE FROM screenings")
        conn.commit()
        conn.close()
        st.session_state.results = []
        st.success("Database cleared ✅")

# ─── MAIN AREA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
  <h1>🧠Resume Screening</h1>
  <p>Multi-agent orchestration: each resume passes through 9 specialized AI agents before a final hiring decision is made.</p>
</div>
""", unsafe_allow_html=True)

# JD input
st.markdown("### 📄 Job Description")
jd = st.text_area("Paste the full job description here",
                   height=160,
                   placeholder="Paste the complete job description including responsibilities, requirements, and company culture...")

# File upload
st.markdown("### 📂 Upload Resumes")
uploaded_files = st.file_uploader(
    "Drop resume PDFs here",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload one or more PDF resumes to screen"
)

if uploaded_files:
    st.markdown(f"""
    <div style="background:#111827;border:1px solid #1E3A5F;border-radius:8px;
                padding:12px 16px;margin:8px 0;font-size:13px;color:#94A3B8">
      📎 {len(uploaded_files)} resume(s) queued — {', '.join(f.name for f in uploaded_files)}
    </div>""", unsafe_allow_html=True)

# ─── RUN PIPELINE BUTTON ───────────────────────────────────────────────────────
col1, col2 = st.columns([1,4])
with col1:
    run_btn = st.button("🚀 Run Agent Pipeline", use_container_width=True)

if run_btn:
    if not jd.strip():
        st.warning("Please paste a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    elif not role_name.strip():
        st.warning("Please enter the role title in the sidebar.")
    else:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Agent Execution Pipeline")

        # Create 3-col agent status grid
        col_a, col_b, col_c = st.columns(3)
        status_containers = {}

        with col_a:
            status_containers["parser"]     = st.empty()
            status_containers["contact"]    = st.empty()
            status_containers["academic"]   = st.empty()
        with col_b:
            status_containers["skills"]     = st.empty()
            status_containers["projects"]   = st.empty()
            status_containers["similarity"] = st.empty()
        with col_c:
            status_containers["llm"]        = st.empty()
            status_containers["ranking"]    = st.empty()
            status_containers["report"]     = st.empty()

        # Initialize all as idle
        for key, label in [
            ("parser","Parsing Agent"),("contact","Contact Agent"),("academic","Academic Agent"),
            ("skills","Skill Matching Agent"),("projects","Project Analysis Agent"),
            ("similarity","Similarity Agent"),("llm","Gemini Analyst Agent"),
            ("ranking","Ranking Agent"),("report","Report Agent")
        ]:
            status_containers[key].markdown(f"""
<div class="agent-card">
  <div class="agent-header">
    <span class="agent-name">{label}</span>
    <span class="agent-status status-idle">○ IDLE</span>
  </div>
</div>""", unsafe_allow_html=True)
        # Run orchestrator
        orchestrator = RecruitIQOrchestrator(
            jd=jd,
            role=role_name,
            required_skills=required_skills,
            required_projects=required_projects,
            min_cgpa=min_cgpa
        )
        
        with st.spinner("🔍 Screening resumes..."):
            results = orchestrator.run(uploaded_files, status_containers)
        
        # Mark all pipeline stages as completed
        for key in status_containers:
            orchestrator._set_status(status_containers, key, "done")
        
        st.session_state.results = results
        
        st.success(f"{len(results)} candidate(s) screened")

        # Trace log placeholder

        # st.markdown("**Live Agent Trace**")
        # trace_placeholder = st.empty()

        # # Run orchestrator
        # orchestrator = RecruitIQOrchestrator(
        #     jd=jd,
        #     role=role_name,
        #     required_skills=required_skills,
        #     required_projects=required_projects,
        #     min_cgpa=min_cgpa
        # )

        # with st.spinner(""):
        #     results = orchestrator.run(uploaded_files, status_containers)

        # # Update trace log live
        # trace_html = "<div class='trace-log'>"
        # for entry in orchestrator.trace:
        #     css_class = {"info":"log-info","success":"log-success",
        #                  "warn":"log-warn","error":"log-error"}.get(entry["level"],"")
        #     trace_html += f'<div class="{css_class}">[{entry["ts"]}] [{entry["agent"]}] {entry["msg"]}</div>'
        # trace_html += "</div>"
        # trace_placeholder.markdown(trace_html, unsafe_allow_html=True)

        # st.session_state.results = results
        # st.session_state.trace = orchestrator.trace
        # st.success(f"✅ Pipeline complete — {len(results)} candidate(s) screened")


# ─── RESULTS ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    results = st.session_state.results
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Summary metrics
    total = len(results)
    hires = sum(1 for r in results if "Strong Hire" in r.get("decision",""))
    considers = sum(1 for r in results if "Consider" in r.get("decision",""))
    rejected = total - hires - considers
    avg_score = round(sum(r.get("final_score",0) for r in results)/total, 1) if total else 0

    st.markdown(f"""
    <div class="metrics-row">
      <div class="metric-box">
        <div class="metric-value">{total}</div>
        <div class="metric-label">Total Screened</div>
      </div>
      <div class="metric-box">
        <div class="metric-value" style="color:#34D399">{hires}</div>
        <div class="metric-label">Strong Hires</div>
      </div>
      <div class="metric-box">
        <div class="metric-value" style="color:#FBBF24">{considers}</div>
        <div class="metric-label">Consider</div>
      </div>
      <div class="metric-box">
        <div class="metric-value" style="color:#F87171">{rejected}</div>
        <div class="metric-label">Rejected</div>
      </div>
      <div class="metric-box">
        <div class="metric-value" style="color:#A78BFA">{avg_score}</div>
        <div class="metric-label">Avg Score</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 Candidate Rankings")

    # DataFrame view
    df_rows = []
    for i, r in enumerate(results, 1):
        df_rows.append({
            "Rank": f"#{i}",
            "Candidate": r.get("name",""),
            "Decision": r.get("decision",""),
            "Final Score": r.get("final_score",0),
            "AI Score": r.get("ai_score",0),
            "Culture Fit": r.get("culture_score",0),
            "JD Match %": r.get("tfidf_score",0),
            "CGPA": r.get("cgpa",0),
            "Exp (yrs)": r.get("years_exp",0),
            "Skills Matched": len(r.get("matched_skills",[])),
            "Salary Est.": r.get("salary_estimate","N/A"),
        })
    df = pd.DataFrame(df_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Detailed candidate cards
    st.markdown("### 🔍 Detailed Candidate Reports")
    for i, r in enumerate(results, 1):
        decision = r.get("decision","")
        badge_class = "badge-hire" if "Strong" in decision else ("badge-consider" if "Consider" in decision else "badge-reject")

        matched_chips = "".join(f'<span class="chip matched">{s}</span>' for s in r.get("matched_skills",[]))
        missing_chips = "".join(f'<span class="chip missing">{s}</span>' for s in r.get("missing_skills",[])[:6])
        extra_chips   = "".join(f'<span class="chip">{s}</span>' for s in r.get("extra_skills",[])[:5])
        strengths_html = "".join(f'<li style="margin:4px 0;color:#94A3B8">{s}</li>' for s in r.get("strengths",[]))
        flags_html = "".join(f'<li style="margin:4px 0;color:#FCA5A5">⚠ {f}</li>' for f in r.get("red_flags",[]))
        qs_html = "".join(f'<li style="margin:6px 0;color:#94A3B8">{q}</li>' for q in r.get("interview_questions",[]))

        score = r.get("final_score",0)
        pct = min(score, 100)

        with st.expander(f"#{i} — {r.get('name','Unknown')} · {decision}"):
            st.markdown(f"""
<div class="candidate-card">
  <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:16px">
    <span class="candidate-name">{r.get('name','Unknown')}</span>
    <span class="score-badge {badge_class}">{decision}</span>
    <span style="color:#64748B;font-size:13px">Score: {score}/100</span>
  </div>

  <div class="progress-outer"><div class="progress-inner" style="width:{pct}%"></div></div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:16px 0">
    <div><div style="font-size:11px;color:#64748B">AI Match</div><div style="font-size:18px;font-weight:700;color:#60A5FA">{r.get('ai_score',0)}%</div></div>
    <div><div style="font-size:11px;color:#64748B">Culture Fit</div><div style="font-size:18px;font-weight:700;color:#A78BFA">{r.get('culture_score',0)}%</div></div>
    <div><div style="font-size:11px;color:#64748B">JD Similarity</div><div style="font-size:18px;font-weight:700;color:#34D399">{r.get('tfidf_score',0)}%</div></div>
    <div><div style="font-size:11px;color:#64748B">CGPA</div><div style="font-size:18px;font-weight:700;color:#FBBF24">{r.get('cgpa',0)}</div></div>
    <div><div style="font-size:11px;color:#64748B">Experience</div><div style="font-size:18px;font-weight:700;color:#FB923C">{r.get('years_exp',0)}y</div></div>
    <div><div style="font-size:11px;color:#64748B">Salary Est.</div><div style="font-size:18px;font-weight:700;color:#F472B6">{r.get('salary_estimate','N/A')}</div></div>
  </div>

  <div class="divider"></div>

  <div class="section-title">Contact</div>
  <div style="font-size:13px;color:#94A3B8">📞 {r.get('phone','')} &nbsp;|&nbsp; ✉ {r.get('email','')} &nbsp;|&nbsp; 🎓 {r.get('education_level','')}</div>

  <div class="section-title" style="margin-top:16px">Matched Skills</div>
  <div>{matched_chips if matched_chips else '<span style="color:#64748B;font-size:13px">None matched</span>'}</div>

  <div class="section-title" style="margin-top:12px">Missing Skills</div>
  <div>{missing_chips if missing_chips else '<span style="color:#64748B;font-size:13px">None missing ✓</span>'}</div>

  <div class="section-title" style="margin-top:12px">Bonus Skills (from resume)</div>
  <div>{extra_chips if extra_chips else '<span style="color:#64748B;font-size:13px">—</span>'}</div>

  <div class="divider"></div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
    <div>
      <div class="section-title">Strengths</div>
      <ul style="margin:0;padding-left:18px">{strengths_html}</ul>
    </div>
    <div>
      <div class="section-title">Red Flags</div>
      <ul style="margin:0;padding-left:18px">{flags_html if flags_html else '<li style="color:#64748B">None</li>'}</ul>
    </div>
  </div>

  <div class="divider"></div>

  <div class="section-title">AI Reasoning</div>
  <div class="reasoning-box">{r.get('reasoning','')}</div>

  <div class="section-title" style="margin-top:16px">Suggested Interview Questions</div>
  <ol style="padding-left:18px">{qs_html}</ol>
</div>
""", unsafe_allow_html=True)

    # Trace log viewer
    if st.session_state.trace:
        with st.expander("🔬 View Full Agent Execution Trace"):
            trace_html = "<div class='trace-log'>"
            for e in st.session_state.trace:
                cls = {"info":"log-info","success":"log-success","warn":"log-warn","error":"log-error"}.get(e["level"],"")
                trace_html += f'<div class="{cls}">[{e["ts"]}] [{e["agent"]}] {e["msg"]}</div>'
            trace_html += "</div>"
            st.markdown(trace_html, unsafe_allow_html=True)

    # Database tab
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    with st.expander("📂 View All Stored Screenings"):
        conn = sqlite3.connect("recruitiq.db")
        df_db = pd.read_sql_query(
            "SELECT id,screened_at,candidate_name,decision,final_score,ai_score,cgpa,salary_estimate FROM screenings ORDER BY id DESC",
            conn
        )
        conn.close()
        st.dataframe(df_db, use_container_width=True, hide_index=True)
