"""App tasks for processing in celery.
"""
import logging

from celery import chain

from api import consts, logic
from noverde_backend.celery import app

logger = logging.getLogger(__name__)


def send_to_credit_analysis(loan_id: str) -> None:
    """Send parameters to credit analysis tasks.

    :param loan_id: uuid of loan
    """
    chain(age_policy.si(loan_id), score_policy.si(loan_id), commitment_policy.si(loan_id))()


@app.task(queue='age_policy', name='age_policy', bind=True, max_retries=consts.MAX_RETRIES)
def age_policy(self, loan_id: str) -> None:
    """Task that starts age_policy.

    :param self: task
    :param loan_id: uuid of loan
    """
    try:
        logic.start_age_policy(loan_id)
    except logic.APIException as exception:
        logger.exception(exception)


@app.task(queue='score_policy', name='score_policy', bind=True, max_retries=consts.MAX_RETRIES)
def score_policy(self, loan_id: str) -> None:
    """Task that starts score_policy.

    :param self: task
    :param loan_id: uuid of loan
    """
    try:
        logic.start_score_policy(loan_id)
    except logic.APIException as exception:
        logger.exception(exception)


@app.task(
    queue='commitment_policy',
    name='commitment_policy',
    bind=True,
    max_retries=consts.MAX_RETRIES,
)
def commitment_policy(self, loan_id: str) -> None:
    """Task that starts commitment_policy.

    :param self: task
    :param loan_id: uuid of loan
    """
    try:
        logic.start_commitment_policy(loan_id)
    except logic.APIException as exception:
        logger.exception(exception)
