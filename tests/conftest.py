import os

import pytest
from envparse import env

from api.app import create_app
from db.utils import setup_db, teardown_db


@pytest.fixture
async def client(aiohttp_client):
    app = create_app()
    return await aiohttp_client(app)


@pytest.fixture(scope='session', autouse=True)
def database():
    db_name = env.str('DB_NAME')
    os.environ['DB_NAME'] = f"test_{db_name}"
    setup_db()
    yield
    teardown_db()

