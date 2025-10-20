import os
from flask import Flask
from flask_cors import CORS
from config import Config
from predict_controller import controller_bp

def create_app():
    """Factory function para crear la aplicación Flask del microservicio ML"""
    app = Flask(__name__)
    
    # Configuración desde el archivo de configuración
    app.config.from_object(Config)
    
    # Habilitar CORS para permitir requests desde el backend
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Registrar el blueprint del controller
    app.register_blueprint(controller_bp)
    
    # Ruta de health check
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ml-microservice'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
