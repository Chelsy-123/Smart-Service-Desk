import { useContext } from "react";
import { ChatbotContext } from "../../context/ChatbotContext";

const TicketSuggestion = ({ message }) => {
  const { createTicket } = useContext(ChatbotContext);

  const handleCreateTicket = () => {
    createTicket({
      message: message.text,
      request_type: message.request_type,
      priority: message.priority,
      confidence: message.confidence,
    });
  };

  return (
    <div className="alert alert-warning mt-2">
      <p className="mb-2">
        ⚠️ If you are not satisfied with my answer, would you like to create a support ticket?
      </p>
      <button className="btn btn-sm btn-primary" onClick={handleCreateTicket}>
        Create Ticket
      </button>
    </div>
  );
};

export default TicketSuggestion;
