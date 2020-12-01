import os
from typing import Optional

from alembic import command
from alembic.config import Config
from envparse import env
from sqlalchemy import create_engine


def generate_db_url(prefix: Optional[str] = None,
                    user: Optional[str] = None,
                    password: Optional[str] = None,
                    db_host: Optional[str] = None,
                    db_port: Optional[str] = None,
                    db_name: Optional[str] = None,
                    mask_password: bool = False):
    prefix = __validate_url_parameter(prefix, "postgresql+asyncpg")
    user = __validate_url_parameter(user, env.str('POSTGRES_USER'))
    if mask_password:
        password = "*****"
    else:
        password = __validate_url_parameter(password, env.str('POSTGRES_PASSWORD'))

    db_host = __validate_url_parameter(db_host, env.str('DB_HOST'))
    db_port = __validate_url_parameter(db_port, env.str('DB_PORT'))
    db_name = __validate_url_parameter(db_name, env.str('POSTGRES_DB'))

    return f"{prefix}://{user}:{password}@{db_host}:{db_port}/{db_name}"


def setup_db():
    db_name = env.str('POSTGRES_DB')
    db_user = env.str('POSTGRES_USER')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    engine = create_engine(
        generate_db_url(prefix="postgresql", db_name="postgres"),
        isolation_level='AUTOCOMMIT'
    )
    with engine.connect() as conn:
        teardown_db()

        conn.execute(f"CREATE DATABASE {db_name}")
        conn.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")

        config = Config(f"{base_dir}/alembic.ini")
        config.set_main_option('sqlalchemy.url', generate_db_url(prefix="postgresql"))
        config.set_main_option('script_location', f"{base_dir}/db/alembic")

        command.upgrade(config, 'head')


def teardown_db():
    db_name = env.str('POSTGRES_DB')

    engine = create_engine(
        generate_db_url(prefix="postgresql", db_name="postgres"),
        isolation_level='AUTOCOMMIT'
    )
    with engine.connect() as conn:
        # terminate all connections to be able to drop database
        conn.execute(f"""
          SELECT pg_terminate_backend(pg_stat_activity.pid)
          FROM pg_stat_activity
          WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid();""")

        conn.execute(f"DROP DATABASE IF EXISTS {db_name}")


def __validate_url_parameter(p: Optional[str], default_value: Optional[str]):
    p = p if p is not None else default_value

    if p is None or len(p) == 0:
        raise ValueError("Parameter is none or empty.")

    return p
