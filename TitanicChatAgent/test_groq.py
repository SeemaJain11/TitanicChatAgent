"""Quick test to verify Groq API key works"""
import os
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key or groq_key == "your-groq-api-key-here":
    print("❌ No Groq API key found!")
    print("\n📝 To get a FREE Groq API key:")
    print("   1. Go to https://console.groq.com")
    print("   2. Sign up (free, no credit card)")
    print("   3. Create API key")
    print("   4. Add to .env file:")
    print("      GROQ_API_KEY=gsk_your_key_here")
    exit(1)

print(f"✅ API Key loaded: {groq_key[:20]}...")

try:
    from langchain_groq import ChatGroq
    
    llm = ChatGroq(
        temperature=0,
        model="llama-3.3-70b-versatile",
        groq_api_key=groq_key
    )
    
    print("🔄 Testing Groq connection...")
    response = llm.invoke("Say 'hello' in one word")
    print(f"\n✅ Groq Connection Successful!")
    print(f"Response: {response.content}")
    print(f"\n🎉 Your chatbot is ready to use!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
