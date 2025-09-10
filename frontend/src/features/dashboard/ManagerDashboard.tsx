import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";

const ManagerDashboard = () => {
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

      {/* PDF report (mock placeholder for now) */}
      <div style={{ marginTop: "2rem" }}>
        <h3>📑 Reports</h3>
        <button onClick={() => alert("Report generated!")}>
          Download Weekly PDF Report
        </button>
      </div>
    </div>
  );
};

export default ManagerDashboard;
