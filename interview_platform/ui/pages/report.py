"""ui/pages/report.py — Light theme performance report"""

import json
from datetime import datetime

import streamlit as st

from ..styles import badge, score_box_html, progress_bar_html, score_color_hex
from ...services.analytics_service import AnalyticsService


def render(state):
    answers  = state.answers
    profile  = state.profile
    strategy = state.engine_state.get("strategy", {})

    if not answers:
        st.warning("No answers recorded yet.")
        if st.button("← Back"):
            state.screen = "interview"; st.rerun()
        return

    readiness = AnalyticsService.compute_readiness(answers)
    breakdown = AnalyticsService.skill_breakdown(answers)
    weak      = AnalyticsService.weak_skill_clusters(answers)
    level     = readiness["level"]
    score     = readiness["score"]
    comp      = readiness["composite"]

    lv_map = {
        "Interview Ready": ("#1A7A4A", "green", "#E8F5EE", "#B8DEC9"),
        "Intermediate":    ("#D4860B", "amber", "#FEF3EC", "#F5C8A8"),
        "Beginner":        ("#C0392B", "red",   "#FDEEEC", "#F0B0AA"),
    }
    lc, lv_badge, lv_bg, lv_border = lv_map.get(level, ("#0F7173","teal","#E6F4F4","#99CCCC"))

    # ── Sidebar ───────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            f"<div style='text-align:center;padding:1rem 0'>"
            f"<div style='font-family:IBM Plex Mono,monospace;font-size:2.5rem;"
            f"font-weight:700;color:#FFFFFF'>{score}</div>"
            f"<div style='font-family:IBM Plex Mono,monospace;font-size:0.65rem;"
            f"color:#A0AEC0;letter-spacing:2px'>/ 10</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        if st.button("← Back to Interview"):
            state.screen = "interview"; st.rerun()
        if st.button("📈 Analytics Dashboard", use_container_width=True):
            state.screen = "analytics"; st.rerun()
        if st.button("🔄 New Interview",        use_container_width=True):
            state.screen = "setup"
            state.answers, state.messages = [], []
            state.current_question, state.engine_state = None, {}
            st.rerun()

    # ── Header ────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:{lv_bg};border:1px solid {lv_border};border-radius:8px;
                padding:28px;text-align:center;margin-bottom:28px;
                box-shadow:0 2px 8px rgba(0,0,0,0.06)'>
      <div style='margin-bottom:10px'>
        {badge("PERFORMANCE REPORT", "teal")}
      </div>
      <h2 style='font-family:IBM Plex Serif,serif;color:#1E3A5F!important;
                 margin:8px 0 4px;font-size:1.6rem'>
        {profile.get("name","Candidate")}
      </h2>
      <p style='color:#718096;margin:0 0 12px;font-size:0.9rem'>
        {profile.get("role","")} · {profile.get("company_type","")} · {profile.get("experience","")}
      </p>
      <div style='font-family:IBM Plex Mono,monospace;font-size:3.5rem;
                  font-weight:700;color:{lc};line-height:1'>{score}/10</div>
      <div style='margin-top:10px'>{badge(level.upper(), lv_badge)}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Four score boxes ──────────────────────────────────────────
    answered = len(answers)
    def avg(k): return round(sum(a[k] for a in answers) / answered, 1)

    c1, c2, c3, c4 = st.columns(4)
    for col_, lbl, k in zip(
        [c1,c2,c3,c4],
        ["OVERALL","CONCEPT","CLARITY","CONFIDENCE"],
        ["overall_score","concept_score","clarity_score","confidence_score"],
    ):
        col_.markdown(score_box_html(avg(k), lbl), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skill + Composite ─────────────────────────────────────────
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("<h3 style='font-family:IBM Plex Serif,serif;font-size:1.2rem'>Skill Performance</h3>", unsafe_allow_html=True)
        for sk, d in breakdown.items():
            v = d["avg_overall"]
            st.markdown(progress_bar_html(v, sk, score_color_hex(v)), unsafe_allow_html=True)

    with r2:
        st.markdown("<h3 style='font-family:IBM Plex Serif,serif;font-size:1.2rem'>Composite Breakdown</h3>", unsafe_allow_html=True)
        for lbl, key in [("Concept (× 0.40)","concept"),("Clarity (× 0.20)","clarity"),
                          ("Confidence (× 0.20)","confidence"),("Consistency (× 0.20)","consistency")]:
            v = comp[key]
            st.markdown(progress_bar_html(v, lbl, score_color_hex(v)), unsafe_allow_html=True)

    # ── Weak skills ───────────────────────────────────────────────
    if weak:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='font-family:IBM Plex Serif,serif;font-size:1.1rem;color:#C0392B'>⚠ Weak Skill Areas</h3>",
            unsafe_allow_html=True,
        )
        st.markdown("".join(badge(w, "red") for w in weak), unsafe_allow_html=True)

    # ── Strategy + Recommendation ─────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("<h3 style='font-family:IBM Plex Serif,serif;font-size:1.1rem'>Strategy Used</h3>", unsafe_allow_html=True)
        if strategy:
            st.markdown(f"""
            <div style='background:#FFFFFF;border:1px solid #DDE1E7;border-radius:6px;
                        padding:18px;box-shadow:0 1px 4px rgba(0,0,0,0.05)'>
              <div style='font-size:0.88rem;margin-bottom:8px;color:#2D3748'>
                Style: <span style='font-family:IBM Plex Mono,monospace;color:#0F7173;font-weight:600'>{strategy.get("interview_style","—")}</span>
              </div>
              <div style='font-size:0.88rem;margin-bottom:8px;color:#2D3748'>
                Difficulty: <span style='font-family:IBM Plex Mono,monospace;color:#0F7173;font-weight:600'>{strategy.get("difficulty","—")}</span>
              </div>
              <div style='font-size:0.88rem;margin-bottom:8px;color:#2D3748'>
                Probing: <span style='font-family:IBM Plex Mono,monospace;color:{"#1A7A4A" if strategy.get("probing_enabled") else "#718096"};font-weight:600'>{"Enabled" if strategy.get("probing_enabled") else "Disabled"}</span>
              </div>
              <p style='color:#718096;font-size:0.82rem;margin:0;line-height:1.6'>{strategy.get("style_reason","")}</p>
            </div>
            """, unsafe_allow_html=True)

    with sc2:
        st.markdown("<h3 style='font-family:IBM Plex Serif,serif;font-size:1.1rem'>Recommendation</h3>", unsafe_allow_html=True)
        if level == "Interview Ready":
            rec = f"Excellent! You're ready for {profile.get('role','')} roles at {profile.get('company_type','')}. Maintain consistency and keep drilling edge cases."
        elif level == "Intermediate":
            wk_str = ", ".join(weak[:2]) if weak else "key fundamentals"
            rec = f"Good foundation. Focus on drilling {wk_str} — especially mathematical derivations. Aim for 2 more sessions."
        else:
            rec = f"More preparation needed. Strengthen {', '.join(weak[:3]) or 'all core ML areas'} before targeting {profile.get('company_type','')}."

        st.markdown(f"""
        <div style='background:{lv_bg};border:1px solid {lv_border};border-left:4px solid {lc};
                    border-radius:6px;padding:18px;height:100%'>
          <p style='color:{lc};font-size:0.92rem;line-height:1.7;margin:0;font-weight:500'>{rec}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Q&A review ────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Full Q&A Review", expanded=False):
        for i, a in enumerate(answers, 1):
            ov    = a.get("overall_score", 0)
            color = score_color_hex(ov)
            skipped = a.get("answer_text","") == "— skipped —" or ov == 0
            tag   = " · SKIPPED" if skipped else ""
            st.markdown(f"""
            <div style='border-bottom:1px solid #DDE1E7;padding:14px 0'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>
                <span style='font-family:IBM Plex Mono,monospace;font-size:0.68rem;color:#718096'>
                  Q{i} · {a.get("skill_tested","")}{tag}
                </span>
                <span style='font-family:IBM Plex Mono,monospace;font-weight:700;color:{color}'>{ov:.1f}/10</span>
              </div>
              <p style='font-size:0.82rem;color:#718096;margin:3px 0'><b style='color:#2D3748'>Strengths:</b> {a.get("strengths","—")}</p>
              <p style='font-size:0.82rem;color:#718096;margin:0'><b style='color:#2D3748'>Weaknesses:</b> {a.get("weaknesses","—")}</p>
            </div>
            """, unsafe_allow_html=True)

    # ── Download ──────────────────────────────────────────────────
    report_data = {
        "profile":             profile,
        "strategy":            strategy,
        "readiness":           readiness,
        "skill_breakdown":     breakdown,
        "weak_skill_clusters": weak,
        "answers":             [{k: v for k, v in a.items()} for a in answers],
        "generated_at":        datetime.utcnow().isoformat(),
    }
    fname = f"aiip_report_{profile.get('name','candidate').replace(' ','_').lower()}.json"
    st.download_button(
        "⬇  Download Full Report (JSON)",
        data=json.dumps(report_data, indent=2),
        file_name=fname,
        mime="application/json",
    )
