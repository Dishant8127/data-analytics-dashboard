// src/features/dashboard/components/FilterBar.tsx


import { useDispatch, useSelector } from "react-redux";
import type { RootState } from "../../../app/store";
import { setFilters, fetchKpis } from "../dashboardSlice";
import type { AppDispatch } from "../../../app/store";

const FilterBar = () => {
  const dispatch = useDispatch<AppDispatch>();
  const filters = useSelector((state: RootState) => state.dashboard.filters);

  const handleDateChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newFilters = { ...filters, dateRange: e.target.value };
    dispatch(setFilters(newFilters));
    dispatch(fetchKpis());
  };

  const handleRegionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newFilters = { ...filters, region: e.target.value };
    dispatch(setFilters(newFilters));
    dispatch(fetchKpis());
  };

  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
      {/* Date Range Filter */}
      <label>
        Date Range:
        <select value={filters.dateRange} onChange={handleDateChange}>
          <option value="last_7_days">Last 7 Days</option>
          <option value="last_30_days">Last 30 Days</option>
          <option value="last_90_days">Last 90 Days</option>
          <option value="year_to_date">Year to Date</option>
        </select>
      </label>

      {/* Region Filter */}
      <label>
        Region:
        <select value={filters.region} onChange={handleRegionChange}>
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

