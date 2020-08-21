"""Business logic should included here.

logic.py
"""
from decimal import Decimal
from typing import List

from django.core.exceptions import ValidationError
from django.db.models import Count  # noqa: WPS347

from api.enums import LoanPolicies
from api.models import (
    Interest as InterestModel,
    Loan as LoanModel,
    Policy as PolicyModel,
    Proposal as ProposalModel,
)
from api.validators import validate_age


def get_interest_rate(score: int, terms: int) -> Decimal:
    """Get rate by score and amount of terms.

    :param score: score represented by a integer
    :param terms: a integer that represents amount of terms
    :raises ValueError: raise when not found interest
    :return: A decimal number with interest rate.
    """
    interests = InterestModel.objects.filter(
        min_score__lte=score,
        max_score__gte=score,
    ).filter(terms=terms).order_by('percentage')

    if not interests:
        raise ValueError('Interest rate not found!')

    interest = interests[0]

    return interest.percentage


def calculate_installment(amount: Decimal, terms: int, interest: Decimal) -> Decimal:
    """Get installment calculation by amount, terms and interest.

    :param amount: loan amount value
    :param terms: loan terms value
    :param interest: interest rate percentage
    :return: A decimal value that represents installment
    """
    decimal_terms = Decimal(terms)
    installment = (amount / decimal_terms) + ((amount / decimal_terms) * interest)

    return round(installment, 2)


def get_all_terms() -> List:
    """Get all possible terms.

    :raises ValueError: exception called when not found interest on database.
    :return: List of terms ids
    """
    interests = InterestModel.objects.values('terms').annotate(qty_terms=Count('terms'))
    if not interests:
        raise ValueError('Have no interest/terms registered!')

    terms: List = []
    for interest in interests:
        terms.append(interest.get('terms'))

    return terms


def get_proposal_terms(loan: LoanModel, commitment: Decimal) -> int:
    """Retrieves new terms value if installment exceeds the commitment.

    :param loan: a loan model object.
    :param commitment: percentage of commitment
    :raises ValueError: exception for no terms found for commitment rate
    :return: a integer that represents proposal term.
    """
    limit_installment = loan.income - (loan.income * commitment)
    all_terms = [terms for terms in get_all_terms() if terms >= loan.terms]
    for terms in all_terms:
        interest = get_interest_rate(score=loan.score, terms=terms)
        installment = calculate_installment(
            amount=loan.amount,
            terms=terms,
            interest=interest,
        )
        if installment <= limit_installment:
            return terms

    raise ValueError('No terms found for commitment rate!')


def start_age_policy(loan_id: str) -> None:
    """Starts the age check policy.

    :param loan_id: id of loan
    """
    loan = LoanModel.objects.get(pk=loan_id)
    policy = PolicyModel()
    policy.name = LoanPolicies.age.value
    policy.body = '{}'  # noqa: P103
    policy.loan = loan
    policy.save()
    try:
        validate_age(loan.birthdate)
    except ValidationError:
        loan.refuse_policy = LoanPolicies.age.value
        loan.refuse()
        loan.save()
        return

    loan.process_age()
    loan.save()


def start_score_policy(loan_id: str) -> None:
    """Starts the age policy check.

    :param loan_id: id of loan
    """
    loan = LoanModel.objects.get(pk=loan_id)
    policy = PolicyModel()
    policy.name = LoanPolicies.score.value
    try:
        # call service and validator here
        loan.score = 600
    except (ValidationError):
        policy.body = '{}'
        policy.save()

    loan.process_score()
    loan.save()


def start_commitment_policy(loan_id: str) -> None:
    """Starts commitment check policy.

    :param loan_id: id of loan
    """
    loan = LoanModel.objects.get(pk=loan_id)
    policy = PolicyModel()
    policy.name = LoanPolicies.commitment.value
    try:
        # call service and validator here
        commitment = Decimal('0.8')
        loan.commitment = commitment
        terms = get_proposal_terms(loan=loan, commitment=commitment)
    except ValidationError:
        policy.body = '{}'
        policy.save()
        loan.refused_policy = LoanPolicies.commitment.value
        loan.refuse()
        loan.save()
        return

    loan.approve()
    loan.save()

    proposal = ProposalModel()
    proposal.loan = loan
    proposal.amount = loan.amount
    proposal.terms = terms
    proposal.save()
