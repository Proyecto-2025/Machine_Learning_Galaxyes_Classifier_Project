import { useLocation, useNavigate } from "react-router-dom";
import "./style/ErrorMessage.css"
export default function ErrorMessage({ message, onRetry }) {
  const {state} = useLocation();
  const navigate = useNavigate();
  return (
     <div className="error-box">
      <h2>Error al cargar la imagen</h2>
      <p> Ocurrió un error desconocido</p>
      <button id="tryagain-btn" onClick={() => navigate("/predict")}>Intentar de nuevo</button>
    </div>
  );
}
