# 🚢 TITANIC CHAT AGENT - QUICK START GUIDE

## Step 1: Setup Environment

1. Copy the environment template:

```bash
copy .env.example .env
```

2. Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
API_URL=http://localhost:8000
```

Get your API key from: https://platform.openai.com/api-keys

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Run the Application

### Option A: Automatic Start (Windows)

```bash
powershell -ExecutionPolicy Bypass -File start.ps1
```

### Option B: Manual Start

**Terminal 1 - Backend:**

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```bash
cd frontend
streamlit run app.py
```

## Step 4: Use the Chatbot!

Open your browser at: http://localhost:8501

Try these questions:

- "What percentage of passengers were male on the Titanic?"
- "Show me a histogram of passenger ages"
- "What was the average ticket fare?"
- "How many passengers embarked from each port?"

## Troubleshooting

### "Module not found" error

```bash
pip install -r requirements.txt
```

### "Unable to connect to API"

Make sure the backend is running on port 8000 first.

### "OpenAI API error"

Check that your OPENAI_API_KEY in .env is correct and has credits.

## Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to: https://share.streamlit.io
3. Click "New app"
4. Select your repository
5. Set main file: `frontend/app.py`
6. Add secrets in settings:
   - OPENAI_API_KEY
   - API_URL (your deployed backend URL)
7. Click "Deploy"!

For detailed instructions, see README.md

---

Need help? Check the full README.md for more details!
