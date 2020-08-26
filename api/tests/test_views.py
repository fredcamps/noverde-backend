"""Test Views.
"""
from decimal import Decimal
from uuid import UUID

import pytest
from django.test.client import Client
from pytest_mock.plugin import MockerFixture
from rest_framework import status

from api.logic import (
    CommitmentService,
    ScoreService,
)


@pytest.mark.django_db()
def test_loan_require_view_post_should_retrieve_201(  # noqa: WPS
    client: Client,
    mocker: MockerFixture,
    interests: str,
) -> None:
    """Test if loan require view post retrieves 201.

    :param client: django test client
    :param mocker: fixture that contains Mock utility
    :param interests: fixturar that have interest rate
    """
    request_data = {
        'name': 'Some Name',
        'cpf': '55822477348',
        'birthdate': '1990-01-01',
        'amount': Decimal('1000'),
        'terms': 6,
        'income': Decimal('1000'),
    }
    mocker.patch.object(ScoreService, 'request', return_value={'score': 701})
    mocker.patch.object(
        CommitmentService,
        'request',
        return_value={'commitment': Decimal('0.1')},
    )
    response = client.post('/api/v1/loan', request_data)

    assert 'id' in response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'interests' == interests


def test_loan_detail_view_get_should_retrieve_201(  # noqa: WPS
    client: Client,
    mocker: MockerFixture,
) -> None:
    """Test if loan detail view get retrieves 200.

    :param mocker: Mock fixture
    :param client: django test client
    """
    loan_id = 'e0257542-0795-409e-b6b5-80dce591aa32'
    mocked_loan = mocker.MagicMock()
    mocked_loan.id = UUID(loan_id)  # noqa: WPS125
    mocked_loan.status = 'completed'
    mocked_loan.result = 'approved'  # noqa: WPS110
    mocked_loan.refused_policy = None
    mocked_loan.proposal.amount = Decimal('1000')
    mocked_loan.proposal.terms = 6
    mocked_get_loan = mocker.patch('api.views.logic.get_loan', return_value=mocked_loan)
    response = client.get('/api/v1/loan/{0}'.format(loan_id))
    mocked_get_loan.assert_called_once_with(loan_id=loan_id)

    assert response.status_code == status.HTTP_200_OK
