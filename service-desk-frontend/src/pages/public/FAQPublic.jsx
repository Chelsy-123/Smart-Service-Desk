import { useEffect, useState } from "react";
import axios from "../../api/axios";

export default function FAQPublic() {
  const [faqs, setFaqs] = useState([]);
  const [openId, setOpenId] = useState(null);

  useEffect(() => {
    axios.get("/kb/faqs/")
      .then(res => setFaqs(res.data))
      .catch(err => console.error("FAQ fetch failed", err));
  }, []);

  const toggle = (id) => {
    setOpenId(openId === id ? null : id);
  };

  return (
    <div className="container mt-4">
      <h4 className="mb-3">Frequently Asked Questions</h4>

      <div className="accordion">
        {faqs.map(faq => (
          <div className="accordion-item mb-2" key={faq.id}>
  <div className="accordion-header d-flex justify-content-between align-items-center p-3">
    <span className="small fw-semibold">
      {faq.question}
    </span>

    <button
      className="btn btn-sm btn-outline-secondary"
      onClick={() => toggle(faq.id)}
    >
      {openId === faq.id ? "−" : "+"}
    </button>
  </div>

  {openId === faq.id && (
    <div className="accordion-body border-top p-3 small text-muted">
      {faq.answer}
    </div>
  )}
</div>

        ))}
      </div>
    </div>
  );
}
