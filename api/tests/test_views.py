"""Test Views.
"""
from decimal import Decimal


def test_loan_require_view_post_should_retrieve_201(client) -> None:
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


def test_loan_detail_view_get_should_retrieve_200(client) -> None:
    """Test if loan detail view get retrieves 200.

    :param client: django test client
    """
    response = client.get('/api/v1/loan/uuidtal')

    assert response.status_code == 200
