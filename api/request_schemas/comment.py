from marshmallow import validate
from webargs import fields

__base_schema = {
    "content": fields.Str(required=True,
                          validate=validate.Length(min=10, max=255)),
    "userName": fields.Str(validate=validate.Length(min=1, max=255))
}

create_schema = {
    **__base_schema,
    **{"parent": fields.Int(validate=lambda i: i > 0)}
}

update_schema = {
    **__base_schema
}
