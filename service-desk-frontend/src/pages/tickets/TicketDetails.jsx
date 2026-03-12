import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getTicketDetails,
  getTicketMessages,
  sendTicketMessage,
  updateTicketStatus,
  submitTicketFeedback,
  getTicketFeedback,
} from "../../api/tickets.api";
import { useAuth } from "../../context/AuthContext";

export default function TicketDetails() {
  const { id } = useParams();
  const { user } = useAuth(); // ✅ IMPORTANT
  const [ticket, setTicket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [rating, setRating] = useState(5);
  const [comments, setComment] = useState("");
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [feedback, setFeedback] = useState(null);





  useEffect(() => {
    async function loadData() {
      try {
        let ticketData;

        // ✅ ROLE-BASED API CALL
        if (user?.is_agent) {
          ticketData = await getTicketDetails(id);
        } else {
          ticketData = await getTicketDetails(id);
        }

        const messagesData = await getTicketMessages(id);

        setTicket(ticketData);
        setMessages(messagesData);
      } catch (err) {
        console.error("Failed to load ticket:", err);
      }
      try {
  const feedbackData = await getTicketFeedback(id);
  if (feedbackData.length > 0) {
    setFeedback(feedbackData[0]); // only one feedback exists
  }
} catch {
  // No feedback yet → do nothing
}

    }

    if (user) {
      loadData();
    }
  }, [id, user, ticket?.status]);

  const send = async () => {
    if (!text.trim()) return;

    await sendTicketMessage(id, text);
    setText("");
    setMessages(await getTicketMessages(id));
  };

  const changeStatus = async (newStatus) => {
  try {
    setUpdatingStatus(true);
    const updated = await updateTicketStatus(id, newStatus);
    setTicket(updated); // instant UI sync
  } catch (err) {
    console.error("Failed to update status", err);
    alert("Status update failed");
  } finally {
    setUpdatingStatus(false);
  }
};
  const submitFeedback = async () => {
  if (!comments.trim()) {
    alert("Please add a comment");
    return;
  }

  try {
    setSubmittingFeedback(true);

    await submitTicketFeedback(id, rating, comments);

    setFeedbackSubmitted(true);
    setFeedbackMessage("✅ Feedback submitted successfully. Thank you!");

    // Reload ticket (it will now be CLOSED)
    const updatedTicket = await getTicketDetails(id);
    setTicket(updatedTicket);
  } catch (err) {
    if (err.response?.status === 500) {
      // Feedback already exists
      setFeedbackSubmitted(true);
      setFeedbackMessage("✅ Feedback already submitted. Thank you!");
    } else {
      console.error("Feedback failed", err);
      alert("Failed to submit feedback");
    }
  } finally {
    setSubmittingFeedback(false);
  }
};



  if (!ticket) return <p>Loading ticket…</p>;

  return (
    <div className="container mt-4">
      <h5>Ticket ID {ticket.id}</h5>

      <p>
        <strong>Subject:</strong> {ticket.subject}
        <br />
        <strong>Description:</strong> {ticket.description}
        <br />
        <strong>Status:</strong>{" "}
        <span className={`badge ${
          ticket.status === "OPEN"
            ? "bg-secondary"
            : ticket.status === "IN_PROGRESS"
            ? "bg-warning"
            : "bg-success"
        }`}>
          {ticket.status}
        </span>
        <br />
        {user?.is_agent && ticket.status !== "CLOSED" && (
  <div className="mt-2">
    <label className="form-label fw-semibold">
      Update Status (Agent)
    </label>
    <select
      className="form-select"
      value={ticket.status}
      disabled={updatingStatus}
      onChange={(e) => changeStatus(e.target.value)}
    >
      <option value="OPEN">OPEN</option>
      <option value="IN_PROGRESS">IN_PROGRESS</option>
      <option value="RESOLVED">RESOLVED</option>
      <option value="CLOSED">CLOSED</option>
    </select>
  </div>
)}
        <br />
        <strong>Created:</strong>{" "}
        {new Date(ticket.created_at).toLocaleString()}
      </p>

      <hr />

      {/* Messages */}
      {messages.map((m) => (
        <div
          key={m.id}
          style={{
            textAlign: m.sender_type === "USER" ? "right" : "left",
            marginBottom: "12px",
          }}
        >
          <div style={{ fontWeight: 600 }}>
            {m.sender_type === "USER" ? "User" : m.sender}
          </div>
          <div>{m.message}</div>
          <small className="text-muted">
            {new Date(m.created_at).toLocaleString()}
          </small>
        </div>
      ))}
      {/* Feedback (User only) */}
{/* Feedback (User only) */}
{!user?.is_agent && ticket.status === "RESOLVED" && !feedbackSubmitted && (
  <div className="card mt-4">
    <div className="card-body">
      <h6 className="fw-bold">Give Feedback</h6>

      <label className="form-label">Rating</label>
      <select
        className="form-select"
        value={rating}
        onChange={(e) => setRating(Number(e.target.value))}
      >
        <option value={5}>⭐⭐⭐⭐⭐ Excellent</option>
        <option value={4}>⭐⭐⭐⭐ Good</option>
        <option value={3}>⭐⭐⭐ Average</option>
        <option value={2}>⭐⭐ Poor</option>
        <option value={1}>⭐ Very Bad</option>
      </select>

      <label className="form-label mt-2">Comment</label>
      <textarea
        className="form-control"
        rows="3"
        value={comments}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Tell us about your experience..."
      />

      <button
        className="btn btn-success mt-3"
        disabled={submittingFeedback}
        onClick={submitFeedback}
      >
        Submit Feedback
      </button>
    </div>
  </div>
)}

{/* Feedback success message */}
{feedbackSubmitted && (
  <div className="alert alert-success mt-4">
    {feedbackMessage}
  </div>
)}
{/* Feedback (Agent View) */}
{user?.is_agent && feedback && (
  <div className="card mt-4 border-success">
    <div className="card-body">
      <h6 className="fw-bold text-success">User Feedback</h6>

      <p>
        <strong>Rating:</strong>{" "}
        {"⭐".repeat(feedback.rating)}
      </p>

      <p>
        <strong>Comment:</strong><br />
        {feedback.comments || "_No comment provided._"}
      </p>
      <small className="text-muted">
  Submitted on{" "}
  {feedback.submitted_at
    ? new Date(feedback.submitted_at).toLocaleString()
    : "—"}
</small>
    </div>
  </div>
)}

      {/* Send message */}
      {ticket.status !== "CLOSED" && (
        <>
          <textarea
            className="form-control mt-3"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Add more details…"
          />
          <button className="btn btn-primary mt-2" onClick={send}>
            Send
          </button>
        </>
      )}
    </div>
  );
}
