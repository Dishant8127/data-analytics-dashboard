// src/ProtectedRoute.tsx


import { useSelector } from "react-redux";
import type { RootState } from "./store";
import { Navigate } from "react-router-dom";

interface Props {
  children: React.ReactNode;
  allowedRoles?: string[]; //  optional role restriction
}

const ProtectedRoute = ({ children, allowedRoles }: Props) => {
  const { token, role } = useSelector((state: RootState) => state.auth);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  //  If route requires specific roles → check
  if (allowedRoles && !allowedRoles.includes(role || "")) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default ProtectedRoute;

