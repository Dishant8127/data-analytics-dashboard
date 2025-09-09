// ProtectedRoutx.tsx

import { useSelector } from "react-redux";
import type { RootState } from "./store";   // ✅ use type-only import
import { Navigate } from "react-router-dom";
import type React from "react";

interface Props {
  children: React.ReactNode;                    // ✅ JSX.Element recognized when react types installed
}

const ProtectedRoute = ({ children }: Props) => {
  const { token } = useSelector((state: RootState) => state.auth);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
