import os
import streamlit as st
from agents import HRAssistantOrchestrator
from PyPDF2 import PdfReader
from docx import Document

# Set API key
import dotenv
dotenv.load_dotenv(".env")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Instantiate the assistant
assistant = HRAssistantOrchestrator(folder_path="data")

# Page Config
st.set_page_config(page_title="GenAI HR Assistant", layout="wide")

# ----------------------------
# Custom Styling
# ----------------------------
st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #f9f8fb;
        padding: 2rem;
    }

    h1, h2, h3, h4 {
        color: #5a189a;
    }

    .stTabs [role="tablist"] {
        background-color: #efe2ff;
        border-radius: 10px;
        padding: 0.5rem;
    }
    .stTabs [role="tab"] {
        font-weight: bold;
        font-size: 1rem;
        color: #5a189a;
    }

    .stFileUploader {
        width: 100% !important;
    }

    button[kind="primary"] {
        background-color: #5a189a !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
    }

    .stAlert {
        border-left: 6px solid #5a189a;
        background-color: #f3e8ff;
    }

    .stTextArea textarea {
        background-color: #f7f3ff;
        border: 1px solid #d3bff5;
    }

    .stSelectbox > div {
        font-size: 0.9rem !important;
        padding: 0.2rem !important;
    }

    .css-1wa3eu0 {
        font-size: 0.9rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
st.markdown("<h1>🤖 AI-Powered HR Assistant</h1>", unsafe_allow_html=True)

# ----------------------------
# Text Extraction Helper
# ----------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        pdf = PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return file.read().decode("utf-8", errors="ignore")

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["📄 Resume Screening", "📬 Candidate Messaging", "💬 Support Bot (RAG)"])

# ----------------------------
# 📄 Resume Screening Tab
# ----------------------------
with tabs[0]:
    st.subheader("📄 Resume Screening")

    job_file = st.file_uploader("📝 Upload Job Description", type=["pdf", "docx", "txt"])
    resume_files = st.file_uploader("📋 Upload Candidate Resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)

    if st.button("🔍 Rank Candidates"):
        if not job_file or not resume_files:
            st.warning("Please upload both job description and at least one resume.")
        else:
            with st.spinner("Analyzing resumes..."):
                job_description = extract_text(job_file)
                resumes = [extract_text(resume) for resume in resume_files]

                results = assistant.handle("screen_resumes", {
                    "resumes": resumes,
                    "job_description": job_description
                })

                st.markdown("### 🏆 Ranked Candidates")
                for i, (res, feedback) in enumerate(results, 1):
                    st.markdown(f"**Candidate {i}:**")
                    st.code(res[:300] + "..." if len(res) > 300 else res)
                    st.success(feedback)

# ----------------------------
# 📬 Candidate Messaging Tab
# ----------------------------
with tabs[1]:
    st.subheader("📬 Candidate Messaging")

    candidate_name = st.text_input("👤 Candidate Name")
    status = st.selectbox("📌 Status", ["Interview", "Rejected", "Offer", "Feedback"], index=0)
    interview_date = st.text_input("📅 Interview Date (Optional)")

    if st.button("✉️ Generate Email"):
        with st.spinner("Generating email..."):
            email = assistant.handle("send_message", {
                "candidate_name": candidate_name,
                "status": status,
                "interview_date": interview_date if interview_date else None
            })
        st.markdown("### 📨 Generated Email")
        st.text_area("", value=email, height=250)

# ----------------------------
# 💬 Support Bot (RAG)
# ----------------------------
with tabs[2]:
    st.subheader("💬 Candidate Support Bot (RAG)")

    query = st.text_input("❓ Ask a question from HR documents")
    if st.button("🔎 Get Answer"):
        with st.spinner("Searching HR documents..."):
            response = assistant.handle("ask_question", {"query": query})
        st.markdown("### ✅ Answer")
        st.success(response)
