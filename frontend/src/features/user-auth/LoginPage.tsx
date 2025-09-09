// src/features/user-auth/LoginPage.tsx

import { useState } from "react";
import { useDispatch } from "react-redux";
import api from "../../services/api";
import { setCredentials } from "./authSlice";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null); // clear old error before new attempt
    try {
      const res = await api.post("/auth/login", { username, password });

      // ✅ Only run if login succeeded
      if (res.data?.access_token) {
        dispatch(
          setCredentials({
            token: res.data.access_token,
            refreshToken: res.data.refresh_token,
            role: res.data.role,
          })
        );
        navigate("/dashboard");
      } else {
        setError("Unexpected response from server.");
      }
    } catch (err: any) {
      // ✅ Show error only once
      if (!error) {
        setError(err.response?.data?.msg || "Login failed. Check username/password.");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto", padding: "1.5rem", border: "1px solid #ddd", borderRadius: "8px" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>

      {/* ✅ Error shows once */}
      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
    </div>
  );
};

export default LoginPage;

