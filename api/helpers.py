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
