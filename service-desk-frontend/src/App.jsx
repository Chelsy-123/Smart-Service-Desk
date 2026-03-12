import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { useContext } from "react";

import { AuthProvider } from "./context/AuthContext";
import { ChatbotProvider, ChatbotContext } from "./context/ChatbotContext";
import ProtectedRoute from "./components/common/ProtectedRoute";

import Navbar from "./components/common/Navbar";
import Register from "./pages/auth/Register";
import Login from "./pages/auth/Login";
import Dashboard from "./pages/Dashboard";
import ChatbotPage from "./pages/chatbot/ChatbotPage";
import MyTickets from "./pages/tickets/MyTickets";
import TicketDetails from "./pages/tickets/TicketDetails";
import AssignedTickets from "./pages/tickets/AssignedTickets";
import ChatWindow from "./components/chatbot/ChatWindow";
import FloatingButton from "./components/chatbot/FloatingButton";
import CreateTicket from "./pages/tickets/CreateTicket";
import FAQPublic from "./pages/public/FAQPublic";
import CreateAgent from "./pages/admin/CreateAgent";
import AgentsList from "./pages/admin/AgentsList";
import FAQAdminForm from "./pages/admin/FAQAdminForm";
import FAQAdminList from "./pages/admin/FAQAdminList";
import KBUpload from "./pages/admin/KBUpload";

// 🔹 Inner layout (safe for hooks)
function AppLayout() {
  const location = useLocation();
  const { isOpen, setIsOpen } = useContext(ChatbotContext);

  // ❗ Hide chatbot on login page for now
  const hideChatbot = location.pathname === "/login";

  return (
    <>
      <Navbar />

      <div className="container-fluid px-4 mt-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
          <Route path="/tickets" element={<MyTickets />} />
          <Route path="/assigned-tickets" element={<AssignedTickets />} />
          <Route path="/tickets/:id" element={<TicketDetails />} />
          <Route path="/tickets/create" element={<CreateTicket />} />
          <Route path="/faqs" element={<FAQPublic />} />
          <Route path="/admin/faqs" element={<ProtectedRoute roles={["ADMIN"]}><FAQAdminList /></ProtectedRoute>} />
          <Route path="/admin/faqs/new" element={<ProtectedRoute roles={["ADMIN"]}><FAQAdminForm /></ProtectedRoute>} />
          <Route path="/admin/faqs/:id" element={<ProtectedRoute roles={["ADMIN"]}><FAQAdminForm /></ProtectedRoute>} />
          <Route path="/admin/agents/create" element={<ProtectedRoute roles={["ADMIN"]}><CreateAgent /></ProtectedRoute>} />
          <Route path="/admin/agents" element={<ProtectedRoute roles={["ADMIN"]}><AgentsList /></ProtectedRoute>} />
          <Route path="/admin/kb/upload" element={<ProtectedRoute roles={["ADMIN"]}><KBUpload /></ProtectedRoute>} />

        </Routes>
      </div>

      {/* ✅ Floating chatbot (temporary logic) */}
      {!hideChatbot && (
        <>
          <FloatingButton onClick={() => setIsOpen(!isOpen)} />
          {isOpen && <ChatWindow />}
        </>
      )}
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <ChatbotProvider>
        <BrowserRouter>
          <AppLayout />
        </BrowserRouter>
      </ChatbotProvider>
    </AuthProvider>
  );
}

export default App;
