import streamlit as st
from groq import Groq
import os
import re
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LogSense — AI Log Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --bg2: #111118;
    --bg3: #1a1a24;
    --accent: #00ff88;
    --accent2: #0066ff;
    --danger: #ff4455;
    --warn: #ffaa00;
    --text: #e8e8f0;
    --muted: #666680;
    --border: #2a2a3a;
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.main .block-container {
    padding: 2rem 3rem !important;
    max-width: 1100px !important;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    padding: 0.3rem 1rem;
    border-radius: 2px;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    line-height: 1 !important;
    margin: 0 0 1rem !important;
    background: linear-gradient(135deg, #fff 40%, #00ff88 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.hero p {
    font-size: 1.1rem !important;
    color: var(--muted) !important;
    max-width: 520px;
    margin: 0 auto 2rem !important;
    line-height: 1.6 !important;
}

/* Cards */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.stat-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}

.stat-card .num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    display: block;
}

.stat-card .label {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Input area */
.input-section {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: block;
}

/* Streamlit overrides */
.stTextArea textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.6 !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.15) !important;
}

.stSelectbox select, [data-testid="stSelectbox"] > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Button */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #00cc6a !important;
    transform: translateY(-1px) !important;
}

/* Result cards */
.result-block {
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-left: 3px solid;
}

.result-block.error {
    background: rgba(255,68,85,0.08);
    border-color: var(--danger);
}

.result-block.warning {
    background: rgba(255,170,0,0.08);
    border-color: var(--warn);
}

.result-block.success {
    background: rgba(0,255,136,0.08);
    border-color: var(--accent);
}

.result-block.info {
    background: rgba(0,102,255,0.08);
    border-color: var(--accent2);
}

.result-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    font-weight: 700;
}

.result-block.error .result-title { color: var(--danger); }
.result-block.warning .result-title { color: var(--warn); }
.result-block.success .result-title { color: var(--accent); }
.result-block.info .result-title { color: var(--accent2); }

.result-content {
    font-size: 0.92rem;
    line-height: 1.7;
    color: var(--text);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--bg3) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 2rem 0 !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.05em;
}

