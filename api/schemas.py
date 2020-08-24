"""Schemas file.

schemas.py
"""
from decimal import Decimal

from schema import And, Schema, Use

from api.validators import (
    validate_amount,
    validate_birthdate,
    validate_cpf,
)

PostLoanRequest = Schema(
    {
        'name': And(str, len),
        'cpf': And(str, validate_cpf),
        'birthdate': And(str, validate_birthdate),
        'amount': And(Use(Decimal), validate_amount),
        'terms': And(Use(int), lambda ter: ter >= 1),
        'income': And(Use(Decimal), lambda inc: inc >= 1),
    },
)
