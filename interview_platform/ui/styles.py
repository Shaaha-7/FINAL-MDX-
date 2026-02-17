"""
ui/styles.py  — Light Professional Theme
─────────────────────────────────────────────────────────────
Clean academic aesthetic:
  • Cream/white background  #FAFAF8 / #FFFFFF
  • Slate navy accents      #1E3A5F
  • Teal action colour      #0F7173
  • Amber highlight         #E07B39
  • Soft greys for text     #4A5568 / #718096
  • IBM Plex Serif + Plex Sans typography
─────────────────────────────────────────────────────────────
"""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --bg:       #FAFAF8;
  --bg2:      #FFFFFF;
  --bg3:      #F0EFE9;
  --border:   #DDE1E7;
  --border2:  #C4CDD6;
  --navy:     #1E3A5F;
  --teal:     #0F7173;
  --teal2:    #0A5254;
  --amber:    #E07B39;
  --red:      #C0392B;
  --green:    #1A7A4A;
  --text:     #2D3748;
  --text2:    #718096;
  --text3:    #A0AEC0;
  --mono:     'IBM Plex Mono', monospace;
  --sans:     'IBM Plex Sans', sans-serif;
  --serif:    'IBM Plex Serif', serif;
  --shadow:   0 1px 4px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.06);
  --shadow-sm:0 1px 3px rgba(0,0,0,0.06);
}

/* ── Base ─────────────────────────────────────────────────── */
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main, .block-container {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--sans) !important;
}

/* Subtle dot-grid background */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: radial-gradient(circle, #C4CDD6 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: 0.45;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--navy) !important;
  border-right: none !important;
}
[data-testid="stSidebar"] * {
  color: #CBD5E0 !important;
  font-family: var(--sans) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: #FFFFFF !important;
  font-family: var(--mono) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,0.1) !important;
  color: #FFFFFF !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 1px !important;
  border-radius: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255,255,255,0.2) !important;
  transform: none !important;
}

/* ── Typography ───────────────────────────────────────────── */
h1, h2, h3, h4 {
  font-family: var(--serif) !important;
  color: var(--navy) !important;
}
p, li, span, div { color: var(--text); font-family: var(--sans) !important; }
label {
  font-family: var(--mono) !important;
  font-size: 0.68rem !important;
  color: var(--text2) !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
}

/* ── Main buttons ─────────────────────────────────────────── */
.stButton > button {
  background: var(--teal) !important;
  color: #FFFFFF !important;
  font-family: var(--mono) !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  letter-spacing: 1.5px !important;
  border: none !important;
  border-radius: 4px !important;
  padding: 10px 22px !important;
  box-shadow: var(--shadow-sm) !important;
  transition: all 0.18s ease !important;
}
.stButton > button:hover {
  background: var(--teal2) !important;
  box-shadow: 0 4px 14px rgba(15,113,115,0.3) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Inputs ───────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stNumberInput > div > div > input {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 4px !important;
  font-family: var(--sans) !important;
  font-size: 0.92rem !important;
  box-shadow: var(--shadow-sm) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
  border-color: var(--teal) !important;
  box-shadow: 0 0 0 2px rgba(15,113,115,0.15) !important;
}
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 4px !important;
  box-shadow: var(--shadow-sm) !important;
}
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div { color: var(--text) !important; }

/* ── Dividers ─────────────────────────────────────────────── */
hr { border-color: var(--border) !important; opacity: 1 !important; }

/* ── Expander ─────────────────────────────────────────────── */
.streamlit-expanderHeader {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  color: var(--text2) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 1px !important;
  border-radius: 4px !important;
}
.streamlit-expanderContent {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  border-radius: 0 0 4px 4px !important;
}

/* ── Progress bar ─────────────────────────────────────────── */
.stProgress > div > div { background: var(--border) !important; border-radius: 8px !important; }
.stProgress > div > div > div { background: var(--teal) !important; border-radius: 8px !important; }

/* ── Spinner ──────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--teal) !important; }

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg3); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* ── Download button ──────────────────────────────────────── */
.stDownloadButton > button {
  background: transparent !important;
  color: var(--teal) !important;
  border: 1.5px solid var(--teal) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  letter-spacing: 1px !important;
  border-radius: 4px !important;
}
.stDownloadButton > button:hover {
  background: var(--teal) !important;
  color: #FFFFFF !important;
}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg2) !important;
  border-bottom: 2px solid var(--border) !important;
  gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text2) !important;
  font-family: var(--mono) !important;
  font-size: 0.70rem !important;
  letter-spacing: 1.5px !important;
  border-radius: 0 !important;
  padding: 10px 22px !important;
  border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
  color: var(--teal) !important;
  border-bottom: 2px solid var(--teal) !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding-top: 1.5rem !important; }

