import { useSelector } from "react-redux";
import type { RootState } from "./store"; // type-only import ✅
import { Navigate } from "react-router-dom";

interface Props {
  children: React.ReactNode; // ✅ works instead of JSX.Element
}

const ProtectedRoute = ({ children }: Props) => {
  const { token } = useSelector((state: RootState) => state.auth);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
