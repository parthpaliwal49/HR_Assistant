import os
import streamlit as st
from agents import HRAssistantOrchestrator
from PyPDF2 import PdfReader
from docx import Document

# Set API key (placeholder)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBvaCZAq2bJkLgdA1kuY_IBLE6TkzP7k1k"

# Instantiate the assistant
assistant = HRAssistantOrchestrator(folder_path="data")

# Page Config
st.set_page_config(page_title="🤖 GenAI HR Assistant", layout="wide")

# ----------------------------
# Custom Styling
# ----------------------------
st.markdown(
    """
    <style>
    /* Custom global styles */
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #f5f3fa;
    }

    /* Title and header styling */
    h1 {
        color: #6a0dad;
    }
    .stTabs [role="tablist"] {
        background-color: #f0e6ff;
        border-radius: 10px;
    }
    .stTabs [role="tab"] {
        font-weight: 600;
        color: #6a0dad;
    }

    /* Upload box sizing */
    .stFileUploader {
        width: 100% !important;
    }

    /* Remove default uploader text */
    .stFileUploader > div > div > div > p,
    .stFileUploader > div > div > div > label {
        display: none;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #6a0dad !important;
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Success, warning, info */
    .stAlert {
        border-left: 5px solid #6a0dad;
    }

    /* Text area styling */
    .stTextArea textarea {
        background-color: #f5f0ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Header & Home Button
# ----------------------------
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1>🤖 AI-Powered HR Assistant</h1>", unsafe_allow_html=True)
with col2:
    if st.button("🏠 Home"):
        st.experimental_rerun()

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
    status = st.selectbox("📌 Status", ["Interview", "Rejected", "Offer", "Feedback"])
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
