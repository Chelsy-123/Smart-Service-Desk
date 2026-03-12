import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (!user) {
    // Not logged in
    return <Navigate to="/login" replace />;
  }

  // Role-based access (optional)
  if (roles && roles.length > 0) {
    // ADMIN check
    if (roles.includes("ADMIN") && !(user.is_staff || user.is_superuser)) {
      return <Navigate to="/" replace />;
    }

    // AGENT check
    if (roles.includes("AGENT") && !user.is_staff) {
      return <Navigate to="/" replace />;
    }
  }

  return children;
}
