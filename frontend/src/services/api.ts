// src/services/api.ts



import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/", // root backend
  headers: { "Content-Type": "application/json" },
});

// Request interceptor → attach token if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor → refresh token if 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    //  Skip refresh logic for login/refresh endpoints
    if (originalRequest.url.includes("/auth/login") || originalRequest.url.includes("/auth/refresh")) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // mark request to avoid infinite loop

      const refreshToken = localStorage.getItem("refreshToken");
      if (refreshToken) {
        try {
          const refreshRes = await axios.post("http://localhost:5000/auth/refresh", {}, {
            headers: { Authorization: `Bearer ${refreshToken}` },
          });

          const newAccessToken = refreshRes.data.access_token;
          localStorage.setItem("token", newAccessToken);

          //  Update original request with new token
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
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


