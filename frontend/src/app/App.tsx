// App.tsx

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "../features/user-auth/LoginPage";
import ManagerDashboard from "../features/dashboard/ManagerDashboard";
import AnalystDashboard from "../features/dashboard/AnalystDashboard";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public route */}
        <Route path="/login" element={<LoginPage />} />

        {/* Manager-only route */}
        <Route
          path="/manager-dashboard"
          element={
            <ProtectedRoute allowedRoles={["manager"]}>
              <ManagerDashboard />
            </ProtectedRoute>
          }
        />

        {/* Analyst-only route */}
        <Route
          path="/analyst-dashboard"
          element={
            <ProtectedRoute allowedRoles={["analyst"]}>
              <AnalystDashboard />
            </ProtectedRoute>
          }
        />

        {/* Unauthorized page */}
        <Route path="/unauthorized" element={<h2>🚫 Unauthorized Access</h2>} />

        {/* Default fallback */}
        <Route path="*" element={<LoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;
