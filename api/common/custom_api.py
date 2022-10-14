
from flask import request, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from flask_restful.utils import http_status_message
from firebase_admin.exceptions import FirebaseError


class CustomApi(Api):
    pass
    # def __init__(self, *args, **kwargs):
    #     super(CustomApi, self).__init__(*args, **kwargs)
    #     self.representations = {
    #         'application/json': self.output_json
    #     }
            
    # def output_json(self, data, code, headers={}):
    #     result= 1 if code // 100 == 2 else 0
    #     if result:
    #         data = {"data": data}
    #     data["result"] = result
    #     res = jsonify(data)
    #     res.status_code = code
    #     referrer = request.referrer[:-1] if request.referrer else "*"
    #     default_headers = {
    #         **headers,
    #         "Access-Control-Allow-Origin": referrer,
    #         "Access-Control-Allow-Methods": "*",
    #         "Access-Control-Allow-Credentials": "true"
    #     }
        
    #     res.headers.extend(default_headers)
    #     return res
    
    # def handle_error(self, e):
        
    #     if isinstance(e, HTTPException):
    #         print('HTTPException', e)
    #         code = e.code
    #         message = getattr(e, "description", http_status_message(code))
    #         headers = e.get_response().headers
    #         return self.output_json({"message": message}, code, headers=headers, result=0 )
        
    #     elif isinstance(e, FirebaseError):
    #         print('FirebaseError', e)
    #         response = e.http_response
    #         code = response.status_code
    #         message = str(e)
    #         print()
    #         return self.output_json({"message": message}, code, result=0)
        
    #     else:
    #         print('else error', e)
    #         code = e.code
    #         message = str(e)
    #         return self.output_json({"message": message}, code, result=0)
       