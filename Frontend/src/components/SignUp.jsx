import { useState } from "react";

export default function SignUp() {
  const [form, setForm] = useState({
    nickname: "",
    password: "",
    confirmPass: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

    if (form.password !== form.confirmPass) {
      setError("Las contraseñas no coinciden");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://localhost:3000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          nickname: form.nickname,
          password: form.password,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || "Error al registrarse");
      }

      const data = await res.json();
      console.log("Registro OK:", data);
      alert("Cuenta creada con éxito!");

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ display:"flex", flexDirection:"column", width:"260px", gap:"12px" }}>

      <h3>Registro</h3>

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

      <input
        type="password"
        name="confirmPass"
        placeholder="Confirmar Password"
        value={form.confirmPass}
        onChange={handleChange}
        required
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button type="submit" disabled={loading}>
        {loading ? "Registrando..." : "Crear Cuenta"}
      </button>

    </form>
  );
}
