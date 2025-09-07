// // src/components/DashboardPage.tsx


import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../../app/store";
import { fetchKpis } from "./dashboardSlice";
import { logout } from "../user-auth/authSlice";
import { useNavigate } from "react-router-dom";
import FilterBar from "./components/FilterBar";
import KPIWidget from "./components/KPIWidget";
import ChartWidget from "./components/ChartWidget";

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
    <div style={{ padding: "2rem", minHeight: "100vh", backgroundColor: "var(--background-color)", color: "var(--color)", fontFamily: "system-ui, sans-serif" }}>
      
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "2rem" }}>
        <h2>Dashboard</h2>
        <button onClick={handleLogout} style={{
          padding: "0.5rem 1rem",
          borderRadius: "8px",
          border: "none",
          backgroundColor: "#646cff",
          color: "#fff",
          cursor: "pointer",
          fontWeight: "bold",
          transition: "background 0.2s"
        }}
        onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#535bf2"}
        onMouseOut={(e) => e.currentTarget.style.backgroundColor = "#646cff"}
        >
          Logout
        </button>
      </div>

      <FilterBar />

      {loading && <p>Loading KPIs...</p>}
      {error && <p style={{ color: "#ff6b6b" }}>{error}</p>}

      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginTop: "1rem" }}>
        {kpis.map((kpi, idx) => (
          <KPIWidget key={idx} title={`Sales (${kpi.region})`} value={`$${kpi.total_sales.toLocaleString()}`} />
        ))}
      </div>

      <div style={{ marginTop: "2rem" }}>
        <ChartWidget />
      </div>
    </div>
  );
};

export default DashboardPage;









// import { useEffect } from "react";
// import { useDispatch, useSelector } from "react-redux";
// import type { RootState, AppDispatch } from "../../app/store";
// import { fetchKpis } from "./dashboardSlice";
// import { logout } from "../user-auth/authSlice"; // ✅ import logout
// import { useNavigate } from "react-router-dom";  // ✅ import useNavigate
// import FilterBar from "./components/FilterBar";
// import KPIWidget from "./components/KPIWidget";
// import ChartWidget from "./components/ChartWidget";

// const DashboardPage = () => {
//   const dispatch = useDispatch<AppDispatch>();
//   const navigate = useNavigate(); // ✅ navigation
//   const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

//   useEffect(() => {
//     dispatch(fetchKpis());
//   }, [dispatch]);

//   const handleLogout = () => {
//     dispatch(logout()); // clear token & role from Redux + localStorage
//     navigate("/login"); // redirect to login page
//   };

//   return (
//     <div style={{ padding: "1rem" }}>
//       <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
//         <h2>Dashboard</h2>
//         <button onClick={handleLogout} style={{ padding: "0.5rem 1rem", cursor: "pointer" }}>
//           Logout
//         </button>
//       </div>

//       <FilterBar />

//       {loading && <p>Loading KPIs...</p>}
//       {error && <p style={{ color: "red" }}>{error}</p>}

//       <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginTop: "1rem" }}>
//         {kpis.map((kpi, idx) => (
//           <KPIWidget
//             key={idx}
//             title={`Sales (${kpi.region})`}
//             value={`$${kpi.total_sales.toLocaleString()}`}
//           />
//         ))}
//       </div>

//       <div style={{ marginTop: "2rem" }}>
//         <ChartWidget />
//       </div>
//     </div>
//   );
// };

// export default DashboardPage;