import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Titanic Dataset Chat Agent",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for Professional Look
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Centered main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1E40AF;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.3rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        border: 1px solid #E2E8F0;
    }
    
    .stButton>button:hover {
        background-color: #EFF6FF;
        border-color: #3B82F6;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E40AF;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #64748B;
        font-weight: 500;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Info box */
    .stAlert {
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #94A3B8;
        font-size: 0.9rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000")


# Define visualization rendering function with improved styling
def render_visualization(viz_config):
    """Render visualization based on configuration"""
    if not viz_config:
        return
    
    viz_type = viz_config.get("type")
    data = viz_config.get("data")
    title = viz_config.get("title", "")
    
    try:
        if viz_type == "histogram":
            fig = px.histogram(
                x=data,
                nbins=30,
                title=title,
                labels={"x": viz_config.get("xlabel", ""), "y": viz_config.get("ylabel", "")}
            )
            fig.update_layout(
                template="plotly_white",
                font=dict(size=12),
                title_font_size=16,
                title_font_color="#1E40AF",
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=1),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "bar":
            fig = go.Figure(data=[
                go.Bar(
                    x=list(data.keys()),
                    y=list(data.values()),
                    marker_color='#3B82F6',
                    marker_line_color='#1E40AF',
                    marker_line_width=1.5
                )
            ])
            fig.update_layout(
                title=title,
                xaxis_title=viz_config.get("xlabel", ""),
                yaxis_title=viz_config.get("ylabel", ""),
                template="plotly_white",
                font=dict(size=12),
                title_font_size=16,
                title_font_color="#1E40AF",
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=1),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', gridwidth=1),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "pie":
            fig = go.Figure(data=[
                go.Pie(
                    labels=list(data.keys()),
                    values=list(data.values()),
                    marker=dict(line=dict(color='#ffffff', width=2))
                )
            ])
            fig.update_layout(
                title=title,
                template="plotly_white",
                font=dict(size=12),
                title_font_size=16,
                title_font_color="#1E40AF",
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering visualization: {str(e)}")


# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 📋 **Example Questions**")
    st.caption("Click any question below to try it")
    
    example_questions = [
        "What was the overall survival rate?",
        "Show me a histogram of passenger ages",
        "What was the average ticket fare?",
        "Compare survival rates by gender",
        "How many passengers were in each class?",
        "Show me the distribution of embarkation ports",
        "What percentage of passengers were male?",
        "Who paid the most expensive ticket?",
        "Give me a dataset overview",
        "What was the average age of survivors vs non-survivors?",
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(question, key=f"example_{i}"):
            st.session_state.selected_question = question
    
    st.divider()
    
    # About section
    st.markdown("### ℹ️ **About**")
    st.markdown("""
    **Technology Stack:**
    - FastAPI (Backend)
    - LangChain (AI Processing)
    - Streamlit (Interface)
    - Groq (FREE AI Engine)
    
    **Features:**
    - Professional formatting
    - Accurate statistics
    - Interactive visualizations
    - Natural language queries
    """)
    
    st.divider()
    
    # Dataset info
    try:
        response = requests.get(f"{API_URL}/dataset/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            st.markdown("### 📊 **Dataset Info**")
            st.metric("Total Passengers", info["total_passengers"])
            st.metric("Features", len(info['columns']))
            
            with st.expander("📋 View all columns"):
                st.write(", ".join(info['columns']))
    except Exception as e:
        st.warning("⚠️ Backend not connected")
    
    st.divider()
    
    # Clear chat button
    if st.session_state.get("messages", []):
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.rerun()


# ========== MAIN CONTENT ==========

# Centered Title
st.markdown('<h1 class="main-title">🚢 Titanic Dataset Chat Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Professional AI-powered analysis of Titanic passenger data</p>', unsafe_allow_html=True)

st.divider()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" in st.session_state:
    user_input = st.session_state.selected_question
    del st.session_state.selected_question
else:
    user_input = None

# Show welcome message and metrics if no messages yet
if not st.session_state.messages:
    st.info("👋 **Welcome!** Ask me anything about the Titanic dataset. Click a question from the sidebar or type your own below.", icon="💡")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metric cards in 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Passengers",
            value="891",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Number of Features",
            value="12",
            delta=None
        )
    
    with col3:
        st.metric(
            label="AI Engine",
            value="Groq",
            delta="FREE"
        )
    
    with col4:
        st.metric(
            label="Analysis Type",
            value="Statistical",
            delta="Professional"
        )
    
    st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("visualization"):
            render_visualization(message["visualization"])

# Chat input
if prompt := (user_input or st.chat_input("💬 Ask a question about the Titanic dataset...")):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing Titanic dataset..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    visualization = data.get("visualization")
                    
                    st.markdown(answer)
                    
                    if visualization:
                        render_visualization(visualization)
                    
                    # Save to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "visualization": visualization
                    })
                else:
                    error_msg = f"⚠️ Error: Server returned status {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            
            except requests.exceptions.ConnectionError:
                error_msg = "❌ **Connection Error:** Unable to reach the backend API. Please ensure the backend server is running on port 8000."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except requests.exceptions.Timeout:
                error_msg = "⏱️ **Timeout Error:** The request took too long. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except Exception as e:
                error_msg = f"❌ **Unexpected Error:** {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div class="footer">Built with ❤️ using <b>FastAPI</b> + <b>LangChain</b> + <b>Streamlit</b> | Powered by Groq AI</div>',
    unsafe_allow_html=True
)
