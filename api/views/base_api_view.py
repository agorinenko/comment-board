from abc import ABC
from typing import Optional, List

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
    def db_session(cls, request) -> AsyncSession:
        if 'db_session' not in request.app:
            raise HTTPInternalServerError(text="DB session not found")
        return request.app['db_session']

    @classmethod
    def routes(cls, path: Optional[str]) -> List[RouteDef]:
        if path.endswith('/'):
            path = path[:-1]

        inst = cls()

        item_path = path + "/{id}"

        return [
            web.get(path, inst.list),
            web.post(path, inst.create),
            web.put(item_path, inst.update),
            web.delete(item_path, inst.destroy),
            web.get(item_path, inst.retrieve)
        ]
