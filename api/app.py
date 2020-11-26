from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from envparse import env
from sqlalchemy import text

from api.middleware import error_middleware
from api.urls import urlpatterns
import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


async def __setup_pg(application: web.Application):
    log = logging.getLogger('aiohttp.server')
    application['logger.server'] = log

    db_info = f"{env.str('POSTGRES_USER')}@{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}/{env.str('POSTGRES_DB')}"

    log.info(f"Connecting to database: {db_info}")

    engine = create_async_engine(
        f"postgresql+asyncpg://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}/{env.str('POSTGRES_DB')}",
        echo=True
    )
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    async with AsyncSession(engine) as session:
        application['db_session'] = session
        log.info(f"Connected to database: {db_info}")
        yield
        log.info(f"Disconnecting from database: {db_info}")

    log.info(f"Disconnected from database: {db_info}")


env.read_envfile()

ENV = env.str('ENV')
IS_DEV = (ENV == "DEV")

app = web.Application(middlewares=[error_middleware])
app.cleanup_ctx.append(__setup_pg)
app.add_routes(urlpatterns)

log_level = logging.DEBUG if IS_DEV else logging.ERROR
logging.basicConfig(level=log_level)

setup_aiohttp_apispec(
    app=app,
    title="REST API",
    version="v1",
    url="/api/docs/swagger.json",
    swagger_path="/swg",
)
# web.run_app(app, port=8000)
