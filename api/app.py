from aiohttp import web
from api.middleware import error_middleware
from api.urls import urlpatterns

app = web.Application(middlewares=[error_middleware])
app.add_routes(urlpatterns)
web.run_app(app)
