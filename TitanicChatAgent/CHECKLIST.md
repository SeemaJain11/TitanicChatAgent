# ✅ SETUP CHECKLIST

Use this checklist to ensure everything is configured correctly.

## Pre-Launch Checklist

### 1. Environment Setup

- [ ] Python 3.8+ installed
- [ ] OpenAI account created
- [ ] OpenAI API key obtained
- [ ] `.env` file created from `.env.example`
- [ ] `OPENAI_API_KEY` added to `.env`

### 2. Dependencies

- [ ] Run `pip install -r requirements.txt`
- [ ] No import errors when running `python backend/test_backend.py`
- [ ] Dataset file exists at `data/titanic.csv`
- [ ] Dataset has 891 passengers

### 3. Local Testing

- [ ] Backend starts successfully on port 8000
- [ ] Frontend starts successfully on port 8501
- [ ] Can access frontend in browser
- [ ] API connection shown in sidebar
- [ ] Example questions work
- [ ] Visualizations display correctly
- [ ] No console errors

### 4. Deployment Preparation

- [ ] Code committed to Git
- [ ] Pushed to GitHub
- [ ] `.env` not committed (in `.gitignore`)
- [ ] README.md is complete
- [ ] All tests pass

### 5. Backend Deployment (Render)

- [ ] Render account created
- [ ] Repository connected
- [ ] Build command configured
- [ ] Start command configured
- [ ] Environment variable `OPENAI_API_KEY` added
- [ ] Deployment successful
- [ ] Backend URL accessible
- [ ] API returns 200 status

### 6. Frontend Deployment (Streamlit Cloud)

- [ ] Streamlit Cloud account created
- [ ] Repository connected
- [ ] Main file path set to `frontend/app.py`
- [ ] Secrets added (OPENAI_API_KEY, API_URL)
- [ ] Deployment successful
- [ ] App loads without errors
- [ ] API connection successful

### 7. Final Testing

- [ ] Test all example questions on deployed app
- [ ] Verify visualizations work
- [ ] Check error handling
- [ ] Test on mobile device (optional)
- [ ] Share URL with friend to test

### 8. Submission

- [ ] Streamlit Cloud URL copied
- [ ] GitHub repository URL (if sharing)
- [ ] Submission format prepared
- [ ] Ready to submit!

---

## Quick Commands Reference

### Local Development

```bash
# Start backend
cd backend
python -m uvicorn main:app --reload

# Start frontend (new terminal)
cd frontend
streamlit run app.py
```

### Testing

```bash
# Test imports and setup
cd backend
python test_backend.py

# Test dataset
python -c "import pandas as pd; print(pd.read_csv('../data/titanic.csv').shape)"
```

### Deployment Commands

```bash
# Git commands
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main

# Test backend URL
curl https://your-backend.onrender.com/

# Test API endpoint
curl https://your-backend.onrender.com/dataset/info
```

---

## Troubleshooting Checklist

### If Backend Won't Start

- [ ] Check Python version: `python --version`
- [ ] Reinstall dependencies: `pip install -r requirements.txt`
- [ ] Verify dataset exists: `dir data\titanic.csv`
- [ ] Check environment variable: `echo $env:OPENAI_API_KEY`
- [ ] Look for error in terminal output

### If Frontend Won't Connect to Backend

- [ ] Backend is running on port 8000
- [ ] Check API_URL in .env or environment
- [ ] Try http://localhost:8000 in browser
- [ ] Check for firewall blocking port 8000
- [ ] Verify CORS is enabled (should be by default)

### If Deployed App Not Working

- [ ] Check backend logs in Render dashboard
- [ ] Check frontend logs in Streamlit dashboard
- [ ] Verify environment variables are set
- [ ] Test backend URL directly in browser
- [ ] Ensure API key has credits

### If Questions Don't Work

- [ ] Verify OpenAI API key is valid
- [ ] Check OpenAI account has available credits
- [ ] Look for error messages in terminal/logs
- [ ] Try simpler questions first
- [ ] Check dataset is loaded correctly

---

## Success Criteria

Your app is ready for submission when:

✅ **Functionality**

- All example questions return answers
- Visualizations display correctly
- No error messages in UI
- Chat history works

✅ **Deployment**

- App accessible via public URL
- No authentication required to view
- Backend responding to requests
- API connection stable

✅ **Quality**

- Clean, professional UI
- Fast response times (< 30 seconds)
- Error handling works
- Documentation is complete

✅ **Requirements Met**

- Python + FastAPI backend ✅
- LangChain agent ✅
- Streamlit frontend ✅
- Natural language queries ✅
- Text responses ✅
- Visualizations ✅
- Working demo URL ✅

---

## Final Pre-Submission Check

Before submitting, test these specific questions on your deployed app:

1. [ ] "What percentage of passengers were male on the Titanic?"
   - Should return approximately 64-65%
2. [ ] "Show me a histogram of passenger ages"
   - Should display a histogram chart
3. [ ] "What was the average ticket fare?"
   - Should return a number (around 32-33)
4. [ ] "How many passengers embarked from each port?"
   - Should show counts for each port
   - May include a bar chart

5. [ ] "What was the survival rate?"
   - Should return percentage (around 38%)
   - May show a pie chart

If all 5 questions work correctly, you're ready to submit! 🎉

---

## Time Estimates

- **Local Setup**: 15-30 minutes
- **Local Testing**: 10-15 minutes
- **Backend Deployment**: 10-15 minutes
- **Frontend Deployment**: 5-10 minutes
- **Final Testing**: 10-15 minutes

**Total**: 50-85 minutes (first time)

---

**Last Updated**: Use this checklist every time you deploy or make changes!
