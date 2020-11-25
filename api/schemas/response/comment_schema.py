from marshmallow import fields

from api.schemas.base_comment_schema import BaseCommentSchema


class CommentSchema(BaseCommentSchema):
    id = fields.Int(dump_only=True)
    parent_id = fields.Int(data_key="parentId", validate=lambda i: i > 0)
    created = fields.DateTime(required=True)
    updated = fields.DateTime()