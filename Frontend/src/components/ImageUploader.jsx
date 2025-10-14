import { useState } from "react";
import "./style/ImageUploader.css"

export default function ImageUploader(){
  const [image,setImage] = useState(null);
  const [uploading,setUploading] = useState(null);
  const handleFileSelect = (e) => {
    if(e.target.file){
      setImage({
        file,
        url: URL.createObjectURL(file),
        name: file.name,
      });
    }
  }

  const handleUpload = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image.file);

    try {
      setUploading(true);
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Error al subir la imagen");

      const data = await response.json();

      if (data.error) {
        onError(data.error);
      } else {
        onSuccess(data);
      }
    } catch (err) {
      onError(err.message);
    } finally {
      setUploading(false);
    }
  };

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

      <button
        onClick={handleUpload}
        className="uploader-btn"
        disabled={!image || uploading}
      >
        {uploading ? "Enviando..." : "Enviar al backend"}
      </button>
    </div>
  );
}