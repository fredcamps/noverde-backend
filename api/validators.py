"""Validators.
"""
from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from validate_docbr import CPF

from api.consts import MAX_AMOUNT, MIN_AMOUNT, MIN_SCORE, MINIMUM_AGE
from api.helpers import convert_str_date_to_object


def validate_age(birthdate: datetime) -> bool:
    """Validate age according to birthdate.

    :param birthdate: a date object for age calculation.
    :raises ValidationError: exception excepted when age is not on minimum rule.
    :return: always return True
    """
    today = datetime.today()
    diff = ((today.month, today.day) < (birthdate.month, birthdate.day))
    age = today.year - birthdate.year - diff
    if age < MINIMUM_AGE:
        raise ValidationError('The age is lower than {0} years'.format(MINIMUM_AGE))

    return True


def validate_amount(amount: Decimal) -> bool:
    """Validate amount.

    :param amount: a decimal type number
    :raises ValidationError: exception expected when amount value is not valid.
    :return: always return True
    """
    if amount < Decimal(MIN_AMOUNT) or amount > Decimal(MAX_AMOUNT):
        raise ValidationError(
            'Invalid amount value, it shoulds from {0} to {1}'.format(MIN_AMOUNT, MAX_AMOUNT),
        )

    return True


def validate_birthdate(birthdate: str) -> bool:
    """Validate string contains birthdate.

    :param birthdate: a string contains birthdate
    :raises ValidationError: exception expected when birthdate is not valid
    :return: always return True
    """
    try:
        convert_str_date_to_object(date=birthdate)
    except ValueError:
        raise ValidationError('Invalid date format, it shoulds Y-m-d format.')

    return True


def validate_cpf(cpf_number: str) -> bool:
    """Validates cpf number.

    :param cpf_number: str containing cpf number
    :raises ValidationError: exception expected when cpf is not valid
    :return: always return True
    """
    cpf = CPF()
    if not cpf.validate(cpf_number):
        raise ValidationError('Invalid CPF')

    return True


def validate_score(score: int) -> bool:
    """Validates if score is greather or equal than minimum allowed.

    :param score: a integer number that represents score value.
    :raises ValidationError: exception expected when score number is less than minimum rule.
    :return: always return True
    """
    if score < MIN_SCORE:
        raise ValidationError('The score is lower than {0}'.format(MIN_SCORE))

    return True
