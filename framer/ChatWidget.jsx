import React, { useState } from 'react'
import { ChatKit, useChatKit } from '@openai/chatkit-react'

// Uppdatera denna URL till din backend
const API_ENDPOINT = 'https://zaai-chatkit.onrender.com/api/chatkit/session'

// Inline CSS för att fungera i Framer
const styles = {
  toggleButton: {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    width: '56px',
    height: '56px',
    borderRadius: '999px',
    border: 'none',
    background: 'radial-gradient(circle at 0 0, #10a37f, #0c8b68)',
    color: '#ffffff',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 18px 40px rgba(0, 0, 0, 0.35)',
    transition: 'transform 0.15s ease, box-shadow 0.15s ease',
    zIndex: 1001,
    fontSize: '24px',
  },
  widgetContainer: {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    zIndex: 1000,
    width: '380px',
    height: '600px',
    maxWidth: 'calc(100vw - 40px)',
    maxHeight: 'calc(100vh - 40px)',
    background: '#ffffff',
    borderRadius: '16px',
    boxShadow: '0 24px 80px rgba(0, 0, 0, 0.35)',
    display: 'flex',
    flexDirection: 'column',
  },
  widgetHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '10px 14px',
    borderBottom: '1px solid #e5e7eb',
    background: 'linear-gradient(135deg, #0f172a, #020617)',
    color: '#f9fafb',
    borderRadius: '16px 16px 0 0',
  },
  widgetTitle: {
    fontSize: '0.95rem',
    fontWeight: 600,
  },
  widgetClose: {
    border: 'none',
    background: 'transparent',
    color: '#e5e7eb',
    fontSize: '1.3rem',
    cursor: 'pointer',
    padding: '0 4px',
    lineHeight: 1,
  },
  widgetBody: {
    flex: 1,
    minHeight: 0,
  },
  widget: {
    width: '100%',
    height: '100%',
    borderRadius: '0 0 16px 16px',
    overflow: 'hidden',
  },
  errorMessage: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '2rem',
    textAlign: 'center',
    height: '100%',
    color: '#dc2626',
  },
  retryButton: {
    padding: '0.5rem 1rem',
    background: '#10a37f',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    transition: 'background 0.2s',
  },
}

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
          const res = await fetch(API_ENDPOINT, {
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
        style={styles.toggleButton}
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={isOpen ? 'Stäng chatten' : 'Öppna chatten'}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'translateY(-1px) scale(1.02)'
          e.currentTarget.style.boxShadow = '0 22px 50px rgba(0, 0, 0, 0.4)'
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'translateY(0) scale(1)'
          e.currentTarget.style.boxShadow = '0 18px 40px rgba(0, 0, 0, 0.35)'
        }}
      >
        💬
      </button>

      {isOpen && (
        <div style={styles.widgetContainer}>
          <div style={styles.widgetHeader}>
            <div style={styles.widgetTitle}>
              ZAAI Assistant
            </div>
            <button
              style={styles.widgetClose}
              onClick={() => setIsOpen(false)}
              aria-label="Minimera chatten"
              onMouseEnter={(e) => {
                e.currentTarget.style.color = '#ffffff'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = '#e5e7eb'
              }}
            >
              ×
            </button>
          </div>
          <div style={styles.widgetBody}>
            {error ? (
              <div style={styles.errorMessage}>
                <p>⚠️ {error}</p>
                <button 
                  onClick={() => {
                    setError(null)
                    window.location.reload()
                  }}
                  style={styles.retryButton}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#0c8b68'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = '#10a37f'
                  }}
                >
                  Försök igen
                </button>
              </div>
            ) : (
              <ChatKit
                control={control}
                style={styles.widget}
              />
            )}
          </div>
        </div>
      )}
    </>
  )
}

