// App.tsx




import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "../src/features/user-auth/LoginPage";
import DashboardPage from "../src/features/dashboard/DashboardPage";
import ProtectedRoute from "../src/app/ProtectedRoute";

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








// import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// import { useSelector } from "react-redux";
// import type { RootState } from "./app/store";
// import LoginPage from "./features/user-auth/LoginPage";
// import DashboardPage from "./features/dashboard/DashboardPage";

// function App() {
//   const token = useSelector((state: RootState) => state.auth.token);

//   return (
//     <Router>
//       <Routes>
//         <Route
//           path="/login"
//           element={token ? <Navigate to="/dashboard" /> : <LoginPage />}
//         />
//         <Route
//           path="/dashboard"
//           element={token ? <DashboardPage /> : <Navigate to="/login" />}
//         />
//         <Route path="*" element={<Navigate to="/login" />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;
