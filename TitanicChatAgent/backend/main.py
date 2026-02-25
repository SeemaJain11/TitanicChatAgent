from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
import os
import json
import asyncio
from typing import Optional
from dotenv import load_dotenv
from functools import partial

try:
    from groq import RateLimitError as GroqRateLimitError
except ImportError:
    GroqRateLimitError = None

# Load environment variables
load_dotenv()

app = FastAPI(title="Titanic Chat Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Titanic dataset
# Get the correct path whether running from backend/ or root directory
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "titanic.csv")
if not os.path.exists(csv_path):
    csv_path = "data/titanic.csv"
df = pd.read_csv(csv_path)

# Professional System Prompt for Titanic Analysis
SYSTEM_PROMPT = """You are a professional Titanic Dataset Analysis Assistant built using Pandas.

Your job is to answer user questions about the Titanic dataset clearly and accurately.

**CRITICAL RULES:**
- ONLY answer questions related to the Titanic dataset.
- If the question is unrelated to Titanic, respond EXACTLY: "I can only answer questions related to the Titanic dataset."
- NEVER show system messages, technical errors, or internal configuration.
- NEVER expose parsing errors or technical flags like 'handle_parsing_errors'.
- Do not generate unrelated information under any circumstances.

**FORMATTING RULES:**
- Format percentages to 2 decimal places (example: 64.76%).
- Format currency with $ symbol and 2 decimal places (example: $32.20).
- Use clear bold headings in responses (use **text** for bold).
- Use small relevant emojis when appropriate (📊 🚢 💰 👥 ⚓).
- Keep answers concise and professional.
- Use bullet points when showing multiple statistics.

**DATA ANALYSIS RULES:**
- Always provide exact numbers from the dataset.
- Calculate percentages accurately.
- Round decimal numbers appropriately.
- Explain your findings clearly.

**DATASET OVERVIEW:**
If user asks for dataset overview, summary, or general statistics, provide:
- Total number of passengers
- Survival rate percentage  
- Average age
- Average ticket fare

**SURVIVAL ANALYSIS:**
If user asks about survival comparison by gender or class:
- Calculate survival percentage grouped by the requested category.
- Clearly explain the result in 2-3 lines.

**NATURAL LANGUAGE:**
Understand different variations of similar questions:
- "Male percentage?" / "How many men?" / "Gender distribution?" → All refer to Sex column analysis.
- "Survival rate?" / "How many survived?" → Analyze Survived column.
- "Ticket price?" / "Fare?" / "Cost?" → Analyze Fare column.

Always behave like a professional data analyst.
Keep responses structured, clean, and readable.

You have access to the Titanic dataset with these columns: {columns}
"""

# Initialize LangChain agent
# Option 2: Use Groq (FREE!) - Get API key from https://console.groq.com
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        temperature=0,
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    print("✅ Using Groq LLM (FREE)")
    agent_type = "zero-shot-react-description"  # Compatible with Groq
except ImportError:
    # Fallback to OpenAI if Groq not installed
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    print("⚠️ Using OpenAI (may have quota issues)")
    agent_type = "openai-tools"

# Create agent with professional system prompt
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    agent_type=agent_type,
    allow_dangerous_code=True,
    prefix=SYSTEM_PROMPT.format(columns=", ".join(df.columns.tolist())),
    max_iterations=3,  # Reduced for faster responses
    early_stopping_method="generate"
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    visualization: Optional[dict] = None


@app.get("/")
async def root():
    return {"message": "Titanic Chat Agent API is running"}


@app.get("/dataset/info")
async def get_dataset_info():
    """Get basic information about the dataset"""
    return {
        "total_passengers": len(df),
        "columns": df.columns.tolist(),
        "shape": df.shape,
        "sample": df.head().fillna("null").to_dict(orient="records")
    }


