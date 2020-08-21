"""conftest.py.
"""
from decimal import Decimal
from typing import Any, Tuple, Generator

import pytest
from django.core.management import call_command
from mixer.backend.django import mixer

from api.helpers import convert_str_date_to_object


def get_some_loans() -> Tuple[Any, ...]:
    """Function that returns a immutable list with some loans.

    :return: A immutable list containing loans
    """
    model_path = 'api.loan'
    return (
        mixer.blend(
            model_path,
            name='Fulano de Tal',
            cpf='26443567099',
            birthdate=convert_str_date_to_object(date='2012-01-01'),
            income=Decimal('1000.00'),  # noqa: WPS432, WPS339, WPS204
            amount=Decimal('1000.00'),  # noqa: WPS432, WPS339
            terms=12,  # noqa: WPS432
        ),
        mixer.blend(
            model_path,
            name='Ciclano de Tal',
            cpf='75518295049',
            birthdate=convert_str_date_to_object(date='1970-01-01'),
            income=Decimal('200.00'),  # noqa: WPS432, WPS339
            amount=Decimal('1000.00'),  # noqa: WPS432, WPS339
            terms=6,
        ),
        mixer.blend(
            model_path,
            name='Beltrano de Tal',
            cpf='47266124093',
            birthdate=convert_str_date_to_object(date='1990-01-01'),
            income=Decimal('1000.00'),  # noqa: WPS432, WPS339
            amount=Decimal('4000.00'),  # noqa: WPS432, WPS339
            terms=6,
        ),
        mixer.blend(
            model_path,
            name='Outrano de Tal',
            cpf='88691901020',
            birthdate=convert_str_date_to_object(date='1980-01-01'),
            income=Decimal('1000.00'),  # noqa: WPS432, WPS339
            amount=Decimal('1000.00'),  # noqa: WPS432, WPS339
            terms=12,  # noqa: WPS432
        ),
    )


@pytest.fixture()
def loans() -> Tuple[Any, ...]:
    """Fixture that contains loans.

    :return: A immutable list containing loans
    """
    return get_some_loans()


@pytest.fixture()
def policies() -> Tuple[Any, ...]:
    """Fixture that contains policies.

    :return: A immutable list containing policies
    """
    loan = get_some_loans()[-1]
    model_path = 'api.policy'
    return (
        mixer.blend(
            model_path,
            loan=loan,
            name='age',
            response='{ "status": "Ok from internal api age"}',
        ),
        mixer.blend(
            model_path,
            loan=loan,
            name='score',
            response='{ "status": "Ok from external api score"}',
        ),
        mixer.blend(
            model_path,
            loan=loan,
            name='commitment',
            response='{ "status": "Ok from external api commitment"}',
        ),
    )


@pytest.fixture()
def interests() -> Generator:
    """Fixture that calls command for loaddata.

    :yields: A generator with string
    """
    call_command('loaddata', 'interest.json')
    yield 'interests'
