"""
State machines transitions.

state_machine.py
"""
from typing import Tuple

from transitions import Machine

from api.enums import LoanPolicies, LoanResult, LoanStatus

PROCESSING_AGE_STATE = 'processing_age'
PROCESSING_SCORE_STATE = 'processing_score'
PROCESSING_COMMITMENT_STATE = 'processing_commitment'
APPROVED_STATE = 'approved'
REFUSED_STATE = 'refused'
LOAN_STATES = (
    PROCESSING_AGE_STATE,
    PROCESSING_SCORE_STATE,
    PROCESSING_COMMITMENT_STATE,
    APPROVED_STATE,
    REFUSED_STATE,
)
LOAN_PROCESSING_STATES = (
    PROCESSING_AGE_STATE,
    PROCESSING_SCORE_STATE,
    PROCESSING_COMMITMENT_STATE,
)


class LoanStateMachine(Machine):
    """State Machine transitions from Loan Entity.
    """

    states: Tuple = LOAN_STATES

    def __init__(self) -> None:
        """Loan state machine constructor.
        """
        super().__init__(model=self, states=self.states, initial=self.states[0])
        self.add_transition(
            trigger='refuse',
            source=LOAN_PROCESSING_STATES,
            dest='refused',
            after='after_refuse',
            conditions=['should_refuse'],
        )
        self.add_transition(
            trigger='process_age',
            source=PROCESSING_AGE_STATE,
            dest=PROCESSING_SCORE_STATE,
            conditions=['should_processing', 'should_process_age'],
        )
        self.add_transition(
            trigger='process_score',
            source=PROCESSING_SCORE_STATE,
            dest=PROCESSING_COMMITMENT_STATE,
            conditions=['should_processing', 'should_process_score'],
        )
        self.add_transition(
            trigger='approve',
            source=PROCESSING_COMMITMENT_STATE,
            dest='approved',
            conditions=['should_processing', 'should_approve'],
            after='after_approve',
        )

    def should_refuse(self) -> bool:
        """Condition that checks if refuse transition should triggered.

        :return: boolean value that satifies the condition
        """
        return bool(self.refused_policy)

    def after_refuse(self) -> None:
        """Event that happens after refuse trigger."""
        self.result = LoanResult.refused.value
        self.status = LoanStatus.completed.value
        self.save()

    def should_processing(self) -> bool:
        """Condition that checks if still able to processing triggers.

        :return: boolean value that satifies the condition
        """
        return not bool(self.refused_policy)

    def should_process_age(self) -> bool:
        """Condition that checks if process_age transition should triggered.

        :return: boolean value that satifies the condition
        """
        for policy in self.policies.all():
            if policy.name == LoanPolicies.age.value and not policy.failed:
                return True

        return False

    def should_process_score(self) -> bool:
        """Condition that checks if process_score transition should triggered.

        :return: boolean value that satifies the condition
        """
        if self.score is None:
            return False

        for policy in self.policies.all():
            if policy.name == LoanPolicies.score.value and not policy.failed:
                return True

        return False

    def should_approve(self) -> bool:
        """Condition that checks if approve transition should triggered.

        :return: boolean value that satifies the condition
        """
        if self.commitment is None:
            return False

        for policy in self.policies.all():
            if policy.name == LoanPolicies.commitment.value and not policy.failed:
                return True

        return False

    def after_approve(self) -> None:
        """Event that happens after approve trigger."""
        self.result = LoanResult.approved.value
        self.status = LoanStatus.completed.value
        self.save()
