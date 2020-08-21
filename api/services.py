"""Module that represents external services call.
"""
from abc import abstractmethod, ABC
from typing import Dict

import requests
from django.conf import settings


class BaseService(ABC):
    """Base class for services.
    """

    def __init__(self) -> None:
        """Base constructor.
        """
        self.headers: Dict = {}

    @abstractmethod
    def request(self, request_data: Dict) -> Dict:
        """DO a url request.

        :param request_data: A dictionary with request sended data
        """


class ScoreService(BaseService):
    """Service for score calculation.
    """

    def __init__(self) -> None:
        """Score Service constructor.
        """
        super().__init__()
        self.url = '{0}/{1}'.format(settings.EXTERNAL_API_URL, '/score')

    def request(self, request_data: Dict) -> Dict:
        """Do a url request.

        :param request_data: A dictionary with request sended data
        """
        import pdb; pdb.set_trace()


class CommitmentService(BaseService):
    """Service for score calculation.
    """

    def __init__(self) -> None:
        """Score Service constructor.
        """
        super().__init__()
        self.url = '{0}/{1}'.format(settings.EXTERNAL_API_URL, '/')

    def request(self, request_data: Dict) -> Dict:
        """Do a url request.

        :param request_data: A dictionary with request sended data
        """
        import pdb; pdb.set_trace()
