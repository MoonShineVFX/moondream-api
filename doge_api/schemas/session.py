from marshmallow import Schema, fields, post_load, post_dump, pre_dump
from datetime import datetime


class SessionBaseSchema(Schema):
    id = fields.String(dump_only=True)
    order_today = fields.Integer()
    start_at = fields.DateTime()
    end_at = fields.DateTime()
    
    @post_load
    def to_timestamp(self, data, **kwargs):
        data["start_at"] = int(data["start_at"].timestamp())
        data["end_at"] = int(data["end_at"].timestamp())
        
        return data
    
    @pre_dump
    def from_timestamp(self, data, **kwargs):
        data["start_at"] = datetime.fromtimestamp(data["start_at"])
        data["end_at"] = datetime.fromtimestamp(data["end_at"])
        
        return data
    
class SessionRecordsByRangeSchema(Schema):
    id = fields.String()
    image_url = fields.Url(attribute="fileURL")
    thumb_url = fields.Url(attribute="thumb")
    type = fields.String()
    create_at = fields.Integer(attribute="create")
    
    @post_dump
    def to_UTC(self, data, **kwargs):
        data["create_at"] = datetime.fromtimestamp(data["create_at"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        return data
    
    

class SessionRecordsLinkSchema(Schema):
    date = fields.Date()
    order = fields.Integer()

    
class SessionRecordsLinkByRangeSchema(Schema):
    start = fields.DateTime()
    end = fields.DateTime()
    