"""Decorators.
"""
from typing import Any, Callable, Type

from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
from schema import Schema, SchemaError


def validate_request_data(schema: Schema) -> Callable:
    """Decorator for validate requrest parameters.

    :param schema: a schema that will use for validation.
    :return: a callable wrapper
    """
    def inner(func: Callable) -> Callable:  # noqa: WPS430
        def wrapper(  # noqa: WPS430
            view: Type[APIView],
            request: HttpRequest,
            *args: Any,
        ) -> Response:
            request_data = dict(request.data.items())
            try:
                schema.validate(request_data)
            except (SchemaError, ValidationError) as exception:
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data={'errors': [str(exception)]},
                )

            return func(view, request, *args)

        return wrapper

    return inner
