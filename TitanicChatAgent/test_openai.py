"""Quick test to verify OpenAI API key works"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found!")

try:
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=api_key
    )
    
    response = llm.invoke("Say 'hello' in one word")
    print(f"\n✅ OpenAI Connection Successful!")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
