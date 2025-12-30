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
        {/* Enkel ikon liknande ChatGPT-bubbla */}
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

