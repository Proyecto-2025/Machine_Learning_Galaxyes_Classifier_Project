import "./style/ImageGallery.css";

export default function ImageGallery({ images }) {
  return (
    <div className="gallery-container">
      {images.length === 0 
          ? (<p className="gallery-empty">No hay imágenes para mostrar.</p>)
          : (
            <div className="gallery-scroll">
              {images.map((img, idx) => (
                <div key={idx} className="gallery-item">
                  <img src={img.url} alt={img.name || 'imagen-${idx}'} />
                  {img.name && <span>{img.name}</span>}
                </div>
              ))}
            </div>
      )}
    </div>
  );
}
