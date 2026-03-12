from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
import json
import time
from typing import Optional
import httpx

# Load environment variables from .env file (for local dev)
env_path = os.path.join(os.path.dirname(__file__), ".env")
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

DOMAIN_PUBLIC_KEY = os.environ.get("CHATKIT_DOMAIN_PUBLIC_KEY")
if not DOMAIN_PUBLIC_KEY:
    print("WARNING: CHATKIT_DOMAIN_PUBLIC_KEY environment variable is not set.")

# n8n webhook – only called for booking/cancellation/rebooking/escalation intents
N8N_INTENT_WEBHOOK = "https://zaaihbg.app.n8n.cloud/webhook/zaai-chattwidget-action"

# In-memory conversation history: thread_id → list of messages
conversation_history: dict = {}

SYSTEM_PROMPT = """Du är ZAAI:s AI-receptionist. Svara på frågor om ZAAI:s tjänster, priser och processer. Svara alltid på svenska om inget annat anges. Var vänlig och professionell. Hänvisa alltid till www.zaai.se för mer info.

Om kunden vill boka, avboka eller omboka en tid – fråga aktivt efter nödvändig information i konversationen: namn, önskat datum, önskad tid och gärna e-post. Anropa funktionen först när du har tillräckligt med uppgifter.

VIKTIGT – informationsinsamling:
- Be aldrig om allt på en gång, ställ en fråga i taget
- Om kunden inte ger e-post vid bokning/ombokning, fortsätt ändå – den är valfri
- Bekräfta alltid de uppgifter du fått innan du anropar funktionen

Om du inte kan svara på en fråga, eller om kunden uttryckligen vill prata med en människa – be först om kundens e-postadress om du inte redan har den. Anropa sedan funktionen eskalera_till_team med e-post, sammanfattning och anledning."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "boka_tid",
            "description": "Boka ett möte eller demo för kunden. Anropa när kunden bekräftat namn, datum och tid.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {"type": "string", "description": "Kundens namn"},
                    "datum": {"type": "string", "description": "Datum för mötet, t.ex. 2026-03-15"},
                    "tid": {"type": "string", "description": "Tid för mötet, t.ex. 14:00"},
                    "email": {"type": "string", "description": "Kundens e-postadress (valfri)"},
                    "meddelande": {"type": "string", "description": "Eventuell notering (valfri)"}
                },
                "required": ["namn", "datum", "tid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "avboka_tid",
            "description": "Avboka ett befintligt möte för kunden.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {"type": "string", "description": "Kundens namn"},
                    "datum": {"type": "string", "description": "Datum för mötet som ska avbokas"},
                    "tid": {"type": "string", "description": "Tid för mötet (valfri)"}
                },
                "required": ["namn", "datum"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "omboka_tid",
            "description": "Omboka ett befintligt möte till ny tid.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namn": {"type": "string", "description": "Kundens namn"},
                    "gammalt_datum": {"type": "string", "description": "Datum för det befintliga mötet"},
                    "gammal_tid": {"type": "string", "description": "Tid för det befintliga mötet (valfri)"},
                    "nytt_datum": {"type": "string", "description": "Nytt datum"},
                    "ny_tid": {"type": "string", "description": "Ny tid"}
                },
                "required": ["namn", "gammalt_datum", "nytt_datum", "ny_tid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "eskalera_till_team",
            "description": "Skicka ärendet till ZAAI-teamet när kunden vill prata med en människa eller AI inte kan svara. Kräver kundens e-post – fråga om den saknas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Kundens e-postadress (obligatorisk)"},
                    "anledning": {"type": "string", "description": "Varför eskaleras ärendet?"},
                    "sammanfattning": {"type": "string", "description": "Sammanfattning av konversationen"}
                },
                "required": ["email", "anledning", "sammanfattning"]
            }
        }
    }
]


def format_conversation(messages: list) -> str:
    """Format conversation history as readable text for n8n escalation emails."""
    lines = []
    for msg in messages:
        role = "Kund" if msg["role"] == "user" else "AI"
        content = msg.get("content", "")
        if isinstance(content, list):
            content = " ".join(
                c.get("text", "") for c in content if isinstance(c, dict)
            )
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


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
            error_msg = "CHATKIT_WORKFLOW_ID environment variable is not set."
            print(f"ERROR: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

        device_id = None
        if request.method == "GET":
            device_id = request.query_params.get("device_id")
        elif request.method == "POST":
            try:
                body = await request.json()
                device_id = body.get("device_id") if body else None
            except Exception:
                device_id = None

        if not device_id:
            device_id = str(uuid.uuid4())

        print(f"Creating ChatKit session: workflow={WORKFLOW_ID}, user={device_id}")

        headers = {
            "Content-Type": "application/json",
            "OpenAI-Beta": "chatkit_beta=v1",
            "Authorization": f"Bearer {api_key}"
        }
        json_data = {"workflow": {"id": WORKFLOW_ID}, "user": device_id}

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
                raise HTTPException(status_code=500, detail="No client_secret in OpenAI API response")
            print(f"Session created successfully: {session_id}")
            return {"client_secret": client_secret}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating ChatKit session: {str(e)}")


@app.post("/chatkit")
async def chatkit_handler(request: Request):
    """
    ChatKit custom backend.
    - FAQ / general questions: answered directly by OpenAI (gpt-4o) with function tools
    - Booking / cancellation / rebooking / escalation: detected via tool_calls, routed to n8n
    """
    body = await request.json()
    req_type = body.get("type", "")
    params = body.get("params", {})

    if req_type == "threads.create":
        thread_id = f"thread_{int(time.time() * 1000)}"
        conversation_history[thread_id] = []
        return JSONResponse({
            "id": thread_id,
            "object": "chatkit.thread",
            "created_at": int(time.time()),
            "metadata": {},
        })

    if req_type == "threads.add_user_message":
        thread_id = params.get("thread_id", f"thread_{int(time.time() * 1000)}")
        content_list = params.get("input", {}).get("content", [])
        user_message = " ".join(
            c.get("text", "") for c in content_list if c.get("type") == "text"
        )

        if thread_id not in conversation_history:
            conversation_history[thread_id] = []

        conversation_history[thread_id].append({"role": "user", "content": user_message})

        async def stream_response():
            item_id = f"item_{int(time.time() * 1000)}"
            reply = "Tyvärr kunde jag inte svara just nu. Vänligen försök igen."

            try:
                messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[thread_id]

                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "gpt-4o",
                            "messages": messages,
                            "tools": TOOLS,
                            "tool_choice": "auto"
                        },
                        timeout=60.0
                    )
                    resp.raise_for_status()
                    result = resp.json()
                    choice = result["choices"][0]
                    message = choice["message"]

                    if choice["finish_reason"] == "tool_calls" and message.get("tool_calls"):
                        # Specific intent detected – route to n8n
                        tool_call = message["tool_calls"][0]
                        intent = tool_call["function"]["name"]
                        tool_args = json.loads(tool_call["function"]["arguments"])
                        conv_text = format_conversation(conversation_history[thread_id])

                        print(f"Tool call: {intent}, args: {tool_args}")

                        n8n_resp = await client.post(
                            N8N_INTENT_WEBHOOK,
                            json={
                                "intent": intent,
                                "thread_id": thread_id,
                                "data": tool_args,
                                "konversation": conv_text
                            },
                            timeout=60.0
                        )
                        n8n_resp.raise_for_status()
                        n8n_data = n8n_resp.json()
                        reply = (
                            n8n_data.get("response")
                            or n8n_data.get("output")
                            or n8n_data.get("text")
                            or "Åtgärden genomfördes."
                        )
                    else:
                        # Regular FAQ – use OpenAI response directly
                        reply = message.get("content", reply)

                conversation_history[thread_id].append({"role": "assistant", "content": reply})

            except Exception as e:
                print(f"Error in chatkit handler: {e}")
                import traceback
                traceback.print_exc()

            events = [
                {"type": "thread.item.added", "item": {"id": item_id, "type": "message", "role": "assistant", "status": "in_progress", "content": []}},
                {"type": "thread.item.updated", "item": {"id": item_id, "delta": {"content": [{"type": "output_text", "output_index": 0, "delta": reply}]}}},
                {"type": "thread.item.done", "item": {"id": item_id, "type": "message", "role": "assistant", "status": "completed", "content": [{"type": "output_text", "text": reply}]}},
            ]
            for event in events:
                yield f"data: {json.dumps(event)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_response(), media_type="text/event-stream")

    return JSONResponse({})


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
