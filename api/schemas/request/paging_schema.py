from marshmallow import Schema, fields


class PagingSchema(Schema):
    limit = fields.Int(validate=lambda i: i > 0, missing=20)
    offset = fields.Int(validate=lambda i: i > 0, missing=0)
