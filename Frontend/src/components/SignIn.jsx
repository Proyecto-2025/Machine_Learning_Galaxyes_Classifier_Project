import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./style/SignIn.css";
export default function SignIn() {
  const [form, setForm] = useState({
    username: "",
    email:"",
    password: ""
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate(); //Para redirigir al SignUp

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      // opcional: podrías validar/decodificar el token aquí
      navigate("/"); // o la ruta que quieras proteger
    }
  }, [navigate]);

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
        const res = await fetch("https://galaxybackend-pwdu.onrender.com/api/v1/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(form), // form = { nickname, password }
        });

        // Si el backend devuelve 4xx/5xx, intentamos leer el mensaje
        if (!res.ok) {
            // si el backend envía JSON con message, lo mostramos
            let errMsg = "Error en el login";
            try {
            const errData = await res.json();
            if (errData && errData.message) errMsg = errData.message;
            } catch (jsonErr) {
            // no es JSON -> dejamos errMsg por defecto
            }
            throw new Error(errMsg);
        }

        // respuesta OK: esperamos JSON con token
        const data = await res.json();

        if (!data || !data.token) {
            throw new Error("Respuesta inválida del servidor (no hay token).");
        }

        // Guardar token (localStorage para una app simple)
        localStorage.setItem("token", data.token);

        // Opcional: guardar datos del usuario si vienen en la respuesta
        if(data.user){
            localStorage.setItem("user", JSON.stringify(data.user));
        }

        // Redirigir a la página principal (o dashboard)
        navigate("/");

    } catch (err) {
        console.error("Login error:", err);
        setError(err.message || "Error al iniciar sesión");
    } finally {
        setLoading(false);
    }
  }

  return (
    <div className="signin-container">
      
      <h3>Sign In as user</h3>

      <form onSubmit={handleSubmit} className="form">
        
        <input
          type="text"
          name="username"
          placeholder="username"
          value={form.username}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="email"
          placeholder="email"
          value={form.email}
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

        <button type="submit" disabled={loading}  className="register-btn">
          {loading ? "Ingresando..." : "Sign In"}
        </button>
      </form>

      {/* Botón SignUp */}
      <button
        onClick={() => navigate("/signup")}
        className="register-btn" id="signup-btn"
      >
        No Account? Sign Up
      </button>

    </div>
  );
}
