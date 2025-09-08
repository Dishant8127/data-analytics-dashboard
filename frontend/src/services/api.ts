// src/services/api.ts
import axios from "axios";

// Base Axios instance
const api = axios.create({
  baseURL: "http://localhost:5000", // 🔹 backend root (not /api)
  headers: { "Content-Type": "application/json" },
});

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (optional refresh token flow)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refreshToken");
      if (refreshToken) {
        try {
          const refreshRes = await axios.post(
            "http://localhost:5000/auth/refresh",
            {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          );

          const newAccessToken = refreshRes.data.access_token;
          localStorage.setItem("token", newAccessToken);
          originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
          return api.request(originalRequest);
        } catch (refreshError) {
          console.error("Refresh token expired → logging out");
          localStorage.clear();
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
