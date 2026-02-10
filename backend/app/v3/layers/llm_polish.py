import os
import time
import traceback
from pathlib import Path
from dotenv import load_dotenv
from groq import AsyncGroq

# Import the monitor
from app.v3.system.observability import SystemMonitor

# --- 1. SETUP HELPERS ---
def get_api_key():
    try:
        env_path = Path(__file__).resolve().parents[3] / '.env'
        load_dotenv(dotenv_path=env_path)
        load_dotenv() 
        return os.getenv("GROQ_API_KEY")
    except Exception:
        return None

# --- 1B. PERSONA PROMPTS ---
def get_persona_instructions(recruiter_type: str, intent: str) -> str:
    rt = (recruiter_type or "").upper()
    intent_key = (intent or "").lower()
    personal_note = ""
    if intent_key == "personal_query":
        if rt == "TECH_LEAD":
            personal_note = (
                "If asked about hobbies, relate them to technology (e.g., home automation, "
                "coding side projects, 3D printing). "
            )
        elif rt == "HR_MANAGER":
            personal_note = (
                "If asked about hobbies, highlight team sports, reading, or volunteering. "
            )

    if rt == "TECH_LEAD":
        return (
            "Persona: Technical Lead. Focus on architecture, stack depth (FastAPI, Python, SQL), "
            "and concise technical accuracy. Use precise engineering language. "
            f"{personal_note}"
        )
    if rt == "HR_MANAGER":
        return (
            "Persona: HR Manager. Emphasize soft skills, reliability, team fit, and career growth. "
            "Keep the tone warm and professional. "
            f"{personal_note}"
        )
    if rt in {"PRODUCT_OWNER", "PRODUCT_MANAGER"}:
        return (
            "Persona: Product Owner. Emphasize project impact, delivery, and user-centric results. "
            "Keep the tone pragmatic and outcomes-focused. "
            f"{personal_note}"
        )
    return (
        "Persona: Generalist recruiter. Keep responses professional, clear, and factual. "
        f"{personal_note}"
    )
# --- 2. THE COMPATIBILITY CLASS ---
class PolishedResult:
    """
    Acts like the Pydantic model the controller expects.
    Allows access via .attribute (dot notation).
    """
    def __init__(self, data: dict):
        self.answer = data.get("answer", "")
        self.llm_used = data.get("llm_used", False)
        self.llm_status = data.get("llm_status", "skipped")
        self.llm_error = data.get("llm_error", False)
        self.llm_error_reason = data.get("llm_error_reason", None)
        
        # Pass through metadata
        self.confidence_score = data.get("confidence_score", 1.0) 
        self.intent = data.get("intent", "unknown")
        self.evidence = data.get("evidence", [])
        
        self._data = data

    def dict(self):
        return self._data

# --- 3. THE LOGIC WITH MONITORING ---
async def polish_response(question: str, answer: str, **kwargs) -> PolishedResult:
    """
    Polishes the response using AsyncGroq and tracks health via SystemMonitor.
    """
    # 1. TRACK REQUEST START
    start_time = time.time()
    
    # FIX: Instantiate the class with ()
    monitor = SystemMonitor() 
    monitor.record_request() 
    
    # Base Data Structure
    base_data = {
        "answer": answer,
        "confidence_score": kwargs.get("confidence_score") or kwargs.get("confidence", 0.85),
        "intent": kwargs.get("intent", "unknown"),
        "evidence": kwargs.get("evidence", []),
        "llm_used": False,
        "llm_status": "skipped",
        "llm_error": False,
        "llm_error_reason": None
    }

    if not answer:
        return PolishedResult(base_data)

    try:
        api_key = get_api_key()
        if not api_key:
            base_data["llm_error"] = True
            base_data["llm_error_reason"] = "GROQ_API_KEY_MISSING"
            
            # FIX: Use correct method name
            monitor.record_llm_failure("GROQ_API_KEY_MISSING") 
            return PolishedResult(base_data)

        # Init Client
        client = AsyncGroq(api_key=api_key)

        persona_prompt = get_persona_instructions(
            kwargs.get("recruiter_type", "GENERALIST"),
            kwargs.get("intent", "unknown"),
        )
        system_prompt = (
            "You are a professional portfolio assistant for a software engineer. "
            f"{persona_prompt} "
            "Rewrite the following raw data into a concise, professional, and friendly response. "
            "Do not invent facts. If the data is a list, make it conversational."
        )
        user_message = f"USER QUESTION: {question}\n\nRAW DATA:\n{answer}"

        # Call Groq
        completion = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Update result
        base_data["answer"] = completion.choices[0].message.content.strip()
        base_data["llm_used"] = True
        base_data["llm_status"] = "healthy"
        
        # 2. TRACK SUCCESS & LATENCY
        duration = (time.time() - start_time) * 1000
        
        # FIX: Use correct method name
        monitor.record_llm_success(duration) 
        
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        base_data["llm_error"] = True
        base_data["llm_error_reason"] = str(e)
        
        # 3. TRACK EXCEPTION (Correct Name)
        monitor.record_llm_failure(str(e))

    return PolishedResult(base_data)
