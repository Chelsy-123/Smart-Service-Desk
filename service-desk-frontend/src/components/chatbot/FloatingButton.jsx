const FloatingButton = ({ onClick }) => {
  return (
    <button
      className="btn btn-dark rounded-circle position-fixed"
      style={{
        bottom: "20px",
        right: "20px",
        width: "60px",
        height: "60px",
        zIndex: 1051
      }}
      onClick={onClick}
    >
      💬
    </button>
  );
};

export default FloatingButton;
