"""Urls from api app.
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r'loan', views.Loan)
