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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #DBEAFE;
    }
    .bot-message {
        background-color: #F3F4F6;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Title and description
st.markdown('<h1 class="main-header">🚢 Titanic Dataset Chat Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask me anything about the Titanic passengers!</p>', unsafe_allow_html=True)

# Sidebar with example questions
with st.sidebar:
    st.header("📋 Example Questions")
    
    example_questions = [
        "What percentage of passengers were male on the Titanic?",
        "Show me a histogram of passenger ages",
        "What was the average ticket fare?",
        "How many passengers embarked from each port?",
        "What was the survival rate?",
        "Show me the distribution of passenger classes",
        "How many children were on board?",
        "What was the most expensive ticket?",
    ]
    
    for question in example_questions:
        if st.button(question, key=question):
            st.session_state.selected_question = question
    
    st.divider()
    st.header("ℹ️ About")
    st.write("""
    This chatbot uses:
    - **FastAPI** for the backend
    - **LangChain** for intelligent query processing
    - **Streamlit** for the interface
    - **OpenAI GPT** for natural language understanding
    """)
    
    # Dataset info
    try:
        response = requests.get(f"{API_URL}/dataset/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            st.divider()
            st.header("📊 Dataset Info")
            st.metric("Total Passengers", info["total_passengers"])
            st.write(f"**Columns:** {', '.join(info['columns'][:5])}...")
    except:
        st.warning("Unable to connect to API")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" in st.session_state:
    user_input = st.session_state.selected_question
    del st.session_state.selected_question
else:
    user_input = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("visualization"):
            render_visualization(message["visualization"])

# Chat input
if prompt := (user_input or st.chat_input("Ask a question about the Titanic dataset...")):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
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
                    
                    st.write(answer)
                    
                    if visualization:
                        render_visualization(visualization)
                    
                    # Save to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "visualization": visualization
                    })
                else:
                    error_msg = f"Error: {response.status_code}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
            
            except requests.exceptions.ConnectionError:
                error_msg = "❌ Unable to connect to the API. Make sure the backend is running on port 8000."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })


def render_visualization(viz_config):
    """Render visualization based on configuration"""
    if not viz_config:
        return
    
    viz_type = viz_config.get("type")
    data = viz_config.get("data")
    title = viz_config.get("title", "")
    
    if viz_type == "histogram":
        fig = px.histogram(
            x=data,
            nbins=30,
            title=title,
            labels={"x": viz_config.get("xlabel", ""), "y": viz_config.get("ylabel", "")}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "bar":
        fig = go.Figure(data=[
            go.Bar(
                x=list(data.keys()),
                y=list(data.values()),
                marker_color='steelblue'
            )
        ])
        fig.update_layout(
            title=title,
            xaxis_title=viz_config.get("xlabel", ""),
            yaxis_title=viz_config.get("ylabel", "")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "pie":
        fig = go.Figure(data=[
            go.Pie(
                labels=list(data.keys()),
                values=list(data.values())
            )
        ])
        fig.update_layout(title=title)
        st.plotly_chart(fig, use_container_width=True)


# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
