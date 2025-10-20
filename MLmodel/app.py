from flask import Flask
from flask_cors import CORS
from predict_controller import controller_bp

def create_app():
    """Factory function para crear la aplicación Flask del microservicio ML"""
    app = Flask(__name__)
    
    # Habilitar CORS para permitir requests desde cualquier origen
    CORS(app, origins=["*"])
    
    # Registrar el blueprint del controller
    app.register_blueprint(controller_bp)
    
    # Ruta de health check
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ml-microservice'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
