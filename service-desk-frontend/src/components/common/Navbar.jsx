import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  console.log("NAVBAR USER:", user);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">
          Smart Service Desk
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navMenu"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navMenu">
          <ul className="navbar-nav ms-auto">
  {user ? (
    <>
      <li className="nav-item">
        <Link className="nav-link" to="/">
          Dashboard
        </Link>
      </li>

      <li className="nav-item">
        <button
          className="btn btn-sm btn-outline-light ms-3"
          onClick={handleLogout}
        >
          Logout
        </button>
      </li>
    </>
  ) : (
    <>
      <li className="nav-item">
        <Link className="nav-link" to="/login">
          Login
        </Link>
      </li>

      <li className="nav-item">
        <Link className="nav-link" to="/register">
          Register
        </Link>
      </li>
    </>
  )}
</ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
