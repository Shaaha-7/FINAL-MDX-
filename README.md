# AIIP — AI/ML/DS Interview Platform v3
### Streamlit · Gemini 2.0 Flash · Light Theme · SQLite · Plotly

---

## Setup & Run (3 steps)

```bash
# 1. Install
pip install streamlit google-generativeai sqlalchemy plotly python-dotenv

# 2. Set Gemini API key (pick ONE)
export GEMINI_API_KEY=AIza...                # Option A: env variable
cp .env.example .env  # then edit .env       # Option B: .env file

# 3. Run
streamlit run app.py
# Opens at http://localhost:8501 automatically
```

**No key?** Click DEMO on landing page — all features work with simulated scores.
Get a FREE key at: https://aistudio.google.com/app/apikey

---

## Where to put the API key

| Method | How |
|--------|-----|
| Env variable | `export GEMINI_API_KEY=AIza...` before running |
| .env file | Copy `.env.example` → `.env`, paste key |
| Runtime UI | Type into landing page field, no restart needed |
| settings.py | Edit `config/settings.py` → `gemini_api_key` default |

---

## Folder Structure

```
project_v3/
├── app.py                               ← Entry point + router
├── requirements.txt
├── .env.example
├── README.md
│
└── interview_platform/
    ├── config/
    │   └── settings.py                  ← Gemini key, model, weights
    ├── data/
    │   └── question_bank.py             ← 10 skills × 3 difficulties
    ├── database/
    │   ├── base.py                      ← SQLAlchemy engine
    │   └── models.py                    ← User, Session, Answer ORM
    ├── services/
    │   ├── ai_service.py                ← Gemini 2.0 Flash calls
    │   └── analytics_service.py        ← Readiness scoring
    ├── engine/
    │   └── interview_engine.py          ← Adaptive flow + skip fix
    └── ui/
        ├── styles.py                    ← Light professional CSS
        └── pages/
            ├── landing.py               ← Hero + API key input
            ├── setup.py                 ← Profile form
            ├── interview.py             ← Chat UI + sidebar
            ├── report.py                ← Report + download
            └── analytics.py            ← 5 Plotly charts
```

---

## What changed in v3

| Fix | Detail |
|-----|--------|
| Theme | Dark cyberpunk → Clean light professional (IBM Plex fonts) |
| Skip bug | Skipped questions → score 0.0 everywhere, honest feedback only |
| LLM accuracy | Temperature 0.1 for evaluation (strict, deterministic) |
| LLM model | Upgraded to `gemini-2.0-flash` (best accuracy) |
| Score honesty | Hard gate: <20 char answers → max score 1.0 |
