// App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import type { RootState } from "./app/store";
import LoginPage from "./features/user-auth/LoginPage";
import DashboardPage from "./features/dashboard/DashboardPage";

function App() {
  const token = useSelector((state: RootState) => state.auth.token);

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={token ? <Navigate to="/dashboard" /> : <LoginPage />}
        />
        <Route
          path="/dashboard"
          element={token ? <DashboardPage /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
