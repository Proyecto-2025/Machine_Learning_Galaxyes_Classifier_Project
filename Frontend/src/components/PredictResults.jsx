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
      <h1 className="headers" id="header1">Image analysis completed... </h1>
      <div className="section">
        
        <h2 className="headers">Features</h2>
         
          <div id="features">
            {data.features.map((feature,index)=>(
              <p key={index}>{feature}</p>
            ))}
          </div>

      </div>
      <div className="section" id="hubble-div">
        <h2 className="headers">Hubble Sequense</h2>
          
        <div id="hubble-data">
          <div id="hubble-data-container">
            {data.hubblesequence?.map((h, index) => (
            <p key={index} id="hubble-value">{h}</p>
            ))} 
          </div>
          <div id="hubble-img-container">
            <div id="img-hubble"></div> 
          </div>
        </div>

      </div>
      <div id="values-section">
        <h2 className="headers">Prediction Values</h2>
          <div id="predict-values">
            {data.prediction?.map((item, index) => (
              <p key={index} className="prediction-item">{item}</p>
            ))}
          </div>
      </div>
      <div id="botonsContainer">

        <button className="results-btn" onClick={handleBack}>
          Subir otra imagen
        </button>
        
      </div>
    </div>
  );
}
