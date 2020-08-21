"""Api views
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from api.tasks import send_to_credit_analysis


def Loan(APIView):
    """Loan View."""

    def get(self, request):
        pass


    def post(self, request):
        pass
