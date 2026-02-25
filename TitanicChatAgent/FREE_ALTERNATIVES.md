# 🆓 FREE API ALTERNATIVES

## ✅ Option 1: Groq (RECOMMENDED - FREE & FAST)

### Why Groq?

- **100% FREE** - No credit card required
- **Very FAST** - 10x faster than OpenAI
- **Easy setup** - Takes 2 minutes
- Uses powerful Llama models

### Setup Steps:

1. **Get FREE API Key:**
   - Go to: https://console.groq.com
   - Sign up with Google/GitHub (free, no card needed)
   - Go to "API Keys" section
   - Click "Create API Key"
   - Copy the key (starts with `gsk_...`)

2. **Update .env file:**

   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

3. **Restart backend:**
   ```powershell
   cd backend
   & "C:/Users/RAHUL JAIN/TitanicChatAgent/.venv/Scripts/python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

That's it! ✨

---

## Option 2: Anthropic Claude (FREE Tier)

Get $5 free credits:

1. Sign up at: https://console.anthropic.com
2. Get API key
3. Install: `pip install langchain-anthropic`
4. Update backend to use `ChatAnthropic`

---

## Option 3: Ollama (FREE Local AI)

Run AI models on your computer (no API needed):

1. **Download Ollama:** https://ollama.com/download
2. **Install model:**
   ```
   ollama pull llama3.2
   ```
3. **Install package:**
   ```
   pip install langchain-community
   ```
4. **Update backend** to use `ChatOllama`

**Pros:** Completely free, private, no internet needed
**Cons:** Slower, requires good computer

---

## Option 4: No LLM (Simple Mode)

Use direct pandas queries without AI:

- Faster responses
- No API needed
- Limited to predefined questions
- See `backend_simple.py` for implementation

---

## Comparison:

| Option    | Cost      | Speed  | Setup  | Quality   |
| --------- | --------- | ------ | ------ | --------- |
| **Groq**  | FREE      | ⚡⚡⚡ | Easy   | Excellent |
| OpenAI    | $$        | ⚡⚡   | Easy   | Excellent |
| Anthropic | FREE tier | ⚡⚡   | Easy   | Excellent |
| Ollama    | FREE      | ⚡     | Medium | Good      |
| No LLM    | FREE      | ⚡⚡⚡ | Easy   | Basic     |

**Recommendation:** Use Groq! It's free, fast, and works great.
