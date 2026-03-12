import { useEffect, useState } from "react";
import { getAllFAQsAdmin, deleteFAQ } from "../../api/kb.api";
import { Link } from "react-router-dom";

export default function FAQAdminList() {
  const [faqs, setFaqs] = useState([]);

  const load = async () => {
    setFaqs(await getAllFAQsAdmin());
  };

  useEffect(() => {
    load();
  }, []);

  const remove = async (id) => {
    if (!window.confirm("Delete this FAQ?")) return;
    await deleteFAQ(id);
    load();
  };

  return (
    <div className="container mt-4">
      <h4>Manage FAQs</h4>

      <Link to="/admin/faqs/new" className="btn btn-primary mb-3">
        + Add FAQ
      </Link>

      {faqs.map((faq) => (
        <div key={faq.id} className="card mb-2">
          <div className="card-body">
            <span className="fw-semibold small mb-0">{faq.question}</span>
            <div className="mt-2">
              <Link
                to={`/admin/faqs/${faq.id}`}
                className="btn btn-sm btn-warning me-2"
              >
                Edit
              </Link>
              <button
                className="btn btn-sm btn-danger"
                onClick={() => remove(faq.id)}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
