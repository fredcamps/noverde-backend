"""logic.py unit tests.
"""
from decimal import Decimal
from typing import Tuple

import pytest

from api import logic
from api.models import Loan


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
    with pytest.raises(ValueError, match='No terms found for commitment rate!'):
        logic.get_proposal_terms(loan=loan, commitment=Decimal('0.8'))

    assert interests == 'interests'
