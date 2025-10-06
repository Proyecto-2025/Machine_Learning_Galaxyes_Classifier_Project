import "./style/PredictResults.css";

export default function PredictResults({ data, onBack, onRetry }) {
  return (
    <div className="results">
      <h2>Resultados de Predicción</h2>
      <p><strong>Mensaje:</strong> {data.message}</p>
      <p><strong>Archivo:</strong> {data.file}</p>
      <p><strong>Clasificación:</strong> {data.classification}</p>

      <h3>Probabilidades</h3>
      <ul>
        <li>C0: {data.c0}</li>
        <li>C1: {data.c1}</li>
        <li>C2: {data.c2}</li>
        <li>C3: {data.c3}</li>
        <li>C4: {data.c4}</li>
        <li>C5: {data.c5}</li>
      </ul>

      <button className="results-btn" onClick={onBack}>
        Subir otra imagen
      </button>
      <button onClick={onRetry}>Ir a /predict</button>

    </div>
  );
}
