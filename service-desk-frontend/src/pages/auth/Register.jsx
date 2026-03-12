import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../../api/auth.api";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
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
      await registerUser(form);
      alert("Registration successful. Please login.");
      navigate("/login");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.non_field_errors?.[0] ||
        err.response?.data?.detail ||
        "Registration failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "420px" }}>
      <h4 className="mb-3">User Registration</h4>

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

        <div className="mb-3">
          <label className="form-label small">Confirm Password</label>
          <input
            type="password"
            name="confirm_password"
            className="form-control form-control-sm"
            required
            value={form.confirm_password}
            onChange={handleChange}
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary btn-sm w-100"
          disabled={loading}
        >
          {loading ? "Registering..." : "Register"}
        </button>
      </form>
    </div>
  );
}
