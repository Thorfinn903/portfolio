import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq  # <--- NEW LIBRARY

# --- 1. ROBUST IMPORT SYSTEM ---
try:
    from .data_loader import load_json, load_markdown
except ImportError:
    try:
        from app.v3.data_loader import load_json, load_markdown
    except ImportError:
        sys.path.append(str(Path(__file__).resolve().parent))
        from data_loader import load_json, load_markdown

# --- 2. LAZY CONNECTION (Groq) ---
def get_groq_client():
    """
    Connects to Groq only when needed.
    """
    # Load .env from backend folder
    env_path = Path(__file__).resolve().parents[2] / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Fallback load
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ CRITICAL: GROQ_API_KEY not found in .env")
        return None

    return Groq(api_key=api_key)


# --- 3. LOGIC FUNCTIONS ---

def search_portfolio(question: str) -> str:
    """
    Your Rule-Based Search (No changes needed here)
    """
    question_lower = question.lower()

    if "about" in question_lower or "who are you" in question_lower:
        return load_markdown("about.md")

    if "skill" in question_lower or "stack" in question_lower:
        skills = load_json("skills.json")
        lines = ["Here is my technical stack:"]
        if "backend" in skills:
            lines.append(f"- Backend: {', '.join(skills['backend'])}")
        if "frontend" in skills:
            lines.append(f"- Frontend: {', '.join(skills['frontend'])}")
        if "programming_languages" in skills:
            langs = skills["programming_languages"]
            lines.append(f"- Languages: {', '.join(langs.get('primary', []))}")
        return "\n".join(lines)

    if "project" in question_lower:
        projects = load_json("projects.json")
        lines = ["Here are my key projects:"]
        for p in projects:
            lines.append(f"- {p.get('title', 'Project')}: {p.get('description', '')}")
        return "\n".join(lines)

    return "I can answer questions about my skills, projects, and experience."


def polish_with_llm(question: str, raw_answer: str) -> str:
    """
    Uses Groq (Llama 3) to rewrite the answer.
    """
    client = get_groq_client()
    
    # Skip if client fails or answer is simple refusal
    if not client or "I can answer questions about" in raw_answer:
        return raw_answer

    prompt = f"""
    You are a professional portfolio assistant.
    USER QUESTION: {question}
    RAW DATA: {raw_answer}
    
    TASK: Rewrite the raw data into a friendly, professional response. 
    Keep it concise. Do not invent new facts.
    """

    try:
        # Groq uses standard OpenAI-like chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Free, fast model
        )
        
        return chat_completion.choices[0].message.content.strip()
            
    except Exception as e:
        print(f"⚠️ Groq Error: {e}")
        return raw_answer
    
    return raw_answer