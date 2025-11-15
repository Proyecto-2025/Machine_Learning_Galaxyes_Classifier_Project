
import os
from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from dotenv import load_dotenv

from .services.db_service import DbService
from .services.file_storage_service import FileStorageService
from .services.com_service import ComService

def create_app(db_service = None, storage_service = None, com_service = None):
    load_dotenv()
    
    instance_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "instance")
    os.makedirs(instance_path, exist_ok=True)
    
    app = Flask(__name__, instance_path=instance_path)
    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    CORS(app)  

    # Init DB
    db.init_app(app)

    # Import models 
    from . import models

    # Init Migrations
    migrate.init_app(app, db)
       
    # Register services
    app.db_service = db_service or DbService()
    app.storage_service = storage_service or FileStorageService()
    app.com_service = com_service or ComService()

    # Registrar blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # Logging
    app.logger.info(f"Using SQLite at: {db_path}")

    return app
