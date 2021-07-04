import jsonschema
import marshmallow

from src.commons.exception import ArgumentNullError, ArgumentEmptyError, ArgumentNullOrEmptyError, ExistError, \
    ValidationError, NotFoundError, BusinessRuleError, FieldValidationError
from src.commons.response import bad_request_result, conflict_result, not_found_result, internal_server_error_result, \
    unauthorized_result


def jwt_handlers_config(jwt):

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return unauthorized_result(
            code="handler.jwt.expired_token_loader",
            message="The token has expired"
        )

    @jwt.invalid_token_loader
    def my_invalid_token_loader(e):
        return unauthorized_result(
            code="handler.jwt.invalid_token_loader",
            message="The token is invalid",
            description=str(e)
        )

    @jwt.unauthorized_loader
    def my_unauthorized_loader(fp):
        return unauthorized_result(
            code="handler.jwt.unauthorized_loader",
            message="The token is unauthorized",
            description=str(fp)
        )

    @jwt.needs_fresh_token_loader
    def my_needs_fresh_token_loader():
        return unauthorized_result(
            code="handler.jwt.needs_fresh_token_loader",
            message="Needs fresh token"
        )


def response_handlers_config(app):

    @app.errorhandler(400)
    def bad_request_error_handler(ex):
        return ex, 400

    @app.errorhandler(404)
    def not_found_error_handler(ex):
        return ex, 404

    @app.errorhandler
    def default_error_handler(ex):
        return ex, 500


def exception_handlers_config(app):

    @app.errorhandler(ArgumentNullError)
    def argument_null_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(ArgumentEmptyError)
    def argument_empty_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(ArgumentNullOrEmptyError)
    def argument_null_or_empty_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(ExistError)
    def exist_error_handler(error):
        return conflict_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(ValidationError)
    def validation_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(FieldValidationError)
    def validation_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
            description=error.sub_message
        )

    @app.errorhandler(NotFoundError)
    def not_found_error_handler(error):
        return not_found_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(BusinessRuleError)
    def business_rule_error_handler(error):
        return bad_request_result(
            code=error.code,
            message=str(error),
        )

    @app.errorhandler(Exception)
    def all_exception_handler(error):
        return internal_server_error_result(
            code="handler.exception.internal_server_error",
            message=str(error)
        )


def jsonschema_handlers_config(app):

    @app.errorhandler(jsonschema.ValidationError)
    def on_validation_error_handler(e):
        return bad_request_result(
            code="VALIDATION_ERROR",
            message=str(e),
        )

"""
def marshmallow_handlers_config(app):

    @app.errorhandler(marshmallow.ValidationError)
    def on_validation_error_handler(e):
        data = e.__dict__["messages"]
        print(data)

        keys = data.keys()

        messages = []
        for key in keys:
            messages.append(data[key])

        return bad_request_result(
            code="VALIDATION_ERROR",
            message=",".join(keys),
            description="asdasd",
        )
"""