from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response.data["detail"] = "Token is invalid or expired"

    return response
