import React from 'react'
import ChatWidget from './components/ChatWidget'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Welcome to ZAAI</h1>
        <p>Your intelligent assistant is ready to help</p>
      </header>
      <main className="app-content">
        <div className="content-section">
          <h2>About ZAAI</h2>
          <p>
            ZAAI is your intelligent assistant, ready to help with any questions
            or tasks you might have. Click the chat widget in the bottom right
            corner to get started!
          </p>
        </div>
      </main>
      {/* Chat Widget positioned in bottom right */}
      <ChatWidget />
    </div>
  )
}

export default App

