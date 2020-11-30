from typing import Optional

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from envparse import env
from sqlalchemy import text

from api.middleware import error_middleware
from api.urls import urlpatterns
import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from db.utils import generate_db_url

env.read_envfile()

ENV = env.str('ENV')
IS_DEV = (ENV == "DEV")

log_level = logging.DEBUG if IS_DEV else logging.ERROR
logging.basicConfig(level=log_level)


async def __setup_pg(application: web.Application):
    db_info = generate_db_url(mask_password=True)

    application['logger.server'].info(f"Connecting to database: {db_info}")

    engine = create_async_engine(
        generate_db_url(),
        echo=True
    )
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with AsyncSession(engine) as session:
        application['db_session'] = session
        application['logger.server'].info(f"Connected to database: {db_info}")
        yield
        application['logger.server'].info(f"Disconnecting from database: {db_info}")

    application['logger.server'].info(f"Disconnected from database: {db_info}")


def create_app() -> web.Application:
    application = web.Application(middlewares=[error_middleware])
    application['logger.server'] = logging.getLogger('aiohttp.server')
    application.cleanup_ctx.append(__setup_pg)
    application.add_routes(urlpatterns)

    return application


app = create_app()
setup_aiohttp_apispec(
    app=app,
    title="REST API",
    version="v1",
    url="/api/docs/swagger.json",
    swagger_path="/swg",
)

# web.run_app(app, port=8000)
