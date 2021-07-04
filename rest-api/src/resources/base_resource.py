from flask_restful import Resource

from src.commons.request import get_auth_token


class BaseResource(Resource):

    def __init__(self):
        pass

    @classmethod
    def auth_token(cls, key: str = None):
        return get_auth_token(key=key)

    @property
    def account_id(self):
        return get_auth_token("_id")
