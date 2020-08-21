"""Api views.
"""
from rest_framework.views import APIView
# from rest_framework.response import Response
# from api.tasks import send_to_credit_analysis


class LoanRequireView(APIView):
    """Loan View.
    """

    def post(self, request):
        import pdb; pdb.set_trace()
        pass

class LoanDetailView(APIView):
    """Loan Detail View.
    """

    def get(self, request):
        pass
