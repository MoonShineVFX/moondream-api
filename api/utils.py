import base64
from flask import jsonify, request
from marshmallow.exceptions import ValidationError


def output_json(data, code, headers={}):
    result= 1 if code // 100 == 2 else 0
    if result:
        data = {"data": data}
    data["result"] = result
    res = jsonify(data)
    res.status_code = code
    referrer = request.referrer[:-1] if request.referrer else "*"
    default_headers = {
        **headers,
        "Access-Control-Allow-Origin": referrer,
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Credentials": "true"
    }
    
    res.headers.extend(default_headers)
    return res



def base64_encode_url(email, password):
    s = email + ":" + password
    encoded = str(base64.b64encode(bytes(s, "utf-8")), 'utf-8')
    return encoded.replace('=', '').replace('+', '-').replace('/', '_')


def base64_decode_url(token):
    if not token:
        raise ValidationError("")
    type, code = token.rsplit(" ", 1)
    if type != "Basic":
        raise ValidationError("")
    
    value = code.replace('-', '+').replace('_', '/')
    value += '=' * (len(value) % 4)
    decode = str(base64.urlsafe_b64decode(value), 'utf-8')
    email, password = decode.rsplit(":", 1)
    return email, password