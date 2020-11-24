from marshmallow import fields

from api.schemas.base_comment_schema import BaseCommentSchema


class CreateCommentSchema(BaseCommentSchema):
    """
    Create comment schema
    """
    parent = fields.Int(validate=lambda i: i > 0)


class UpdateCommentSchema(BaseCommentSchema):
    """
    Update comment schema
    """
