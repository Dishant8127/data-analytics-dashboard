// authSlice.ts

import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  role: string | null;
}

const initialState: AuthState = {
  token: localStorage.getItem("token"),
  refreshToken: localStorage.getItem("refreshToken"),
  role: localStorage.getItem("role"),
};


const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
setCredentials: (
  state,
  action: PayloadAction<{ token: string; refreshToken: string; role: string }>
) => {
  state.token = action.payload.token;
  state.refreshToken = action.payload.refreshToken;
  state.role = action.payload.role;

  // ✅ Persist to localStorage
  localStorage.setItem("token", action.payload.token);
  localStorage.setItem("refreshToken", action.payload.refreshToken);
  localStorage.setItem("role", action.payload.role);
},

    logout: (state) => {
      state.token = null;
      state.refreshToken = null;
      state.role = null;
      localStorage.removeItem("token");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("role");
    },
  },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;
