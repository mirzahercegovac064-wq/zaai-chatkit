from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid
from typing import Optional

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# Enable CORS for frontend
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
# Allow Framer domains and local development
# For production, we allow all origins to support Framer's dynamic domains
# You can restrict this later by adding specific domains to the list
allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "http://localhost:5173",
    # Add your specific Framer domain here when you know it
    # Example: "https://din-site.framer.website"
]

# In production, allow all origins for Framer compatibility
# This allows any Framer domain (*.framer.website, *.framer.app) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safe for public API endpoints)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file in the project root with your OPENAI_API_KEY.")

openai_client = OpenAI(api_key=api_key)

# Get workflow ID from environment
WORKFLOW_ID = os.environ.get("CHATKIT_WORKFLOW_ID")
if not WORKFLOW_ID:
    print("WARNING: CHATKIT_WORKFLOW_ID environment variable is not set. Please add it to your .env file.")

class SessionRequest(BaseModel):
    device_id: Optional[str] = None

@app.post("/api/chatkit/session")
async def create_chatkit_session(request: Optional[SessionRequest] = None):
    """
    Create a new ChatKit session and return the client secret.
    """
    try:
        if not WORKFLOW_ID:
            error_msg = "CHATKIT_WORKFLOW_ID environment variable is not set. Please add it to your .env file."
            print(f"ERROR: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Generate a device ID if not provided
        device_id = request.device_id if request and request.device_id else str(uuid.uuid4())
        
        print(f"Creating ChatKit session with workflow_id: {WORKFLOW_ID}, user: {device_id}")
        
        # Create ChatKit session
        session = openai_client.chatkit.sessions.create(
            workflow={"id": WORKFLOW_ID},
            user=device_id,
        )
        
        print(f"Session created successfully: {session.id}")
        return {"client_secret": session.client_secret}
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error creating ChatKit session: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "workflow_id_set": WORKFLOW_ID is not None,
        "api_key_set": api_key is not None
    }

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "ChatKit Backend API",
        "endpoints": {
            "health": "/health",
            "create_session": "/api/chatkit/session (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

