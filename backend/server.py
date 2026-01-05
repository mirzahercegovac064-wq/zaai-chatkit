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

class SessionRequest(BaseModel):
    device_id: Optional[str] = None

@app.post("/api/chatkit/session")
async def create_chatkit_session(request: Optional[SessionRequest] = None):
    """
    Create a new ChatKit session and return the client secret.
    """
    if not WORKFLOW_ID:
        raise HTTPException(
            status_code=500,
            detail="CHATKIT_WORKFLOW_ID environment variable is not set. Please set it.",
        )

    # Generate a device ID if not provided
    device_id = request.device_id if request and request.device_id else str(uuid.uuid4())

    print(f"Creating ChatKit session with workflow_id: {WORKFLOW_ID}, user: {device_id}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chatkit/sessions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "OpenAI-Beta": "chatkit_beta=v1",
                },
                json={
                    "workflow": {"id": WORKFLOW_ID},
                    "user": device_id,
                },
            )

        if resp.status_code >= 400:
            # Log the upstream error for debugging
            print(f"ChatKit session create failed: {resp.status_code} {resp.text}")
            raise HTTPException(
                status_code=500,
                detail=f"ChatKit session create failed: {resp.text}",
            )

        data = resp.json()

        client_secret = data.get("client_secret")
        if not client_secret:
            print(f"Unexpected ChatKit response: {data}")
            raise HTTPException(status_code=500, detail="Missing client_secret in response.")

        # Optional: log session id if present
        session_id = data.get("id")
        if session_id:
            print(f"Session created successfully: {session_id}")

        return {"client_secret": client_secret}

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
        "api_key_set": api_key is not None,
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

if __name__ == "__main__":
    import uvicorn
    # For local dev only. Render uses the start command you configured.
    uvicorn.run(app, host="0.0.0.0", port=8000)
