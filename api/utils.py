from flask import jsonify, Response, request


def base_response(status_code, message="", errors=[], data={}) -> Response:
    result = 1 if status_code // 100 == 2 else 0
    response = jsonify({
        "result": result,
        "message": str(message),
        "errors": errors,
        "data": data
    })
    
    response.status_code = status_code
    referrer = request.referrer[:-1] if request.referrer else "*"
    response.headers.add("Access-Control-Allow-Origin", referrer)
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    
    return response
