from flask import Flask
from flask_cors import CORS
from .routes.routes import api_bp
from .db import db, migrate

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa TODOS los modelos después de init_app y antes de migrate
    from . import models

    migrate.init_app(app, db)

    app.register_blueprint(api_bp)
    return app
