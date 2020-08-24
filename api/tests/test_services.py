"""Test services.
"""
import json
from decimal import Decimal

from pytest_mock.plugin import MockFixture
from rest_framework import status

from api import services


def test_score_service_should_get_succesfull_response(mocker: MockFixture) -> None:
    """Test if score service should get succesfull response.

    :param mocker: fixture that contains Mock utility
    """
    request_data = {
        'cpf': '72456336062',
    }
    expected_response = {
        'score': 701,
    }
    mocked_response = mocker.MagicMock()
    mocked_response.status_code = status.HTTP_200_OK
    mocked_response.json.return_value = expected_response
    mocked_request = mocker.patch('api.services.requests.post', return_value=mocked_response)
    service = services.ScoreService()
    response = service.request(request_data=request_data)
    mocked_request.assert_called_once_with(
        service.url,
        data=json.dumps(request_data),
        headers=service.headers,
    )
    assert expected_response == response


def test_commitment_service_should_get_succesfull_response(mocker: MockFixture) -> None:
    """Test if commitment service should get succesfull response.

    :param mocker: fixture that contains Mock utility
    """
    request_data = {
        'cpf': '72456336062',
    }
    expected_response = {
        'commitment': 0.09,
    }
    mocked_response = mocker.MagicMock()
    mocked_response.status_code = status.HTTP_200_OK
    mocked_response.json.return_value = expected_response
    mocked_request = mocker.patch('api.services.requests.post', return_value=mocked_response)
    service = services.CommitmentService()
    response = service.request(request_data=request_data)
    mocked_request.assert_called_once_with(
        service.url,
        data=json.dumps(request_data),
        headers=service.headers,
    )

    assert Decimal(expected_response.get('commitment')) == Decimal(response.get('commitment'))
