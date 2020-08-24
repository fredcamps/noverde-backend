"""Test Views.
"""
from decimal import Decimal

import pytest
from django.test.client import Client
from pytest_mock.plugin import MockerFixture


@pytest.mark.django_db()
def test_loan_require_view_post_should_retrieve_201(client: Client) -> None:   # noqa
    """Test if loan require view post retrieves 201.

    :param client: django test client
    """
    request_data = {
        'name': 'Some Name',
        'cpf': '55822477348',
        'birthdate': '1990-01-01',
        'amount': Decimal('1000'),
        'terms': 6,
        'income': Decimal('1000'),
    }
    response = client.post('/api/v1/loan', request_data)

    assert response.status_code == 201


def test_loan_detail_view_get_should_retrieve_200(
    client: Client,
    mocker: MockerFixture,
) -> None:  # noqa
    """Test if loan detail view get retrieves 200.

    :param mocker: Mock fixture
    :param client: django test client
    """
    mocked_loan = mocker.MagicMock()
    mocked_loan.id = 'uuidtal'
    mocked_loan.status = 'completed'
    mocked_loan.result = 'approved'
    mocked_loan.refused_policy = None
    mocked_loan.proposal.amount = Decimal('1000')
    mocked_loan.proposal.terms = 6
    mocked_get_loan = mocker.patch('api.views.logic.get_loan', return_value=mocked_loan)
    response = client.get('/api/v1/loan/uuidtal')
    mocked_get_loan.assert_called_once_with(loan_id='uuidtal')

    assert response.status_code == 200
