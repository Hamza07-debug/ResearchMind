import streamlit as st
import time
import sys
import os
import html
import re

# ─── Page config (must be first) ────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind — Multi-Agent AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Inject custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0a;
    color: #e8e8e8;
}
.stApp { background-color: #0a0a0a; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #ff6b00; border-radius: 3px; }

/* ── Hero section ── */
.hero-wrapper {
    position: relative;
    text-align: center;
    padding: 80px 20px 60px;
    overflow: hidden;
}
.hero-wrapper::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60vw;
    height: 60vh;
    background: radial-gradient(circle, rgba(255,107,0,0.15) 0%, transparent 70%);
    filter: blur(50px);
    z-index: 0;
    animation: pulseGlow 8s ease-in-out infinite alternate;
}
@keyframes pulseGlow {
    0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.6; }
    100% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
}
.hero-eyebrow {
    position: relative;
    z-index: 1;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #ff6b00;
    text-transform: uppercase;
    margin-bottom: 24px;
}
.hero-title {
    position: relative !important;
    z-index: 1 !important;
    font-family: 'Archivo Black', 'Arial Black', Impact, sans-serif !important;
    font-size: clamp(50px, 8vw, 90px) !important;
    font-weight: 900 !important;
    line-height: 1.0 !important;
    letter-spacing: -2px !important;
    margin: 0 !important;
    color: #ffffff !important;
    display: inline-block !important;
}
.hero-title .hero-accent { 
    color: #ff6b00 !important;
}
.animated-subtitle-container {
    position: relative;
    z-index: 1;
    height: 30px;
    margin: 30px auto 0;
    max-width: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.animated-subtitle-container span {
    position: absolute;
    font-size: 18px;
    font-weight: 400;
    color: #b0b0b0;
    opacity: 0;
    animation: textCycle 18s linear infinite;
    white-space: nowrap;
}
.animated-subtitle-container span:nth-child(1) { animation-delay: 0s; }
.animated-subtitle-container span:nth-child(2) { animation-delay: 3s; }
.animated-subtitle-container span:nth-child(3) { animation-delay: 6s; }
.animated-subtitle-container span:nth-child(4) { animation-delay: 9s; }
.animated-subtitle-container span:nth-child(5) { animation-delay: 12s; }
.animated-subtitle-container span:nth-child(6) { animation-delay: 15s; }

@keyframes textCycle {
    0% { opacity: 0; transform: translateY(15px); }
    2.77% { opacity: 1; transform: translateY(0); }
    13.88% { opacity: 1; transform: translateY(0); }
    16.66% { opacity: 0; transform: translateY(-15px); }
    100% { opacity: 0; transform: translateY(-15px); }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Input label ── */
.input-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #ff6b00;
    text-transform: uppercase;
    margin-bottom: 6px;
}

/* ── Streamlit text_input override ── */
.stTextInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #ff6b00 !important;
    box-shadow: 0 0 15px rgba(255,107,0,0.4), 0 0 0 2px rgba(255,107,0,0.2) !important;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff6b00, #ff8c38) !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    transform: scale(1.02) translateY(-2px) !important;
    box-shadow: 0 10px 40px rgba(255,107,0,0.5) !important;
    background: linear-gradient(135deg, #ff8c38, #ff6b00) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Suggestion chips ── */
.chips-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
.chip {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: #888;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.chip:hover { 
    border-color: #ff6b00; 
    color: #ff6b00; 
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 4px 15px rgba(255,107,0,0.2);
}

/* ── Pipeline card ── */
.pipeline-header {
    font-size: 20px;
    font-weight: 700;
    color: #f0f0f0;
    margin-bottom: 18px;
}
.agent-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: border-color 0.3s, background 0.3s;
    position: relative;
    overflow: hidden;
}
.agent-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.4), 0 0 15px rgba(255,107,0,0.1);
    border-color: #333;
}
.agent-card.active {
    border-color: #ff6b00;
    background: #141414;
    box-shadow: 0 0 20px rgba(255,107,0,0.08);
}
.agent-card.active:hover {
    border-color: #ff6b00;
    box-shadow: 0 10px 20px rgba(0,0,0,0.4), 0 0 25px rgba(255,107,0,0.2);
}
.agent-card.done { border-color: #2a5c2a; background: #0f1a0f; }
.agent-card.done:hover {
    border-color: #4caf50;
    box-shadow: 0 10px 20px rgba(0,0,0,0.4), 0 0 15px rgba(76, 175, 80, 0.2);
}
.agent-card.idle { opacity: 0.5; }
.agent-num {
    font-size: 11px;
    font-weight: 700;
    color: #444;
    min-width: 22px;
}
.agent-info { flex: 1; }
.agent-name { font-size: 14px; font-weight: 600; color: #e0e0e0; }
.agent-desc { font-size: 12px; color: #555; margin-top: 2px; }
.agent-status-done { font-size: 11px; font-weight: 600; color: #4caf50; }
.agent-status-active { font-size: 11px; font-weight: 600; color: #ff6b00; }

/* ── Spinner dot animation ── */
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}
.dot-pulse { display: inline-flex; gap: 4px; align-items: center; }
.dot-pulse span {
    width: 5px; height: 5px; border-radius: 50%;
    background: #ff6b00; display: inline-block;
    animation: pulse 1.2s infinite;
}
.dot-pulse span:nth-child(2) { animation-delay: 0.2s; }
.dot-pulse span:nth-child(3) { animation-delay: 0.4s; }

/* ── UI Animations ── */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
.agent-card { animation: fadeInUp 0.4s ease-out forwards; }
.agent-card:nth-child(1) { animation-delay: 0.1s; }
.agent-card:nth-child(2) { animation-delay: 0.2s; }
.agent-card:nth-child(3) { animation-delay: 0.3s; }
.agent-card:nth-child(4) { animation-delay: 0.4s; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Section divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 40px 0;
}

/* ── Results area ── */
.results-wrapper {
    background: #0d0d0d;
    border: 1px solid #1e1e1e;
    border-radius: 16px;
    padding: 32px;
    margin-top: 10px;
}
.results-title {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #ff6b00;
    text-transform: uppercase;
    margin-bottom: 24px;
}
.tab-bar { display: flex; gap: 6px; margin-bottom: 24px; flex-wrap: wrap; }
.tab-btn {
    background: #1a1a1a;
    border: 1px solid #252525;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
    color: #666;
    cursor: pointer;
    transition: all 0.2s;
}
.tab-btn.active { background: #ff6b00; border-color: #ff6b00; color: #fff; }

/* ── Report content ── */
.report-content {
    background: #111;
    border-radius: 12px;
    padding: 28px;
    line-height: 1.8;
    font-size: 15px;
    color: #d0d0d0;
    border: 1px solid #1e1e1e;
    white-space: pre-wrap;
    word-break: break-word;
}
.report-content h2, .report-content h3 {
    color: #f0f0f0;
    margin-top: 20px;
    margin-bottom: 8px;
}

/* ── Score badge ── */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #1a1a1a, #141414);
    border: 1px solid #ff6b00;
    border-radius: 12px;
    padding: 14px 24px;
    margin-bottom: 20px;
}
.score-value {
    font-size: 36px;
    font-weight: 900;
    color: #ff6b00;
    line-height: 1;
}
.score-label { font-size: 13px; color: #666; }

/* ── Raw search expander override ── */
.streamlit-expanderHeader {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 10px !important;
    color: #888 !important;
    font-size: 13px !important;
}

/* ── Success toast ── */
.success-banner {
    background: linear-gradient(135deg, #0f1a0f, #111);
    border: 1px solid #2a5c2a;
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}
.success-icon { font-size: 22px; }
.success-text { font-size: 14px; font-weight: 600; color: #4caf50; }

/* ── Stat pills ── */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px; }
.stat-pill {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 12px;
    color: #666;
}
.stat-pill strong { color: #e0e0e0; display: block; font-size: 18px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─── Session state ───────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "pipeline_step" not in st.session_state:
    st.session_state.pipeline_step = -1   # -1 = idle
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

SUGGESTIONS = [
    "LLM agents 2025",
    "Quantum computing breakthroughs",
    "AI in healthcare 2025",
    "Climate tech startups",
    "Neuralink updates",
]

AGENTS_META = [
    ("01", "Search Agent",  "Gathers recent web information"),
    ("02", "Reader Agent",  "Scrapes & extracts deep content"),
    ("03", "Writer Chain",  "Synthesises a structured report"),
    ("04", "Critic Chain",  "Scores & reviews the report"),
]

# ─── Helper: render pipeline sidebar cards ───────────────────────────────────
def render_pipeline_cards(current_step: int):
    st.markdown('<div class="pipeline-header">Pipeline</div>', unsafe_allow_html=True)
    for i, (num, name, desc) in enumerate(AGENTS_META):
        if current_step == -1:           # idle
            card_class = "idle"
            status_html = ""
        elif i < current_step:           # done
            card_class = "done"
            status_html = '<span class="agent-status-done">✓ DONE</span>'
        elif i == current_step:          # active
            card_class = "active"
            status_html = (
                '<span class="agent-status-active">'
                '<span class="dot-pulse"><span></span><span></span><span></span></span>'
                ' RUNNING</span>'
            )
        else:                            # upcoming
            card_class = "idle"
            status_html = ""

        st.markdown(f"""
        <div class="agent-card {card_class}">
            <span class="agent-num">{num}</span>
            <div class="agent-info">
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{desc}</div>
            </div>
            {status_html}
        </div>
        """, unsafe_allow_html=True)

# ─── Helper: extract score from critic feedback ───────────────────────────────
def extract_score(feedback: str) -> str:
    m = re.search(r"Score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10", feedback, re.IGNORECASE)
    return m.group(1) if m else "—"

# ─── Helper: word count ───────────────────────────────────────────────────────
def word_count(text: str) -> int:
    return len(text.split())

# ─── Helper: flatten agent content to plain text ─────────────────────────────
def flatten_content(raw) -> str:
    """Agent messages can return a string OR a list of content blocks.
    This normalises both into a single plain string."""
    if isinstance(raw, str):
        return raw
    if isinstance(raw, list):
        parts = []
        for block in raw:
            if isinstance(block, dict):
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(p for p in parts if p.strip())
    return str(raw)

# ─── Helper: retry LLM call on 429 rate-limit ────────────────────────────────
def with_retry(fn, max_retries: int = 3, base_wait: int = 5):
    """Call fn(). On HTTP 429, wait and retry up to max_retries times."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if "429" in msg or "rate_limit" in msg.lower() or "rate limit" in msg.lower() or "too many requests" in msg.lower():
                wait = base_wait * (attempt + 1)
                st.toast(f"⏳ API rate limit hit — briefly pausing for {wait}s before retry {attempt+1}/{max_retries}...", icon="⚠️")
                time.sleep(wait)
            else:
                raise   # not a rate-limit error — re-raise immediately
    raise RuntimeError(f"Still rate-limited after {max_retries} retries. Try again in a minute.")

# ─── Helper: render a card title label ───────────────────────────────────────
def _render_card_title(title: str, icon: str):
    """Renders the orange uppercase section label using native st.markdown."""
    st.markdown(
        f"<div style='font-size:11px;font-weight:700;letter-spacing:3px;"
        f"color:#ff6b00;text-transform:uppercase;margin-bottom:10px;'>"
        f"{icon}&nbsp; {title}</div>",
        unsafe_allow_html=True,
    )

# ─── Helper: render a completed result block ──────────────────────────────────
def render_live_block(placeholder, title: str, icon: str, content: str,
                      score: str = "", font_size: str = "15px"):
    with placeholder.container():
        if title:
            _render_card_title(title, icon)
        # Score badge — rendered as native Streamlit metric, no raw HTML
        if score:
            st.markdown(
                f"<div style='display:inline-block;background:linear-gradient(135deg,#1a1a1a,#141414);"
                f"border:1px solid #ff6b00;border-radius:12px;padding:10px 22px;margin-bottom:14px;'>"
                f"<span style='font-size:28px;font-weight:900;color:#ff6b00;'>{score}</span>"
                f"<span style='font-size:12px;color:#888;margin-left:8px;'>/ 10 &nbsp; Quality score by Critic Agent</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        # Content rendered as plain markdown — never injected into HTML
        st.markdown(content)

# ─── Helper: stream a LangChain chain token-by-token into a placeholder ───────
def stream_chain_into(placeholder, chain, inputs: dict,
                      title: str, icon: str, score: str = "") -> str:
    """
    Streams chain output token-by-token. Title and score badge are native
    Streamlit elements; content is plain st.markdown — no HTML injection.
    """
    accumulated = ""

    for chunk in chain.stream(inputs):
        if isinstance(chunk, str):
            accumulated += chunk
        elif isinstance(chunk, dict):
            accumulated += chunk.get("content", "") or chunk.get("text", "")
        else:
            accumulated += str(chunk)

        with placeholder.container():
            if title:
                _render_card_title(title, icon)
            st.markdown(accumulated + " ▌")

    # Final render — no cursor
    with placeholder.container():
        if title:
            _render_card_title(title, icon)
        st.markdown(accumulated)

    return accumulated

# ─── Helper: simulate streaming for static content ────────────────────────────
def simulate_stream_into(placeholder, text: str, title: str, icon: str) -> str:
    """Simulates token-by-token streaming for a complete string."""
    accumulated = ""
    chunk_size = max(8, len(text) // 30)

    for i in range(0, len(text), chunk_size):
        accumulated += text[i:i+chunk_size]
        with placeholder.container():
            if title:
                _render_card_title(title, icon)
            st.markdown(accumulated + " ▌")

    with placeholder.container():
        if title:
            _render_card_title(title, icon)
        st.markdown(accumulated)
    return accumulated

# ─── Helper: Generate PDF ──────────────────────────────────────────────────
def create_pdf(title: str, content: str) -> bytes:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    # Simple multi-cell text rendering
    clean_content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, clean_content)
    return bytes(pdf.output())


# ─── Pipeline runner — token-by-token streaming for writer & critic ──────────
def run_pipeline_live(topic: str, cards_placeholder,
                      ph_search, ph_report, ph_scraped, ph_critic):

    from io import StringIO
    import contextlib
    from agents import (build_search_agent, build_reader_agent,
                        writer_chain, critic_chain)

    def _update_cards(step):
        st.session_state.pipeline_step = step
        with cards_placeholder.container():
            render_pipeline_cards(step)

    # ── Step 1 : Search Agent (invoke — no streaming for tool-calling agents) ─
    _update_cards(0)
    search_agent = build_search_agent()

    def _search():
        with contextlib.redirect_stdout(StringIO()):
            return search_agent.invoke({
                "messages": [{"role": "user",
                              "content": f"Find the most recent and latest information (within the last 30 days if possible) on the topic: {topic}. Focus on new developments, recent news, and current data. Include the current year in your search queries."}]
            })

    raw = with_retry(_search)
    search_result = flatten_content(raw["messages"][-1].content)
    simulate_stream_into(ph_search, search_result, "", "")

    time.sleep(3) # Small cooldown to prevent rapid-fire rate limits


    # ── Step 2 : Reader Agent (invoke) ──────────────────────────────────────
    _update_cards(1)
    reader_agent = build_reader_agent()

    def _read():
        with contextlib.redirect_stdout(StringIO()):
            return reader_agent.invoke({
                "messages": [{
                    "role": "user",
                    "content": (
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{search_result[:800]}"
                    ),
                }]
            })

    raw2 = with_retry(_read)
    scraped_content = flatten_content(raw2["messages"][-1].content)
    # Show scraped content immediately after Reader Agent is done
    simulate_stream_into(ph_scraped, scraped_content, "", "")

    time.sleep(3) # Small cooldown to prevent rapid-fire rate limits


    # ── Step 3 : Writer Chain — STREAMING token by token ────────────────────
    _update_cards(2)
    research_combined = (
        f"Search Results:\n{search_result}\n\n"
        f"Scraped Content:\n{scraped_content}"
    )

    def _stream_writer():
        return stream_chain_into(
            ph_report, writer_chain,
            {"topic": topic, "research": research_combined},
            title="FINAL RESEARCH REPORT", icon="📑",
        )

    report = with_retry(_stream_writer)
    report = flatten_content(report)

    time.sleep(3) # Small cooldown to prevent rapid-fire rate limits


    # ── Step 4 : Critic Chain — STREAMING token by token ────────────────────
    _update_cards(3)
    score_html_placeholder = ""   # score badge added after streaming finishes

    def _stream_critic():
        return stream_chain_into(
            ph_critic, critic_chain,
            {"report": report},
            title="Critic Review", icon="🧐",
        )

    feedback = with_retry(_stream_critic)
    feedback = flatten_content(feedback)

    # Re-render critic with score badge
    score = extract_score(feedback)
    render_live_block(ph_critic, "Critic Review", "🧐", feedback, score=score)

    _update_cards(4)

    return {
        "search_result": search_result,
        "scraped_content": scraped_content,
        "report": report,
        "feedback": feedback,
    }

# ════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ════════════════════════════════════════════════════════════════════════════

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1 class="hero-title">Research<span class="hero-accent">Mind</span></h1>
    <div class="animated-subtitle-container">
        <span>Four specialized AI agents collaborate</span>
        <span>Searching the web in real time</span>
        <span>Scraping deep content</span>
        <span>Writing structured reports</span>
        <span>Critiquing for accuracy</span>
        <span>To deliver a polished research report on any topic</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main columns ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.05, 0.95], gap="large")

with col_left:
    st.markdown('<div style="padding: 0 40px 40px;">', unsafe_allow_html=True)

    # Input label
    st.markdown('<div class="input-label">Research Topic</div>', unsafe_allow_html=True)

    topic = st.text_input(
        label="topic_hidden",
        value=st.session_state.topic_input,
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_field",
    )

    # Run button
    run_clicked = st.button("⚡  Run Research Pipeline", use_container_width=True)

    # Suggestion chips (cosmetic label + HTML)
    st.markdown('<div style="font-size:11px;color:#444;margin-top:14px;margin-bottom:6px;">TRY →</div>', unsafe_allow_html=True)
    chips_html = '<div class="chips-row">' + "".join(
        f'<span class="chip">{s}</span>' for s in SUGGESTIONS
    ) + "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div style="padding: 0 40px 0 0;">', unsafe_allow_html=True)
    cards_placeholder = st.empty()
    with cards_placeholder.container():
        render_pipeline_cards(st.session_state.pipeline_step)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Results area — four persistent placeholders rendered below the hero ──────
# These are always created so run_pipeline_live can write into them live.
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div style="padding: 0 40px 60px;">', unsafe_allow_html=True)

# Success / stat banner placeholder (filled after full run)
banner_ph = st.empty()

st.markdown('<h3 style="color:#f0f0f0; margin-bottom:20px; font-weight:700;">Results</h3>', unsafe_allow_html=True)

# Expanders for raw data
with st.expander("🔍 Search Results (raw)", expanded=False):
    ph_search = st.empty()

with st.expander("📄 Scraped Content (raw)", expanded=False):
    ph_scraped = st.empty()

st.markdown("<br>", unsafe_allow_html=True)

# Full width report
ph_report = st.empty()
ph_critic = st.empty()

# Download button placeholder (filled after report is ready)
download_ph = st.empty()

st.markdown("</div>", unsafe_allow_html=True)

# ── Pre-fill placeholders if we already have saved results (after rerun) ─────
if st.session_state.results and not run_clicked:
    res           = st.session_state.results
    report_text   = res.get("report", "")
    feedback_text = res.get("feedback", "")
    search_text   = res.get("search_result", "")
    scraped_text  = res.get("scraped_content", "")
    score         = extract_score(feedback_text)
    wc            = word_count(report_text)

    banner_ph.markdown(f"""<div class="success-banner">
<span class="success-icon">✅</span>
<span class="success-text">
Pipeline completed for &ldquo;{st.session_state.topic_input}&rdquo;
</span>
</div>
<div class="stat-row">
<div class="stat-pill"><strong>{score}/10</strong> Critic Score</div>
<div class="stat-pill"><strong>{wc:,}</strong> Report Words</div>
<div class="stat-pill"><strong>4</strong> Agents Used</div>
<div class="stat-pill"><strong>✓</strong> Complete</div>
</div>""", unsafe_allow_html=True)

    render_live_block(ph_search,  "", "", search_text)
    render_live_block(ph_report,  "FINAL RESEARCH REPORT", "📑", report_text)
    render_live_block(ph_scraped, "", "", scraped_text)
    render_live_block(ph_critic, "Critic Review", "🧐", feedback_text, score=score)

    with download_ph:
        dl_col1, dl_col2 = st.columns([1, 1])
        with dl_col1:
            st.download_button(
                label="⬇ Download Report (.txt)",
                data=report_text,
                file_name=f"research_{st.session_state.topic_input[:30].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with dl_col2:
            try:
                pdf_bytes = create_pdf(st.session_state.topic_input, report_text)
                st.download_button(
                    label="⬇ Download Report (.pdf)",
                    data=pdf_bytes,
                    file_name=f"research_{st.session_state.topic_input[:30].replace(' ','_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Could not generate PDF: {e}")

# ── Run logic ────────────────────────────────────────────────────────────────
if run_clicked:
    raw_topic = topic.strip()
    if not raw_topic:
        st.warning("Please enter a research topic first.")
    else:
        # Clear previous results
        st.session_state.results = None
        st.session_state.running = True
        st.session_state.topic_input = raw_topic
        banner_ph.empty()
        ph_search.empty()
        ph_report.empty()
        ph_scraped.empty()
        ph_critic.empty()
        download_ph.empty()

        try:
            results = run_pipeline_live(
                raw_topic,
                cards_placeholder,
                ph_search, ph_report, ph_scraped, ph_critic,
            )
            st.session_state.results = results
            st.session_state.running = False

            # Show banner + stats now that everything is done
            score = extract_score(results["feedback"])
            wc    = word_count(results["report"])
            banner_ph.markdown(f"""<div class="success-banner">
<span class="success-icon">✅</span>
<span class="success-text">
Pipeline completed for &ldquo;{raw_topic}&rdquo;
</span>
</div>
<div class="stat-row">
<div class="stat-pill"><strong>{score}/10</strong> Critic Score</div>
<div class="stat-pill"><strong>{wc:,}</strong> Report Words</div>
<div class="stat-pill"><strong>4</strong> Agents Used</div>
<div class="stat-pill"><strong>✓</strong> Complete</div>
</div>""", unsafe_allow_html=True)

            with download_ph:
                dl_col1, dl_col2 = st.columns([1, 1])
                with dl_col1:
                    st.download_button(
                        label="⬇ Download Report (.txt)",
                        data=results["report"],
                        file_name=f"research_{raw_topic[:30].replace(' ','_')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with dl_col2:
                    try:
                        pdf_bytes = create_pdf(raw_topic, results["report"])
                        st.download_button(
                            label="⬇ Download Report (.pdf)",
                            data=pdf_bytes,
                            file_name=f"research_{raw_topic[:30].replace(' ','_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"Could not generate PDF: {e}")

        except Exception as e:
            st.session_state.running = False
            st.session_state.pipeline_step = -1
            st.error(f"Pipeline error: {e}")

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 30px 20px 50px;
    font-size: 14px;
    color: #999;
    border-top: 1px solid #2a2a2a;
    margin-top: 40px;
}
.footer span { color: #ff6b00; font-weight: 600; }
</style>
<div class="footer">
    Built with <span>LangChain</span> · <span>Mistral AI</span> · <span>Tavily</span> · <span>Streamlit</span>
    &nbsp;|&nbsp; <span>ResearchMind</span> Multi-Agent System
</div>
""", unsafe_allow_html=True)
