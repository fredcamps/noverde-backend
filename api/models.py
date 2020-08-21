"""Api models.

models.py
"""
import uuid
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.enums import LoanPolicies, LoanResult, LoanStatus
from api.state_machine import LOAN_STATES, LoanStateMachine
from api.validators import validate_amount, validate_cpf


class Interest(models.Model):
    """Interest rate model.
    """

    min_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    max_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    terms = models.IntegerField(validators=[MinValueValidator(1)])
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0'))],
    )


class Loan(models.Model, LoanStateMachine):
    """Model that represents loan entity.
    """

    id = models.UUIDField(  # noqa: VNE003, WPS125
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=200)  # noqa: WPS432
    cpf = models.CharField(max_length=11, validators=[validate_cpf])  # noqa: WPS432
    birthdate = models.DateField()
    amount = models.DecimalField(validators=[validate_amount], max_digits=6, decimal_places=2)
    score = models.IntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    terms = models.IntegerField(validators=[MinValueValidator(1)])
    income = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(1))],
    )
    refused_policy = models.CharField(
        max_length=30,  # noqa: WPS432
        default=None,
        null=True,
        choices=LoanPolicies.choices(),
    )
    result = models.CharField(    # noqa: WPS110
        max_length=30,  # noqa: WPS432
        default=None,
        null=True,
        choices=LoanResult.choices(),
    )
    state = models.CharField(
        max_length=30,  # noqa: WPS432
        default=LOAN_STATES[0],
        choices=[(loan_state, loan_state) for loan_state in LOAN_STATES],
    )
    status = models.CharField(
        max_length=30,  # noqa: WPS432
        choices=LoanStatus.choices(),
        default=LoanStatus.processing.value,
    )


class Policy(models.Model):
    """Model that represents loan policies.
    """

    name = models.CharField(
        max_length=30,  # noqa: WPS432
        choices=LoanPolicies.choices(),
    )
    failed = models.BooleanField(default=False)
    response = models.TextField()
    loan = models.ForeignKey(
        Loan,
        on_delete=models.RESTRICT,
        related_name='policies',
    )


class Proposal(models.Model):
    """Model that represent approved proposal.
    """

    loan = models.OneToOneField(
        Loan,
        on_delete=models.RESTRICT,
        related_name='proposal',
        primary_key=True,
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_amount])
    terms = models.IntegerField(validators=[MinValueValidator(1)])
