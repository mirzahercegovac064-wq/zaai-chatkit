# ZAAI ChatKit Integration

A chat widget integration for the ZAAI website using OpenAI's ChatKit. The chat widget is positioned in the bottom-right corner of the page.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- OpenAI API key
- ChatKit Workflow ID (from Agent Builder)

## Setup Instructions

### 1. Get Your Credentials

1. **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Workflow ID**: Create an agent workflow using [Agent Builder](https://platform.openai.com/agent-builder) and copy the workflow ID

### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here
   ```

### 3. Set Up Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Load environment variables and run the server:
   ```bash
   # On macOS/Linux:
   export $(cat ../.env | xargs) && python server.py
   
   # Or use python-dotenv (already in requirements.txt):
   python -c "from dotenv import load_dotenv; load_dotenv('../.env'); import server; import uvicorn; uvicorn.run(server.app, host='0.0.0.0', port=8000)"
   ```

   The backend will run on `http://localhost:8000`

### 4. Set Up Frontend

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:3000`

## Project Structure

```
zaai-chatkit/
├── backend/
│   ├── server.py          # FastAPI server for ChatKit sessions
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWidget.jsx    # Chat widget component
│   │   │   └── ChatWidget.css    # Chat widget styles
│   │   ├── App.jsx               # Main app component
│   │   ├── App.css               # App styles
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Global styles
│   ├── index.html                # HTML template with ChatKit script
│   ├── package.json              # Node dependencies
│   └── vite.config.js            # Vite configuration
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Features

- ✅ Chat widget positioned in bottom-right corner
- ✅ Responsive design for mobile and desktop
- ✅ Session management via backend API
- ✅ Customizable styling
- ✅ Easy integration with existing websites

## Customization

### Styling the Chat Widget

Edit `frontend/src/components/ChatWidget.css` to customize:
- Position (currently bottom-right)
- Size (currently 380px × 600px)
- Border radius and shadows
- Responsive breakpoints

### Backend Configuration

Edit `backend/server.py` to:
- Change CORS settings for production
- Add authentication
- Customize session creation logic
- Add logging or analytics

## Production Deployment

### Backend

1. Use a production ASGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. Set up environment variables on your hosting platform
3. Configure CORS to allow only your frontend domain

### Frontend

1. Build for production:
   ```bash
   npm run build
   ```

2. Deploy the `dist/` folder to your hosting service
3. Update the API endpoint in `ChatWidget.jsx` if your backend URL changes

## Troubleshooting

### Chat widget not appearing
- Check browser console for errors
- Verify the ChatKit script is loaded in `index.html`
- Ensure backend is running and accessible

### Session creation fails
- Verify `OPENAI_API_KEY` is set correctly
- Verify `CHATKIT_WORKFLOW_ID` is correct
- Check backend logs for detailed error messages

### CORS errors
- Update CORS settings in `backend/server.py`
- Ensure frontend URL matches the allowed origins

## Resources

- [ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [Agent Builder](https://platform.openai.com/agent-builder)
- [ChatKit React SDK](https://github.com/openai/chatkit-js)
- [ChatKit Python SDK](https://github.com/openai/chatkit-python)

## License

MIT