/* ── Metric widget ────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  padding: 14px 18px !important;
  box-shadow: var(--shadow-sm) !important;
}
[data-testid="stMetricValue"] { font-family: var(--mono) !important; color: var(--navy) !important; }
[data-testid="stMetricLabel"] {
  font-family: var(--mono) !important;
  color: var(--text2) !important;
  font-size: 0.62rem !important;
  letter-spacing: 2px !important;
}

/* ── Alert ────────────────────────────────────────────────── */
.stAlert {
  background: var(--bg3) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 4px !important;
}
</style>
"""

# ── HTML component helpers ────────────────────────────────────────

def badge(text: str, variant: str = "navy") -> str:
    colours = {
        "navy":   ("#EBF0F8", "#1E3A5F", "#B8C9E0"),
        "teal":   ("#E6F4F4", "#0F7173", "#99CCCC"),
        "amber":  ("#FEF3EC", "#E07B39", "#F5C8A8"),
        "red":    ("#FDEEEC", "#C0392B", "#F0B0AA"),
        "green":  ("#E8F5EE", "#1A7A4A", "#9ACFB5"),
        "grey":   ("#F2F4F7", "#718096", "#C4CDD6"),
    }
    bg, fg, bd = colours.get(variant, colours["navy"])
    return (
        f"<span style='display:inline-block;background:{bg};color:{fg};"
        f"border:1px solid {bd};font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
        f"letter-spacing:2px;padding:2px 10px;border-radius:3px;margin:2px'>{text}</span>"
    )


def section_label(text: str) -> str:
    return (
        f"<p style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;"
        f"color:#718096;letter-spacing:3px;text-transform:uppercase;"
        f"margin-bottom:6px;margin-top:4px'>{text}</p>"
    )


def score_color_hex(val: float) -> str:
    return "#1A7A4A" if val >= 7 else "#D4860B" if val >= 4 else "#C0392B"


def progress_bar_html(val: float, label: str, color: str = "") -> str:
    color = color or score_color_hex(val)
    pct   = val * 10
    bg_color = "#E8F5EE" if val >= 7 else "#FEF3EC" if val >= 4 else "#FDEEEC"
    return f"""
<div style='margin-bottom:12px'>
  <div style='display:flex;justify-content:space-between;
              font-family:IBM Plex Mono,monospace;font-size:0.68rem;
              margin-bottom:5px;color:#4A5568'>
    <span>{label}</span>
    <span style='color:{color};font-weight:600'>{val:.1f}<span style='color:#A0AEC0'>/10</span></span>
  </div>
  <div style='background:#DDE1E7;border-radius:6px;height:7px;overflow:hidden'>
    <div style='width:{pct}%;height:7px;background:{color};border-radius:6px;
                transition:width 0.5s ease'></div>
  </div>
</div>"""


def score_box_html(value: float, label: str) -> str:
    color  = score_color_hex(value)
    bg_map = {True: "#E8F5EE", False: "#FEF3EC"}
    bg     = "#E8F5EE" if value >= 7 else "#FEF3EC" if value >= 4 else "#FDEEEC"
    return f"""
<div style='background:{bg};border:1px solid {color}33;border-radius:6px;
            text-align:center;padding:18px 10px;box-shadow:0 1px 3px rgba(0,0,0,0.05)'>
  <div style='font-family:IBM Plex Mono,monospace;font-size:2rem;
              font-weight:700;color:{color};line-height:1'>{value:.1f}</div>
  <div style='font-family:IBM Plex Mono,monospace;font-size:0.55rem;
              letter-spacing:2px;color:#718096;margin-top:5px'>{label}</div>
</div>"""


def question_bubble(question: str, skill: str, difficulty: str, is_follow_up: bool = False) -> str:
    fu = ""
    if is_follow_up:
        fu = "<div style='font-family:IBM Plex Mono,monospace;font-size:0.60rem;color:#E07B39;letter-spacing:2px;margin-bottom:8px'>↳ FOLLOW-UP PROBE</div>"
    diff_color = {"easy": "#1A7A4A", "medium": "#D4860B", "hard": "#C0392B"}.get(difficulty, "#0F7173")
    return f"""
<div style='background:#FFFFFF;border:1px solid #DDE1E7;border-left:4px solid #0F7173;
            border-radius:6px;padding:20px 24px;margin:12px 0;
            box-shadow:0 1px 4px rgba(0,0,0,0.06)'>
  {fu}
  <div style='display:flex;gap:8px;align-items:center;margin-bottom:10px'>
    {badge(skill, "teal")}
    {badge(difficulty.upper(), "amber" if difficulty=="medium" else "green" if difficulty=="easy" else "red")}
  </div>
  <div style='font-size:1.02rem;font-weight:500;color:#1E3A5F;
              line-height:1.75;font-family:IBM Plex Serif,serif'>{question}</div>
</div>"""


def user_bubble(text: str) -> str:
    preview = text[:600] + "..." if len(text) > 600 else text
    return f"""
<div style='background:#F0F7F7;border:1px solid #99CCCC;border-right:4px solid #0F7173;
            border-radius:6px;padding:16px 20px;margin:8px 0'>
  <div style='font-family:IBM Plex Mono,monospace;font-size:0.58rem;
              color:#0F7173;letter-spacing:2px;margin-bottom:8px'>YOUR ANSWER</div>
  <div style='font-size:0.90rem;color:#2D3748;line-height:1.7'>{preview}</div>
</div>"""


def sidebar_metric(label: str, value: str, color: str = "#FFFFFF") -> str:
    return f"""
<div style='display:flex;justify-content:space-between;align-items:center;
            padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.1);font-size:0.82rem'>
  <span style='color:#A0AEC0'>{label}</span>
  <span style='font-family:IBM Plex Mono,monospace;color:{color};font-weight:600'>{value}</span>
</div>"""
