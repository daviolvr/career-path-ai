
class AppException(Exception):
    status_code: int = 400
    default_code: str = "application_error"

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or self.default_code
        super().__init__(message)


class ValidationException(AppException):
    status_code = 400
    default_code = "validation_error"


class QueryValidationException(ValidationException):
    default_code = "query_validation_error"


class NotFoundException(AppException):
    status_code = 404
    default_code = "not_found"


class ConflictException(AppException):
    status_code = 409
    default_code = "conflict"


class PermissionDeniedException(AppException):
    status_code = 403
    default_code = "forbidden"


class AuthenticationException(AppException):
    status_code = 401
    default_code = "unauthorized"


class EntityNotFoundException(NotFoundException):
    default_code = "entity_not_found"

    def __init__(self, entity_name: str):
        message = f"{entity_name} not found"
        super().__init__(message)
