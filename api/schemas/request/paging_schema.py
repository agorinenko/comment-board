from marshmallow import fields

from api.schemas.base_schema import BaseSchema


class PagingSchema(BaseSchema):
    limit = fields.Int(validate=lambda i: i > 0, missing=20)
    offset = fields.Int(validate=lambda i: i >= 0, missing=0)
