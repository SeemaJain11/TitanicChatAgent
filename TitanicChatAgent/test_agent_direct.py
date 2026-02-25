"""Direct test of the agent to debug empty responses"""
import pandas as pd
import os
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

# Load dataset
df = pd.read_csv("data/titanic.csv")
print(f"✅ Loaded dataset: {len(df)} passengers")

# Initialize Groq LLM
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        temperature=0,
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    print("✅ Using Groq LLM")
    
    # Create simple agent
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type="zero-shot-react-description",
        allow_dangerous_code=True,
        handle_parsing_errors=True,
        max_iterations=3,
        early_stopping_method="generate"
    )
    
    print("\n" + "="*60)
    print("Testing Agent")
    print("="*60 + "\n")
    
    # Test query
    question = "Compare survival rates by gender"
    print(f"Question: {question}\n")
    
    try:
        response = agent.invoke(question)
        print(f"\nResponse type: {type(response)}")
        print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
        print(f"\nFull response: {response}")
        
        if isinstance(response, dict):
            output = response.get("output", "NO OUTPUT KEY")
            print(f"\nOutput: {output}")
    except Exception as error:
        print(f"\n❌ AGENT ERROR: {type(error).__name__}")
        print(f"Error message: {str(error)[:1000]}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
