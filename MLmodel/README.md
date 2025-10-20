# Microservicio ML - Clasificador de Galaxias

Este microservicio proporciona predicciones de clasificación de galaxias utilizando un modelo de TensorFlow entrenado.

## Características

- API REST para predicción de galaxias
- Modelo TensorFlow pre-entrenado
- Clasificación según la secuencia de Hubble
- Health check endpoint
- Microservicio independiente y desplegable por separado
- Configuración simplificada

## Estructura del Proyecto

```
MLmodel/
├── app.py                 # Aplicación Flask principal
├── start.py              # Script de inicio simplificado
├── predict_controller.py # Controlador de predicciones
├── model/                # Modelo ML y lógica
│   ├── PredictGalaxy.py  # Función de predicción
│   ├── Response.py       # Procesamiento de respuestas
│   └── galaxy_model.h5   # Modelo pre-entrenado
├── requirements.txt      # Dependencias Python
└── README.md           # Este archivo
```

## Instalación y Ejecución

### Ejecución Local (Recomendado)

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el microservicio:
```bash
python start.py
```

El microservicio estará disponible en `http://localhost:5001`

### Ejecución Alternativa

También puedes ejecutar directamente:
```bash
python app.py
```

## API Endpoints

### POST /predict
Predice la clasificación de una galaxia a partir de una imagen.

**Request:**
- Content-Type: multipart/form-data
- Parámetro: `image` (archivo de imagen)

**Response:**
```json
{
    "prediction": [0.1, 0.8, 0.3, ...],
    "features": ["SUAVE", "VISTA DE PERFIL", ...],
    "hubblesequence": [0.1, 0.8, 0.3, ...]
}
```

### GET /health
Health check del microservicio.

**Response:**
```json
{
    "status": "healthy",
    "service": "ml-microservice"
}
```

## Configuración

El microservicio está configurado para ejecutarse en:
- **Puerto**: 5001
- **Host**: 0.0.0.0 (acepta conexiones desde cualquier IP)
- **Debug**: Activado por defecto

## Integración con el Backend

El backend principal debe configurar el `ComService` con la URL del microservicio ML:

```python
# En com_service.py
self.ml_base_url = "http://localhost:5001"  # URL del microservicio ML
self.timeout = 30  # Timeout en segundos
```

## Desarrollo

Para desarrollo local, simplemente ejecuta:

```bash
python start.py
```

El microservicio se iniciará automáticamente en modo debug.

## Notas

- El modelo espera imágenes de 64x64 píxeles
- Las imágenes se procesan automáticamente al tamaño correcto
- El microservicio es stateless y puede escalarse horizontalmente
