// frontend/src/features/dashboard/AnalystDashboard.tsx

import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "../../app/hooks"; // typed dispatch
import { fetchKpis } from "./dashboardSlice";
import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";
import api from "../../services/api";


const AnalystDashboard = () => {
  const dispatch = useAppDispatch();
  const { kpis, loading, error, filters } = useAppSelector((state) => state.dashboard);


  //  Fetch KPIs on mount
  useEffect(() => {
    dispatch(fetchKpis());
  }, [dispatch]);

  const handleExportCSV = async () => {
    try {
      const { dateRange, region } = filters; // from Redux
      const response = await api.get("/api/export-csv", {
        params: { dateRange, region },
        responseType: "blob", // Important for CSV
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "kpi_export.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("CSV export failed");
    }
  };

  return (
    <div>
      <h2>🔎 Analyst Dashboard</h2>
      <p style={{ color: "gray" }}>Deep dive filters, drill-downs, and exports</p>

      {/* Filters */}
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

      {/* CSV Export */}
      <div style={{ marginTop: "2rem" }}>
        <button onClick={handleExportCSV}>📥 Export CSV</button>
      </div>
    </div>
  );
};

export default AnalystDashboard;