/* API key input */
.stTextInput input {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.15) !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg3) !important;
    color: var(--accent) !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ─── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI-POWERED LOG ANALYSIS</div>
    <h1>LogSense</h1>
    <p>Paste your log file. Get a plain-English diagnosis and exact fix — in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Row ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <span class="num">5</span>
        <span class="label">Log Types Supported</span>
    </div>
    <div class="stat-card">
        <span class="num">{st.session_state.analysis_count}</span>
        <span class="label">Analyses This Session</span>
    </div>
    <div class="stat-card">
        <span class="num">&lt;5s</span>
        <span class="label">Avg Response Time</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Main Layout ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<span class="section-label">🔑 Configuration</span>', unsafe_allow_html=True)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free at console.groq.com — your key is never stored."
    )

    st.markdown('<span class="section-label" style="margin-top:1.2rem; display:block;">📋 Log Type</span>', unsafe_allow_html=True)
    log_type = st.selectbox(
        "Select log type",
        ["Auto Detect", "Python Error", "Apache / Nginx", "Linux System", "Node.js", "Other"],
        label_visibility="collapsed"
    )

    st.markdown('<span class="section-label" style="margin-top:1.2rem; display:block;">📂 Input Method</span>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Paste Log", "Upload File"])

    log_content = ""
    with tab1:
        log_content_paste = st.text_area(
            "Paste your log here",
            height=220,
            placeholder="[ERROR] 2024-01-15 14:23:01 - Connection refused at 127.0.0.1:5432\nTraceback (most recent call last):\n  ...",
            label_visibility="collapsed"
        )
        log_content = log_content_paste

    with tab2:
        uploaded = st.file_uploader(
            "Upload log file",
            type=["log", "txt", "out", "err"],
            label_visibility="collapsed"
        )
        if uploaded:
            log_content = uploaded.read().decode("utf-8", errors="ignore")
            st.success(f"✅ Loaded: {uploaded.name} ({len(log_content)} chars)")

    st.markdown('</div>', unsafe_allow_html=True)

    analyze_btn = st.button("🔍 Analyze Log", use_container_width=True)

# ─── Analysis Logic ────────────────────────────────────────────────────────────
def detect_log_type(content):
    if "Traceback" in content or "SyntaxError" in content or "ImportError" in content:
        return "Python Error Log"
    if "apache" in content.lower() or "nginx" in content.lower() or "GET /" in content or "POST /" in content:
        return "Apache/Nginx Server Log"
    if "systemd" in content.lower() or "kernel" in content.lower() or "sudo" in content.lower():
        return "Linux System Log"
    if "node_modules" in content or "npm" in content.lower() or "TypeError" in content and "undefined" in content:
        return "Node.js Log"
    return "General Log"

def analyze_log(api_key, log_content, log_type):
    client = Groq(api_key=api_key)

    detected = detect_log_type(log_content) if log_type == "Auto Detect" else log_type
    truncated = log_content[:4000] if len(log_content) > 4000 else log_content

    system_prompt = """You are LogSense, an expert log file analyzer. 
Analyze the provided log and respond ONLY in this exact format:

## DETECTED LOG TYPE
[type]

## SEVERITY
[CRITICAL / HIGH / MEDIUM / LOW]

## WHAT WENT WRONG
[2-3 sentences in plain English, no jargon]

## ROOT CAUSE
[The actual technical reason, explained simply]

## EXACT FIX
[Step-by-step numbered fix — be specific and actionable]

## PREVENTION TIP
[One sentence on how to prevent this in the future]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Log Type Hint: {detected}\n\nLog Content:\n{truncated}"}
        ],
        temperature=0.3,
        max_tokens=900
    )

    return response.choices[0].message.content, detected

def parse_severity(result_text):
    if "CRITICAL" in result_text: return "error", "🔴 CRITICAL"
    if "HIGH" in result_text: return "error", "🟠 HIGH"
    if "MEDIUM" in result_text: return "warning", "🟡 MEDIUM"
    return "success", "🟢 LOW"

def render_section(title, content, card_type="info"):
    st.markdown(f"""
    <div class="result-block {card_type}">
        <div class="result-title">{title}</div>
        <div class="result-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Results Panel ─────────────────────────────────────────────────────────────
with col2:
    st.markdown('<span class="section-label">📊 Analysis Results</span>', unsafe_allow_html=True)

    if analyze_btn:
        if not api_key:
            st.error("⚠️ Please enter your OpenAI API key.")
        elif not log_content.strip():
            st.error("⚠️ Please paste or upload a log file.")
        else:
            with st.spinner("🤖 Analyzing your log..."):
                try:
                    result, detected_type = analyze_log(api_key, log_content, log_type)
                    st.session_state.last_result = result
                    st.session_state.analysis_count += 1

                    # Parse and display sections
                    sections = re.split(r'## ', result)
                    severity_type, severity_label = parse_severity(result)

                    for section in sections:
                        if not section.strip():
                            continue
                        lines = section.strip().split('\n', 1)
                        title = lines[0].strip()
                        content = lines[1].strip() if len(lines) > 1 else ""
                        content_html = content.replace('\n', '<br>')

                        if "SEVERITY" in title:
                            render_section(f"⚡ {title}", f"<strong>{severity_label}</strong>", severity_type)
                        elif "WHAT WENT WRONG" in title:
                            render_section(f"❌ {title}", content_html, "error")
                        elif "ROOT CAUSE" in title:
                            render_section(f"🔎 {title}", content_html, "warning")
                        elif "EXACT FIX" in title:
                            render_section(f"🔧 {title}", content_html, "success")
                        elif "PREVENTION" in title:
                            render_section(f"🛡️ {title}", content_html, "info")
                        elif "DETECTED" in title:
                            render_section(f"📋 {title}", content_html, "info")

                    # Download button
                    st.download_button(
                        "⬇️ Download Report",
                        data=f"LogSense Analysis Report\n{'='*50}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{result}",
                        file_name=f"logsense_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception as e:
                    err = str(e).lower()
                    if "invalid api key" in err or "authentication" in err:
                        st.error("❌ Invalid Groq API key. Get a free one at console.groq.com")
                    elif "rate limit" in err:
                        st.error("⚠️ Rate limit hit. Wait a moment and try again.")
                    else:
                        st.error(f"❌ Error: {str(e)}")

    elif st.session_state.last_result:
        st.info("👆 Your last result is above. Paste a new log and click Analyze again.")
    else:
        # Placeholder state
        st.markdown("""
        <div style="background: #111118; border: 1px dashed #2a2a3a; border-radius: 12px; padding: 3rem 2rem; text-align: center; color: #666680;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <div style="font-family: 'Space Mono', monospace; font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; color: #444460;">Waiting for input</div>
            <div style="font-size: 0.9rem; line-height: 1.6;">Paste your log on the left<br>and hit <strong style="color:#00ff88">Analyze Log</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Supported log types
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="section-label">✅ Supported Log Types</span>', unsafe_allow_html=True)
        for log in ["🐍 Python Tracebacks & Errors", "🌐 Apache / Nginx Access & Error Logs", "🐧 Linux System & Kernel Logs", "⬡ Node.js Runtime Errors", "📄 Any Custom Log Format"]:
            st.markdown(f"""
            <div style="background:#1a1a24; border:1px solid #2a2a3a; border-radius:6px; padding:0.6rem 1rem; margin-bottom:0.5rem; font-size:0.88rem; color:#e8e8f0;">
                {log}
            </div>
            """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div class="footer">
    LOGSENSE v1.0 — Built with Python + Groq (Llama 3.3 70B) + Streamlit &nbsp;|&nbsp; Your API key is never stored
</div>
""", unsafe_allow_html=True)