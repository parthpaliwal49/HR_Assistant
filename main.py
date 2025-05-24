import os
import streamlit as st
from hr_assistant import HRAssistantOrchestrator

os.environ["GOOGLE_API_KEY"] = "AIzaSyBvaCZAq2bJkLgdA1kuY_IBLE6TkzP7k1k"

# Instantiate the assistant
assistant = HRAssistantOrchestrator(folder_path="data")

st.set_page_config(page_title="GenAI HR Assistant", layout="wide")
st.title("🤖 GenAI-Powered HR Assistant")

tabs = st.tabs(["📄 Resume Screening", "📬 Candidate Messaging", "💬 Candidate Support Bot"])

# --- Resume Screening ---
with tabs[0]:
    st.header("📄 Resume Screening")
    job_description = st.text_area("Job Description", height=150)
    resumes_input = st.text_area("Paste resumes here (one per line)", height=200)
    if st.button("🔍 Rank Candidates"):
        resumes = resumes_input.strip().split("\n")
        results = assistant.handle("screen_resumes", {"resumes": resumes, "job_description": job_description})
        for i, (res, feedback) in enumerate(results, 1):
            st.markdown(f"**Candidate {i}:** `{res}`")
            st.success(feedback)

# --- Candidate Messaging ---
with tabs[1]:
    st.header("📬 Candidate Messaging")
    candidate_name = st.text_input("Candidate Name")
    status = st.selectbox("Status", ["Interview", "Rejected", "Offer", "Feedback"])
    interview_date = st.text_input("Interview Date (optional)", placeholder="e.g., Monday 10AM")
    if st.button("✉️ Generate Email"):
        email = assistant.handle("send_message", {
            "candidate_name": candidate_name,
            "status": status,
            "interview_date": interview_date if interview_date else None
        })
        st.text_area("📨 Generated Email", value=email, height=250)

# --- Candidate Support Bot ---
with tabs[2]:
    st.header("💬 Candidate Support Bot (RAG)")
    query = st.text_input("Ask a question from HR docs")
    if st.button("❓ Get Answer"):
        response = assistant.handle("ask_question", {"query": query})
        st.markdown(f"**Answer:** {response}")
