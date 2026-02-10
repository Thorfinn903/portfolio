import os
from pathlib import Path
from dotenv import load_dotenv

# Fast, direct load
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)
from fastapi import FastAPI, Request
from app.data_loader import load_json, load_markdown
from fastapi.middleware.cors import CORSMiddleware
from app.chat_engine import search_portfolio, polish_with_llm
from app.v3.controller import handle_chat, ChatRequest
import time
from app.v3.middleware.debug_tracing import DebugTracingMiddleware
from app.v3.system.observability import SystemMonitor
from app.v3.analytics.analytics_engine import AnalyticsEngine
from app.v3.system.observability import SystemMonitor


def build_cors_settings():
    origins_env = os.getenv("CORS_ORIGINS", "").strip()
    if origins_env:
        if origins_env == "*":
            return {
                "allow_origins": ["*"],
                "allow_credentials": False,
                "allow_origin_regex": None,
            }
        origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
        return {
            "allow_origins": origins,
            "allow_credentials": True,
            "allow_origin_regex": None,
        }

    return {
        "allow_origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://bnm-portfolio.vercel.app",
        ],
        "allow_credentials": True,
        "allow_origin_regex": r"^https://.*\.vercel\.app$",
    }


app = FastAPI(
    title="Portfolio Backend API",
    description="Backend API for personal portfolio",
    version="1.0.0"
)

cors_settings = build_cors_settings()
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    **cors_settings,
)
app.add_middleware(DebugTracingMiddleware)

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

@app.get("/system/health", tags=["System"])
def system_health():
    return SystemMonitor().get_status()

@app.get("/system/analytics", tags=["System"])
def system_analytics():
    return AnalyticsEngine().get_analytics()

@app.post("/chat")
async def chat(payload: dict, request: Request):
    question = payload.get("question", "")
    session_id = payload.get("session_id")
    metadata = payload.get("metadata")
    use_v2 = payload.get("v2") is True

    if use_v2:
        raw_answer = search_portfolio(question)
        final_answer = polish_with_llm(question, raw_answer)
        return {"answer": final_answer}

    v3_response = await handle_chat(
        ChatRequest(
            question=question,
            session_id=session_id,
            metadata=metadata,
        )
    )

    response = {
        "answer": v3_response.answer,
        "intent": v3_response.intent,
        "strategy": v3_response.strategy,
        "confidence_score": v3_response.confidence_score,
        "evidence": v3_response.evidence,
        "debug": v3_response.debug,
    }
    if response.get("debug") is not None:
        response["debug"]["request_id"] = getattr(request.state, "request_id", None)
        start_time = getattr(request.state, "start_time", None)
        response["debug"]["process_time_ms"] = round(
            (time.monotonic() - start_time) * 1000, 2
        ) if start_time else 0
    return response



