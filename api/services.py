"""Module that represents external services call.
"""
import json
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict

import requests
from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.response import Response


class BaseService(ABC):
    """Base class for services.
    """

    def __init__(self) -> None:
        """Base constructor.
        """
        self.headers: Dict = {
            'x-api-key': settings.EXTERNAL_API_TOKEN,
            'content-type': 'application/json',
        }
        self.url: str = None

    def request(self, request_data: Dict) -> Dict[str, Any]:
        """Do a url request.

        :param request_data: A dictionary with request sended data
        :raises APIException: raised when get unexpected response from server
        :return: A dict with response data eg: {'score': 704}
        """
        response = self._request_helper(request_data=request_data)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.APIException('Unexpected response from server')

        return dict(response.json())

    def _post(self, request_data: Dict) -> Response:
        return requests.post(
            self.url,
            data=json.dumps(request_data),
            headers=self.headers,
        )

    @abstractmethod
    def _request_helper(self, request_data: Dict) -> Response:
        """Should override.

        :param request_data: A dict with request data
        """


class ScoreService(BaseService):
    """Service for score calculation.
    """

    def __init__(self) -> None:
        """Score Service constructor.
        """
        super().__init__()
        self.url = '{0}/{1}'.format(settings.EXTERNAL_API_URL, 'score')

    def _request_helper(self, request_data: Dict) -> Response:
        return self._post(request_data)


class CommitmentService(BaseService):
    """Service for score calculation.
    """

    def __init__(self) -> None:
        """Score Service constructor.
        """
        super().__init__()
        self.url = '{0}/{1}'.format(settings.EXTERNAL_API_URL, 'commitment')

    def request(self, request_data: Dict) -> Dict[str, Any]:
        """Do a url request.

        :param request_data: A dictionary with request sended data
        :return: A dict with response data eg: {'commitment': Decimal('0.12')}
        """
        response = super().request(request_data)
        response.update({'commitment': Decimal(response.get('commitment'))})
        return response

    def _request_helper(self, request_data: Dict) -> Response:
        return self._post(request_data)
