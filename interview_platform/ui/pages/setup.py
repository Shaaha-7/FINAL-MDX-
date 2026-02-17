"""ui/pages/setup.py — Production profile setup with settings panel"""

import streamlit as st
from ..styles import badge
from ...data.question_bank import SKILLS

ROLES = [
    "ML Engineer", "Data Scientist", "AI Researcher",
    "Deep Learning Engineer", "MLOps Engineer", "NLP Engineer",
    "Computer Vision Engineer", "Data Engineer", "AI Product Manager",
]
COMPANIES  = ["FAANG / Big Tech", "Startup", "Research Lab", "Mid-size Tech", "Finance / Quant"]
EXPERIENCE = ["Student", "Fresher / New Grad", "1-2 Years", "3-5 Years", "5+ Years"]


def render(state):
    # ── Sidebar — Settings (API key lives here) ───────────────────
    with st.sidebar:
        st.markdown("""
        <div style='padding:0.5rem 0 1rem'>
          <div style='font-family:IBM Plex Mono,monospace;font-size:0.75rem;
                      color:#FFFFFF;letter-spacing:2px;margin-bottom:4px'>NEURALPREP</div>
          <div style='font-size:0.72rem;color:#94A3B8'>AI Interview Platform</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:0 0 16px'>", unsafe_allow_html=True)

        st.markdown("""
        <p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;
                  color:#94A3B8;letter-spacing:3px;margin-bottom:8px'>⚙ SETTINGS</p>
        """, unsafe_allow_html=True)

        key_input = st.text_input(
            "Gemini API Key",
            value=state.api_key or "",
            type="password",
            placeholder="AIza...",
            help="Get your free key at aistudio.google.com/app/apikey",
        )
        if key_input != (state.api_key or ""):
            state.api_key = key_input

        status_html = (
            "<div style='font-family:IBM Plex Mono,monospace;font-size:0.62rem;"
            "color:#4ADE80;margin-top:6px'>✓ Key configured</div>"
            if state.api_key else
            "<div style='font-family:IBM Plex Mono,monospace;font-size:0.62rem;"
            "color:#F87171;margin-top:6px'>✗ No key — enter above</div>"
        )
        st.markdown(status_html, unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.70rem;color:#64748B;margin-top:8px'>"
            "<a href='https://aistudio.google.com/app/apikey' "
            "style='color:#67B8BA' target='_blank'>Get free key →</a></p>",
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:16px 0'>", unsafe_allow_html=True)
        if st.button("← Back to Home"):
            state.screen = "landing"
            st.rerun()

    # ── Main form ─────────────────────────────────────────────────
    st.markdown("""
    <div style='margin-bottom:6px'>
      <span style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;
                   color:#0F7173;letter-spacing:3px'>STEP 01 OF 01</span>
    </div>
    <h2 style='font-family:IBM Plex Serif,serif;margin-bottom:4px;font-size:1.7rem;color:#1E3A5F'>
      Your Interview Profile
    </h2>
    <p style='color:#718096;margin-bottom:24px;font-size:0.92rem'>
      This shapes your personalised strategy — role, company type, and experience 
      determine question difficulty and focus areas.
    </p>
    <hr style='border-color:#DDE1E7;margin-bottom:28px'>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        name       = st.text_input("Full Name *", placeholder="e.g. Alex Chen")
        role       = st.selectbox("Target Role *", ROLES)
        experience = st.selectbox("Experience Level *", EXPERIENCE)
    with c2:
        email        = st.text_input("Email", placeholder="you@example.com (optional)")
        company_type = st.selectbox("Target Company Type *", COMPANIES)
        career_goal  = st.text_input(
            "Career Goal",
            placeholder="e.g. Senior ML Engineer at Google — optional",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family:IBM Plex Mono,monospace;font-size:0.62rem;
              color:#718096;letter-spacing:3px;text-transform:uppercase;margin-bottom:8px'>
      Weak Areas to Focus On
    </p>
    <p style='color:#A0AEC0;font-size:0.80rem;margin-bottom:10px'>
      Select skills where you feel least confident. The AI will prioritise these.
    </p>
    """, unsafe_allow_html=True)

    weak_areas = st.multiselect(
        "", SKILLS,
        placeholder="Select skills... (leave blank to let AI decide)",
        label_visibility="collapsed",
    )

    # ── Difficulty override ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚙ Advanced Options", expanded=False):
        difficulty_override = st.select_slider(
            "Difficulty Override",
            options=["Auto (AI decides)", "Easy", "Medium", "Hard"],
            value="Auto (AI decides)",
        )
        max_q = st.slider("Number of Questions", min_value=4, max_value=12, value=8)

    # ── Submit ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if not state.api_key:
        st.warning(
            "⚠ No Gemini API key configured. "
            "Add your key in the sidebar to use real AI evaluation. "
            "The platform will use simulated scoring without a key.",
            icon=None,
        )

    cc1, cc2, _ = st.columns([1.5, 2, 2])
    with cc1:
        if st.button("← Back"):
            state.screen = "landing"; st.rerun()
    with cc2:
        ready = st.button("GENERATE STRATEGY & START →", use_container_width=True)

    if ready:
        if not name.strip():
            st.error("Please enter your name to continue.")
            return

        state.profile = {
            "name":         name.strip(),
            "email":        email.strip() or f"user@neuralprep.app",
            "role":         role,
            "company_type": company_type,
            "experience":   experience,
            "career_goal":  career_goal,
            "weak_areas":   weak_areas,
            "max_questions": max_q,
        }
        state.max_questions_override = max_q

        from ...services.ai_service import AIService
        from ...engine.interview_engine import InterviewEngine
        from ...database.base import SessionLocal, init_db

        mock = not bool(state.api_key)
        ai   = AIService(api_key=state.api_key or None, mock=mock)
        state.mock_mode = mock
        init_db()
        db  = SessionLocal()
        eng = InterviewEngine(ai, db)

        with st.spinner("Building your personalised interview strategy with Gemini 2.5 Pro..."):
            eng.setup_profile(state.profile)
            # Apply difficulty override
            if difficulty_override != "Auto (AI decides)":
                eng.strategy["difficulty"] = difficulty_override.lower()

        first_q = eng.next_question()

        state.engine_state = {
            "strategy":        eng.strategy,
            "session_id":      eng.session_obj.session_id,
            "user_id":         eng.session_obj.user_id,
            "used_skills":     eng.used_skills.copy(),
            "question_count":  eng.question_count,
            "follow_up_count": eng.follow_up_count.copy(),
            "max_questions":   max_q,
        }
        state.current_question = first_q
        state.answers, state.messages = [], []
        state.screen = "interview"
        db.close()
        st.rerun()
