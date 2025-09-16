// src/features/dashboard/DashboardPage.tsx

import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../../app/store";  //  type-only import
import { fetchKpis } from "./dashboardSlice";
import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";
import { useNavigate } from "react-router-dom";
import { logout } from "../user-auth/authSlice";

const DashboardPage = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

  useEffect(() => {
    dispatch(fetchKpis());
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  return (
    <div style={{ padding: "1rem" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h2>Dashboard</h2>
        <button
          onClick={handleLogout}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#f44336",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </header>

      <FilterBar />

      {loading && <p>Loading KPIs...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginTop: "1rem" }}>
        {kpis.map((kpi) => (
          <KPIWidget
            key={kpi.region}  //  use region if id doesn’t exist
            title={`Sales (${kpi.region})`}
            value={`$${kpi.total_sales.toLocaleString()}`}
          />
        ))}
      </div>

      <div style={{ marginTop: "2rem" }}>
        <ChartWidget />
      </div>
    </div>
  );
};

export default DashboardPage;
