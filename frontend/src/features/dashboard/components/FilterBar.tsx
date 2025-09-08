// src/features/dashboard/components/FilterBar.tsx
import { useState } from "react";
import { useDispatch } from "react-redux";
import { fetchKpis } from "../dashboardSlice";
import type { AppDispatch } from "../../../app/store";

const FilterBar = () => {
  const dispatch = useDispatch<AppDispatch>();

  const [dateRange, setDateRange] = useState("last_30_days");
  const [region, setRegion] = useState("all");

  const handleDateChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newDateRange = e.target.value;
    setDateRange(newDateRange);
    dispatch(fetchKpis({ dateRange: newDateRange, region }));
  };

  const handleRegionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newRegion = e.target.value;
    setRegion(newRegion);
    dispatch(fetchKpis({ dateRange, region: newRegion }));
  };

  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
      <div>
        <label>Date Range: </label>
        <select value={dateRange} onChange={handleDateChange}>
          <option value="last_7_days">Last 7 Days</option>
          <option value="last_30_days">Last 30 Days</option>
          <option value="last_90_days">Last 90 Days</option>
        </select>
      </div>

      <div>
        <label>Region: </label>
        <select value={region} onChange={handleRegionChange}>
          <option value="all">All</option>
          <option value="NA">NA</option>
          <option value="EU">EU</option>
          <option value="APAC">APAC</option>
        </select>
      </div>
    </div>
  );
};

export default FilterBar;
