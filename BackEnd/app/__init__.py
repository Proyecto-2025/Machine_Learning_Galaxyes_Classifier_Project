
import os
from flask import Flask
from flask_cors import CORS
from .db import db, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, "database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    CORS(app)  

    # Init DB
    db.init_app(app)

    # IMPORTAR MODELOS 
    from . import models

    # Init Migrations
    migrate.init_app(app, db)

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    app.logger.info(f"Using SQLite at: {db_path}")

    return app
