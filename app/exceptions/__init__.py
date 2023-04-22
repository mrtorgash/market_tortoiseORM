from fastapi import status
from typing import Optional


class APIexception(Exception):
    status_code: int
    message: str
    debug: str

    def __init__(self, message: Optional[str] = None, debug: Optional[str] = None):
        self.message = message or self.message
        self.debug = debug


class InternalServerError(APIexception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Упс, пофикси."


class ForbiddenError(APIexception):  # запрещен
    status_code = status.HTTP_403_FORBIDDEN
    message = "forbidden"


class UnAuthorized(APIexception):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid authentication credentials"


class NotFoundError(APIexception):
    status_code = status.HTTP_404_NOT_FOUND
    message = "not found"


class BadRequestError(APIexception):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "bad req"
