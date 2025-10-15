// src\features\dashboard\ManagerDashboard.tsx
import { useEffect } from "react";
import { useAppDispatch } from "../../app/hooks";
import { fetchKpis } from "./dashboardSlice";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";
import api from "../../services/api";

const ManagerDashboard = () => {
  // const dispatch = useDispatch();
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchKpis());
  }, [dispatch]);

  const handleDownloadPDF = async () => {
    try {
      const response = await api.get("/api/generate-pdf", { responseType: "blob" })
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "manager_report.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to download PDF report");
    }
  };

  return (
    <div>
      <h2>📊 Manager Dashboard</h2>
      <p style={{ color: "gray" }}>High-level overview for strategic decision-making</p>

      {/* KPI summary row */}
      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <KPIWidget title="Total Sales (YTD)" value="$12.4M" />
        <KPIWidget title="New Customers" value="3,245" />
        <KPIWidget title="Churn Rate" value="4.2%" />
      </div>

      {/* High-level chart */}
      <ChartWidget />

      {/* PDF report */}
      <div style={{ marginTop: "2rem" }}>
        <h3>📑 Reports</h3>
        <button onClick={handleDownloadPDF}>Download Weekly PDF Report</button>
      </div>
    </div>
  );
};

export default ManagerDashboard;
