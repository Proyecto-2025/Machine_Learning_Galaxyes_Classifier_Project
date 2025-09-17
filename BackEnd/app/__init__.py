from flask import Flask
from flask_cors import CORS
from app.routes.routes import api_bp
from app.db import db, migrate
#from app.models import image_model

def create_app():
    app = Flask(__name__)
    
    #Habilita cross-origin resource sharing (para recibir request del Frontend)
    CORS(app)
       
    #Definición del motor sql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #Inicialización sql en la instancia de la app
    db.init_app(app)
    
    #Inicialización la herramienta de migraciones
    migrate.init_app(app, db)
      
    #Registro del blueprint de rutas en la app 
    app.register_blueprint(api_bp)
    
    return app