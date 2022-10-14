from marshmallow import Schema, fields, pre_load, post_load
from datetime import datetime, time

class FileSchema(Schema):
    id = fields.String()
    create = fields.Integer()
    type = fields.String()
    path = fields.String()
    size = fields.Integer()
    name = fields.String(attribute="file_name")
    fileURL = fields.String(attribute="file_url")
    thumb = fields.String(attribute="thumb_url")
    creator = fields.String()
    sessionId = fields.String(attribute="session_id")

    
class FileQuerySchema(Schema):
    begin = fields.Integer()
    end = fields.Integer()
    
    @pre_load
    def check_params(self, data, **kwargs):
        data["begin"] = int(data.get("begin", datetime.combine(datetime.now(), time.min).timestamp()))
        data["end"] = int(data.get("end", datetime.combine(datetime.now(), time.max).timestamp()))
        
        return data
    
class PathsOfFilesSchema(Schema):
    paths = fields.List(fields.String())
    
    
    
class UploadFilesSchema(Schema):
    created_at = fields.DateTime()
    sessionId = fields.String(attribute="session_id", )
    
    @pre_load
    def check_params(self, data, **kwargs):
        data["sessionId"] = data.get("sessionId", "")
        return data