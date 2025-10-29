# Microservicio ML - Clasificador de Galaxias

Este microservicio proporciona predicciones de clasificación de galaxias utilizando un modelo de TensorFlow entrenado con datos del Galaxy Zoo. El modelo implementa una CNN personalizada para clasificar galaxias según la secuencia de Hubble.

## Características

- **API REST** para predicción de galaxias
- **Modelo CNN personalizado** con arquitectura optimizada para clasificación de galaxias
- **Clasificación según la secuencia de Hubble** (E, S0, Sa, Sb, Sc, SBa, SBb, SBc)
- **37 características morfológicas** detectadas automáticamente
- **Health check endpoint** para monitoreo
- **Microservicio independiente** y desplegable por separado
- **Dockerizado** para fácil despliegue
- **Desplegado en producción** en Google Cloud Run: https://galaxy-classifier-279086139631.us-central1.run.app

## Arquitectura del Modelo

### Red Neuronal Convolucional (CNN)

El modelo implementa una CNN personalizada con la siguiente arquitectura:

```python
# Arquitectura del modelo
model = Sequential([
    Input(shape=(64, 64, 3)),
    
    # Bloque 1: Extracción de características básicas
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # Bloque 2: Características intermedias
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # Bloque 3: Características complejas
    Conv2D(128, (3, 3), activation='relu'),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    # Clasificador
    Flatten(),
    Dense(512, activation='relu'),
    Dense(512, activation='relu'),
    Dense(37, activation='sigmoid')  # 37 características morfológicas
])
```

### Características del Modelo

- **Entrada**: Imágenes de 64x64 píxeles en RGB
- **Salida**: 37 probabilidades (características morfológicas)
- **Función de pérdida**: Binary Crossentropy (clasificación multilabel)
- **Optimizador**: Adam
- **Regularización**: Dropout implícito en capas densas
- **Data Augmentation**: Rotación, traslación, zoom y flip horizontal

### Dataset y Entrenamiento

- **Fuente**: Galaxy Zoo (training_solutions_rev1.csv)
- **Tamaño**: ~61,578 galaxias etiquetadas
- **División**: 80% entrenamiento, 20% validación
- **Preprocesamiento**: Normalización [0,1], redimensionado a 64x64
- **Checkpoints**: Guardado cada 50 épocas
- **Épocas**: 100 épocas con early stopping

## Estructura del Proyecto

```
MLmodel/
├── app.py                    # Aplicación Flask principal
├── start.py                  # Script de inicio simplificado
├── predict_controller.py     # Controlador de predicciones
├── Dockerfile               # Configuración Docker
├── requirements.txt         # Dependencias Python
├── model/                   # Modelo ML y lógica
│   ├── GalaxyMLmodel.py     # Entrenamiento del modelo
│   ├── PredictGalaxy.py     # Función de predicción
│   ├── Response.py          # Procesamiento de respuestas
│   ├── DataAugmentation.py  # Técnicas de aumento de datos
│   ├── epochCheckPoint.py   # Callback para checkpoints
│   ├── galaxy_model.h5      # Modelo entrenado final
│   ├── checkpoints/         # Modelos intermedios
│   │   ├── galaxy_model_epoch_050.h5
│   │   └── galaxy_model_epoch_100.h5
│   └── plots/               # Gráficos de entrenamiento
└── README.md
```

## Instalación y Ejecución

### 1. Ejecución Local (Desarrollo)

#### Requisitos Previos
- Python 3.11+
- pip o conda

#### Pasos de Instalación

1. **Clonar el repositorio y navegar al directorio:**
```bash
cd MLmodel/
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar el microservicio:**
```bash
python start.py
```

El microservicio estará disponible en `http://localhost:5001`

### 2. Despliegue con Docker

#### Construir la imagen Docker:
```bash
docker build -t galaxy-classifier-ml .
```

#### Ejecutar el contenedor:
```bash
docker run -p 5001:5001 galaxy-classifier-ml
```

### 3. Despliegue en Producción (Google Cloud Run)

El microservicio está desplegado en Google Cloud Run y disponible públicamente:

**URL de Producción:** https://galaxy-classifier-279086139631.us-central1.run.app

#### Health Check en Producción:
```bash
curl https://galaxy-classifier-279086139631.us-central1.run.app/health
```

#### Test de Predicción en Producción:
```bash
curl -X POST -F "image=@ruta/a/imagen.jpg" https://galaxy-classifier-279086139631.us-central1.run.app/predict
```

### Verificación del Despliegue

#### Health Check:
```bash
curl http://localhost:5001/health
```

#### Test de Predicción:
```bash
curl -X POST -F "image=@ruta/a/imagen.jpg" http://localhost:5001/predict
```

## API Endpoints

### POST /predict
Predice la clasificación de una galaxia a partir de una imagen.

