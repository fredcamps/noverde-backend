"""logic.py unit tests.
"""
import json
from decimal import Decimal
from typing import Tuple

import pytest
from mixer.backend.django import mixer
from pytest_mock.plugin import MockFixture

from api import logic
from api.models import Policy, Loan
from api.logic import APIException, CommitmentService, ScoreService, ValidationError
from api.helpers import convert_str_date_to_object


@pytest.mark.django_db()
def test_get_interest_rate_should_retrieve_percentage(interests: str) -> None:  # noqa: WPS
    """Test if get_interest_rate should retrieve percentage.

    :param interests: a fixture that initialiazes loaddata of interests.
    """
    percentage1 = logic.get_interest_rate(score=600, terms=6)  # noqa: WPS432
    percentage2 = logic.get_interest_rate(score=699, terms=6)  # noqa: WPS432
    percentage3 = logic.get_interest_rate(score=700, terms=6)  # noqa: WPS432
    percentage4 = logic.get_interest_rate(score=799, terms=6)  # noqa: WPS432
    percentage5 = logic.get_interest_rate(score=800, terms=6)  # noqa: WPS432
    percentage6 = logic.get_interest_rate(score=899, terms=6)  # noqa: WPS432
    percentage7 = logic.get_interest_rate(score=900, terms=6)  # noqa: WPS432
    percentage8 = logic.get_interest_rate(score=1000, terms=6)  # noqa: WPS432

    assert percentage1 == Decimal('0.064')
    assert percentage2 == Decimal('0.064')
    assert percentage3 == Decimal('0.055')
    assert percentage4 == Decimal('0.055')
    assert percentage5 == Decimal('0.047')
    assert percentage6 == Decimal('0.047')
    assert percentage7 == Decimal('0.039')
    assert percentage8 == Decimal('0.039')
    assert interests == 'interests'


@pytest.mark.django_db()
def test_get_interest_rate_should_raise_does_not_exist(interests: str) -> None:  # noqa: WPS
    """Test if get_interest_rate should raises DoesNotExist.

    :param interests: a fixture that initialiazes loaddata of interests.
    """
    with pytest.raises(ValueError, match='Interest rate not found!'):
        logic.get_interest_rate(score=500, terms=13)  # noqa: WPS432
    assert interests == 'interests'


@pytest.mark.django_db()
def test_get_all_terms_should_retrieve_result(interests: str) -> None:  # noqa: WPS
    """Test if get_all_terms should retrieve result.

    :param interests: a fixture that initialiazes loaddata of interests.
    """
    terms = logic.get_all_terms()
    assert terms == [6, 9, 12]
    assert interests == 'interests'


@pytest.mark.django_db()
def test_get_all_terms_should_raises_value_error() -> None:  # noqa: WPS
    """Test if get_all_terms should raises Value Error.
    """
    with pytest.raises(ValueError, match='Have no interest/terms registered!'):
        logic.get_all_terms()


def test_calculate_installment_should_retrieve_result() -> None:  # noqa: WPS
    """Test if calculate_installment should retrieve result.
    """
    installment = logic.calculate_installment(
        amount=Decimal('1000'),
        terms=6,
        interest=Decimal('0.055'),
    )
    assert installment == Decimal('175.83')


@pytest.mark.django_db()
def test_get_proposal_terms_should_retrieve_result(interests: str, loans: Tuple) -> None:  # noqa
    """Test if get_proposal_terms should retrieve result.

    :param interests: a fixture that initialiazes loaddata of interests
    :param loans: a fixture that contains a immutable list of loans
    """
    loan = loans[-1]
    loan.score = 600
    loan.save()
    terms = logic.get_proposal_terms(loan=loan, commitment=Decimal('0.8'))

    assert terms == 12  # noqa: WPS432
    assert interests == 'interests'


@pytest.mark.django_db()
def test_get_proposal_terms_should_raise_value_error(interests: str, loans: Tuple) -> None:  # noqa
    """Test if get_proposal_terms should retrieve result.

    :param interests: a fixture that initialiazes loaddata of interests
    :param loans: a fixture that contains a immutable list of loans
    """
    loan = loans[-2]
    loan.score = 600
    loan.save()
    with pytest.raises(ValidationError, match='No terms found for commitment rate!'):
        logic.get_proposal_terms(loan=loan, commitment=Decimal('0.8'))

    assert interests == 'interests'


