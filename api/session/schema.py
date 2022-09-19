from marshmallow import Schema, fields


class SessionBaseSchema(Schema):
    id = fields.String()


class SessionIdRequiredSchema(SessionBaseSchema):
    id = fields.String(required=True)


class SessionDownloadSchema(Schema):
    urls = fields.List(fields.String())
