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
        <p><strong>Archivo:</strong> {data.file}</p>
      </div>
      <div className="section">
        <h2 className="headers">Probabilidades</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>C0</th>
              <th>C1</th>
              <th>C2</th>
              <th>C3</th>
              <th>C4</th>
              <th>C5</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{data.c0}</td>
              <td>{data.c1}</td>
              <td>{data.c2}</td>
              <td>{data.c3}</td>
              <td>{data.c4}</td>
              <td>{data.c5}</td>
            </tr>
          </tbody>
        </table>
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
