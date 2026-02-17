"""ui/pages/interview.py — Production interview screen"""

import streamlit as st
from ..styles import (
    badge, section_label, score_box_html, progress_bar_html,
    question_bubble, user_bubble, sidebar_metric, score_color_hex
)
from ...config import settings
from ...services.analytics_service import AnalyticsService


def _rebuild_engine(state):
    from ...services.ai_service import AIService
    from ...engine.interview_engine import InterviewEngine
    from ...database.base import SessionLocal, init_db
    from ...database.models import InterviewSession
    init_db()
    ai  = AIService(api_key=state.api_key or None, mock=state.mock_mode)
    db  = SessionLocal()
    eng = InterviewEngine(ai, db)
    es  = state.engine_state
    eng.strategy         = es["strategy"]
    eng.used_skills      = list(es.get("used_skills", []))
    eng.question_count   = es.get("question_count", 0)
    eng.follow_up_count  = dict(es.get("follow_up_count", {}))
    eng.current_question = state.current_question
    eng.session_obj      = db.query(InterviewSession).filter_by(
                               session_id=es["session_id"]).first()
    return eng, db


def render(state):
    answered   = len(state.answers)
    strat      = state.engine_state.get("strategy", {})
    max_q      = state.engine_state.get("max_questions", settings.max_questions)

    # ── Sidebar ───────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='font-family:IBM Plex Mono,monospace;font-size:0.78rem;
                    color:#FFFFFF;letter-spacing:1px;margin-bottom:2px'>NEURALPREP</div>
        """, unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.72rem;color:#94A3B8;margin-bottom:12px'>"
            f"{state.profile.get('name','Candidate')} · {state.profile.get('role','')}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:0 0 12px'>", unsafe_allow_html=True)

        avg = round(sum(a["overall_score"] for a in state.answers) / answered, 1) if answered else 0
        rd  = AnalyticsService.compute_readiness(state.answers)
        lc  = {"Interview Ready":"#4ADE80","Intermediate":"#FBB040","Beginner":"#F87171"}.get(rd["level"],"#FFFFFF")

        st.markdown(
            sidebar_metric("Progress",  f"{answered}/{max_q}")
            + sidebar_metric("Avg Score", f"{avg:.1f}/10" if answered else "—")
            + sidebar_metric("Level",     rd["level"], lc),
            unsafe_allow_html=True,
        )

        if answered:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-family:IBM Plex Mono,monospace;font-size:0.55rem;"
                "color:#64748B;letter-spacing:3px;margin-bottom:8px'>DIMENSION SCORES</p>",
                unsafe_allow_html=True,
            )
            for lbl, key in [("Concept","concept_score"),("Clarity","clarity_score"),("Confidence","confidence_score")]:
                v   = round(sum(a[key] for a in state.answers) / answered, 1)
                c_  = "#4ADE80" if v>=7 else "#FBB040" if v>=4 else "#F87171"
                pct = v * 10
                st.markdown(f"""
                <div style='margin-bottom:8px'>
                  <div style='display:flex;justify-content:space-between;
                              font-family:IBM Plex Mono,monospace;font-size:0.60rem;
                              color:#94A3B8;margin-bottom:3px'>
                    <span>{lbl}</span><span style='color:{c_}'>{v:.1f}</span>
                  </div>
                  <div style='background:rgba(255,255,255,0.1);border-radius:4px;height:4px'>
                    <div style='width:{pct}%;height:4px;background:{c_};border-radius:4px'></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        if strat.get("focus_skills"):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-family:IBM Plex Mono,monospace;font-size:0.55rem;"
                "color:#64748B;letter-spacing:3px;margin-bottom:8px'>FOCUS SKILLS</p>",
                unsafe_allow_html=True,
            )
            for sk in strat["focus_skills"]:
                done   = any(a.get("skill_tested") == sk for a in state.answers)
                prefix = "✓" if done else "·"
                color  = "#4ADE80" if done else "#94A3B8"
                st.markdown(
                    f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.64rem;"
                    f"color:{color};padding:2px 0'>{prefix} {sk}</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.15);margin:16px 0 10px'>", unsafe_allow_html=True)

        # Eval mode indicator
        mode_text = "✓ Gemini 2.5 Pro" if not state.mock_mode else "⚠ Simulated (no key)"
        mode_color = "#4ADE80" if not state.mock_mode else "#F87171"
        st.markdown(
            f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            f"color:{mode_color};margin-bottom:12px'>{mode_text}</div>",
            unsafe_allow_html=True,
        )

        if st.button("📊 Report",    use_container_width=True, disabled=answered==0):
            state.screen = "report"; st.rerun()
        if st.button("📈 Analytics", use_container_width=True, disabled=answered<2):
            state.screen = "analytics"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 New Session", use_container_width=True):
            state.screen = "setup"
            state.answers, state.messages = [], []
            state.current_question, state.engine_state = None, {}
            st.rerun()

    # ── Page header ───────────────────────────────────────────────
    h1, h2 = st.columns([5,1])
    with h1:
        st.markdown(
            "<h2 style='margin:0;font-family:IBM Plex Serif,serif;font-size:1.4rem;color:#1E3A5F'>"
            "Interview Session</h2>",
            unsafe_allow_html=True,
        )
        if strat:
            st.markdown(
                f"<p style='color:#718096;font-size:0.82rem;margin:2px 0 0'>"
                f"{strat.get('interview_style','').title()} · {strat.get('difficulty','').title()} Difficulty · "
                f"{'Probing enabled' if strat.get('probing_enabled') else 'Standard mode'}</p>",
                unsafe_allow_html=True,
            )
    with h2:
        st.markdown(
            f"<div style='text-align:right;font-family:IBM Plex Mono,monospace;"
            f"font-size:0.88rem;color:#718096;padding-top:8px'>"
            f"Q{answered+1 if state.current_question else answered}/{max_q}</div>",
            unsafe_allow_html=True,
        )

    st.progress(answered / max_q)
    st.markdown("<hr style='border-color:#DDE1E7;margin:8px 0 20px'>", unsafe_allow_html=True)

    # ── Message history ───────────────────────────────────────────
    for msg in state.messages:
        if msg["role"] == "question":
            st.markdown(
                question_bubble(msg["text"], msg["skill"], msg["difficulty"], msg.get("is_follow_up", False)),
                unsafe_allow_html=True,
            )
        elif msg["role"] == "user":
            st.markdown(user_bubble(msg["text"]), unsafe_allow_html=True)
        elif msg["role"] == "evaluation":
            ev = msg["evaluation"]
            c1,c2,c3,c4 = st.columns(4)
            for col_, lbl, k in zip(
                [c1,c2,c3,c4],
                ["OVERALL","CONCEPT","CLARITY","CONFIDENCE"],
                ["overall_score","concept_score","clarity_score","confidence_score"],
            ):
                col_.markdown(score_box_html(ev[k], lbl), unsafe_allow_html=True)

            if ev.get("reasoning"):
                st.markdown(
                    f"<div style='background:#F7F8FA;border-left:3px solid #DDE1E7;"
                    f"border-radius:0 4px 4px 0;padding:8px 14px;margin:8px 0;"
                    f"font-size:0.80rem;color:#718096;font-style:italic'>"
                    f"Evaluator: {ev['reasoning']}</div>",
                    unsafe_allow_html=True,
                )

            with st.expander("📋 Full Evaluation + Model Answer", expanded=False):
                fc1, fc2 = st.columns(2)
                with fc1:
                    st.markdown(
                        f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
                        f"color:#1A7A4A;letter-spacing:2px;margin-bottom:6px'>✓ STRENGTHS</div>"
                        f"<p style='font-size:0.88rem;line-height:1.75;color:#2D3748'>{ev['strengths']}</p>",
                        unsafe_allow_html=True,
                    )
                with fc2:
                    st.markdown(
                        f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
                        f"color:#C0392B;letter-spacing:2px;margin-bottom:6px'>✗ WEAKNESSES</div>"
                        f"<p style='font-size:0.88rem;line-height:1.75;color:#2D3748'>{ev['weaknesses']}</p>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
                    f"color:#E07B39;letter-spacing:2px;margin-bottom:6px'>→ HOW TO IMPROVE</div>"
                    f"<p style='font-size:0.88rem;line-height:1.75;color:#2D3748'>{ev['improvement_tips']}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='background:#E6F4F4;border:1px solid #99CCCC;"
                    f"border-left:4px solid #0F7173;border-radius:4px;padding:16px;margin-top:12px'>"
                    f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.58rem;"
                    f"color:#0F7173;letter-spacing:3px;margin-bottom:8px'>EXPERT ANSWER</div>"
                    f"<div style='font-size:0.90rem;line-height:1.8;color:#1E3A5F;"
                    f"font-family:IBM Plex Serif,serif'>{ev['ideal_answer']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if ev.get("weak_skills"):
                    st.markdown(
                        "<div style='margin-top:10px;font-family:IBM Plex Mono,monospace;"
                        "font-size:0.58rem;color:#718096;letter-spacing:2px'>STUDY THESE AREAS</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        "".join(badge(s, "red") for s in ev["weak_skills"]),
                        unsafe_allow_html=True,
                    )
            st.markdown("<br>", unsafe_allow_html=True)

    # ── Active question ───────────────────────────────────────────
    q = state.current_question
    if not q:
        st.info("Session complete — view your full report in the sidebar.")
        return

    st.markdown(
        question_bubble(q["question"], q["skill"], q["difficulty"], q.get("is_follow_up", False)),
        unsafe_allow_html=True,
    )

    answer_text = st.text_area(
        "",
        height=170,
        placeholder=(
            "Write your answer here.\n\n"
            "Tip: Strong answers include — a precise definition, the key equation or "
            "algorithm, a real-world example, and at least one trade-off or limitation."
        ),
        key=f"ans_{answered}",
        label_visibility="collapsed",
    )

    sc1, sc2, sc3 = st.columns([2, 1, 4])
    with sc1:
        submit = st.button("✔  SUBMIT ANSWER", use_container_width=True)
    with sc2:
        skip = st.button("SKIP →", use_container_width=True)

    if submit or skip:
        is_skipped  = skip and not (submit and answer_text.strip())
        answer_body = answer_text.strip() if (submit and answer_text.strip()) else ""

        if submit and not answer_body:
            st.warning("Please write your answer before submitting.")
            return

        display = "— skipped —" if is_skipped else answer_body

        state.messages.append({
            "role": "question", "text": q["question"],
            "skill": q["skill"], "difficulty": q["difficulty"],
            "is_follow_up": q.get("is_follow_up", False),
        })
        state.messages.append({"role": "user", "text": display})

        eng, db = _rebuild_engine(state)
        spinner_msg = "Analysing your answer with Gemini 2.5 Pro..." if not is_skipped else "Logging skip..."
        with st.spinner(spinner_msg):
            ev = eng.submit_answer(answer_body, skipped=is_skipped)

        state.messages.append({"role": "evaluation", "evaluation": ev})
        state.answers.append({**ev, "skill_tested": q["skill"]})
        answered += 1

        state.engine_state["used_skills"]     = eng.used_skills.copy()
        state.engine_state["question_count"]  = eng.question_count
        state.engine_state["follow_up_count"] = eng.follow_up_count.copy()

        if answered >= max_q:
            state.current_question = None
            state.screen = "report"
            db.close(); st.rerun(); return

        follow_up = None
        if (
            not is_skipped
            and strat.get("probing_enabled")
            and ev.get("follow_up_question")
            and not q.get("is_follow_up")
        ):
            follow_up = ev["follow_up_question"]

        next_q = eng.next_question(follow_up=follow_up)
        state.engine_state["used_skills"]     = eng.used_skills.copy()
        state.engine_state["question_count"]  = eng.question_count
        state.engine_state["follow_up_count"] = eng.follow_up_count.copy()
        state.current_question = next_q
        db.close(); st.rerun()
