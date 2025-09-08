// src/features/dashboard/DashboardPage.tsx
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import type { RootState, AppDispatch } from "../../app/store";
import { fetchKpis } from "./dashboardSlice";
import { logout } from "../user-auth/authSlice";

import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";

const DashboardPage = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

  // Fetch default KPIs on load
  useEffect(() => {
    dispatch(fetchKpis({ dateRange: "last_30_days", region: "all" }));
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  return (
    <div style={{ padding: "2rem", minHeight: "100vh", backgroundColor: "var(--background-color)", color: "var(--color)" }}>
      
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h2>Dashboard</h2>
        <button
          onClick={handleLogout}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#646cff",
            color: "#fff",
            cursor: "pointer",
            fontWeight: "bold",
            transition: "background 0.2s",
          }}
          onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#535bf2")}
          onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#646cff")}
        >
          Logout
        </button>
      </div>

      {/* Filters */}
      <FilterBar />

      {/* KPI Loading/Error */}
      {loading && <p>Loading KPIs...</p>}
      {error && (
        <div
          style={{
            backgroundColor: "#ffe6e6",
            color: "#cc0000",
            padding: "1rem",
            borderRadius: "8px",
            border: "1px solid #ff6b6b",
            marginTop: "1rem",
            fontWeight: "bold",
          }}
        >
          ⚠️ {error}
        </div>
      )}

      {/* KPI Widgets */}
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginTop: "1rem" }}>
        {kpis.map((kpi, idx) => (
          <KPIWidget key={idx} title={`Sales (${kpi.region})`} value={`$${kpi.total_sales.toLocaleString()}`} />
        ))}
      </div>

      {/* Chart */}
      <div style={{ marginTop: "2rem" }}>
        <ChartWidget />
      </div>
    </div>
  );
};

export default DashboardPage;
