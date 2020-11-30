from marshmallow import fields, validate

from api.schemas.base_comment_schema import BaseCommentSchema
from api.schemas.request.paging_schema import PagingSchema


class CommentsListSchema(PagingSchema):
    """
    Comments list schema
    """
    parent_id = fields.Int(data_key="parentId", validate=lambda i: i > 0)
    board_id = fields.Str(data_key="boardId", validate=validate.Length(min=32, max=36))


class CreateCommentSchema(BaseCommentSchema):
    """
    Create comment schema
    """
    parent_id = fields.Int(data_key="parentId", validate=lambda i: i > 0)
    board_id = fields.Str(data_key="boardId", required=True, validate=validate.Length(min=32, max=36))


class UpdateCommentSchema(BaseCommentSchema):
    """
    Update comment schema
    """
