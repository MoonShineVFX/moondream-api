from flask_restful import Resource
from firebase_admin.exceptions import FirebaseError

from marshmallow.exceptions import MarshmallowError
from flask import request
from werkzeug.exceptions import HTTPException
from flask_restful.utils import http_status_message

from api.common.utils import output_json, base64_decode_url

class BaseResource(Resource):
    def parse_request_authorization(self):
        token = request.headers.get("Authorization")
        return base64_decode_url(token)
       
    def _parse_request_values(self, schema):
        values = request.values.to_dict() or {}
        return schema.load(values)
    
    def _parse_request_json(self, schema):
        json = request.get_json() or {}
        return schema.load(json)
    
    def parse_request_data(self, schema):
        if request.content_type == "application/json":
            return self._parse_request_json(schema)
        return self._parse_request_values(schema)
    
    def parse_request_files(self, key="files"):
        return request.files.getlist(key) or []
    
    def parse_request_file(self, key="file"):
        return request.files.get(key)
   
    def handle_errors_response(self, e):
        message = ""
        code = 500
        headers = {}
        
        print(e.__class__, isinstance(e, FirebaseError))
        
        if isinstance(e, FirebaseError):
            response = e.http_response
            code = response.status_code or code
            message = str(e)
        elif isinstance(e, HTTPException):
            code = e.code
            message = getattr(e, "description", http_status_message(code))
            headers = e.get_response().headers
        elif isinstance(e, MarshmallowError):
            code = 400
            message = str(e)
            headers = {}
        else:
            code = 500
            message = str(e)
            headers = {}
            
        return output_json(data={"message": message}, code=code, headers=headers)

    def handle_success_response(self, data={}, code=200, headers={}):
        return output_json(data=data, code=code, headers=headers)