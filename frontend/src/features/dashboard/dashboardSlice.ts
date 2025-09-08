// src/features/dashboard/dashboardSlice.ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import api from "../../services/api";

export type KPI = {
  region: string;
  total_sales: number;
};

type DashboardState = {
  kpis: KPI[];
  loading: boolean;
  error: string | null;
};

const initialState: DashboardState = {
  kpis: [],
  loading: false,
  error: null,
};

// ✅ Async thunk to fetch KPIs with optional filters
export const fetchKpis = createAsyncThunk(
  "dashboard/fetchKpis",
  async (
    filters: { dateRange?: string; region?: string } = {},
    { rejectWithValue }
  ) => {
    try {
      const params = new URLSearchParams();
      if (filters.dateRange) params.append("dateRange", filters.dateRange);
      if (filters.region) params.append("region", filters.region);

      const res = await api.get(`/api/kpi-summary?${params.toString()}`);
      return res.data as KPI[];
    } catch (err: any) {
      console.error("KPI fetch failed:", err);
      return rejectWithValue(
        err.response?.data?.message || "Network Error"
      );
    }
  }
);

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchKpis.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchKpis.fulfilled, (state, action) => {
        state.loading = false;
        state.kpis = action.payload;
      })
      .addCase(fetchKpis.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default dashboardSlice.reducer;
