from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from sqlalchemy import select, func
from sqlalchemy.orm import query
from webargs.aiohttpparser import use_kwargs

from webargs import fields

from api.response.json_response import JsonResponse
from api.schemas.request.comment_schema import CreateCommentSchema, UpdateCommentSchema, CommentsListSchema
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
        return JsonResponse(serializer).get_response(comment)

    @use_kwargs(CreateCommentSchema(), location="form")
    async def create(self, request, *args, **kwargs):
        """
        Create comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        new_comment = Comment(**kwargs)

        self.db_session(request).add(new_comment)
        await self.db_session(request).flush()
        await self.db_session(request).refresh(new_comment)

        serializer = CommentSchema()
        return JsonResponse(serializer).get_response(new_comment)

    @use_kwargs(CommentsListSchema(), location="querystring")
    async def list(self, request, *args, **kwargs):
        """
        Get comments
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        total_statement = select(func.count(Comment.id))

        paging_statement = select(Comment) \
            .order_by(Comment.id, Comment.created) \
            .limit(kwargs['limit']) \
            .offset(kwargs['offset'])

        criteria = []
        if 'board_id' in kwargs:
            criteria.append((Comment.board_id == kwargs['board_id']))

        if 'parent' in kwargs:
            criteria.append((Comment.parent == kwargs['parent']))

        paging_statement = paging_statement.filter(*criteria)
        total_statement = total_statement.filter(*criteria)

        result = await self.db_session(request).execute(paging_statement)
        comments = result.scalars().all()

        total_result = await self.db_session(request).execute(total_statement)
        count = total_result.scalar()

        serializer = CommentSchema(many=True)

        return JsonResponse(serializer).get_response(comments, count=count)

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
