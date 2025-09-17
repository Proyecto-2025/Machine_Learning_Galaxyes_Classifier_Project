import React from "react";

export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-box">
      <h2>❌ Error</h2>
      <p>{message || "Ha ocurrido un error inesperado."}</p>
      <button onClick={onRetry}>Ir a /predict</button>
    </div>
  );
}
