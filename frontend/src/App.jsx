import { Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Feed from "./pages/Feed";
import { isLoggedIn } from "./lib/auth";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          isLoggedIn() ? <Navigate to="/feed" /> : <Navigate to="/login" />
        }
      />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route
        path="/feed"
        element={
          <ProtectedRoute>
            <Feed />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;
