import logging
from logging.config import fileConfig
import sys
import os

from alembic import context

# --- Configuración de path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.db import db
from app.models import image_model  # importa tus modelos

# --- Configuración Alembic ---
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# --- Crear app y contexto ---
app = create_app()
with app.app_context():
    target_metadata = db.metadata

    def run_migrations_offline():
        """Run migrations in 'offline' mode."""
        url = app.config['SQLALCHEMY_DATABASE_URI']
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online():
        """Run migrations in 'online' mode."""
        connectable = db.engine
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()

    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
