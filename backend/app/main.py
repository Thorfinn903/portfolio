from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.data_loader import load_json, load_markdown
from fastapi.middleware.cors import CORSMiddleware
from app.chat_engine import search_portfolio, polish_with_llm




app = FastAPI(
    title="Portfolio Backend API",
    description="Backend API for personal portfolio",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Portfolio backend is running"}


@app.get("/about")
def get_about():
    """
    Return About section (Markdown).
    """
    content = load_markdown("about.md")
    return {"content": content}


@app.get("/skills")
def get_skills():
    """
    Return skills data.
    """
    return load_json("skills.json")


@app.get("/projects")
def get_projects():
    """
    Return projects list.
    """
    return load_json("projects.json")


@app.get("/experience")
def get_experience():
    """
    Return work experience data.
    """
    return load_json("experience.json")

@app.get("/education")
def get_education():
    return load_json("education.json")

@app.get("/certificates")
def get_certificates():
    return load_json("certificates.json")


@app.get("/contact")
def get_contact():
    """
    Return contact information.
    """
    return load_json("contact.json")

@app.post("/chat")
def chat(payload: dict):
    question = payload.get("question", "")
    raw_answer = search_portfolio(question)
    final_answer = polish_with_llm(question, raw_answer)
    return {"answer": final_answer}



