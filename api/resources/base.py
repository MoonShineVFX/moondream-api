import base64
from flask_restful import Resource
from firebase_admin.exceptions import FirebaseError
from marshmallow.exceptions import ValidationError
from flask import request

from ..utils import base_response

class BaseResource(Resource):
    def parse_request_authorization(self):
        s = request.headers.get("Authorization")
        if not s:
            raise ValidationError("")
        type, code = s.rsplit(" ", 1)
        if type != "Basic":
            raise ValidationError("")
        decode = base64.b64decode(code).decode("utf-8")
        email, password = decode.rsplit(":", 1)
        return email, password
    
    def parse_request_files(self, key="data"):
        return request.files.getlist(key) or []
    
    def parse_request_form(self, schema):
        form = request.form.to_dict() or {}
        return schema.load(form)
    
    def parse_request_json(self, schema):
        json = request.get_json() or {}
        return schema.load(json)
    
    
    def firebase_error_response(self, e: FirebaseError):
        response = e.http_response
        status_code = response.status_code or 400
        default_message = str(e) or ""
        return base_response(status_code=status_code, message=default_message)

    def handle_errors_response(self, e):
        
        if e.__class__ == FirebaseError:
            return self.firebase_error_response(e)
        elif e.__class__ == ValidationError:
            return base_response(status_code=400, message=str(e))
        else:
            return base_response(status_code=400, message=str(e))

    def handle_success_response(self, status_code=200, data: object = {}, message: str = ""):
        return base_response(status_code=status_code, data=data, message=message)