"""Urls from api app.
"""
from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('/loan/<str:loan_id>', views.Loan.as_view()),
]
