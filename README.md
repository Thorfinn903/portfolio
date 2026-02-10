# Narayan.AI (Cortex V4) - An Intelligent, Context-Aware Portfolio System

*A futuristic, full-stack AI portfolio that adapts to the recruiter in real time.*

**Badges**: `React` `FastAPI` `Python` `Tailwind CSS` `Framer Motion`

**Dashboard Screenshot**: `docs/screenshots/cortex-dashboard.png` (placeholder)

---

## Why
Static portfolios are passive and boring. Recruiters ask different questions depending on whether they are technical (CTO/Engineering) or business-focused (HR/Product). Narayan.AI turns the portfolio into an adaptive system that understands intent and responds in the right tone and depth.

---

## Key Intelligence Features (The Brain)
- ?? **Adaptive Persona System**: Detects whether the user is a CTO, HR, or Product Manager and adjusts tone, complexity, and detail.
- ?? **V4.0 Session Memory**: Remembers the user’s identity across the conversation. Once identified as a CTO, it continues answering with technical depth, even for personal questions.
- ?? **Cortex Dashboard**: Real-time observability deck monitoring API latency, intent distribution, and system health.
- ??? **Fallback & Safety**: Robust error handling for unknown intents and edge cases.

---

## Tech Stack (The Spine)
- **Frontend**: React.js, Vite, Framer Motion (animations), Recharts (analytics), Tailwind CSS (glassmorphism)
- **Backend**: FastAPI (Python), Async/Await, Custom Logic Layers (intent, persona, analytics)
- **Data**: Dynamic JSON-based profile loading

---

## Installation & Setup

### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

Default URLs:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

---

## API Documentation (Brief)
- `POST /chat` Main intelligence endpoint
- `GET /system/health` Cortex status check
- `GET /system/analytics` Dashboard data

---

## Data Sources
The backend loads content from `data/`:
- `about.md`
- `skills.json`
- `projects.json`
- `experience.json`
- `education.json`
- `certificates.json`
- `contact.json`

---

## Notes
- CORS is set to allow `http://localhost:5173`.
- If `/chat` returns auth errors, confirm `GROQ_API_KEY` is set in `backend/.env`.
