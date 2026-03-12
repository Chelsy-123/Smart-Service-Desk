import MessageBubble from "./MessageBubble";
import TicketSuggestion from "./TicketSuggestion";

const ChatMessage = ({ message }) => {
  return (
    <div className="mb-2">
      <MessageBubble message={message} />

      {/* Show ticket suggestion ONLY when backend suggests */}
      {message.suggestTicket && (
        <TicketSuggestion />
      )}
    </div>
  );
};

export default ChatMessage;
