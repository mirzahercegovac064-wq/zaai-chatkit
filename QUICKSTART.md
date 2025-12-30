# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your Credentials

1. **OpenAI API Key**: 
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy it (you'll need it in Step 2)

2. **ChatKit Workflow ID**:
   - Go to https://platform.openai.com/agent-builder
   - Create a new agent workflow
   - Copy the workflow ID (starts with `wf_`)

### Step 2: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials:
# OPENAI_API_KEY=sk-your-key-here
# CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here
```

### Step 3: Start Backend (Terminal 1)

```bash
./start-backend.sh
```

Or manually:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export $(cat ../.env | xargs)
python server.py
```

Backend will run on: http://localhost:8000

### Step 4: Start Frontend (Terminal 2)

```bash
./start-frontend.sh
```

Or manually:
```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:3000

### Step 5: Open Your Browser

Visit http://localhost:3000

You should see the ZAAI website with a chat widget in the bottom-right corner! 🎉

## Troubleshooting

**Backend won't start?**
- Make sure `.env` file exists and has both `OPENAI_API_KEY` and `CHATKIT_WORKFLOW_ID`
- Check that Python 3.8+ is installed: `python3 --version`

**Frontend won't start?**
- Make sure Node.js 18+ is installed: `node --version`
- Try deleting `node_modules` and running `npm install` again

**Chat widget not showing?**
- Open browser console (F12) and check for errors
- Make sure backend is running on port 8000
- Verify the ChatKit script is loaded (check Network tab)

**Session creation fails?**
- Double-check your API key is correct
- Verify your workflow ID is correct (should start with `wf_`)
- Check backend terminal for error messages

## Next Steps

- Customize the styling in `frontend/src/components/ChatWidget.css`
- Modify the website content in `frontend/src/App.jsx`
- Add authentication or other features to the backend in `backend/server.py`

