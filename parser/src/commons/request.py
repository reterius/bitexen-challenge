from flask import request
from flask_jwt_extended import current_user, get_jwt_identity
from flask_marshmallow import Schema
from typing import TypeVar

from src.commons.exception import ValidationError, AuthenticationError

"""
def is_valid(scheme: dict) -> dict:
    try:
        data = request.json

        if data is None:
            raise ValidationError("request.validator.input_parameters_are_required", "input parameters not null")

        validate(data, scheme)

        return data

    except Exception as ex:
        print(ex)

        raise ValidationError("request.validator.input_parameters_not_valid", "input parameters not valid : " + str(ex))
"""

T = TypeVar('T')


def is_valid(schema: Schema):
    payload = request.json

    if payload is None:
        raise ValidationError("request.validator.input_parameters_are_required", "input parameters not null")

    try:
        validation_errors = schema.validate(payload)

        if len(validation_errors.keys()) > 0:
            raise Exception(validation_errors)

        obj = schema.load(payload)
        # obj = schema.dump(payload)

        return obj.data

    except ValidationError as err:
        raise ValidationError("request.validator.input_parameters_not_valid",
                              "input parameters not valid : " + str(err))

    except Exception as err:
        raise ValidationError("request.validator.input_parameters_not_valid",
                              "input parameters not valid : " + str(err))


def is_auth():
    try:
        if current_user is not None:
            return True

        return False

    except Exception as ex:
        raise AuthenticationError("request.jwt.authentication_not_found", "" + str(ex))


def get_auth_token(key: str = None):
    """
    print(1, current_user)
    print(2, get_current_user())
    print(3, get_raw_jwt())
    print(4, get_jwt_identity())
    print(5, get_jwt_claims())
    """

    jwt_identity = get_jwt_identity()
    if jwt_identity is None:
        raise AuthenticationError("request.jwt.authentication_identity_not_found", "jwt_identity is null",
                                  "jwt_identity")

    if key is None:
        return jwt_identity

    try:
        value = jwt_identity[key]
        return value

    except Exception:
        raise AuthenticationError("request.jwt.authentication_identity_key_not_found", "key not found", "key")
