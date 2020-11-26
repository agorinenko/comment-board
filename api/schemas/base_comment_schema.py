from marshmallow import fields, validate

from api.schemas.base_schema import BaseSchema


class IdSchema(BaseSchema):
    id = fields.Int(required=True, validate=lambda i: i > 0)


class BaseCommentSchema(BaseSchema):
    content = fields.Str(required=True, validate=validate.Length(min=10, max=255))
    user_name = fields.Str(data_key="userName", validate=validate.Length(min=1, max=255))
