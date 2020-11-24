from marshmallow import Schema, fields, validate


class BaseCommentSchema(Schema):
    board_id = fields.Str(data_key="boardId", required=True, validate=validate.Length(min=32, max=36))
    content = fields.Str(required=True, validate=validate.Length(min=10, max=255))
    user_name = fields.Str(data_key="userName", validate=validate.Length(min=1, max=255))
