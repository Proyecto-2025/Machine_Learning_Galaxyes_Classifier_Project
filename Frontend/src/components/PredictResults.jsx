import { useNavigate, useLocation } from "react-router-dom";
import "./style/PredictResults.css";

export default function PredictResults({onBack}) {
  const navigate = useNavigate();
  const {state} = useLocation();
  const data = state?.data;
  const handleBack = () => {
    navigate("/predict");
  };
   if (!data) {
    return <p>No se encontraron resultados.</p>;
  }
  return (
    <div className="results">
      <h2 className="headers">Resultados de Predicción</h2>
      <div className="section">
        <h2 className="headers">Archivo recidido</h2>
        <p><strong>Archivo:</strong> {data.filename}</p>
      </div>
      <div className="section">
        <h2 className="headers">Features</h2>
        {data.features.map((feature,index)=>(
          <p key={index}>{feature}</p>
        ))}
      </div>
      <div className="section">
        <h2 className="headers">Tipo de Galaxia Estimado</h2>
        <p><strong>Clasificación:</strong> {data.classification}</p>
      </div>
      {/*<p><strong>Mensaje:</strong> {data.message}</p> */}
      <div className="section">
        <button className="results-btn" onClick={onBack}>
          Subir otra imagen
        </button>
        <button onClick= {handleBack}>
          Ir a /predict
        </button>
      </div>
    </div>
  );
}
