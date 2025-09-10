


import { useSelector } from "react-redux";
import type { RootState } from "../../app/store";
import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";
import api from "../../services/api"; // <-- assuming you have an axios instance setup

const AnalystDashboard = () => {
  const { kpis, loading, error, filters } = useSelector((state: RootState) => state.dashboard);

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






// import { useSelector } from "react-redux";
// import type { RootState } from "../../app/store";
// import FilterBar from "./components/FilterBar";
// import KPIWidget from "./components/KPIWidget";
// import ChartWidget from "./components/ChartWidget";

// const AnalystDashboard = () => {
//   const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

//   const handleExportCSV = () => {
//     // Mock CSV export (later we’ll call Flask /export endpoint)
//     const csvContent =
//       "region,total_sales\n" +
//       kpis.map((k) => `${k.region},${k.total_sales}`).join("\n");

//     const blob = new Blob([csvContent], { type: "text/csv" });
//     const url = URL.createObjectURL(blob);

//     const a = document.createElement("a");
//     a.href = url;
//     a.download = "kpi_export.csv";
//     a.click();
//     URL.revokeObjectURL(url);
//   };

//   return (
//     <div>
//       <h2>🔎 Analyst Dashboard</h2>
//       <p style={{ color: "gray" }}>Deep dive filters, drill-downs, and exports</p>

//       {/* Filters */}
//       <FilterBar />

//       {loading && <p>Loading KPIs...</p>}
//       {error && <p style={{ color: "red" }}>{error}</p>}

//       {/* KPI Widgets */}
//       <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
//         {kpis.map((kpi, idx) => (
//           <KPIWidget
//             key={idx}
//             title={`Sales (${kpi.region})`}
//             value={`$${kpi.total_sales.toLocaleString()}`}
//           />
//         ))}
//       </div>

//       {/* Chart */}
//       <ChartWidget />

//       {/* CSV Export */}
//       <div style={{ marginTop: "2rem" }}>
//         <button onClick={handleExportCSV}>📥 Export CSV</button>
//       </div>
//     </div>
//   );
// };

// export default AnalystDashboard;
