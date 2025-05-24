---

````markdown
# 🤖 GenAI-Powered HR Assistant

This project is an **Agent-based HR Assistant** built with **LangChain**, **Gemini (Google Generative AI)**, and **Streamlit**. It simulates the role of a recruiter — from screening resumes to answering candidate questions — all in a unified interface.

---

## 🔧 Features

- **📄 Resume Screening Agent**  
  Ranks candidates against a given job description using LLM evaluation.

- **📬 Smart Candidate Messaging Agent**  
  Automatically generates personalized interview invites, rejection emails, or feedback.

- **❓ Candidate Support Bot (RAG)**  
  Answers HR-related queries by retrieving context from HR policies and job descriptions.

- **🖥️ Streamlit UI**  
  Intuitive frontend to interact with the assistant through a web browser.

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/hr-assistant.git
cd hr-assistant
````

### 2. Set up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, create it with:

```txt
streamlit
langchain
faiss-cpu
google-generativeai
langchain-google-genai
```

### 4. Set Your Gemini API Key

Create a `.env` file and add your key:

```
GOOGLE_API_KEY=your-api-key-here
```

Or export it directly:

```bash
export GOOGLE_API_KEY=your-api-key-here  # On Windows: set GOOGLE_API_KEY=your-api-key-here
```

---

## 🚀 Running the App

```bash
streamlit run main.py
```

Visit [http://localhost:8501](http://localhost:8501) to interact with the assistant.

---

## 📁 Project Structure

```bash
.
├── main.py                # Main Streamlit app
├── agents.py              # All agent classes
├── requirements.txt       # Required Python packages
├── .env                   # API key (DO NOT COMMIT)
├── .gitignore             # Git ignore rules
├── /data                  # HR policy files, job descriptions, resumes (in .txt format)
└── README.md              # This file
```

---

## 🔐 Security Note

**Never commit your `.env` file or API keys**. Add `.env` to `.gitignore` to keep secrets safe.

---

## 🙋‍♂️ Future Work

* Add multi-language support
* Integrate calendar APIs for scheduling
* Extend to support video resume analysis

---

## 📜 License

MIT License. Feel free to fork and extend.

```

---

Let me know if you want badges (build status, license, stars, etc.), deployment instructions (like Streamlit Cloud), or a logo/header.
```
