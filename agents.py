import os
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

# Instantiate your LLM once here
# Set API key (placeholder)
import dotenv
dotenv.load_dotenv(".env")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)


### --- Resume Screening Agent --- ###
class ResumeScreeningAgent:
    def __init__(self, llm):
        self.llm = llm

    def rank_resumes(self, resumes: list[str], job_description: str):
        ranked = []
        for resume in resumes:
            prompt = f"""
                        Job Description:
                        {job_description}

                        Candidate Resume:
                        {resume}

                        Rate this candidate out of 10 for this job and explain briefly.
                      """
            print("prompt for rank_resume_function :: ","\n", prompt)
            response = self.llm.predict(prompt)
            print("Response from rank_resume function","\n", response)
            ranked.append((resume, response))
        return ranked


### --- Candidate Messaging Agent --- ###
class CandidateMessagingAgent:
    def __init__(self, llm):
        
        self.llm = llm

    def generate_email(self, candidate_name, status, interview_date=None):
        prompt = f"""
                    Write a professional email to {candidate_name} for the following status: {status}.
                    {"Include interview details for: " + interview_date if interview_date else ""}
                    Be clear, warm, and concise.
                  """
        print("Prompt to generate email :: ", "\n", prompt, "\n")
        generated_email = self.llm.predict(prompt)
        print("Generated EMail :: ", "\n", generated_email)
        return generated_email


### --- Support Bot Agent --- ###
class SupportBotAgent:
    def __init__(self, folder_path):
        docs = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                loader = TextLoader(os.path.join(folder_path, filename))
                docs.extend(loader.load())

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vectorstore = FAISS.from_documents(docs, embeddings)

        self.llm = llm
        self.qa = RetrievalQA.from_chain_type(llm=self.llm, retriever=self.vectorstore.as_retriever())

    def answer(self, query):
        return self.qa.run(query)




### --- Orchestrator to glue all agents --- ###
class HRAssistantOrchestrator:
    def __init__(self, folder_path):
        self.resume_agent = ResumeScreeningAgent(llm)
        self.messaging_agent = CandidateMessagingAgent(llm)
        self.support_agent = SupportBotAgent(folder_path)

    def handle(self, task_type, payload):
        if task_type == "screen_resumes":
            return self.resume_agent.rank_resumes(**payload)
        elif task_type == "send_message":
            return self.messaging_agent.generate_email(**payload)
        elif task_type == "ask_question":
            return self.support_agent.answer(payload["query"])
        else:
            return "Unknown task."
