import { ChatbotProvider } from "../../context/ChatbotContext";
import ChatWindow from "../../components/chatbot/ChatWindow";

const ChatbotPage = () => {
  return (
    <ChatbotProvider>
      <h4 className="mb-3">Smart Support Assistant</h4>
      <ChatWindow />
    </ChatbotProvider>
  );
};

export default ChatbotPage;
