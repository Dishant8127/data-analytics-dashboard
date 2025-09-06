import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "../features/user-auth/LoginPage";
import DashboardPage from "../features/dashboard/DashboardPage";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public route */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected route */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />

        {/* Default redirect to dashboard */}
        <Route path="*" element={<DashboardPage />} />
      </Routes>
    </Router>
  );
}

export default App;
