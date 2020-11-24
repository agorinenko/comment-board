from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from sqlalchemy import select
from webargs.aiohttpparser import use_kwargs

from webargs import fields

from api.schemas.request.comment_schema import CreateCommentSchema, UpdateCommentSchema
from api.schemas.request.paging_schema import PagingSchema
from api.schemas.response.comment_schema import CommentSchema
from api.views.base_api_view import BaseApiView
from db.models import Comment


class CommentsView(BaseApiView):
    """
    https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#adapting-orm-lazy-loads-to-asyncio
    https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """

    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    async def retrieve(self, request, *args, **kwargs):
        """
        Get comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        result = await self.db_session(request).execute(
            select(Comment).filter(Comment.id == kwargs['id'])
        )
        comment = result.scalars().one_or_none()

        if comment is None:
            raise HTTPNotFound(text=f"Comment '{kwargs['id']}' not found")

        serializer = CommentSchema()
        data = serializer.dump(comment)
        return web.json_response(data)

    @use_kwargs(CreateCommentSchema(), location="form")
    async def create(self, request, *args, **kwargs):
        """
        Create comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return web.json_response(kwargs, status=201)

    @use_kwargs(PagingSchema(), location="querystring")
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
    @use_kwargs(UpdateCommentSchema(), location="form")
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
