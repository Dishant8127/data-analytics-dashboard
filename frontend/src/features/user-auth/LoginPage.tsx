// src/features/user-auth/LoginPage.tsx
import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import { setCredentials } from "./authSlice";

const LoginPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    try {
      const res = await api.post("/auth/login", { username, password });
      const { access_token, refresh_token, role } = res.data;

      if (access_token && refresh_token) {
        // Save tokens & role
        localStorage.setItem("token", access_token);
        localStorage.setItem("refreshToken", refresh_token);
        localStorage.setItem("role", role);

        // Update Redux
        dispatch(setCredentials({ token: access_token, refreshToken: refresh_token, role }));

        navigate("/dashboard"); // redirect
      } else {
        setErrorMsg("Invalid response from server.");
      }
    } catch (error: any) {
      if (error.response?.status === 401) {
        setErrorMsg("Invalid username or password.");
      } else {
        setErrorMsg("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div style={{
      maxWidth: "400px",
      margin: "4rem auto",
      padding: "2rem",
      borderRadius: "12px",
      backgroundColor: "#1a1a1a",
      color: "#fff",
      boxShadow: "0 4px 20px rgba(0,0,0,0.3)"
    }}>
      <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>Login</h2>
      <form onSubmit={handleLogin} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
          style={{ padding: "0.8rem", borderRadius: "8px", border: "1px solid #ccc", fontSize: "1rem" }}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          style={{ padding: "0.8rem", borderRadius: "8px", border: "1px solid #ccc", fontSize: "1rem" }}
        />
        <button type="submit" style={{
          padding: "0.8rem",
          borderRadius: "8px",
          backgroundColor: "#646cff",
          color: "#fff",
          fontWeight: "bold",
          fontSize: "1rem"
        }}>Login</button>
      </form>
      {errorMsg && <p style={{ color: "#ff6b6b", textAlign: "center", marginTop: "1rem" }}>{errorMsg}</p>}
    </div>
  );
};

export default LoginPage;
