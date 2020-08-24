"""Urls from api app.
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import LoanDetailView, LoanRequireView

urlpatterns = [
    path('/loan', LoanRequireView.as_view()),
    path('/loan/<str:id>', LoanDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
