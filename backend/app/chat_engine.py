from app.data_loader import load_json, load_markdown
import os
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])



def search_portfolio(question: str) -> str:
    """
    Very simple rule-based search over portfolio data.
    This will later be replaced by embeddings + LLM.
    """

    question_lower = question.lower()

    # About
    about = load_markdown("about.md")
    if "about" in question_lower or "who are you" in question_lower:
        return about

    # Skills
    if "erpnext" in question_lower or "erp next" in question_lower:
        skills = load_json("skills.json")
        backend = ", ".join(skills.get("backend", []))
        if "Frappe Framework" in backend:
            return "ERPNext is not listed in my skills. I do have experience with the Frappe Framework, which is the foundation behind ERPNext."
        return "ERPNext is not listed in my skills."

    if "skill" in question_lower or "technology" in question_lower:
        skills = load_json("skills.json")

        lines = ["My skills include:"]

        # Programming Languages
        langs = skills.get("programming_languages", {})
        primary = ", ".join(langs.get("primary", []))
        core = ", ".join(langs.get("core", []))
        if primary:
            lines.append(f"- Programming Languages: {primary}")
        if core:
            lines.append(f"- Core Languages: {core}")

        # Backend
        backend = ", ".join(skills.get("backend", []))
        if backend:
            lines.append(f"- Backend: {backend}")

        # Frontend
        frontend = ", ".join(skills.get("frontend", []))
        if frontend:
            lines.append(f"- Frontend: {frontend}")

        # Databases
        dbs = skills.get("databases", {})
        relational = ", ".join(dbs.get("relational", []))
        if relational:
            lines.append(f"- Databases: {relational}")

        # Tools
        tools = ", ".join(skills.get("tools_platforms", []))
        if tools:
            lines.append(f"- Tools & Platforms: {tools}")

        return "\n".join(lines)

    # Projects
    if "project" in question_lower:
        projects = load_json("projects.json")

        lines = ["Here are some projects I have built:"]
        for p in projects:
            lines.append(f"- {p['title']}: {p['description']}")

        return "\n".join(lines)

    # Experience
    if "experience" in question_lower or "work" in question_lower:
        experience = load_json("experience.json")

        lines = ["My work experience includes:"]
        for e in experience:
            lines.append(f"- {e['role']} at {e['company']} ({e['duration']})")

        return "\n".join(lines)


    # Education
    if "education" in question_lower or "study" in question_lower or "college" in question_lower:
        education = load_json("education.json")

        lines = ["My education includes:"]
        for e in education:
            lines.append(f"- {e['degree']} at {e['institution']} ({e['duration']})")

        return "\n".join(lines)


    # Certificates
    if "certificate" in question_lower or "certification" in question_lower:
        certs = load_json("certificates.json")

        lines = ["My certifications include:"]
        for c in certs:
            lines.append(f"- {c['title']}")

        return "\n".join(lines)


    return "I can only answer questions about my skills, projects, experience, education, and certificates."


def polish_with_llm(question: str, raw_answer: str) -> str:
    # Do not send refusal messages to the LLM
    if "only answer questions about" in raw_answer.lower():
        return raw_answer

    prompt = f"""
You are an assistant for a personal portfolio.

STRICT RULES:
- Use ONLY the information provided.
- Do NOT add new facts.
- Do NOT answer outside the portfolio.
- Keep it professional and concise.

QUESTION:
{question}

SOURCE ANSWER:
{raw_answer}

Rewrite the answer clearly and professionally.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        if response and response.text:
            return response.text.strip()

        return raw_answer

    except Exception as e:
        print("Gemini error:", e)
        return raw_answer

