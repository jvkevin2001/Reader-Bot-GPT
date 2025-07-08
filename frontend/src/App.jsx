// frontend/src/App.jsx
// frontend/src/App.jsx

import React, { useState, useEffect, useRef } from 'react';

// --- Componentes de Iconos ---
const SendIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"></line>
    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
  </svg>
);

const TypingIndicator = () => (
  <div className="flex items-start gap-3 mb-4">
    <div className="bot-message p-3 rounded-2xl rounded-tl-none">
      <div className="flex items-center gap-1.5 py-1">
        <span className="h-2 w-2 bg-white/50 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
        <span className="h-2 w-2 bg-white/50 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
        <span className="h-2 w-2 bg-white/50 rounded-full animate-bounce"></span>
      </div>
    </div>
  </div>
);

function App() {
  // --- ESTADO DE LA APLICACIÓN ---
  const [messages, setMessages] = useState([
    { sender: 'bot', text: '¡Hola! Soy tu asistente de documentos. ¿En qué puedo ayudarte hoy?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null); // Referencia para hacer scroll automático

  // --- EFECTO PARA SCROLL AUTOMÁTICO ---
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);


  // --- LÓGICA PARA CONECTAR CON EL BACKEND ---
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage, { sender: 'bot', text: '' }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        
        // --- CORRECCIÓN DEL BUG DE DUPLICACIÓN ---
        // Se actualiza el estado de forma inmutable, creando siempre un nuevo array
        // y un nuevo objeto de mensaje para evitar efectos secundarios.
        setMessages(prev => {
          const allButLast = prev.slice(0, -1);
          const lastMessage = prev[prev.length - 1];
          const updatedLastMessage = { ...lastMessage, text: lastMessage.text + chunk };
          return [...allButLast, updatedLastMessage];
        });
      }

    } catch (error) {
      console.error("Error al conectar con el servidor:", error);
      setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          const updatedLastMessage = { ...lastMessage, text: "Lo siento, no pude conectar con el servidor. Por favor, inténtalo de nuevo más tarde." };
          return [...prev.slice(0, -1), updatedLastMessage];
        });
    } finally {
      setIsLoading(false);
    }
  };
  
  // --- LÓGICA PARA LIMPIAR EL CHAT ---
  const handleClearChat = () => {
    setMessages([
      { sender: 'bot', text: '¡Hola! Soy tu asistente de documentos. ¿En qué puedo ayudarte hoy?' }
    ]);
  };


  // --- RENDERIZADO DEL COMPONENTE ---
  return (
    <div className="w-full max-w-lg mx-4 sm:mx-0 flex flex-col h-[90vh] max-h-[700px] glass-container rounded-3xl shadow-2xl overflow-hidden">
      
      <header className="p-4 flex items-center justify-between text-white border-b border-white/20 flex-shrink-0">
        <div className="flex items-center gap-4">
          <img src="https://placehold.co/48x48/ffffff/764ba2?text=AI" alt="Avatar" className="w-12 h-12 rounded-full border-2 border-white/50" />
          <div>
            <h1 className="text-lg font-semibold">Asistente de PDF</h1>
            <p className="text-sm opacity-80 flex items-center gap-2">
              <span className={`h-2 w-2 rounded-full ${isLoading ? 'animate-pulse bg-yellow-400' : 'bg-green-400'}`}></span>
              {isLoading ? 'Procesando...' : 'Activo ahora'}
            </p>
          </div>
        </div>
        <button onClick={handleClearChat} className="text-xs bg-white/10 hover:bg-white/20 p-2 rounded-md transition-colors">Limpiar Chat</button>
      </header>

      <main className="flex-1 p-6 overflow-y-auto chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`flex items-start gap-3 mb-4 ${msg.sender === 'user' ? 'justify-end' : ''}`}>
            <div className={`${msg.sender === 'bot' ? 'bot-message' : 'user-message'} text-white p-3 rounded-2xl ${msg.sender === 'user' ? 'rounded-br-none' : 'rounded-tl-none'} max-w-xs md:max-w-md shadow-lg`}>
              <p className="text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </main>

      <footer className="p-4 border-t border-white/20 flex-shrink-0">
        <form onSubmit={handleSend} className="flex items-center gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pregunta algo sobre el documento..."
            autoComplete="off"
            className="flex-1 w-full px-4 py-2 text-white placeholder-white/60 bg-white/10 border border-white/20 rounded-full focus:outline-none focus:ring-2 focus:ring-white/50 transition-shadow"
            disabled={isLoading}
          />
          <button type="submit" className="bg-white/20 text-white p-3 rounded-full hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white/50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed" disabled={isLoading}>
            <SendIcon />
          </button>
        </form>
      </footer>
    </div>
  );
}

export default App;