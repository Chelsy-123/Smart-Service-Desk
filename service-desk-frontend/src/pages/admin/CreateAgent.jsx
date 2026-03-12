import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createAgent } from "../../api/auth.api";
export default function CreateAgent() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    agent_name: "",
    department: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
        await createAgent(form);

      alert("Agent created successfully");
      navigate("/");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        "Failed to create agent"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4" style={{ maxWidth: "520px" }}>
      <h4 className="mb-3">Create Agent</h4>

      {error && <div className="alert alert-danger small">{error}</div>}

      <form onSubmit={submit}>
        <div className="mb-3">
          <label className="form-label small">Username</label>
          <input
            type="text"
            name="username"
            className="form-control form-control-sm"
            required
            value={form.username}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label className="form-label small">Agent Name</label>
          <input
            type="text"
            name="agent_name"
            className="form-control form-control-sm"
            required
            value={form.agent_name}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label className="form-label small">Email</label>
          <input
            type="email"
            name="email"
            className="form-control form-control-sm"
            required
            value={form.email}
            onChange={handleChange}
          />
        </div>

        <div className="mb-3">
          <label className="form-label small">Department</label>
          <select
            name="department"
            className="form-select form-select-sm"
            required
            value={form.department}
            onChange={handleChange}
          >
            <option value="">Select department</option>
            <option value="IT">IT</option>
            <option value="HR">HR</option>
            <option value="FINANCE">FINANCE</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label small">Password</label>
          <input
            type="password"
            name="password"
            className="form-control form-control-sm"
            required
            value={form.password}
            onChange={handleChange}
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary btn-sm"
          disabled={loading}
        >
          {loading ? "Creating..." : "Create Agent"}
        </button>
      </form>
    </div>
  );
}
