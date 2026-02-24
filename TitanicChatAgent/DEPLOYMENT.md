# 🚀 DEPLOYMENT GUIDE - Titanic Chat Agent

This guide walks you through deploying your Titanic Chat Agent to the cloud.

## Overview

We'll deploy:

1. **Backend** (FastAPI) → Render or Railway
2. **Frontend** (Streamlit) → Streamlit Cloud

## Prerequisites

- [x] GitHub account
- [x] OpenAI API key
- [x] Code pushed to GitHub repository

---

## Part 1: Deploy Backend (FastAPI)

### Option A: Deploy to Render (Recommended)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repo containing your code

3. **Configure Service**

   ```
   Name: titanic-chat-backend
   Environment: Python 3
   Region: Oregon (US West) or closest to you
   Branch: main
   Root Directory: backend
   Build Command: pip install -r ../requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   - Click "Environment"
   - Add: `OPENAI_API_KEY` = `your-api-key-here`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Copy your service URL (e.g., `https://titanic-chat-backend.onrender.com`)

6. **Test Backend**
   ```bash
   curl https://your-backend-url.onrender.com/
   # Should return: {"message":"Titanic Chat Agent API is running"}
   ```

### Option B: Deploy to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `OPENAI_API_KEY`
   - Wait for deployment

4. **Get URL**
   - Click "Settings" → "Generate Domain"
   - Copy your domain (e.g., `https://titanic-chat-backend.up.railway.app`)

---

## Part 2: Deploy Frontend (Streamlit Cloud)

1. **Prepare Repository**

   Ensure your repository has:
   - ✅ `requirements.txt` in root
   - ✅ `frontend/app.py`
   - ✅ Code pushed to GitHub

2. **Create Streamlit Account**
   - Go to https://share.streamlit.io
   - Sign in with GitHub

3. **Deploy New App**
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `frontend/app.py`

4. **Configure Secrets**

   Click "Advanced settings" → "Secrets"

   Add this configuration:

   ```toml
   OPENAI_API_KEY = "sk-your-openai-key-here"
   API_URL = "https://your-backend-url.onrender.com"
   ```

   Replace with your actual:
   - OpenAI API key
   - Backend URL from Part 1

5. **Deploy**
   - Click "Deploy!"
   - Wait 3-5 minutes for first deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

6. **Test Your App**
   - Open the Streamlit URL
   - Try example questions
   - Verify visualizations work
   - Check API connection in sidebar

---

## Part 3: Custom Domain (Optional)

### For Streamlit App

1. Go to your app settings on Streamlit Cloud
2. Click "Custom domain"
3. Follow instructions to add DNS records
4. Wait for SSL certificate provisioning

### For Backend

1. In Render/Railway, go to Settings
2. Add custom domain
3. Update DNS records as instructed
4. Update `API_URL` in Streamlit secrets

---

## Environment Variables Summary

### Backend (Render/Railway)

```
OPENAI_API_KEY=sk-your-key-here
```

### Frontend (Streamlit Cloud)

```toml
OPENAI_API_KEY = "sk-your-key-here"
API_URL = "https://your-backend.onrender.com"
```

---

## Testing Your Deployment

### 1. Test Backend Directly

```bash
# Test health endpoint
curl https://your-backend-url.com/

# Test dataset info
curl https://your-backend-url.com/dataset/info

# Test query endpoint
curl -X POST https://your-backend-url.com/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What percentage of passengers were male?"}'
```

### 2. Test Frontend

1. Open your Streamlit URL
2. Check sidebar for API connection status
3. Try example questions:
   - "What percentage of passengers were male?"
   - "Show me a histogram of passenger ages"
   - "What was the average ticket fare?"
4. Verify visualizations display correctly

---

## Troubleshooting Deployment

### Backend Issues

**"Application failed to respond"**

- Check logs in Render/Railway dashboard
- Verify `OPENAI_API_KEY` is set
- Ensure `requirements.txt` includes all dependencies
- Check start command is correct

**"OpenAI API Error"**

- Verify API key is valid
- Check OpenAI account has credits
- Ensure no extra spaces in environment variable

### Frontend Issues

**"Unable to connect to API"**

- Verify `API_URL` in Streamlit secrets
- Check backend is running and accessible
- Test backend URL directly in browser
- Ensure backend allows CORS

