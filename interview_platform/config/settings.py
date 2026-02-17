"""
config/settings.py
─────────────────────────────────────────────────────────────
Production configuration.

API KEY SETUP (choose one):
  1. .env file:    GEMINI_API_KEY=AIza...
  2. Env var:      export GEMINI_API_KEY=AIza...
  3. Sidebar:      Settings panel inside the app

Free key: https://aistudio.google.com/app/apikey
─────────────────────────────────────────────────────────────
"""

import os
from dataclasses import dataclass, field
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass
class Settings:
    # ── Google Gemini ─────────────────────────────────────────────
    gemini_api_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY", "AIzaSyCC9Oga9mVE39Ke6CD8XvOplLIRW5zoz4c")
    )
    # Best model for deep technical evaluation & reasoning
    gemini_model_eval:     str = "gemini-2.5-pro-preview-06-05"
    gemini_model_strategy: str = "gemini-2.5-pro-preview-06-05"
    gemini_model_fallback: str = "gemini-1.5-pro"

    # ── Database ──────────────────────────────────────────────────
    database_url: str = field(
        default_factory=lambda: os.environ.get(
            "DATABASE_URL", "sqlite:///./aiip_sessions.db"
        )
    )

    # ── Interview rules ───────────────────────────────────────────
    max_questions:            int   = 8
    max_follow_ups_per_skill: int   = 1

    # ── Readiness weights ─────────────────────────────────────────
    w_concept:     float = 0.40
    w_clarity:     float = 0.20
    w_confidence:  float = 0.20
    w_consistency: float = 0.20

    # ── App ───────────────────────────────────────────────────────
    app_title: str = "NeuralPrep — AI Interview Platform"
    app_icon:  str = "🎓"
    version:   str = "3.0"


settings = Settings()
