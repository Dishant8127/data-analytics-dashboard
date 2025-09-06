import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import api from "../../services/api";

interface KPIData {
  region: string;
  total_sales: number;
}

interface DashboardState {
  kpis: KPIData[];
  loading: boolean;
  error: string | null;
  filters: {
    dateRange: string;  
    region: string;
  };
}

const initialState: DashboardState = {
  kpis: [],
  loading: false,
  error: null,
  filters: {
    dateRange: "last_30_days",
    region: "all",
  },
};

// ✅ Async action: fetch KPI summary with filters
export const fetchKpis = createAsyncThunk(
  "dashboard/fetchKpis",
  async (_, thunkAPI) => {
    try {
      const state: any = thunkAPI.getState();
      const { dateRange, region } = state.dashboard.filters;

      // Send filters as query params
      const res = await api.get("/kpi-summary", {
        params: { dateRange, region },
      });

      return res.data;
    } catch (err: any) {
      return thunkAPI.rejectWithValue(
        err.response?.data?.msg || "Failed to fetch KPIs"
      );
    }
  }
);

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {
    setFilters: (
      state,
      action: PayloadAction<{ dateRange: string; region: string }>
    ) => {
      state.filters = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchKpis.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchKpis.fulfilled, (state, action: PayloadAction<KPIData[]>) => {
        state.loading = false;
        state.kpis = action.payload;
      })
      .addCase(fetchKpis.rejected, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { setFilters } = dashboardSlice.actions;
export default dashboardSlice.reducer;


