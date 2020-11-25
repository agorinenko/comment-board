from marshmallow import fields, validate

from api.schemas.base_comment_schema import BaseCommentSchema
from api.schemas.request.paging_schema import PagingSchema


class CommentsListSchema(PagingSchema):
    """
    Comments list schema
    """
    board_id = fields.Str(data_key="boardId", validate=validate.Length(min=32, max=36))
    parent = fields.Int(validate=lambda i: i > 0)


class CreateCommentSchema(BaseCommentSchema):
    """
    Create comment schema
    """
    parent = fields.Int(validate=lambda i: i > 0)


class UpdateCommentSchema(BaseCommentSchema):
    """
    Update comment schema
    """
