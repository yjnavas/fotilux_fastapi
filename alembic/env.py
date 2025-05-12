from logging.config import fileConfig
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import Base from our app
from app.core.database import Base
from app.core.config import DATABASE_URL

# Import all models to ensure they are registered with Base.metadata
# Import each model separately to avoid circular imports
from app.models.user import User, Follow
from app.models.post import Post, PostStatus
from app.models.media import Media
from app.models.comment import Comment
from app.models.like import Like
from app.models.favorite import Favorite

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
try:
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
except Exception as e:
    print(f"Warning: Error setting up logging: {e}")
    # Continue without logging configuration

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Override the sqlalchemy.url with our DATABASE_URL
    url = DATABASE_URL
    
    # Set the sqlalchemy.url in the config
    config.set_main_option("sqlalchemy.url", url)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Override the sqlalchemy.url with our DATABASE_URL
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    
    # Get the configuration with our updated URL
    configuration = config.get_section(config.config_ini_section)
    
    # Create the engine with our configuration
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
