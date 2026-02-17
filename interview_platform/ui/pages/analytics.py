"""ui/pages/analytics.py — Light theme analytics dashboard with Plotly"""

import streamlit as st
from ..styles import badge, section_label, score_color_hex
from ...services.analytics_service import AnalyticsService

# Light-theme Plotly constants
_BG    = "#FAFAF8"
_BG2   = "#FFFFFF"
_GRID  = "#DDE1E7"
_TEXT  = "#718096"
_NAVY  = "#1E3A5F"
_TEAL  = "#0F7173"
_AMBER = "#E07B39"
_RED   = "#C0392B"
_GREEN = "#1A7A4A"

try:
    import plotly.graph_objects as go
    _PLOTLY = True
except ImportError:
    _PLOTLY = False


def _base_layout(fig, title: str = ""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="IBM Plex Mono", size=10, color=_TEXT)) if title else None,
        paper_bgcolor=_BG2, plot_bgcolor=_BG2,
        font=dict(family="IBM Plex Mono", size=10, color=_TEXT),
        xaxis=dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_TEXT, family="IBM Plex Mono", size=9)),
        yaxis=dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(color=_TEXT, family="IBM Plex Mono", size=9)),
        margin=dict(l=40, r=20, t=30, b=40),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, color=_TEXT)),
    )
    return fig


