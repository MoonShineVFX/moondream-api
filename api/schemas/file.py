from marshmallow import Schema, fields, post_load
from ..models.file import MediaFile

class FileSchema(Schema):
    fileName = fields.String(attribute="file_name")
    fileURL = fields.String(attribute="file_url")
    id = fields.String()
    path = fields.String()
    size = fields.Integer()
    thumbURL = fields.String(attribute="thumb_url")
    type = fields.String()
    userId = fields.String(attribute="user_id")
    sessionId = fields.String(attribute="session_id")
    create = fields.Integer()

    @post_load
    def load_SessionFile(self, data, **kwargs):
        return MediaFile(**data)

    
class FileQuerySchema(Schema):
    begin = fields.Integer()
    end = fields.Integer()
    
class PathsOfFilesSchema(Schema):
    paths = fields.List(fields.String())
    
class UploadFilesSchema(Schema):
    sessionId = fields.String(attribute="session_id")
    