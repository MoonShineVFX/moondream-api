from firebase_admin.exceptions import FirebaseError
from marshmallow.exceptions import ValidationError
from flask import jsonify, Response


def parse_request_form(schema, request):
    files = request.files.getlist('data') or []
    form = request.form.to_dict()
    return schema.load(form), files


def moonshine_response_format(result: int, message: str = "", errors: list = [], data: object = {}) -> dict:
    return {
        "result": result,
        "message": str(message),
        "errors": errors,
        "data": data
    }


def successful_format(data: object = {}, message: str = ""):
    return moonshine_response_format(result=1, data=data, message=message)


def error_format(message: str, errors: list = []):
    return moonshine_response_format(result=0, message=message, errors=errors)


# def moonshine_common_response(status_code: int, message: str = "", errors: list = [], data: object = {}) -> Response:
#     result = 1 if 200 <= status_code <= 299 else 0
#     return jsonify({
#         "result": result,
#         "message": str(message),
#         "errors": errors,
#         "data": data
#     }), status_code


# def successful_response(status_code, data: object = {}, message: str = ""):
#     return moonshine_common_response(status_code, data=data, message=message)


# def error_response(status_code, message: str, errors: list = []):
#     return moonshine_common_response(status_code, message=message, errors=errors)


def firebase_error_response(e: FirebaseError) -> Response:
    response = e.http_response
    status_code = response.status_code or 400
    default_message = str(e) or ''
    return jsonify(moonshine_response_format(result=0, message=default_message)), status_code


def handle_errors_response(e) -> Response:
    print(e.__class__, e)
    if e.__class__ == FirebaseError:
        return firebase_error_response(e)
    elif e.__class__ == ValidationError:
        return jsonify(error_format(message=str(e))), 400
    else:
        return jsonify(error_format(message=str(e))), 400
