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
        <p>{data.filename}</p>

      </div>
      <div className="section">
      
          <h2 className="headers">Features</h2>
         
          <div id="features">
            {data.features.map((feature,index)=>(
              <p key={index}>{feature}</p>
            ))}
          </div>
       
      </div>
      <div className="section">
        
          <h2 className="headers">Tipo de Galaxia Estimado</h2>
          
          <p>HardCoded Result, TODO Implement Backend Clasification prediction</p>
        
      </div>
      {/*<p><strong>Mensaje:</strong> {data.message}</p> */}
      <div id="botonsContainer">

        <button className="results-btn" onClick={handleBack}>
          Subir otra imagen
        </button>
        
      </div>
    </div>
  );
}
