import { useState } from "react";
import ErrorMessage from "./ErrorMessage"
import PredictResults from "./PredictResults";
import "./style/ImageUploader.css";

export default function ImageUploader() {
  const [image, setImage] = useState(null);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

   const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage({
        file, // ✅ importante para el upload
        url: URL.createObjectURL(file),
        name: file.name,
      });
    }
  };

  // Enviar imágenes al backend
  const handleUpload = async () => {

    const formData = new FormData();
    formData.append("image",image.file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Error al subir las imágenes");

      const data = await response.json();
      console.log("Respuesta del backend:", data);

      if (data.error) {
      // 🔹 si el backend devuelve { error: ... }
        setError(data.error);
      } else {
        alert("Imágenes enviadas correctamente!");
        setImage(null);
        setResults(data);
      }
      } catch (err) {
        console.error("Error en la subida:", err);
        setError(err.message); // 🔹 guarda el mensaje de error
        setImage(null)
      }
    };
    if (error) {
      return <ErrorMessage message={error} onRetry={() => setError(null)} />;
    }

    if (results) {
      return <PredictResults data={results} onBack={() => setResults(null)} />;
    }

  return (
    <div className="uploader">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="uploader-input"
      />

      <div className="uploader-grid">
        {image && (
          <div className="uploader-item">
            <img src={image.url} alt={image.name} className="uploader-img" />
            <span className="uploader-name">{image.name}</span>
          </div>
        )}
      </div>

      <button onClick={handleUpload} className="uploader-btn" disabled={!image}>
        Enviar al backend
      </button>
    </div>
  );
}
