from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
import os
import json
from typing import Optional
from dotenv import load_dotenv

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

# Initialize LangChain agent
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    agent_type="openai-tools",
    allow_dangerous_code=True
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
        question = request.question.lower()
        
        # Check if the user is asking for a visualization
        viz_keywords = ["histogram", "chart", "graph", "plot", "show me", "visualize", "distribution"]
        needs_viz = any(keyword in question for keyword in viz_keywords)
        
        # Get the answer from the agent
        response = agent.invoke(question)
        answer = response.get("output", str(response))
        
        # Prepare visualization data if needed
        visualization = None
        if needs_viz:
            visualization = generate_visualization_config(question, df)
        
        return QueryResponse(answer=answer, visualization=visualization)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
