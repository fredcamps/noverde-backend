"""Schemas file.

schemas.py
"""
from decimal import Decimal

from schema import Schema, And


PostLoanRequest = Schema(
    {
        'name': And(str, len),
        'cpf': str,
        'birthdate': str,
        'amount': Decimal,
        'terms': int,
        'income': Decimal,
    },
)


GetLoanRequest = Schema(
    {
        'id': str,
        'status': str,
        'result': str,
        'refused_policy': str,
        'amount': Decimal,
        'terms': int,
    },
)

PostAgeRequest = Schema(
    {
        'age': int,
    },
)


PostScoreRequest = Schema(
    {
        'cpf': str,
    },
)


PostCommitmentRequest = Schema(
    {
        'cpf': str,
    },
)
