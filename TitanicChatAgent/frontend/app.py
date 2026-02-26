import sys
import streamlit as st

# Enforce running with `streamlit run` command
if "streamlit" not in sys.modules:
    print("\n❌ ERROR: This app must be run with Streamlit!\n")
    print("🔧 Fix: Use this command instead:\n")
    print("   streamlit run app.py\n")
    sys.exit(1)

import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Titanic Chat Agent",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root {
    --navy:    #0B1F3A;
    --ocean:   #1A3A6B;
    --wave:    #1565C0;
    --sky:     #1E88E5;
    --foam:    #42A5F5;
    --mint:    #00BCD4;
    --gold:    #FFC107;
    --coral:   #FF6B6B;
    --success: #26A69A;
    --bg:      #F0F6FF;
    --card:    #FFFFFF;
    --border:  #DDEEFF;
    --text:    #0B1F3A;
    --muted:   #546E8A;
    --shadow:    0 4px 24px rgba(11,31,58,0.10);
    --shadow-lg: 0 8px 40px rgba(11,31,58,0.16);
}
html,body,[class*="css"]{ font-family:'Inter',sans-serif; }
.main{ background:var(--bg); }
.block-container{ padding-top:1.5rem !important; }

.hero{
    background:linear-gradient(135deg,var(--navy) 0%,var(--ocean) 50%,var(--wave) 100%);
    border-radius:20px; padding:2.5rem 3rem; margin-bottom:1.8rem;
    position:relative; overflow:hidden; box-shadow:var(--shadow-lg);
}
.hero::before{
    content:""; position:absolute; top:-40px; right:-60px;
    width:280px; height:280px; background:rgba(255,255,255,0.04); border-radius:50%;
}
.hero::after{
    content:""; position:absolute; bottom:-60px; left:-30px;
    width:200px; height:200px; background:rgba(66,165,245,0.08); border-radius:50%;
}
.hero-badge{
    display:inline-block; background:rgba(255,255,255,0.15);
    border:1px solid rgba(255,255,255,0.25); color:#FFF;
    font-size:0.73rem; font-weight:600; padding:3px 10px;
    border-radius:20px; margin-bottom:0.75rem; letter-spacing:0.5px; text-transform:uppercase;
}
.hero-title{ font-size:2.6rem; font-weight:700; color:#FFF; margin:0 0 0.3rem; line-height:1.2; letter-spacing:-0.5px; }
.hero-sub  { font-size:1.05rem; color:rgba(255,255,255,0.72); margin:0; font-weight:400; }

.stat-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.8rem; }
.stat-card{
    background:var(--card); border-radius:16px; padding:1.25rem 1.5rem;
    border:1px solid var(--border); box-shadow:var(--shadow);
    position:relative; overflow:hidden; transition:transform .2s,box-shadow .2s;
}
.stat-card:hover{ transform:translateY(-2px); box-shadow:var(--shadow-lg); }
.stat-card .accent-bar{ position:absolute; top:0; left:0; width:4px; height:100%; border-radius:16px 0 0 16px; }
.stat-card .stat-icon { font-size:1.8rem; margin-bottom:0.3rem; }
.stat-card .stat-value{ font-size:1.7rem; font-weight:700; color:var(--navy); line-height:1; margin-bottom:0.2rem; }
.stat-card .stat-label{ font-size:0.82rem; color:var(--muted); font-weight:500; text-transform:uppercase; letter-spacing:0.5px; }
.stat-card .stat-sub  { font-size:0.78rem; font-weight:600; padding:2px 8px; border-radius:20px; display:inline-block; margin-top:0.4rem; }

