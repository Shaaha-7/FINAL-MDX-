"""ui/pages/landing.py — Production landing page, zero prototype elements"""

import streamlit as st


def render(state):
    st.markdown("<br>", unsafe_allow_html=True)

    col = st.columns([1, 3, 1])[1]
    with col:

        # ── Hero ──────────────────────────────────────────────────
        st.markdown("""
        <div style='text-align:center;padding:2.5rem 0 2rem'>
          <div style='display:inline-block;background:#EBF4F4;color:#0F7173;
                      font-family:IBM Plex Mono,monospace;font-size:0.62rem;
                      letter-spacing:3px;padding:5px 16px;border-radius:3px;
                      margin-bottom:1.6rem'>
            AI-POWERED TECHNICAL INTERVIEW TRAINING
          </div>
          <h1 style='font-family:IBM Plex Serif,serif;font-size:2.9rem;
                     font-weight:700;line-height:1.15;color:#1E3A5F;margin:0 0 1.2rem'>
            Prepare smarter.<br>
            <span style='color:#0F7173'>Interview with confidence.</span>
          </h1>
          <p style='color:#718096;font-size:1.05rem;line-height:1.85;
                    max-width:480px;margin:0 auto 2.2rem;font-family:IBM Plex Sans,sans-serif'>
            NeuralPrep delivers personalised AI/ML technical interviews 
            powered by Gemini 2.5 Pro. Get honest scores, expert feedback, 
            and targeted coaching — no fluff, no guesswork.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Feature cards ─────────────────────────────────────────
        features = [
            ("🎯", "Personalised Strategy", "Interview plan calibrated to your role, company, and experience level."),
            ("🧠", "Honest AI Scoring",     "Three-pass evaluation engine. No inflated scores — only real feedback."),
            ("🔁", "Adaptive Probing",      "Follow-up questions triggered by your answer quality, just like real interviews."),
            ("📊", "Deep Analytics",        "Skill radar, score progression, dimension breakdown, and gap detection."),
        ]
        c1, c2 = st.columns(2)
        for i, (icon, title, desc) in enumerate(features):
            col_ = c1 if i % 2 == 0 else c2
            col_.markdown(f"""
            <div style='background:#FFFFFF;border:1px solid #DDE1E7;border-top:3px solid #0F7173;
                        border-radius:6px;padding:18px 16px;margin-bottom:14px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05)'>
              <div style='font-size:1.2rem;margin-bottom:6px'>{icon}</div>
              <div style='font-family:IBM Plex Serif,serif;font-weight:600;
                          color:#1E3A5F;font-size:0.96rem;margin-bottom:5px'>{title}</div>
              <div style='color:#718096;font-size:0.82rem;line-height:1.6'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Skill chips ───────────────────────────────────────────
        st.markdown("""
        <div style='text-align:center;margin:1.5rem 0'>
          <div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;
                      color:#A0AEC0;letter-spacing:3px;margin-bottom:12px'>
            10 SKILL AREAS COVERED
          </div>
          <div>
        """, unsafe_allow_html=True)

        skills_html = ""
        from ...data.question_bank import SKILLS
        for sk in SKILLS:
            skills_html += (
                f"<span style='display:inline-block;background:#F7F8FA;color:#4A5568;"
                f"border:1px solid #DDE1E7;border-radius:3px;font-family:IBM Plex Mono,monospace;"
                f"font-size:0.60rem;letter-spacing:1px;padding:3px 10px;margin:3px'>{sk}</span>"
            )
        st.markdown(skills_html + "</div></div>", unsafe_allow_html=True)

        # ── CTA ───────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("START YOUR INTERVIEW SESSION →", use_container_width=True):
            state.screen = "setup"
            st.rerun()

        # ── 3-step how it works ───────────────────────────────────
        st.markdown("""
        <div style='margin:2rem 0 1rem;display:flex;justify-content:space-between;
                    text-align:center;gap:12px'>
          <div style='flex:1'>
            <div style='font-family:IBM Plex Mono,monospace;font-size:1.5rem;
                        color:#0F7173;font-weight:700;line-height:1'>01</div>
            <div style='font-size:0.80rem;color:#4A5568;margin-top:6px;font-weight:500'>Set Your Profile</div>
            <div style='font-size:0.74rem;color:#A0AEC0;margin-top:3px'>Role, company, experience</div>
          </div>
          <div style='flex:0;color:#DDE1E7;font-size:1.2rem;padding-top:8px'>→</div>
          <div style='flex:1'>
            <div style='font-family:IBM Plex Mono,monospace;font-size:1.5rem;
                        color:#0F7173;font-weight:700;line-height:1'>02</div>
            <div style='font-size:0.80rem;color:#4A5568;margin-top:6px;font-weight:500'>Answer Questions</div>
            <div style='font-size:0.74rem;color:#A0AEC0;margin-top:3px'>AI-generated, adaptive</div>
          </div>
          <div style='flex:0;color:#DDE1E7;font-size:1.2rem;padding-top:8px'>→</div>
          <div style='flex:1'>
            <div style='font-family:IBM Plex Mono,monospace;font-size:1.5rem;
                        color:#0F7173;font-weight:700;line-height:1'>03</div>
            <div style='font-size:0.80rem;color:#4A5568;margin-top:6px;font-weight:500'>Get Your Report</div>
            <div style='font-size:0.74rem;color:#A0AEC0;margin-top:3px'>Score, gaps, next steps</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style='text-align:center;color:#A0AEC0;font-size:0.76rem;margin-top:1.5rem'>
          Powered by Gemini 2.5 Pro · Built for ML, Data Science & AI engineers
        </p>
        """, unsafe_allow_html=True)
