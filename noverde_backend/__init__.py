"""Noverde Backend init file.

__init__.py
"""

from noverde_backend.celery import app as celery_app

__all__ = ('celery_app',)
