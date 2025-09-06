import { useSelector } from "react-redux";
import type { RootState } from "../../../app/store";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const ChartWidget = () => {
  const { kpis, loading, error } = useSelector((state: RootState) => state.dashboard);

  if (loading) return <p>Loading chart...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!kpis.length) return <p>No KPI data available.</p>;

  return (
    <div style={{ width: "100%", height: 300, marginTop: "2rem" }}>
      <h3>Sales by Region</h3>
      <ResponsiveContainer>
        <BarChart data={kpis}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="region" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="total_sales" fill="#4f46e5" /> {/* Tailwind Indigo-600 */}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartWidget;
