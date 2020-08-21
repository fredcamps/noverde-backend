def test_loan_require_view_post_should_retrieve_201(client) -> None:
    """Test if loan require view post retrieves 201.

    :param client: django test client
    """
    request_data = {

    }
    response = client.post('/api/v1/loan', request_data)

    assert response.status_code == 201


def test_loan_detail_view_should_get_200(client) -> None:
    """Test if loan detail view get retrieves 200.

    :param client: django test client
    """
    response = client.get('/api/v1/loan/uuidtal')

    assert response.status_code == 200