@app.post("/query", response_model=QueryResponse)
async def query_dataset(request: QueryRequest):
    """
    Process natural language queries about the Titanic dataset
    """
    try:
        question = request.question.strip()
        question_lower = question.lower()
        
        # Comprehensive list of unrelated topics
        unrelated_keywords = [
            "weather", "news", "joke", "recipe", "movie", "song", "game", "sports", 
            "politics", "celebrity", "stock", "crypto", "bitcoin", "programming",
            "hello", "hi", "who are you", "what is your name", "how are you",
            "president", "country", "capital", "football", "basketball", 
            "restaurant", "food", "travel", "hotel", "car", "phone", "computer"
        ]
        
        # Check if question is about Titanic dataset
        titanic_keywords = ["titanic", "passenger", "survival", "survived", "age", "fare", "class", "embarked", "sex", "male", "female", "dataset"]
        is_titanic_related = any(keyword in question_lower for keyword in titanic_keywords)
        
        # If unrelated keywords found and no Titanic keywords, reject
        if any(keyword in question_lower for keyword in unrelated_keywords) and not is_titanic_related:
            return QueryResponse(
                answer="I can only answer questions related to the Titanic dataset.",
                visualization=None
            )
        
        # Additional check for very short or generic questions
        if len(question.split()) <= 2 and not is_titanic_related:
            return QueryResponse(
                answer="I can only answer questions related to the Titanic dataset.",
                visualization=None
            )
        
        # Check if the user is asking for a visualization
        viz_keywords = ["histogram", "chart", "graph", "plot", "show me", "visualize", "distribution", "bar chart"]
        needs_viz = any(keyword in question_lower for keyword in viz_keywords)
        
        # Get the answer from the agent with enhanced prompt
        enhanced_question = f"{question}\n\nRemember to format numbers properly: percentages with %, currency with $, and use emojis appropriately."
        
        try:
            # Call agent with timeout protection via concurrent.futures
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(agent.invoke, enhanced_question)
                try:
                    response = future.result(timeout=30)  # 30 second timeout
                    # Handle different response formats
                    if isinstance(response, dict):
                        answer = response.get("output", response.get("result", str(response)))
                    else:
                        answer = str(response)
                    
                    # Check if answer is empty
                    if not answer or answer.strip() == "":
                        answer = "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                except concurrent.futures.TimeoutError:
                    return QueryResponse(
                        answer="⏱️ The query is taking too long. Please try asking a simpler question about the Titanic dataset.",
                        visualization=None
                    )
        except Exception as agent_error:
            # Check for Groq rate limit error
            if GroqRateLimitError and isinstance(agent_error, GroqRateLimitError):
                return QueryResponse(
                    answer="⚠️ **Daily Groq API limit reached!**\n\nThe free tier allows 100,000 tokens/day. You've used today's quota.\n\n**Options:**\n• Wait ~10 minutes for daily reset\n• Upgrade at https://console.groq.com/settings/billing",
                    visualization=None
                )
            
            # Also check by error message
            error_str = str(agent_error)
            if "rate_limit" in error_str.lower() or "rate limit" in error_str.lower():
                return QueryResponse(
                    answer="⚠️ **API Rate Limit Reached**\n\nYou've exceeded your daily API usage limit.\n\nPlease wait for the reset or check your API provider's dashboard.",
                    visualization=None
                )
            
            if "Could not parse LLM output:" in error_str:
                # Extract the actual output between backticks
                import re
                match = re.search(r'`([^`]+)`', error_str)
                if match:
                    answer = match.group(1).strip()
                else:
                    # Return user-friendly message instead of technical error
                    return QueryResponse(
                        answer="I apologize, but I'm having trouble processing that question. Please try rephrasing it or ask about specific Titanic dataset statistics.",
                        visualization=None
                    )
            else:
                # Return user-friendly message for any other error
                return QueryResponse(
                    answer="I apologize, but I encountered an issue processing your question. Please try asking about Titanic passenger statistics, survival rates, or demographics.",
                    visualization=None
                )
        
        # Clean up the answer and remove any technical artifacts
        answer = answer.strip()
        
        # Remove technical phrases that might leak through
        technical_phrases = [
            "handle_parsing_errors=True",
            "agent_type=",
            "AgentExecutor",
            "LLM output",
            "parsing error",
            "For troubleshooting"
        ]
        for phrase in technical_phrases:
            if phrase in answer:
                answer = answer.replace(phrase, "")
        
        # If answer contains technical jargon, provide generic response
        if any(word in answer.lower() for word in ["traceback", "error:", "exception", "failed to"]):
            answer = "I can only answer questions related to the Titanic dataset."
        
        # Prepare visualization data if needed
        visualization = None
        if needs_viz:
            visualization = generate_visualization_config(question_lower, df)
        
        return QueryResponse(answer=answer, visualization=visualization)
    
    except Exception as e:
        # Check if it's a Groq API rate limit error
        if GroqRateLimitError and isinstance(e, GroqRateLimitError):
            return QueryResponse(
                answer="⚠️ **Daily Groq API limit reached!**\n\nFree tier: 100,000 tokens/day\n\n**Options:**\n• Wait for daily reset\n• Upgrade at https://console.groq.com/settings/billing",
                visualization=None
            )
        
        error_message = str(e)
        if "rate_limit" in error_message.lower():
            return QueryResponse(
                answer="⚠️ **API Rate Limit Reached**\n\nDaily usage limit exceeded. Please wait for reset.",
                visualization=None
            )
        
        # Never expose technical errors to users
        return QueryResponse(
            answer="I apologize, but I'm currently unable to process that request. Please try asking a different question about the Titanic dataset.",
            visualization=None
        )


def generate_visualization_config(question: str, df: pd.DataFrame) -> dict:
    """
    Generate visualization configuration based on the question
    """
    question = question.lower()
    
    # Age histogram
    if "age" in question and ("histogram" in question or "distribution" in question):
        return {
            "type": "histogram",
            "data": df["age"].dropna().tolist(),
            "title": "Age Distribution of Titanic Passengers",
            "xlabel": "Age",
            "ylabel": "Count"
        }
    
    # Gender distribution
    if "gender" in question or "sex" in question or "male" in question or "female" in question:
        sex_counts = df["sex"].value_counts().to_dict()
        return {
            "type": "bar",
            "data": sex_counts,
            "title": "Gender Distribution",
            "xlabel": "Gender",
            "ylabel": "Count"
        }
    
    # Survival rate
    if "surviv" in question:
        survival_counts = df["survived"].value_counts().to_dict()
        return {
            "type": "pie",
            "data": {
                "Survived": survival_counts.get(1, 0),
                "Did Not Survive": survival_counts.get(0, 0)
            },
            "title": "Survival Rate"
        }
    
    # Embarkation ports
    if "embark" in question or "port" in question:
        embark_counts = df["embarked"].value_counts().to_dict()
        return {
            "type": "bar",
            "data": embark_counts,
            "title": "Passengers by Embarkation Port",
            "xlabel": "Port",
            "ylabel": "Count"
        }
    
    # Fare distribution
    if "fare" in question and ("histogram" in question or "distribution" in question):
        return {
            "type": "histogram",
            "data": df["fare"].dropna().tolist(),
            "title": "Fare Distribution",
            "xlabel": "Fare",
            "ylabel": "Count"
        }
    
    # Class distribution
    if "class" in question:
        class_counts = df["pclass"].value_counts().sort_index().to_dict()
        return {
            "type": "bar",
            "data": class_counts,
            "title": "Passenger Class Distribution",
            "xlabel": "Class",
            "ylabel": "Count"
        }
    
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
