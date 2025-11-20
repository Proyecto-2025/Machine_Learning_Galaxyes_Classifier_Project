import { useState , useEffect } from "react";
import "./style/SignIn.css"
import { useNavigate } from "react-router-dom";
export default function SignUp() {
  const [form, setForm] = useState({
    username: "",
    email:"",
    password: "",
    confirmPass: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const navigate = useNavigate();
  // Si ya existe un token, no tiene sentido registrar
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) navigate("/");
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
    setError("");
    setSuccessMsg("");
    setLoading(true);
    if (form.password !== form.confirmPass) {
      setError("Las contraseñas no coinciden");
      setLoading(false);
      return;
    }
    try {
      const res = await fetch("https://galaxybackend-pwdu.onrender.com/api/v1/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        username: form.username,
        email: form.email,
        password: form.password
      })
      });

      if (!res.ok) {
        let msg = "Error al registrar";
        try {
          const info = await res.json();
          if (info.error) msg = info.error;
          if(info.message) msg = info.message;
          console.log("Backend error:", info);

        } catch {}
        throw new Error(msg);
      }

      const data = await res.json();

      // El backend puede devolver success, user o mensaje
      setSuccessMsg("Usuario registrado correctamente. Ahora inicia sesión.");
      console.log(successMsg);
      setForm({ username: "",email:"", password: "",confirmPass:"", });

      // Esperar 1 segundo y llevar a SignIn
      setTimeout(() => navigate("/signin"), 1000);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="signin-container" >
      <form onSubmit={handleSubmit} className="form">

        <h3>Welcome to Galaxy Zoo!</h3>

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
          required>
        </input>
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="confirmPass"
          placeholder="Check Password"
          value={form.confirmPass}
          onChange={handleChange}
          required
        />

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" disabled={loading} className="register-btn">
          {loading ? "Registrando..." : "Sign Up"}
        </button>

      </form>
    </div>
    
  );
}
