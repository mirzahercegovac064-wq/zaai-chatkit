from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
from typing import Optional
import httpx

# Load environment variables from .env file (for local dev)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# CORS (keep it permissive for Framer)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Env vars
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in Render Environment or in a local .env file."
    )

WORKFLOW_ID = os.environ.get("CHATKIT_WORKFLOW_ID")
if not WORKFLOW_ID:
    print("WARNING: CHATKIT_WORKFLOW_ID environment variable is not set.")

# Get domain public key from environment (for domain authorization)
DOMAIN_PUBLIC_KEY = os.environ.get("CHATKIT_DOMAIN_PUBLIC_KEY")
if not DOMAIN_PUBLIC_KEY:
    print("WARNING: CHATKIT_DOMAIN_PUBLIC_KEY environment variable is not set. ChatKit may not work on your domain.")

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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating ChatKit session: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "workflow_id_set": WORKFLOW_ID is not None,
        "api_key_set": api_key is not None
    }

@app.get("/")
def root():
    return {
        "message": "ChatKit Backend API",
        "endpoints": {
            "health": "/health",
            "create_session": "/api/chatkit/session (POST)",
        },
    }
from fastapi import Request

@app.api_route("/api/chatkit/session", methods=["GET", "POST"])
async def chatkit_session(request: Request):
    if request.method == "GET":
        device_id = request.query_params.get("device_id")
    else:
        body = await request.json()
        device_id = body.get("device_id")

    return await _create_chatkit_session_internal(device_id)
if __name__ == "__main__":
    import uvicorn
    # For local dev only. Render uses the start command you configured.
    uvicorn.run(app, host="0.0.0.0", port=8000)