@pytest.mark.django_db()
def test_start_age_policy_should_validate_age(loans: Tuple) -> None:
    """Test if start_age_policy validates age.

    :param loans: a fixture that contains a immutable list of loans
    """
    loan = logic.start_age_policy(loan_id=str(loans[-2].id))
    assert loan.state == 'processing_score'


@pytest.mark.django_db()
def test_start_age_policy_should_handle_validation_error(loans: Tuple) -> None:  # noqa: WPS118
    """Test if start_age_policy handles validation error.

    :param loans: a fixture that contains a immutable list of loans
    """
    loan = logic.start_age_policy(loan_id=str(loans[0].id))
    assert loan.refused_policy == 'age'
    assert loan.state == 'refused'


@pytest.mark.django_db()
def test_start_score_policy_should_validate_score(policies: Tuple, mocker: MockFixture) -> None:
    """Test if start score policy validates score.

    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-2]
    policy.loan.process_age()
    policy.loan.save()
    expected_response = {'score': 701}
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(ScoreService, 'request', return_value=expected_response)
    processed_loan = logic.start_score_policy(loan_id=str(policy.loan.id))
    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})

    assert processed_loan.state == 'processing_commitment'
    assert processed_loan.score == expected_response.get('score')


@pytest.mark.django_db()
def test_start_score_policy_should_handle_validation_error(  # noqa: WPS118
    policies: Tuple,
    mocker: MockFixture,
) -> None: # noqa
    """Test if start_score_policy handles validation error.

    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-2]
    policy.loan.process_age()
    policy.loan.save()
    expected_response = {'score': 100}
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(ScoreService, 'request', return_value=expected_response)
    logic.start_score_policy(loan_id=str(policy.loan.id))
    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})
    assert policy.loan.refused_policy == 'score'


@pytest.mark.django_db()
def test_start_score_policy_should_handle_api_exception(  # noqa: WPS118
    policies: Tuple,
    mocker: MockFixture,
) -> None:
    """Test if start_score_policy handles api exception.

    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-2]
    policy.loan.process_age()
    policy.loan.save()
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(ScoreService, 'request', side_effect=APIException('A'))
    with pytest.raises(APIException, match='A'):
        logic.start_score_policy(loan_id=str(policy.loan.id))

    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})


@pytest.mark.django_db()
def test_start_commitment_policy_should_validate_commitment(   # noqa: WPS118
    policies: Tuple,
    mocker: MockFixture,
    interests: str,
) -> None:
    """Test if start_commitment_policy validates commitment.

    :param interests: a loaddata setup fixture
    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-1]
    policy.loan.score = 701
    policy.loan.process_age()
    policy.loan.process_score()
    policy.loan.save()
    expected_response = {'commitment': Decimal('0.2')}
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(
        CommitmentService,
        'request',
        return_value=expected_response,
    )
    loan = logic.start_commitment_policy(loan_id=str(policy.loan.id))
    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})
    assert loan.state == 'approved'
    assert interests == 'interests'


@pytest.mark.django_db()
def test_start_commitment_policy_should_handle_validation_error(  # noqa: WPS118
    policies: Tuple,
    mocker: MockFixture,
    interests: str,
) -> None:
    """Test if start_commitment_policy handles validation error.

    :param interests: a loaddata setup fixture
    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-1]
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(
        CommitmentService,
        'request',
        return_value={'commitment': Decimal('0.99')},
    )
    loan = logic.start_commitment_policy(loan_id=str(policy.loan.id))
    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})
    assert loan.state == 'refused'
    assert loan.refused_policy == 'commitment'
    assert interests == 'interests'


@pytest.mark.django_db()
def test_start_commitment_policy_should_handle_api_exception(  # noqa: WPS118
    policies: Tuple,
    mocker: MockFixture,
    interests: str,
) -> None:
    """Test if start_commitment_policy handles api exception.

    :param interests: a loaddata setup fixture
    :param policies: a fixture that contains a immutable list of policies
    :param mocker: fixture that contains Mock utility
    """
    policy = policies[-1]
    mocked_loan = mocker.patch('api.logic.get_loan', return_value=policy.loan)
    mocked_service = mocker.patch.object(
        CommitmentService,
        'request',
        side_effect=APIException('A'),
    )
    with pytest.raises(APIException, match='A'):
        logic.start_commitment_policy(loan_id=str(policy.loan.id))

    assert interests == 'interests'
    mocked_loan.assert_called_once_with(policy.loan.id)
    mocked_service.assert_called_once_with(request_data={'cpf': policy.loan.cpf})