**Request:**
- Content-Type: `multipart/form-data`
- Parámetro: `image` (archivo de imagen JPG/PNG)

**Response:**
```json
{
    "prediction": [0.1, 0.8, 0.3, ...],  // 37 probabilidades
    "features": ["SUAVE", "VISTA DE PERFIL", "CON PATRON DE BRAZOS ESPIRALES"],
    "hubblesequence": ["Sa"]  // Clasificación Hubble
}
```

**Características detectadas (37 total):**
- SUAVE, CON CARACTERISTICAS O DISCO, ESTRELLA O ARTEFACTO
- VISTA DE PERFIL, NO VISTA DE PERFIL
- BARRA ATRAVESANDO EL CENTRO, SIN BARRA EN EL CENTRO
- CON PATRON DE BRAZOS ESPIRALES, SIN PATRON DE BRAZOS ESPIRALES
- BULTO CENTRAL (SIN/APENAS PERCEPTIBLE/OBVIO/DOMINANTE)
- HAY ALGO EXTRAÑO (ODD), NO HAY NADA EXTRAÑO (ODD)
- FORMA: COMPLETAMENTE REDONDA, MEDIANAMENTE REDONDA, CIGARRO, ANILLO
- BRAZOS ESPIRALES: MUY APRETADOS, MEDIANAMENTE APRETADOS, SUELTOS
- NÚMERO DE BRAZOS: 1, 2, 3, 4, MÁS DE 4, NO SE PUEDEN CONTAR

### GET /health
Health check del microservicio.

**Response:**
```json
{
    "status": "healthy",
    "service": "ml-microservice"
}
```

## Clasificación Hubble

El modelo clasifica las galaxias según la secuencia de Hubble:

### Tipos Principales:
- **E**: Elípticas (suaves y redondas)
- **S0**: Lenticulares (disco visto de perfil)
- **S**: Espirales normales (Sa, Sb, Sc)
- **SB**: Espirales barradas (SBa, SBb, SBc)
- **Irregular**: Galaxias con características extrañas

### Subclasificaciones:
- **a, b, c**: Tamaño del bulbo central (a=pequeño, c=grande)
- **(ODD)**: Características extrañas o perturbadas

## Configuración

### Variables de Entorno
- **Puerto**: 5001 (configurable)
- **Host**: 0.0.0.0 (acepta conexiones desde cualquier IP)
- **Debug**: Activado por defecto en desarrollo
- **Modelo**: `model/galaxy_model.h5`

### Configuración del Modelo
- **Tamaño de imagen**: 64x64 píxeles (redimensionado automáticamente)
- **Canales**: RGB (3 canales)
- **Normalización**: [0, 1] (automática)
- **Formato de entrada**: JPG, PNG

## Integración con el Backend

El backend principal debe configurar el `ComService` con la URL del microservicio ML:

### Configuración para Desarrollo Local:
```python
# En com_service.py
self.ml_base_url = "http://localhost:5001"  # URL del microservicio ML local
self.timeout = 30  # Timeout en segundos
```

### Configuración para Producción:
```python
# En com_service.py
self.ml_base_url = "https://galaxy-classifier-279086139631.us-central1.run.app"  # URL de producción
self.timeout = 30  # Timeout en segundos
```

### Ejemplo de Integración:
```python
import requests

def classify_galaxy(image_file, production=False):
    if production:
        url = "https://galaxy-classifier-279086139631.us-central1.run.app/predict"
    else:
        url = "http://localhost:5001/predict"
    
    files = {"image": image_file}
    response = requests.post(url, files=files, timeout=30)
    return response.json()
```

## Monitoreo y Logs

### Health Check

#### Desarrollo Local:
```bash
curl http://localhost:5001/health
```

#### Producción:
```bash
curl https://galaxy-classifier-279086139631.us-central1.run.app/health
```

### Logs del Contenedor
```bash
docker logs galaxy-ml
```

### Monitoreo en Producción
El servicio está desplegado en Google Cloud Run y puede ser monitoreado a través de:
- **Google Cloud Console**: Logs y métricas del servicio
- **Health Check**: Endpoint `/health` disponible públicamente
- **URL de Producción**: https://galaxy-classifier-279086139631.us-central1.run.app

## Desarrollo

### Entrenar el Modelo
```bash
cd model/
python GalaxyMLmodel.py
```

### Verificar Predicciones
```bash
python -c "
from model.PredictGalaxy import makePrediction
from model.Response import Response
# Test con imagen de ejemplo
"
```

## Notas Técnicas

- **Modelo**: CNN personalizada optimizada para galaxias
- **Dataset**: Galaxy Zoo (61,578 galaxias etiquetadas)
- **Precisión**: ~85% en características principales
- **Escalabilidad**: Stateless, escalable horizontalmente
- **Compatibilidad**: Python 3.11+, TensorFlow 2.13+
- **Docker**: Imagen basada en Python 3.11-slim
