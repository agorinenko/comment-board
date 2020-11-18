from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from webargs.aiohttpparser import use_kwargs

from schemas.comment import update_schema, create_schema
from schemas.paging import paging_schema
from views.base_api_view import BaseApiView
from webargs import fields


class CommentsView(BaseApiView):
    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    async def retrieve(self, request, *args, **kwargs):
        """
        Get comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # raise HTTPNotFound(text="Comment not found")
        return web.json_response(kwargs)

    @use_kwargs(create_schema, location="form")
    async def create(self, request, *args, **kwargs):
        """
        Create comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return web.json_response(kwargs, status=201)

    @use_kwargs(paging_schema, location="querystring")
    async def list(self, request, *args, **kwargs):
        """
        Get comments
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return web.json_response(kwargs)

    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    @use_kwargs(update_schema, location="form")
    async def update(self, request, *args, **kwargs):
        """
        Update comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return web.json_response(kwargs)

    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    async def destroy(self, request, *args, **kwargs):
        """
        Delete comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return web.json_response({}, status=204)
