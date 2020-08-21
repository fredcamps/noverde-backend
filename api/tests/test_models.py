"""Test of api.models.
"""
from decimal import Decimal
from typing import Tuple

import pytest


@pytest.mark.django_db
def test_loan_should_refuse(loans: Tuple) -> None:
    """Test if loan model should get refused result.

    :param loans: a fixture that contains a immutable list of loans.
    """
    loan = loans[-1]
    loan.refused_policy = 'age'
    loan.refuse()
    loan.save()

    assert loan.status == 'completed'
    assert loan.result == 'refused'


@pytest.mark.django_db
def test_loan_should_not_refuse(loans: Tuple) -> None:
    """Test if loan model should not get refused result.

    :param loans: a fixture that contains a immutable list of loans.
    """
    loan = loans[-1]
    loan.refuse()
    loan.save()

    assert loan.status == 'processing'
    assert loan.result is None


@pytest.mark.django_db
def test_loan_should_approve(policies: Tuple) -> None:
    """Test if loan model should get approved result.

    :param policies: a fixture that contains a immutable list of policies.
    """
    loan = policies[0].loan
    loan.process_age()
    loan.score = 600
    loan.process_score()
    loan.commitment = Decimal('0.1')
    loan.approve()
    loan.save()

    assert loan.status == 'completed'
    assert loan.result == 'approved'


@pytest.mark.django_db
def test_loan_should_not_approve(loans: Tuple) -> None:
    """Test if loan model should not get approved result.

    :param loans: a fixture that contains a immutable list of loans.
    """
    loan = loans[-1]
    loan.state = 'processing_commitment'
    loan.approve()
    loan.save()

    assert loan.status == 'processing'
    assert loan.result is None


@pytest.mark.django_db
def test_loan_should_not_process_age(loans: Tuple) -> None:
    """Test if loan model should not process age.

    :param loans: a fixture that contains a immutable list of loans.
    """
    loan1 = loans[-1]
    loan1.process_age()
    loan1.save()

    loan2 = loans[-1]
    loan2.process_age()
    loan2.age =
    loan2.save()

    assert loan1.status == 'processing'
    assert loan1.state == 'processing_age'
    assert loan1.result is None


@pytest.mark.django_db
def test_loan_should_not_process_score(loans: Tuple) -> None:  # noqa: WPS218
    """Test if loan model should not process age.

    :param loans: a fixture that contains a immutable list of loans.
    """
    loan1 = loans[-1]
    loan1.state = 'processing_score'
    loan1.score = 600
    loan1.process_score()
    loan1.save()

    loan2 = loans[1]
    loan2.state = 'processing_score'
    loan2.process_score()
    loan2.save()

    assert loan1.status == 'processing'
    assert loan1.state == 'processing_score'
    assert loan1.result is None

    assert loan2.status == 'processing'
    assert loan2.state == 'processing_score'
    assert loan2.result is None
