const FeatureCard = ({ icon, title, description, onClick }) => {
  return (
    <div className="col-md-4 mb-4">
      <div
        className="card shadow-sm h-100 text-center dashboard-card"
        style={{ cursor: "pointer" }}
        onClick={onClick}
      >
        <div className="card-body">

          <div style={{ fontSize: "2rem" }}>
            {icon}
          </div>

          <h5 className="card-title mt-2">
            {title}
          </h5>

          <p className="card-text text-muted">
            {description}
          </p>

        </div>
      </div>
    </div>
  );
};

export default FeatureCard;