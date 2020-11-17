from aiohttp import web

from error_middleware import error_middleware
from urls import urlpatterns

app = web.Application(middlewares=[error_middleware])
app.add_routes(urlpatterns)

if __name__ == "__main__":
    web.run_app(app)
