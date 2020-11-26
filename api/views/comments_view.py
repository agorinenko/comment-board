from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import docs, request_schema, response_schema, match_info_schema, querystring_schema
from marshmallow import Schema
from sqlalchemy import select, func
from webargs.aiohttpparser import use_kwargs

from webargs import fields

from api.response.json_response import JsonResponse
from api.schemas.base_comment_schema import IdSchema
from api.schemas.request.comment_schema import CreateCommentSchema, UpdateCommentSchema, CommentsListSchema
from api.schemas.response.comment_schema import CommentSchema
from api.views.base_api_view import BaseApiView
from db.models import Comment


class CommentsView(BaseApiView):
    TAG = "Comment"
    """
    https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#adapting-orm-lazy-loads-to-asyncio
    https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """

    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    @docs(tags=[TAG], summary='Get comment',)
    @response_schema(Schema(), code=200)
    @match_info_schema(IdSchema())
    async def retrieve(self, request: Request, *args, **kwargs):
        """
        Get comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        comment = await self.__get_instance(request, *args, **kwargs)

        serializer = CommentSchema()
        return JsonResponse(serializer).get_response(comment)

    @use_kwargs(CreateCommentSchema(), location="form")
    @docs(tags=[TAG], summary='Create comment')
    @request_schema(CreateCommentSchema())
    @response_schema(CommentSchema(), code=200)
    async def create(self, request: Request, *args, **kwargs):
        """
        Create comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        new_comment = Comment(**kwargs)

        self.db_session(request).add(new_comment)
        await self.db_session(request).commit()
        await self.db_session(request).refresh(new_comment)

        serializer = CommentSchema()
        return JsonResponse(serializer).get_response(new_comment)

    @use_kwargs(CommentsListSchema(), location="querystring")
    @docs(tags=[TAG], summary='Get comments')
    @response_schema(CommentSchema(many=True), code=200)
    @querystring_schema(CommentsListSchema())
    async def list(self, request: Request, *args, **kwargs):
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

    @use_kwargs(IdSchema(), location="match_info")
    @use_kwargs(UpdateCommentSchema(), location="form")
    @docs(tags=[TAG], summary='Update comment')
    @request_schema(UpdateCommentSchema())
    @response_schema(CommentSchema(), code=200)
    @match_info_schema(IdSchema())
    async def update(self, request: Request, *args, **kwargs):
        """
        Update comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        comment = await self.__get_instance(request, *args, **kwargs)
        comment.content = kwargs['content']
        if 'user_name' in kwargs:
            comment.user_name = kwargs["user_name"]

        await self.db_session(request).commit()
        await self.db_session(request).refresh(comment)

        serializer = CommentSchema()
        return JsonResponse(serializer).get_response(comment)

    @use_kwargs({"id": fields.Int(validate=lambda i: i > 0)}, location="match_info")
    @docs(tags=[TAG], summary='Delete comment')
    @response_schema(Schema(), code=204)
    @match_info_schema(IdSchema())
    async def destroy(self, request: Request, *args, **kwargs):
        """
        Delete comment
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        comment = await self.__get_instance(request, *args, **kwargs)

        self.db_session(request).delete(comment)
        await self.db_session(request).commit()

        return web.json_response({}, status=204)

    async def __get_instance(self, request: Request, *args, **kwargs) -> Comment:
        result = await self.db_session(request).execute(
            select(Comment).filter(Comment.id == kwargs['id'])
        )
        comment = result.scalars().one_or_none()

        if comment is None:
            raise HTTPNotFound(text=f"Comment '{kwargs['id']}' not found")

        return comment
