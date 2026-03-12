import { useContext, useState, useRef, useEffect } from "react";
import { ChatbotContext } from "../../context/ChatbotContext";
import ChatMessage from "./ChatMessage";

const ChatWindow = () => {
  const { messages, sendMessage, loading } = useContext(ChatbotContext);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  // auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div
      className="card shadow"
      style={{
        position: "fixed",
        bottom: "80px",
        right: "20px",
        width: "350px",
        height: "450px",
        zIndex: 1050,
      }}
    >
      <div className="card-header bg-secondary text-white">
        Smart Assistant
      </div>

      <div
        className="card-body overflow-auto"
        style={{ height: "320px" }}
      >
        {messages.length === 0 && (
          <p className="text-muted text-center">
            Hey I'm Zeus your support AI assistant👋 Ask me anything !
          </p>
        )}

        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}

        {loading && (
          <p className="text-muted small">Bot is typing...</p>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="card-footer d-flex gap-2">
        <input
          type="text"
          className="form-control"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button className="btn btn-secondary" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