**"ModuleNotFoundError"**

- Verify `requirements.txt` is in repository root
- Check all dependencies are listed
- Try redeploying the app

**"Secrets not found"**

- Ensure secrets are added in Streamlit Cloud settings
- Check secret key names match code exactly
- Secrets are case-sensitive!

### General Issues

**"App is slow"**

- Backend and frontend should be in same region
- Consider upgrading to paid tier for better performance
- Add caching with `@st.cache_data`

**"Rate limit exceeded"**

- Implement rate limiting in backend
- Monitor OpenAI API usage
- Consider adding user authentication

---

## Monitoring & Maintenance

### Check Logs

**Render:**

- Go to service dashboard
- Click "Logs" tab
- Real-time log streaming

**Railway:**

- Click on service
- View "Deployments" → "Logs"

**Streamlit:**

- App dashboard → "Logs"
- Shows runtime errors and warnings

### Update Deployment

**Backend:**

1. Push changes to GitHub
2. Render/Railway auto-deploys from main branch
3. Wait 2-3 minutes for build

**Frontend:**

1. Push changes to GitHub
2. Streamlit Cloud auto-deploys
3. Click "Reboot app" if needed

---

## Cost Estimate

### Free Tier (Perfect for Assignment)

| Service         | Free Tier       | Limitations                 |
| --------------- | --------------- | --------------------------- |
| Render          | 750 hours/month | Spins down after inactivity |
| Railway         | $5 free credits | Limited hours               |
| Streamlit Cloud | Unlimited       | Public apps only            |
| OpenAI          | $5-18 credit    | New accounts                |

**Total Cost: $0** (using free tiers)

### Paid Tier (Production)

| Service         | Cost/Month                |
| --------------- | ------------------------- |
| Render Starter  | $7                        |
| Railway Pro     | $5-20                     |
| Streamlit Cloud | $0 (stay on Community)    |
| OpenAI API      | ~$5-10 (depends on usage) |

**Total: ~$12-30/month**

---

## Security Best Practices

1. **Never commit secrets**

   ```bash
   # Ensure .gitignore includes:
   .env
   .streamlit/secrets.toml
   ```

2. **Rotate API keys regularly**
   - Generate new OpenAI keys monthly
   - Update in all deployment platforms

3. **Monitor API usage**
   - Set up usage alerts in OpenAI dashboard
   - Set spending limits

4. **Enable HTTPS only**
   - Both Render and Streamlit provide free SSL
   - Never use HTTP in production

5. **Add rate limiting**

   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)

   @app.post("/query")
   @limiter.limit("10/minute")
   async def query_dataset(request: QueryRequest):
       ...
   ```

---

## Sharing Your Deployment

Once deployed, share:

1. **Streamlit URL** (your live app)

   ```
   https://your-app-name.streamlit.app
   ```

2. **GitHub Repository**

   ```
   https://github.com/your-username/TitanicChatAgent
   ```

3. **Demo Video** (optional)
   - Record a quick demo using the app
   - Upload to YouTube or Loom

---

## Submission Checklist

For your assignment submission:

- [ ] Backend deployed and accessible
- [ ] Frontend deployed on Streamlit Cloud
- [ ] All example questions work correctly
- [ ] Visualizations display properly
- [ ] No errors in logs
- [ ] README.md is complete
- [ ] GitHub repository is public (or shared with evaluator)
- [ ] Streamlit URL is accessible without authentication

---

## Example Submission Format

```
Titanic Chat Agent Submission
================================

🚀 Live Demo: https://titanic-chat-agent.streamlit.app

📦 GitHub Repository: https://github.com/yourusername/TitanicChatAgent

🛠️ Tech Stack:
- Backend: FastAPI (deployed on Render)
- Frontend: Streamlit (deployed on Streamlit Cloud)
- AI: LangChain + OpenAI GPT-3.5
- Visualizations: Plotly

✅ Features Implemented:
- Natural language query processing
- Automatic visualization generation
- Interactive chat interface
- Multiple chart types (histogram, bar, pie)
- Dataset statistics in sidebar

📝 Notes:
- All example questions work as expected
- Backend API documentation: https://your-backend.onrender.com/docs
- Dataset contains 891 Titanic passengers
```

---

## Need Help?

Common resources:

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- LangChain Docs: https://python.langchain.com

Good luck with your deployment! 🚀