[data-testid="stChatMessage"]{
    border-radius:16px !important; padding:0.875rem 1.125rem !important;
    margin-bottom:0.75rem !important; box-shadow:0 1px 6px rgba(11,31,58,0.07) !important;
}
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0B1F3A 0%,#1A3A6B 100%) !important;
    border-right:none !important;
}
[data-testid="stSidebar"] *{ color:rgba(255,255,255,0.88) !important; }
[data-testid="stSidebar"] .sidebar-label{
    font-size:0.70rem; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,0.45) !important;
    margin:1.2rem 0 0.5rem;
}
[data-testid="stSidebar"] .stButton>button{
    background:rgba(255,255,255,0.06) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    color:rgba(255,255,255,0.85) !important;
    border-radius:10px !important; padding:0.55rem 0.9rem !important;
    font-size:0.83rem !important; font-weight:400 !important;
    width:100% !important; transition:all .2s !important; margin-bottom:4px !important;
}
[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(66,165,245,0.22) !important;
    border-color:rgba(66,165,245,0.50) !important;
    color:#FFF !important; transform:translateX(3px) !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"]{
    font-size:1.4rem !important; font-weight:700 !important; color:#FFE082 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"]{
    font-size:0.78rem !important; color:rgba(255,255,255,0.55) !important;
}
[data-testid="stSidebar"] hr{ border-color:rgba(255,255,255,0.10) !important; }
.clear-div .stButton>button{
    background:rgba(255,107,107,0.18) !important;
    border-color:rgba(255,107,107,0.40) !important;
    color:#FFAAAA !important;
}
.clear-div .stButton>button:hover{
    background:rgba(255,107,107,0.32) !important;
    border-color:#FF6B6B !important; color:#FFDDDD !important;
    transform:none !important;
}
[data-testid="stChatInput"]{
    border-radius:14px !important; border:2px solid var(--border) !important;
    background:var(--card) !important; box-shadow:0 2px 12px rgba(11,31,58,0.07) !important;
    transition:border-color .2s !important;
}
[data-testid="stChatInput"]:focus-within{
    border-color:var(--sky) !important; box-shadow:0 0 0 3px rgba(30,136,229,0.15) !important;
}
[data-testid="stPlotlyChart"]{
    background:var(--card); border-radius:16px; padding:0.5rem;
    border:1px solid var(--border); box-shadow:var(--shadow); margin-top:0.75rem;
}
.welcome-card{
    background:linear-gradient(135deg,#E3F2FD,#F3E5F5);
    border:1px solid #BBDEFB; border-radius:16px;
    padding:1.2rem 1.5rem; margin-bottom:1.2rem;
    display:flex; align-items:flex-start; gap:0.75rem;
}
.footer{
    text-align:center; padding:1.5rem 0 0.75rem; color:var(--muted);
    font-size:0.83rem; border-top:1px solid var(--border); margin-top:2rem;
}
.footer a{ color:var(--sky); text-decoration:none; }
::-webkit-scrollbar{ width:6px; height:6px; }
::-webkit-scrollbar-track{ background:transparent; }
::-webkit-scrollbar-thumb{ background:#BBDEFB; border-radius:10px; }
::-webkit-scrollbar-thumb:hover{ background:var(--sky); }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://localhost:8000")

EXAMPLE_QUESTIONS = {
    "📊 Statistics": [
        "What was the overall survival rate?",
        "What was the average ticket fare?",
        "What was the average age of passengers?",
        "Give me a dataset overview",
    ],
    "👥 Demographics": [
        "What percentage of passengers were male?",
        "How many passengers were in each class?",
        "Compare survival rates by gender",
        "Show distribution of embarkation ports",
    ],
    "🔍 Deep Dive": [
        "Show me a histogram of passenger ages",
        "Average age of survivors vs non-survivors?",
        "Who paid the most expensive ticket?",
        "Survival rate by passenger class?",
    ],
}

CHART_THEME = dict(
    template="plotly_white",
    font=dict(family="Inter, sans-serif", size=12, color="#0B1F3A"),
    title_font=dict(size=15, color="#0B1F3A", family="Inter, sans-serif"),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=50, b=10),
    colorway=["#1E88E5","#00BCD4","#FFC107","#26A69A","#FF6B6B","#7C4DFF","#FF8F00"],
    xaxis=dict(showgrid=True, gridcolor="rgba(11,31,58,0.07)", gridwidth=1, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(11,31,58,0.07)", gridwidth=1, zeroline=False),
)

def render_visualization(viz_config):
    if not viz_config:
        return
    vtype  = viz_config.get("type")
    data   = viz_config.get("data")
    title  = viz_config.get("title", "")
    xlabel = viz_config.get("xlabel", "")
    ylabel = viz_config.get("ylabel", "")
    try:
        if vtype == "histogram":
            fig = px.histogram(x=data, nbins=30, title=title,
                               labels={"x": xlabel, "y": ylabel},
                               color_discrete_sequence=["#1E88E5"])
            fig.update_traces(marker_line_color="#1565C0", marker_line_width=1)
        elif vtype == "bar":
            fig = go.Figure(go.Bar(
                x=list(data.keys()), y=list(data.values()),
                marker=dict(color=list(range(len(data))),
                            colorscale=[[0,"#1565C0"],[0.5,"#1E88E5"],[1,"#42A5F5"]],
                            line=dict(color="#0B1F3A", width=1), showscale=False)))
            fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
        elif vtype == "pie":
            fig = go.Figure(go.Pie(
                labels=list(data.keys()), values=list(data.values()), hole=0.45,
                marker=dict(colors=["#26A69A","#FF6B6B"], line=dict(color="#FFF", width=3)),
                textinfo="label+percent", textfont_size=13))
            fig.update_layout(title=title)
        else:
            return
        fig.update_layout(**CHART_THEME)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")

def stream_text(text):
    words = text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.022)

def fetch_answer(question):
    r = requests.post(f"{API_URL}/query", json={"question": question}, timeout=45)
    r.raise_for_status()
    d = r.json()
    return d.get("answer", ""), d.get("visualization")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='padding:1rem 0 0.5rem;'>
            <div style='font-size:1.6rem;font-weight:700;color:#FFF;letter-spacing:-0.3px;'>🚢 Titanic AI</div>
            <div style='font-size:0.8rem;color:rgba(255,255,255,0.5);margin-top:4px;'>Powered by Groq · LangChain · FastAPI</div>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    try:
        resp = requests.get(f"{API_URL}/dataset/info", timeout=4)
        if resp.status_code == 200:
            info = resp.json()
            c1, c2 = st.columns(2)
            with c1: st.metric("Passengers", info["total_passengers"])
            with c2: st.metric("Features",   len(info["columns"]))
            with st.expander("📋 Columns", expanded=False):
                for col in info["columns"]:
                    st.markdown(f"<span style='color:rgba(255,255,255,0.75);font-size:0.83rem;'>• {col}</span>",
                                unsafe_allow_html=True)
        else:
            st.warning("⚠️ Backend offline")
    except Exception:
        st.markdown("""<div style='background:rgba(255,107,107,0.15);border:1px solid rgba(255,107,107,0.35);
            border-radius:10px;padding:0.6rem 0.9rem;font-size:0.83rem;color:#FFAAAA;'>⚠️ Backend not reachable.<br>
            <span style='opacity:.7;'>Run <code style='background:rgba(255,255,255,0.1);padding:1px 5px;border-radius:4px;'>python main.py</code></span></div>""",
            unsafe_allow_html=True)

    st.divider()

    for category, questions in EXAMPLE_QUESTIONS.items():
        st.markdown(f"<div class='sidebar-label'>{category}</div>", unsafe_allow_html=True)
        for i, q in enumerate(questions):
            if st.button(q, key=f"q_{category}_{i}", use_container_width=True):
                st.session_state.selected_question = q

    st.divider()

    if st.session_state.get("messages"):
        st.markdown("<div class='clear-div'>", unsafe_allow_html=True)
        if st.button("🗑️  Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🧠 AI Analytics · Live Streaming</div>
    <div class="hero-title">🚢 Titanic Dataset Chat Agent</div>
    <div class="hero-sub">Ask questions in plain English — get professional statistical insights,
    comparisons, and interactive visualizations streamed back in real time.</div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = None
if "selected_question" in st.session_state:
    user_input = st.session_state.pop("selected_question")

# Stats cards always visible
st.markdown("""
<div class="stat-grid">
    <div class="stat-card">
        <div class="accent-bar" style="background:linear-gradient(180deg,#1565C0,#42A5F5);"></div>
        <div class="stat-icon">👥</div>
        <div class="stat-value">891</div>
        <div class="stat-label">Total Passengers</div>
    </div>
    <div class="stat-card">
        <div class="accent-bar" style="background:linear-gradient(180deg,#00838F,#00BCD4);"></div>
        <div class="stat-icon">📋</div>
        <div class="stat-value">12</div>
        <div class="stat-label">Dataset Features</div>
    </div>
    <div class="stat-card">
        <div class="accent-bar" style="background:linear-gradient(180deg,#E65100,#FFC107);"></div>
        <div class="stat-icon">⚡</div>
        <div class="stat-value">Groq</div>
        <div class="stat-label">AI Engine</div>
        <span class="stat-sub" style="background:#FFF8E1;color:#E65100;">FREE Tier</span>
    </div>
    <div class="stat-card">
        <div class="accent-bar" style="background:linear-gradient(180deg,#1B5E20,#26A69A);"></div>
        <div class="stat-icon">📡</div>
        <div class="stat-value">Live</div>
        <div class="stat-label">Streaming</div>
        <span class="stat-sub" style="background:#E8F5E9;color:#1B5E20;">Real-time</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <span style="font-size:1.5rem;margin-top:2px;">💡</span>
        <div style="font-size:0.92rem;color:#1A3A6B;line-height:1.5;">
            <b>Welcome!</b> I'm your AI analyst for the Titanic dataset. Choose a question from
            the sidebar or type anything below — I'll stream the answer back in real time
            with charts when relevant.
        </div>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("visualization"):
            render_visualization(message["visualization"])

# Always render chat_input so the widget is never dropped from the DOM
chat_input = st.chat_input("💬  Ask anything about the Titanic dataset…")
prompt = user_input or chat_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status = st.empty()
        status.markdown("<span style='color:#546E8A;font-size:0.88rem;'>🔍 Analysing dataset…</span>",
                        unsafe_allow_html=True)
        try:
            answer, visualization = fetch_answer(prompt)
            status.empty()
            streamed = st.write_stream(stream_text(answer))
            if visualization:
                render_visualization(visualization)
            st.session_state.messages.append({"role": "assistant", "content": streamed, "visualization": visualization})
        except requests.exceptions.ConnectionError:
            status.empty()
            msg = "❌ **Connection Error** — Cannot reach the backend API.\n\nMake sure it is running:\n```\ncd backend && python main.py\n```"
            st.error(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except requests.exceptions.Timeout:
            status.empty()
            msg = "⏱️ **Timeout** — The query took too long. Please try a simpler question."
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            status.empty()
            msg = f"❌ **Unexpected error:** {e}"
            st.error(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    Built with ❤️ using
    <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a> ·
    <a href="https://python.langchain.com" target="_blank">LangChain</a> ·
    <a href="https://streamlit.io" target="_blank">Streamlit</a> ·
    <a href="https://console.groq.com" target="_blank">Groq AI</a>
</div>
""", unsafe_allow_html=True)
