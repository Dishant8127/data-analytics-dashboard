// RoleRedirect.tsx

import { useSelector } from "react-redux";
import type { RootState } from "./store";
import { Navigate } from "react-router-dom";

const RoleRedirect = () => {
  const { token, role } = useSelector((state: RootState) => state.auth);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (role === "manager") {
    return <Navigate to="/manager-dashboard" replace />;
  }

  if (role === "analyst") {
    return <Navigate to="/analyst-dashboard" replace />;
  }

  return <Navigate to="/unauthorized" replace />;
};

export default RoleRedirect;
