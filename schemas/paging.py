from webargs import fields

paging_schema = {
    "limit": fields.Int(validate=lambda i: i > 0, missing=20),
    "offset": fields.Int(validate=lambda i: i > 0, missing=0),
}
