export default function FAQCard({ faq }) {
  return (
    <div className="card mb-3">
      <div className="card-body">
        <h6 className="fw-semibold small mb-0">{faq.question}</h6>
        <p className="mb-0">{faq.answer}</p>
        <small className="text-muted">
          Category: {faq.category}
        </small>
      </div>
    </div>
  );
}
