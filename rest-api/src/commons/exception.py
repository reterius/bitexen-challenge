class BusinessRuleError(Exception):
    def __init__(self, code: str, message, sub_message: str = None):
        super(Exception, self).__init__(message)
        self.code = code or "handler.exception.business_rule_error"
        self.sub_message = sub_message

    @staticmethod
    def get_code(code: str, default: str) -> str:
        if code is None or "":
            return default

        return code


class NotFoundError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.not_found_error")
        super(NotFoundError, self).__init__(code, message, sub_message)


class ValidationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.validation_error")
        super(ValidationError, self).__init__(code, message, sub_message)


class ExistError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.exist_error")
        super(ExistError, self).__init__(code, message, sub_message)


class ArgumentNullError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_null_error")
        super(ArgumentNullError, self).__init__(code, message, sub_message)


class ArgumentEmptyError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_empty_error")
        super(ArgumentEmptyError, self).__init__(code, message, sub_message)


class ArgumentNullOrEmptyError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.argument_null_or_empty_error")
        super(ArgumentNullOrEmptyError, self).__init__(code, message, sub_message)


class AuthenticationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.authentication_error")
        super(AuthenticationError, self).__init__(code, message, sub_message)


class AuthorizationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.authorization_error")
        super(AuthorizationError, self).__init__(code, message, sub_message)


class FieldValidationError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.validation_error")
        super(FieldValidationError, self).__init__(code, message, sub_message)


class DbUpdateError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.db_update_error")
        super(DbUpdateError, self).__init__(code, message, sub_message)


class CacheUpdateError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.cache_update_error")
        super(CacheUpdateError, self).__init__(code, message, sub_message)


class DbGetDataError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.db_get_data_error")
        super(DbGetDataError, self).__init__(code, message, sub_message)


class AuthorityError(BusinessRuleError):
    def __init__(self, code: str, message: str, sub_message: str = None):
        code = self.get_code(code, "handler.exception.authority")
        super(AuthorityError, self).__init__(code, message, sub_message)