def render(state):
    answers  = state.answers
    profile  = state.profile

    with st.sidebar:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.75rem;"
            "color:#FFFFFF;letter-spacing:2px'>ANALYTICS</p>",
            unsafe_allow_html=True,
        )
        if st.button("← Back to Interview"):
            state.screen = "interview"; st.rerun()
        if st.button("📋 View Report",    use_container_width=True):
            state.screen = "report"; st.rerun()
        if st.button("🔄 New Interview",  use_container_width=True):
            state.screen = "setup"
            state.answers, state.messages = [], []
            state.current_question, state.engine_state = None, {}
            st.rerun()

    st.markdown(
        f"<h2 style='font-family:IBM Plex Serif,serif;margin:0'>Analytics Dashboard</h2>"
        f"<p style='color:#718096;margin:4px 0 20px;font-size:0.9rem'>"
        f"{profile.get('name','Candidate')} · {profile.get('role','')} · {len(answers)} questions answered</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#DDE1E7;margin-bottom:24px'>", unsafe_allow_html=True)

    if not answers:
        st.info("Complete some questions first to see analytics.")
        return

    readiness = AnalyticsService.compute_readiness(answers)
    breakdown = AnalyticsService.skill_breakdown(answers)
    weak      = AnalyticsService.weak_skill_clusters(answers)
    comp      = readiness["composite"]

    # ── KPI row ───────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Readiness Score", f"{readiness['score']}/10")
    k2.metric("Avg Overall",     f"{round(sum(a['overall_score'] for a in answers)/len(answers),1)}/10")
    k3.metric("Questions Done",  f"{len(answers)}/{state.engine_state.get('strategy',{}).get('max_questions',8)}")
    k4.metric("Weak Skills",     str(len(weak)))

    st.markdown("<br>", unsafe_allow_html=True)

    if not _PLOTLY:
        st.warning("Install plotly for charts:  `pip install plotly`")
        return

    # ── Score progression ─────────────────────────────────────────
    qs   = [f"Q{i+1}" for i in range(len(answers))]
    fig1 = go.Figure()
    dims = [
        ("overall_score",   "Overall",    _TEAL,  dict(width=2.5)),
        ("concept_score",   "Concept",    _NAVY,  dict(width=1.5, dash="dot")),
        ("clarity_score",   "Clarity",    _AMBER, dict(width=1.5, dash="dot")),
        ("confidence_score","Confidence", _GREEN, dict(width=1.5, dash="dot")),
    ]
    for key, name, color, ls in dims:
        vals = [a[key] for a in answers]
        fig1.add_trace(go.Scatter(
            x=qs, y=vals, name=name, mode="lines+markers",
            line=dict(color=color, **ls),
            marker=dict(color=color, size=7),
        ))
    fig1.update_yaxes(range=[0, 10.5])
    fig1.add_hline(y=7, line_dash="dash", line_color=_GREEN, opacity=0.4,
                   annotation_text="Interview Ready ≥7", annotation_position="right",
                   annotation_font=dict(color=_GREEN, size=9))
    fig1.add_hline(y=4, line_dash="dash", line_color=_AMBER, opacity=0.4,
                   annotation_text="Intermediate ≥4", annotation_position="right",
                   annotation_font=dict(color=_AMBER, size=9))

    st.markdown(
        "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
        "color:#718096;letter-spacing:3px'>SCORE PROGRESSION</p>",
        unsafe_allow_html=True,
    )
    st.plotly_chart(_base_layout(fig1), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)

    # ── Skill bar chart ───────────────────────────────────────────
    with ch1:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            "color:#718096;letter-spacing:3px'>SKILL PERFORMANCE</p>",
            unsafe_allow_html=True,
        )
        skills = list(breakdown.keys())
        avgs   = [breakdown[s]["avg_overall"] for s in skills]
        colors = [score_color_hex(v) for v in avgs]
        short  = [s.split(" ")[0] + ("…" if " " in s else "") for s in skills]
        fig2   = go.Figure(go.Bar(
            x=avgs, y=short, orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}" for v in avgs],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=9, color=_TEXT),
        ))
        fig2.update_xaxes(range=[0, 11])
        fig2.update_layout(bargap=0.35)
        st.plotly_chart(_base_layout(fig2), use_container_width=True, config={"displayModeBar": False})

    # ── Radar chart ───────────────────────────────────────────────
    with ch2:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            "color:#718096;letter-spacing:3px'>COMPETENCY RADAR</p>",
            unsafe_allow_html=True,
        )
        cats   = ["Concept", "Clarity", "Confidence", "Consistency"]
        vals   = [comp["concept"], comp["clarity"], comp["confidence"], comp["consistency"]] + [comp["concept"]]
        cats_c = cats + [cats[0]]
        fig3   = go.Figure(go.Scatterpolar(
            r=vals, theta=cats_c, fill="toself",
            fillcolor="rgba(15,113,115,0.12)",
            line=dict(color=_TEAL, width=2),
            marker=dict(color=_TEAL, size=7),
        ))
        fig3.update_layout(
            polar=dict(
                bgcolor=_BG2,
                radialaxis=dict(range=[0, 10], gridcolor=_GRID, tickcolor=_TEXT,
                                tickfont=dict(size=8, color=_TEXT), showline=False),
                angularaxis=dict(gridcolor=_GRID, tickfont=dict(size=9, family="IBM Plex Mono", color=_NAVY)),
            ),
            paper_bgcolor=_BG2, showlegend=False,
            margin=dict(l=40, r=40, t=30, b=40),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    ch3, ch4 = st.columns(2)

    # ── Dimension comparison ──────────────────────────────────────
    with ch3:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            "color:#718096;letter-spacing:3px'>DIMENSION BREAKDOWN</p>",
            unsafe_allow_html=True,
        )
        dim_names = ["Concept", "Clarity", "Confidence", "Consistency"]
        dim_vals  = [comp["concept"], comp["clarity"], comp["confidence"], comp["consistency"]]
        dim_cols  = [score_color_hex(v) for v in dim_vals]
        fig4 = go.Figure(go.Bar(
            x=dim_names, y=dim_vals,
            marker=dict(color=dim_cols, line=dict(width=0)),
            text=[f"{v:.1f}" for v in dim_vals],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=9, color=_TEXT),
        ))
        fig4.update_yaxes(range=[0, 11])
        fig4.update_layout(bargap=0.4)
        st.plotly_chart(_base_layout(fig4), use_container_width=True, config={"displayModeBar": False})

    # ── Difficulty split ──────────────────────────────────────────
    with ch4:
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            "color:#718096;letter-spacing:3px'>SCORE BY DIFFICULTY</p>",
            unsafe_allow_html=True,
        )
        diff_groups: dict = {}
        for a in answers:
            d = a.get("difficulty", "medium")
            diff_groups.setdefault(d, []).append(a["overall_score"])
        diffs  = list(diff_groups.keys())
        d_avgs = [round(sum(v)/len(v),1) for v in diff_groups.values()]
        d_cols = [_GREEN if d=="easy" else _AMBER if d=="medium" else _RED for d in diffs]
        fig5   = go.Figure(go.Bar(
            x=diffs, y=d_avgs,
            marker=dict(color=d_cols, line=dict(width=0)),
            text=[f"{v:.1f}" for v in d_avgs],
            textposition="outside",
            textfont=dict(family="IBM Plex Mono", size=10, color=_TEXT),
        ))
        fig5.update_yaxes(range=[0, 11])
        fig5.update_layout(bargap=0.5)
        st.plotly_chart(_base_layout(fig5), use_container_width=True, config={"displayModeBar": False})

    if weak:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
            "color:#718096;letter-spacing:3px;margin-bottom:6px'>WEAK SKILL CLUSTERS (avg &lt; 5)</p>",
            unsafe_allow_html=True,
        )
        st.markdown("".join(badge(w, "red") for w in weak), unsafe_allow_html=True)
