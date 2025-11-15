import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style/SignIn.css";
export default function SignIn() {
  const [form, setForm] = useState({
    nickname: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate(); // 👈 Para redirigir

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://localhost:3000/api/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || "Error al iniciar sesión");
      }

      const data = await res.json();
      console.log("Login OK:", data);

      // redirigir al home (puede ser otra ruta)
      navigate("/");

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="signin-container">
      
      <h3>Sign In</h3>

      <form onSubmit={handleSubmit} >
        
        <input
          type="text"
          name="nickname"
          placeholder="Nickname"
          value={form.nickname}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        {error && <p style={{ color:"red" }}>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? "Ingresando..." : "Sign In"}
        </button>
      </form>

      {/* Botón SignUp */}
      <button
        onClick={() => navigate("/signup")}
        className="singup-btn"
      >
        ¿No tenés cuenta? Sign Up
      </button>

    </div>
  );
}
