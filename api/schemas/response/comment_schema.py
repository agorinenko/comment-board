from marshmallow import fields, validate

from api.schemas.base_comment_schema import BaseCommentSchema


class CommentSchema(BaseCommentSchema):
    id = fields.Int(dump_only=True)
    board_id = fields.Str(data_key="boardId", required=True, validate=validate.Length(min=32, max=36))
    parent_id = fields.Int(data_key="parentId", validate=lambda i: i > 0)
    created = fields.DateTime(required=True)
    updated = fields.DateTime()