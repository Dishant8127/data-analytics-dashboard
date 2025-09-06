import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../../app/store";
import { fetchKpis } from "./dashboardSlice";
import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";

const DashboardPage = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

  // ✅ Fetch KPIs when page first loads
  useEffect(() => {
    dispatch(fetchKpis());
  }, [dispatch]);

  return (
    <div>
      <h2>Dashboard</h2>
      <FilterBar />

      {loading && <p>Loading KPIs...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* KPI Widgets */}
      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        {kpis.map((kpi, idx) => (
          <KPIWidget
            key={idx}
            title={`Sales (${kpi.region})`}
            value={`$${kpi.total_sales.toLocaleString()}`}
          />
        ))}
      </div>

      {/* Chart */}
      <ChartWidget />
    </div>
  );
};

export default DashboardPage;
