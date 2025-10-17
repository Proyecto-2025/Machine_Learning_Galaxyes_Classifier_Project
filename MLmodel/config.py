import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración del microservicio ML"""
    
    # Configuración del servidor
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5001))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # URL del backend principal (para CORS)
    BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
    
    # Configuración del modelo
    MODEL_PATH = os.getenv('MODEL_PATH', 'model/galaxy_model.h5')
    IMG_SIZE = int(os.getenv('IMG_SIZE', 64))
    
    # Configuración de CORS
    CORS_ORIGINS = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        BACKEND_URL
    ]
