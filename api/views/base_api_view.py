import logging
from abc import ABC
from typing import Optional, List, Any

from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed, HTTPInternalServerError
from aiohttp.web_request import Request
from aiohttp.web_routedef import RouteDef
from sqlalchemy.ext.asyncio import AsyncSession


class BaseApiView(ABC):
    async def retrieve(self, request: Request, *args, **kwargs):
        raise HTTPMethodNotAllowed('retrieve', allowed_methods=[])

    async def create(self, request: Request, *args, **kwargs):
        raise HTTPMethodNotAllowed('create', allowed_methods=[])

    async def list(self, request: Request, *args, **kwargs):
        raise HTTPMethodNotAllowed('list', allowed_methods=[])

    async def update(self, request: Request, *args, **kwargs):
        raise HTTPMethodNotAllowed('update', allowed_methods=[])

    async def destroy(self, request: Request, *args, **kwargs):
        raise HTTPMethodNotAllowed('destroy', allowed_methods=[])

    @classmethod
    def db_session(cls, request: Request) -> AsyncSession:
        return cls.get_app_data(request, 'db_session')

    @classmethod
    def logger(cls, request: Request) -> logging.Logger:
        return cls.get_app_data(request, 'logger.server')

    @classmethod
    def get_app_data(cls, request: Request, key: str) -> Any:
        if key not in request.app:
            raise HTTPInternalServerError(text=f"App data \"{key}\" not found")
        return request.app[key]

    @classmethod
    def routes(cls, prefix: Optional[str] = None, path: Optional[str] = None) -> List[RouteDef]:
        prefix = prefix if prefix is not None else ""
        path = path if path is not None else ""

        path = cls.urljoin("/", prefix, path)

        inst = cls()

        item_path = cls.urljoin("/", path, "{id}")

        path = f"/{cls.prepare_url(path)}"
        item_path = f"/{cls.prepare_url(item_path)}"

        return [
            web.get(path, inst.list),
            web.post(path, inst.create),
            web.put(item_path, inst.update),
            web.delete(item_path, inst.destroy),
            web.get(item_path, inst.retrieve)
        ]

    @classmethod
    def urljoin(cls, separator: str, *args) -> str:
        urls = list(filter(lambda url: url is not None, args))
        urls = list(map(cls.prepare_url, urls))
        return separator.join(urls)

    @classmethod
    def prepare_url(cls, url: str) -> str:
        if url.endswith('/'):
            url = url[:-1]

        if url.startswith('/'):
            url = url[1:]

        return url
