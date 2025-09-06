import { useDispatch, useSelector } from "react-redux";
import type       { RootState, AppDispatch } from "../../../app/store";
import { setFilters, fetchKpis } from "../dashboardSlice";

const FilterBar = () => {
  const dispatch = useDispatch<AppDispatch>();
  const filters = useSelector((state: RootState) => state.dashboard.filters);

  const handleChange = (field: "dateRange" | "region", value: string) => {
    // Update Redux filters
    const newFilters = { ...filters, [field]: value };
    dispatch(setFilters(newFilters));

    // ✅ Trigger API fetch with updated filters
    dispatch(fetchKpis());
  };

  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
      {/* Date Range Filter */}
      <label>
        Date Range:
        <select
          value={filters.dateRange}
          onChange={(e) => handleChange("dateRange", e.target.value)}
        >
          <option value="last_7_days">Last 7 Days</option>
          <option value="last_30_days">Last 30 Days</option>
          <option value="last_90_days">Last 90 Days</option>
          <option value="year_to_date">Year to Date</option>
        </select>
      </label>

      {/* Region Filter */}
      <label>
        Region:
        <select
          value={filters.region}
          onChange={(e) => handleChange("region", e.target.value)}
        >
          <option value="all">All</option>
          <option value="NA">North America</option>
          <option value="EU">Europe</option>
          <option value="APAC">Asia-Pacific</option>
        </select>
      </label>
    </div>
  );
};

export default FilterBar;
