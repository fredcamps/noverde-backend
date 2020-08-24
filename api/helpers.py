"""Some helpers.

helpers.py
"""
from datetime import datetime

from api.consts import VALID_DATE_FORMAT


def convert_str_date_to_object(date: str) -> datetime:
    """Convert date str to datetime object.

    :param date: a str contains 'Y-m-d' date
    :return: datetime object
    """
    return datetime.strptime(date, VALID_DATE_FORMAT)


def calculate_age_by_date(birthdate: datetime) -> int:
    """Calculate age by birthdate.

    :param birthdate: A datetime object containing birth date.
    :return: return calculated age
    """
    today = datetime.today()
    diff = ((today.month, today.day) < (birthdate.month, birthdate.day))
    return today.year - birthdate.year - diff
