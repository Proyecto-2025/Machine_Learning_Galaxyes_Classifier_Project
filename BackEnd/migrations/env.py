import logging
from logging.config import fileConfig

from alembic import context
from app.db import db
from app.models import image_model  # importa todos los modelos

config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# --- Metadata de SQLAlchemy ---
target_metadata = db.Model.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = db.engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
