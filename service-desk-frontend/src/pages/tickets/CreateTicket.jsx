import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createTicket } from "../../api/tickets.api";

export default function CreateTicket() {
  const navigate = useNavigate();

  const [subject, setSubject] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!subject.trim() || !description.trim()) {
      alert("Subject and description are required");
      return;
    }

    try {
      setLoading(true);
      await createTicket({ subject, description });
      navigate("/tickets"); // back to My Tickets
    } catch (err) {
      console.error("Ticket creation failed", err);
      alert("Failed to create ticket");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h4>Create Ticket</h4>

      <label className="form-label mt-3">Subject</label>
      <input
        className="form-control"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        placeholder="Short summary"
      />

      <label className="form-label mt-3">Description</label>
      <textarea
        className="form-control"
        rows="5"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Describe your issue..."
      />

      <button
        className="btn btn-success mt-3"
        disabled={loading}
        onClick={submit}
      >
        Create Ticket
      </button>
    </div>
  );
}
