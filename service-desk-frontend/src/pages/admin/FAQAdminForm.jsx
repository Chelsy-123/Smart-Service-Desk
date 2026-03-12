import { useEffect, useState } from "react";
import { createFAQ, updateFAQ } from "../../api/kb.api";
import axios from "../../api/axios";
import { useNavigate, useParams } from "react-router-dom";

export default function FAQAdminForm() {
  const { id } = useParams(); // 👈 NEW
  const navigate = useNavigate();

  const [form, setForm] = useState({
    question: "",
    answer: "",
    category: "",
    is_active: true,
  });

  // 👇 LOAD FAQ WHEN EDITING
  useEffect(() => {
    if (id) {
      axios.get(`/kb/faqs/${id}/`).then((res) => {
        setForm(res.data);
      });
    }
  }, [id]);

  const submit = async () => {
    if (id) {
      await updateFAQ(id, form);
    } else {
      await createFAQ(form);
    }
    navigate("/admin/faqs");
  };

  return (
    <div className="container mt-4" style={{ maxWidth: 600 }}>
      <h4>{id ? "Edit FAQ" : "Create FAQ"}</h4>

      <input
        className="form-control mb-2"
        placeholder="Question"
        value={form.question}
        onChange={(e) =>
          setForm({ ...form, question: e.target.value })
        }
      />

      <textarea
        className="form-control mb-2"
        placeholder="Answer"
        rows="4"
        value={form.answer}
        onChange={(e) =>
          setForm({ ...form, answer: e.target.value })
        }
      />

      <input
        className="form-control mb-2"
        placeholder="Category (IT / HR / FAC)"
        value={form.category}
        onChange={(e) =>
          setForm({ ...form, category: e.target.value })
        }
      />

      <div className="form-check mb-3">
        <input
          type="checkbox"
          className="form-check-input"
          checked={form.is_active}
          onChange={(e) =>
            setForm({ ...form, is_active: e.target.checked })
          }
        />
        <label className="form-check-label small">
          Active (visible to users)
        </label>
      </div>

      <button className="btn btn-success btn-sm" onClick={submit}>
        Save FAQ
      </button>
    </div>
  );
}
