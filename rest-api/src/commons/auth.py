import functools
from src.commons.request import get_auth_token
from src.commons.response import bad_request_result, forbidden_result


def check(auth_roles, user_roles):
    for auth_role in auth_roles:
        if auth_role in user_roles:
            return True

    return False


def authorize(_func=None, *, roles: list, rule: str = "any"):  # = ["anonymous", ]
    def decorator_auth(func):

        @functools.wraps(func)
        def wrapper_auth(*args, **kwargs):
            auth_token = get_auth_token()

            if rule not in ["all", "any"]:
                return bad_request_result(code="all/any", message="all yada any kullanilmali...")

            auth_roles = sorted(roles)
            user_roles = sorted(auth_token["roles"])

            if rule == "all":
                if auth_roles != user_roles:
                    return forbidden_result(code="all", message="Kullanicinin rolu uygun degil...")

            if rule == "any":
                if not check(auth_roles, user_roles):
                    return forbidden_result(code="any", message="Kullanicinin rolu uygun degil...")

            return func(*args, **kwargs)

        return wrapper_auth

    if _func is None:
        return decorator_auth
    else:
        return decorator_auth(_func)
