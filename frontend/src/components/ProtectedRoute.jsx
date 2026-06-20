import { Navigate } from "react-router-dom";
import { isLoggedIn } from "../lib/auth";

function ProtectedRoute({ children }) {
  if (!isLoggedIn()) {
    return <Navigate to="/login" />;
  }
  return children;
}

export default ProtectedRoute;
