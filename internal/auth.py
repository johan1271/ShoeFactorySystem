import jwt
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


def write_token(data: dict):
    token = jwt.encode({
        "id": data['id'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "role": data['role'],
        "exp": expire_date(15)
    }, key="ANYKEY", algorithm="HS256")
    return token.encode("UTF-8")


def validate_token(token, output=False):
    try:
        if output:
            return jwt.decode(token, key="ANYKEY", algorithms=["HS256"])
        jwt.decode(token, key="ANYKEY", algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except jwt.exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response