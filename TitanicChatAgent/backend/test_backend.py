"""
Simple test script to verify the backend is working correctly
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        import pandas as pd
        import langchain
        import openai
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_dataset():
    """Test that the dataset loads correctly"""
    print("\nTesting dataset...")
    try:
        import pandas as pd
        df = pd.read_csv("../data/titanic.csv")
        print(f"✅ Dataset loaded: {len(df)} passengers")
        print(f"✅ Columns: {df.columns.tolist()[:5]}...")
        return True
    except Exception as e:
        print(f"❌ Dataset load failed: {e}")
        return False

def test_api_key():
    """Test that OpenAI API key is configured"""
    print("\nTesting API key configuration...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print(f"✅ API key configured (length: {len(api_key)})")
        return True
    else:
        print("❌ API key not configured")
        print("   Set OPENAI_API_KEY in .env file")
        return False

def test_backend_server():
    """Test that the backend can start"""
    print("\nTesting backend server...")
    try:
        from main import app
        print("✅ FastAPI app imports successfully")
        return True
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False

def main():
    print("=" * 50)
    print("Titanic Chat Agent - Backend Tests")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Dataset", test_dataset()))
    results.append(("API Key", test_api_key()))
    results.append(("Backend", test_backend_server()))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Backend is ready.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY in .env file")
        print("2. Run: uvicorn main:app --reload")
        print("3. Test at: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
