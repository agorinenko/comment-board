from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound

from views.base_api_view import BaseApiView


class CommentsView(BaseApiView):
    async def retrieve(self, request, *args, **kwargs):
        # raise HTTPNotFound(text="Comment not found")
        id = request.match_info['id']
        data = {'id': id}
        return web.json_response(data)

    async def create(self, request, *args, **kwargs):
        data = await request.post()
        data = dict(data)
        return web.json_response(data, status=201)

    async def list(self, request, *args, **kwargs):
        data = [{'id': 1},{'id': 2}]
        return web.json_response(data)

    async def update(self, request, *args, **kwargs):
        data = await request.post()
        data = dict(data)
        return web.json_response(data)

    async def destroy(self, request, *args, **kwargs):
        return web.json_response({}, status=204)
