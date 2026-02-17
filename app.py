"""
app.py — NeuralPrep AI Interview Platform
──────────────────────────────────────────
Run:   streamlit run app.py

API KEY: Set GEMINI_API_KEY in .env or env variable,
         or enter it in the Settings panel (sidebar on setup page).
"""

import streamlit as st
from interview_platform.config import settings

st.set_page_config(
    page_title="NeuralPrep — AI Interview Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from interview_platform.ui.styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

from interview_platform.ui.pages import landing, setup, interview, report, analytics


class _State:
    _DEFAULTS = {
        "screen":               "landing",
        "api_key":              settings.gemini_api_key or "",
        "mock_mode":            False,
        "profile":              {},
        "engine_state":         {},
        "current_question":     None,
        "answers":              [],
        "messages":             [],
        "max_questions_override": 8,
    }

    def __init__(self):
        for k, v in self._DEFAULTS.items():
            if k not in st.session_state:
                st.session_state[k] = v

    def __getattr__(self, key):
        if key.startswith("_"):
            return super().__getattribute__(key)
        return st.session_state.get(key)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            st.session_state[key] = value


state = _State()

# ── Navigation bar (shown on non-landing pages) ───────────────────
if state.screen != "landing":
    n1, n2, n3, n4, n5 = st.columns([3, 1, 1, 1, 1])
    with n1:
        st.markdown(
            "<span style='font-family:IBM Plex Serif,serif;font-size:1.05rem;"
            "font-weight:700;color:#1E3A5F'>NeuralPrep</span>"
            "<span style='font-size:0.78rem;color:#A0AEC0;margin-left:10px;"
            "font-family:IBM Plex Mono,monospace'>AI Interview Platform</span>",
            unsafe_allow_html=True,
        )
    with n2:
        if st.button("Session", use_container_width=True,
                     disabled=state.screen in ("interview","setup") or not state.engine_state):
            state.screen = "interview"; st.rerun()
    with n3:
        if st.button("Report", use_container_width=True,
                     disabled=state.screen=="report" or not state.answers):
            state.screen = "report"; st.rerun()
    with n4:
        if st.button("Analytics", use_container_width=True,
                     disabled=state.screen=="analytics" or len(state.answers or [])<2):
            state.screen = "analytics"; st.rerun()
    with n5:
        if st.button("← Home", use_container_width=True):
            state.screen = "landing"; st.rerun()
    st.markdown("<hr style='border-color:#DDE1E7;margin:4px 0 12px'>", unsafe_allow_html=True)

# ── Router ────────────────────────────────────────────────────────
{
    "landing":   landing.render,
    "setup":     setup.render,
    "interview": interview.render,
    "report":    report.render,
    "analytics": analytics.render,
}.get(state.screen, landing.render)(state)
