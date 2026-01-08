from fastapi import FastAPI, HTTPException, Request
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

@app.api_route("/api/chatkit/session", methods=["GET", "POST"])
async def create_chatkit_session(request: Request):
    """
    Create a new ChatKit session and return the client secret.
    Supports both GET and POST methods.
    
    GET: Accepts optional device_id as query parameter (?device_id=abc)
    POST: Accepts optional device_id in JSON body ({"device_id": "abc"})
    """
    try:
        if not WORKFLOW_ID:
            error_msg = "CHATKIT_WORKFLOW_ID environment variable is not set. Please add it to your .env file."
            print(f"ERROR: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Extract device_id from either query param (GET) or request body (POST)
        device_id = None
        
        if request.method == "GET":
            # GET: device_id from query parameter
            device_id = request.query_params.get("device_id")
        elif request.method == "POST":
            # POST: device_id from request body
            try:
                body = await request.json()
                device_id = body.get("device_id") if body else None
            except Exception:
                # If no JSON body or invalid JSON, body is None
                device_id = None
        
        # Generate a device ID if not provided
        if not device_id:
            device_id = str(uuid.uuid4())
        
        print(f"Creating ChatKit session with workflow_id: {WORKFLOW_ID}, user: {device_id}")
        
        # Create ChatKit session using REST API (OpenAI SDK 2.x doesn't have chatkit attribute)
        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "chatkit_beta=v1",
            "Authorization": f"Bearer {api_key}"
        }
        json_data = {
            "workflow": {"id": WORKFLOW_ID},
            "user": device_id
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chatkit/sessions",
                headers=headers,
                json=json_data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                error_text = response.text
                print(f"ERROR: OpenAI API returned {response.status_code}: {error_text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OpenAI API error: {error_text}"
                )
            
            session_data = response.json()
            session_id = session_data.get("id", "unknown")
            client_secret = session_data.get("client_secret")
            
            if not client_secret:
                error_msg = "No client_secret in OpenAI API response"
                print(f"ERROR: {error_msg}")
                raise HTTPException(status_code=500, detail=error_msg)
            
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
        "api_key_set": api_key is not None
    }

@app.get("/")
def root():
    return {
        "message": "ChatKit Backend API",
        "endpoints": {
            "health": "/health",
            "create_session": "/api/chatkit/session (GET or POST)",
        },
    }
if __name__ == "__main__":
    import uvicorn
    # For local dev only. Render uses the start command you configured.
    uvicorn.run(app, host="0.0.0.0", port=8000)
