"""Business logic should included here.

logic.py
"""
import json
from decimal import Decimal
from typing import Dict, List
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import Count
from rest_framework.exceptions import APIException

from api.helpers import convert_str_date_to_object
from api.enums import LoanPolicies
from api.models import (
    Interest as InterestModel,
    Loan as LoanModel,
    Policy as PolicyModel,
    Proposal as ProposalModel,
)
from api.validators import validate_age, validate_score
from api.services import CommitmentService, ScoreService


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
    :raises ValidationError: exception for no terms found for commitment rate
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

    raise ValidationError('No terms found for commitment rate!')


def _generate_policy(loan: LoanModel, policy_name: str) -> PolicyModel:
    policy = PolicyModel()
    policy.name = policy_name
    policy.response = json.dumps({})  # noqa: P103
    policy.loan = loan
    policy.save()
    return policy


def _handle_api_exception(policy: PolicyModel, api_exception: APIException) -> None:
    policy.response = json.dumps({'error': str(api_exception)})
    policy.failed = True
    policy.save()


def _handle_validation_error(policy: PolicyModel, error: ValidationError) -> None:
    policy.response = json.dumps({'error': str(error)})
    policy.save()
    loan = policy.loan
    loan.refused_policy = policy.name
    loan.refuse()
    loan.save()


def start_age_policy(loan_id: str) -> LoanModel:
    """Starts the age check policy.

    :param loan_id: id of loan
    :return: A model object with loan registry
    """
    loan = LoanModel.objects.get(pk=UUID(loan_id))
    policy = _generate_policy(loan, LoanPolicies.age.value)
    try:
        validate_age(loan.birthdate)
    except ValidationError as error:
        _handle_validation_error(policy, error)
        return loan

    loan.process_age()
    loan.save()

    return loan


def get_loan(loan_id: UUID) -> LoanModel:
    """Get loan by id.

    :param loan_id: UUID object
    :return: A model object of loan
    """
    return LoanModel.objects.get(pk=loan_id)


def create_loan(loan_data: Dict) -> LoanModel:
    """Creates a new loan.

    :param loan_data: loan data
    :return: loan model
    """
    loan = LoanModel()
    loan.name = loan_data.get('name')
    loan.cpf = loan_data.get('cpf')
    loan.birthdate = convert_str_date_to_object(date=loan_data.get('birthdate'))
    loan.income = loan_data.get('income')
    loan.amount = loan_data.get('amount')
    loan.terms = loan_data.get('terms')
    loan.save()
    return loan


def start_score_policy(loan_id: str) -> None:
    """Starts the age policy check.

    :param loan_id: id of loan
    :raises APIException: raises when service get unexpected response
    :return: A model object with loan registry
    """
    loan = get_loan(UUID(loan_id))
    service = ScoreService()
    policy = _generate_policy(loan, LoanPolicies.score.value)
    try:
        response = service.request(request_data={'cpf': loan.cpf})
    except APIException as api_exception:
        _handle_api_exception(policy, api_exception)
        raise api_exception

    try:
        validate_score(response.get('score'))
    except ValidationError as error:
        _handle_validation_error(policy, error)
        return loan

    loan.score = response.get('score')
    loan.process_score()
    loan.save()

    return loan


def start_commitment_policy(loan_id: str) -> None:  # noqa: WPS210
    """Starts commitment check policy.

    :param loan_id: id of loan
    :raises APIException: raises when service get unexpected response
    :return: A model object with loan registry
    """
    loan = get_loan(UUID(loan_id))
    service = CommitmentService()
    policy = _generate_policy(loan, LoanPolicies.commitment.value)
    try:
        response = service.request(request_data={'cpf': loan.cpf})
    except APIException as api_exception:
        _handle_api_exception(policy, api_exception)
        raise api_exception

    try:
        terms = get_proposal_terms(loan=loan, commitment=response.get('commitment'))
    except (ValidationError, ValueError) as error:
        _handle_validation_error(policy, error)
        return loan

    loan.commitment = response.get('commitment')
    loan.approve()
    loan.save()

    proposal = ProposalModel()
    proposal.loan = loan
    proposal.amount = loan.amount
    proposal.terms = terms
    proposal.save()

    return loan
