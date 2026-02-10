# Portfolio (React + FastAPI + AI Assistant)

A modern personal portfolio with structured profile data, dynamic pages, and an AI chat assistant backed by FastAPI.

## Why I made this
- Replace a static resume with a living, queryable portfolio.
- Let recruiters ask questions and get tailored responses.
- Showcase full stack skills in a real product.

## Core features
- Multi page React portfolio with clean sections.
- Structured data source (Data/) for easy updates.
- AI chat assistant with intent, persona, psychology, and LLM polish.
- System health and analytics dashboard.
- Floating assistant that can wake a sleeping backend.

## Tech stack
- Frontend: React, Vite, Tailwind CSS, Framer Motion, React Router, Recharts.
- Backend: FastAPI, Uvicorn, Pydantic, httpx.
- AI providers: Groq (Llama 3), optional Gemini.
- Tooling: ESLint, PostCSS.

## How it works
1. The React app renders routes from frontend/src/App.jsx.
2. Page components call the FastAPI API to fetch content.
3. The backend reads JSON and Markdown from Data/ via backend/app/data_loader.py.
4. The /chat endpoint uses the v3 controller pipeline: intent detection -> strategy -> domain rules -> persona and psychology -> optional LLM polish -> response.
5. /system/health and /system/analytics power the dashboard.

## Frontend routes
- / Home
- /about About
- /experience Experience
- /education Education
- /skills Skills
- /projects Projects
- /certificates Certificates
- /contact Contact
- /chat Chat page
- /dashboard AI dashboard
- /profile Profile summary

## API endpoints
- GET / health check message
- GET /about
- GET /skills
- GET /projects
- GET /experience
- GET /education
- GET /certificates
- GET /contact
- GET /system/health
- GET /system/analytics
- POST /chat

## Environment variables
Backend:
- GROQ_API_KEY required for v2 and v3 LLM polish.
- GEMINI_API_KEY optional for the Gemini client.
- LLM_LONG_ANSWER_CHARS optional threshold for when to allow LLM polish.
- CORS_ORIGINS optional comma-separated list of allowed origins (use `*` to allow all, credentials disabled).

Frontend:
- VITE_API_BASE_URL base URL for the backend API (example: `https://your-backend.example.com`).

## File structure (high level)
```text
.
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- data_loader.py
|   |   |-- chat_engine.py
|   |   |-- v3/
|   |   |   |-- controller.py
|   |   |   |-- data/data_access.py
|   |   |   |-- layers/
|   |   |   |-- persona/
|   |   |   |-- psychology/
|   |   |   |-- llm/
|   |   |   |-- analytics/
|   |   |   |-- system/observability.py
|   |   |   `-- middleware/debug_tracing.py
|   |   `-- v4/state/session_manager.py
|   |-- requirements.txt
|   `-- .env
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |   |-- components/
|   |   `-- pages/
|   |-- index.html
|   |-- tailwind.config.js
|   |-- vite.config.js
|   `-- vercel.json
|-- Data/
|   |-- about.md
|   |-- skills.json
|   |-- projects.json
|   |-- experience.json
|   |-- education.json
|   |-- certificates.json
|   `-- contact.json
`-- README.md
```

## Key backend modules
- backend/app/main.py FastAPI app, routes, and CORS.
- backend/app/data_loader.py Loads JSON and Markdown from Data/ (case sensitive).
- backend/app/chat_engine.py v2 rule based search plus Groq polish.
- backend/app/v3/controller.py Orchestrates the v3 chat pipeline.
- backend/app/v3/layers/* Intent detection, strategy, rules, entities, LLM polish.
- backend/app/v3/persona/* Recruiter classification and persona tuning.
- backend/app/v3/psychology/* Evidence weighting and psychology profiles.
- backend/app/v3/analytics/analytics_engine.py Tracks intents and recruiter types.
- backend/app/v3/system/observability.py Health metrics.
- backend/app/v4/state/session_manager.py Session based recruiter memory.

## Key frontend components
- frontend/src/components/Navbar.jsx Top navigation.
- frontend/src/components/PortfolioAgent.jsx Floating assistant container and API calls.
- frontend/src/components/ChatAssistant.jsx Assistant UI and wake message.
- frontend/src/components/ChatMessage.jsx Message bubble layout.
- frontend/src/pages/* Route pages and data fetch logic.

## Data files
Update these to change the portfolio content without touching code:
- Data/about.md
- Data/skills.json
- Data/projects.json
- Data/experience.json
- Data/education.json
- Data/certificates.json
- Data/contact.json

## Local development
- Backend: cd backend then uvicorn app.main:app --reload
- Frontend: cd frontend then npm install and npm run dev

## Deployment notes
- Frontend uses frontend/vercel.json to rewrite all routes to index.html.
- Backend CORS defaults to localhost + Vercel, including preview subdomains. Override with CORS_ORIGINS.
- If the backend sleeps on free tiers, the assistant shows a wake message after 4 seconds.

## Ideas to make it more useful
- Move the API base URL to an environment variable for dev and prod.
- Add SEO meta tags per route.
- Add a contact form that posts to a backend endpoint.
- Cache projects and skills responses for faster loads.
- Add tests for the v3 intent pipeline and key API endpoints.
