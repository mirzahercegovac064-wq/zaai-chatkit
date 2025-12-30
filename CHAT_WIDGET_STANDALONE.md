# ChatKit Widget - Fristående kod

Här är all kod du behöver för att integrera ChatKit-widgeten på en annan webbplats.

## 1. React-komponent (ChatWidget.jsx)

```jsx
import React, { useState } from 'react'
import { ChatKit, useChatKit } from '@openai/chatkit-react'
import './ChatWidget.css'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [error, setError] = useState(null)

  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          console.log('Using existing client secret')
          return existing
        }

        try {
          console.log('Fetching new client secret from backend...')
          // Ändra denna URL till din backend-endpoint
          const res = await fetch('/api/chatkit/session', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
          })

          if (!res.ok) {
            const errorText = await res.text()
            console.error('Backend error response:', errorText)
            const errorMsg = `Failed to create session: ${res.status} ${res.statusText}`
            setError(errorMsg)
            throw new Error(errorMsg)
          }

          const data = await res.json()
          console.log('Client secret received successfully', data)
          
          if (!data.client_secret) {
            const errorMsg = 'No client_secret in response'
            setError(errorMsg)
            throw new Error(errorMsg)
          }
          
          setError(null)
          return data.client_secret
        } catch (error) {
          console.error('Error fetching client secret:', error)
          const errorMsg = error.message || 'Kunde inte ansluta till chatten. Kontrollera att backend-servern körs.'
          setError(errorMsg)
          throw error
        }
      },
    },
  })

  return (
    <>
      <button
        className="chat-toggle-button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={isOpen ? 'Stäng chatten' : 'Öppna chatten'}
      >
        <span className="chat-toggle-icon">💬</span>
      </button>

      {isOpen && (
        <div className="chat-widget-container">
          <div className="chat-widget-header">
            <div className="chat-widget-title">
              ZAAI Assistant
            </div>
            <button
              className="chat-widget-close"
              onClick={() => setIsOpen(false)}
              aria-label="Minimera chatten"
            >
              ×
            </button>
          </div>
          <div className="chat-widget-body">
            {error ? (
              <div className="chat-error-message">
                <p>⚠️ {error}</p>
                <button 
                  onClick={() => {
                    setError(null)
                    window.location.reload()
                  }}
                  className="chat-retry-button"
                >
                  Försök igen
                </button>
              </div>
            ) : (
              <ChatKit
                control={control}
                className="chat-widget"
              />
            )}
          </div>
        </div>
      )}
    </>
  )
}
```

## 2. CSS-stilar (ChatWidget.css)

```css
.chat-widget-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  width: 380px;
  height: 600px;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 40px);
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
}

.chat-widget {
  width: 100%;
  height: 100%;
  border-radius: 0 0 16px 16px;
  overflow: hidden;
}

.chat-toggle-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 999px;
  border: none;
  background: radial-gradient(circle at 0 0, #10a37f, #0c8b68);
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
  z-index: 1001;
}

.chat-toggle-button:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 22px 50px rgba(0, 0, 0, 0.4);
}

.chat-toggle-icon {
  font-size: 24px;
}

.chat-widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #0f172a, #020617);
  color: #f9fafb;
  border-radius: 16px 16px 0 0;
}

.chat-widget-title {
  font-size: 0.95rem;
  font-weight: 600;
}

.chat-widget-close {
  border: none;
  background: transparent;
  color: #e5e7eb;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}

.chat-widget-close:hover {
  color: #ffffff;
}

.chat-widget-body {
  flex: 1;
  min-height: 0;
}

.chat-error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  height: 100%;
  color: #dc2626;
}

.chat-error-message p {
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.chat-retry-button {
  padding: 0.5rem 1rem;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.chat-retry-button:hover {
  background: #0c8b68;
}

/* Responsive design for mobile */
@media (max-width: 768px) {
  .chat-widget-container {
    width: calc(100vw - 20px);
    height: calc(100vh - 20px);
    bottom: 12px;
    right: 12px;
    max-width: none;
    max-height: none;
  }

  .chat-toggle-button {
    bottom: 16px;
    right: 16px;
  }
}
```

## 3. HTML - Lägg till ChatKit-scriptet

I din `index.html` eller huvud-HTML-fil, lägg till detta i `<head>`:

```html
<meta http-equiv="Cross-Origin-Embedder-Policy" content="credentialless" />
<script
  src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
  async
></script>
```

## 4. Package.json - Dependencies

Se till att du har dessa dependencies:

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@openai/chatkit-react": "^1.0.0"
  }
}
```

Installera med:
```bash
npm install @openai/chatkit-react
```

## 5. Användning i din App

```jsx
import ChatWidget from './components/ChatWidget'

function App() {
  return (
    <div>
      {/* Din befintliga kod */}
      
      {/* Lägg till widgeten */}
      <ChatWidget />
    </div>
  )
}
```

## 6. Backend-endpoint

Din backend behöver ha en endpoint som returnerar `client_secret`. Exempel med FastAPI:

```python
from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.post("/api/chatkit/session")
async def create_chatkit_session():
    session = openai_client.chatkit.sessions.create(
        workflow={"id": os.environ.get("CHATKIT_WORKFLOW_ID")},
        user=str(uuid.uuid4()),
    )
    return {"client_secret": session.client_secret}
```

## 7. Viktiga punkter

1. **Ändra API-endpoint**: I `ChatWidget.jsx`, ändra `/api/chatkit/session` till din backend-URL om den är annorlunda
2. **CORS**: Se till att din backend tillåter requests från din frontend-domän
3. **Environment variables**: Backend behöver `OPENAI_API_KEY` och `CHATKIT_WORKFLOW_ID`
4. **Z-index**: Widgeten använder `z-index: 1000` och `1001`, justera om det krockar med din befintliga design

## 8. Anpassning

- **Färger**: Ändra färgerna i CSS (sök efter `#10a37f`, `#0c8b68`, etc.)
- **Titel**: Ändra "ZAAI Assistant" till vad du vill
- **Storlek**: Ändra `width` och `height` i `.chat-widget-container`
- **Position**: Ändra `bottom` och `right` för att flytta widgeten



