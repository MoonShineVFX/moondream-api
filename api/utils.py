from flask import jsonify, Response, request
from firebase_admin import auth


def base_response(status_code, message="", errors=[], data={}) -> Response:
    result = 1 if status_code // 100 == 2 else 0
    response = jsonify({
        "result": result,
        "message": str(message),
        "errors": errors,
        "data": data
    })
    
    response.status_code = status_code
    return response

