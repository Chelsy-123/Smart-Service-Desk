import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import FeatureCard from "../components/dashboard/FeatureCard";

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div className="container mt-4">

      <div className="mb-4">
        <h3>Welcome {user?.username}</h3>
        <p className="text-muted">
          Use the chatbot to get instant help or raise a support ticket.
        </p>
      </div>

      <div className="row">

        <FeatureCard
          icon="🤖"
          title="Chatbot"
          description="Ask the AI assistant for quick help."
          onClick={() => navigate("/chatbot")}
        />

        <FeatureCard
          icon="📄"
          title="FAQs"
          description="Browse frequently asked questions."
          onClick={() => navigate("/faqs")}
        />

        <FeatureCard
          icon="🎫"
          title="My Tickets"
          description="Track tickets you created."
          onClick={() => navigate("/tickets")}
        />

        {user?.is_agent && (
          <FeatureCard
            icon="📥"
            title="Assigned Tickets"
            description="View tickets assigned to you."
            onClick={() => navigate("/assigned-tickets")}
          />
        )}

        {user?.is_superuser && (
          <>
            <FeatureCard
              icon="👨‍💼"
              title="Manage Agents"
              description="View and manage support agents."
              onClick={() => navigate("/admin/agents")}
            />

            <FeatureCard
              icon="➕"
              title="Create Agent"
              description="Add a new support agent."
              onClick={() => navigate("/admin/agents/create")}
            />

            <FeatureCard
              icon="📚"
              title="Manage FAQs"
              description="Create and update FAQs."
              onClick={() => navigate("/admin/faqs")}
            />

            <FeatureCard
              icon="📂"
              title="Upload Knowledge Base"
              description="Upload documents for the RAG chatbot."
              onClick={() => navigate("/admin/kb/upload")}
            />
          </>
        )}

      </div>

    </div>
  );
};

export default Dashboard;