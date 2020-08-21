"""
Objects that represents Enum types.

enums.py
"""
from enum import Enum
from typing import List


class BaseEnum(Enum):
    """Abstract base class for enum.
    """

    @classmethod
    def choices(cls) -> List:
        """Enum choices.

        :return: a list containing tuple of key and value
        """
        return [(key.value, key.name) for key in cls]


class LoanStatus(BaseEnum):
    """Enum of loan status.
    """

    processing = 'processing'
    completed = 'completed'


class LoanPolicies(BaseEnum):
    """Enum of loan policies.
    """

    age = 'age'
    score = 'score'
    commitment = 'commitment'


class LoanResult(BaseEnum):
    """Enum of loan result.
    """

    approved = 'approved'
    refused = 'refused'


# class LoanTerms(BaseEnum):
#     """Enum of loan terms.
#     """

#     six = 6
#     nine = 9
#     twelve = 12
