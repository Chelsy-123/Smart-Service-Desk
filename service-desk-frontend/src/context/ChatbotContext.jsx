import { createContext, useState } from "react";
import { sendMessageToBot } from "../api/chatbot.api";
import { createTicketFromChatbot } from "../api/chatbot.api";

export const ChatbotContext = createContext();

export const ChatbotProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // ✅ NEW: controls floating chatbot visibility
  const [isOpen, setIsOpen] = useState(false);

  const sendMessage = async (text) => {
    setMessages((prev) => [
      ...prev,
      { sender: "user", text },
    ]);

    setLoading(true);

    try {
      const data = await sendMessageToBot(text);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.chatbot_reply,
          confidence: data.confidence,
          suggestTicket: data.suggest_create_ticket,
        },
      ]);
    } catch (error) {
  setMessages((prev) => [
    ...prev,
    {
      sender: "bot",
      text:
        error.response?.status === 401
          ? "Please login to chat with support."
          : "Sorry, something went wrong.",
    },
  ]);
} finally {
  setLoading(false);
}
    };
    
 // 🔴 ADD THIS FUNCTION (THIS WAS MISSING)
  const createTicket = async ({ message, request_type, priority, confidence }) => {
    try {
      const data = await createTicketFromChatbot({
        message,
        request_type,
        priority,
        confidence,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `✅ Ticket created successfully (ID: ${data.ticket_id})`,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Failed to create ticket. Please try again later.",
        },
      ]);
    }
  };

  return (
    <ChatbotContext.Provider
      value={{
        messages,
        sendMessage,
        createTicket,  // ✅ exposed
        loading,
        isOpen,        // ✅ exposed
        setIsOpen,     // ✅ exposed
      }}
    >
      {children}
    </ChatbotContext.Provider>
  );
};
