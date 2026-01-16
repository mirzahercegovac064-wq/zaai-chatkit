import { addEffect } from "framer"
import { useEffect, useState, useRef } from "react"

// Konfiguration - uppdatera din backend URL här
const BACKEND_BASE_URL = "https://zaai-chatkit.onrender.com"
const SESSION_ENDPOINT = `${BACKEND_BASE_URL}/api/chatkit/session`

// Lägg till ChatKit script om det inte redan finns
function loadChatKitScript() {
  if (document.querySelector('script[src*="chatkit.js"]')) {
    return Promise.resolve<void>(undefined)
  }

  return new Promise<void>((resolve, reject) => {
    const script = document.createElement("script")
    script.src = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
    script.defer = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error("Failed to load ChatKit script"))
    document.head.appendChild(script)
  })
}

// Vänta på att ChatKit web component ska bli tillgänglig
async function waitForChatKit() {
  if (customElements.get("openai-chatkit")) {
    return
  }

  await loadChatKitScript()

  return new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error("ChatKit component didn't load within 15s"))
    }, 15000)

    customElements.whenDefined("openai-chatkit").then(() => {
      clearTimeout(timeout)
      resolve()
    })
  })
}

// Skapa session
async function createSession() {
  const deviceIdKey = "chatkit_device_id"
  const existingDeviceId = localStorage.getItem(deviceIdKey)

  const res = await fetch(SESSION_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ device_id: existingDeviceId || null }),
  })

  if (!res.ok) {
    const errorText = await res.text()
    throw new Error(`Session failed ${res.status}: ${errorText || res.statusText}`)
  }

  const data = await res.json()
  if (data.user) {
    localStorage.setItem(deviceIdKey, data.user)
  }
  if (!data.client_secret) {
    throw new Error("Missing client_secret in response")
  }

  return String(data.client_secret)
}

export default function ChatkitWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const chatkitRef = useRef<HTMLElement | null>(null)
  const mountRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isOpen || chatkitRef.current) return

    let mounted = false

    async function mountChatKit() {
      if (mounted) return
      setIsLoading(true)
      setError(null)

      try {
        await waitForChatKit()

        if (!mountRef.current || mounted) return

        const el = document.createElement("openai-chatkit") as any

        el.setOptions({
          api: {
            async getClientSecret(existing: string | undefined) {
              if (existing) return existing
              return await createSession()
            },
          },
          theme: {
            colorScheme: "light" as const,
            radius: "pill" as const,
            density: "normal" as const,
            color: {
              accent: {
                primary: "#9F80DA",
                level: 1,
              },
              surface: {
                background: "#ffffff",
                foreground: "#ffffff",
              },
            },
            typography: {
              baseSize: 16,
              fontFamily:
                '"OpenAI Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
              fontFamilyMono:
                'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "DejaVu Sans Mono", "Courier New", monospace',
              fontSources: [
                {
                  family: "OpenAI Sans",
                  src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Regular.woff2",
                  weight: 400,
                  style: "normal",
                  display: "swap",
                },
                {
                  family: "OpenAI Sans",
                  src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Medium.woff2",
                  weight: 500,
                  style: "normal",
                  display: "swap",
                },
                {
                  family: "OpenAI Sans",
                  src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Semibold.woff2",
                  weight: 600,
                  style: "normal",
                  display: "swap",
                },
                {
                  family: "OpenAI Sans",
                  src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Bold.woff2",
                  weight: 700,
                  style: "normal",
                  display: "swap",
                },
              ],
            },
          },
          composer: {
            placeholder: "Skriv ett meddelande till ZAAI",
            attachments: {
              enabled: false,
            },
          },
          startScreen: {
            greeting: "Chatta med oss!",
            prompts: [],
          },
        })

        el.style.width = "100%"
        el.style.height = "100%"

        mountRef.current.appendChild(el)
        chatkitRef.current = el
        mounted = true
        setIsLoading(false)
      } catch (e: any) {
        if (mounted) return
        const errorMsg = e?.message || String(e)
        setError(errorMsg)
        setIsLoading(false)
        console.error("ChatKit mount error:", e)
      }
    }

    mountChatKit()

    return () => {
      mounted = true
    }
  }, [isOpen])

  return (
    <>
      {/* Bubble Button */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: "fixed",
          right: "20px",
          bottom: "20px",
          width: "56px",
          height: "56px",
          borderRadius: "999px",
          background: "#ffffff",
          color: "#333",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "24px",
          cursor: "pointer",
          boxShadow: "0 10px 30px rgba(0,0,0,.2)",
          border: "1px solid #e9e9e9",
          zIndex: 2147483001,
          userSelect: "none",
        }}
        role="button"
        tabIndex={0}
        aria-label={isOpen ? "Stäng chat" : "Öppna chat"}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault()
            setIsOpen(!isOpen)
          }
        }}
      >
        💬
      </div>

      {/* Chat Panel */}
      {isOpen && (
        <div
          style={{
            position: "fixed",
            right: "20px",
            bottom: "90px",
            width: "380px",
            maxWidth: "calc(100vw - 40px)",
            height: "560px",
            maxHeight: "calc(100vh - 140px)",
            background: "#ffffff",
            borderRadius: "16px",
            border: "1px solid #e9e9e9",
            boxShadow: "0 20px 60px rgba(0, 0, 0, 0.25)",
            zIndex: 2147483000,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          {/* Chat Mount */}
          <div
            ref={mountRef}
            style={{
              flex: 1,
              minHeight: 0,
              background: "#fff",
              overflow: "hidden",
            }}
          >
            {isLoading && (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  height: "100%",
                  color: "#666",
                }}
              >
                Laddar...
              </div>
            )}
            {error && (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  height: "100%",
                  padding: "20px",
                  textAlign: "center",
                  color: "#dc2626",
                }}
              >
                <p>⚠️ {error}</p>
                <button
                  onClick={() => {
                    setError(null)
                    setIsOpen(false)
                    setTimeout(() => setIsOpen(true), 100)
                  }}
                  style={{
                    marginTop: "12px",
                    padding: "8px 16px",
                    background: "#9F80DA",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    fontSize: "14px",
                  }}
                >
                  Försök igen
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  )
}
