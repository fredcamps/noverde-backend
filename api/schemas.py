"""Schemas file.

schemas.py
"""
from decimal import Decimal
from typing import List

from schema import And, Or, Schema

from api.validators import (
    validate_amount,
    validate_birthdate,
    validate_cpf,
    validate_terms,
)

PostLoanRequest = Schema(
    {
        'name': And(str, len),
        'cpf': And(str, validate_cpf),
        'birthdate': And(str, validate_birthdate),
        'amount': And(Decimal, validate_amount),
        'terms': And(int, validate_terms),
        'income': And(Decimal, lambda inc: inc >= 1),
    },
)

PostLoanSucessResponse = Schema(
    {
        'id': str,
    },
)

PostLoanErrorResponse = Schema(
    {
        'errors': List,
    },
)

GetLoanResponse = Schema(
    {
        'id': str,
        'status': str,
        'result': Or(str, None),
        'refused_policy': Or(str, None),
        'amount': Or(Decimal, None),
        'terms': Or(int, None),
    },
)

PostScoreRequest = Schema(
    {
        'cpf': And(str, validate_cpf),
    },
)

PostCommitmentRequest = Schema(
    {
        'cpf': And(str, validate_cpf),
    },
)

DefaultResponse = Schema(
    {
        'message': str,
    },
)
