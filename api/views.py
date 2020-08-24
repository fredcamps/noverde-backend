"""Api views.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from api.tasks import send_to_credit_analysis

from api import logic
from api.decorators import validate_request_data
from api.schemas import PostLoanRequest


class LoanRequireView(APIView):
    """Loan View.
    """

    @validate_request_data(schema=PostLoanRequest)
    def post(self, request: HttpRequest) -> Response:
        """Endpoint that creates loan.

        :param request: A request object
        :return: A response object
        """
        loan = logic.create_loan(dict(request.data.items()))
        send_to_credit_analysis(loan_id=str(loan.id))
        return Response(
            data={'id': loan.id},
            status=status.HTTP_201_CREATED,
        )


class LoanDetailView(APIView):
    """Loan Detail View.
    """

    def get(self, request: HttpRequest, id: str) -> Response:
        """Endpoint that gets loan details.

        :param request: A request object
        :param id: A string that contains loan id
        :return: A response object
        """
        try:
            loan = logic.get_loan(loan_id=id)
        except Exception:
            Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            data={
                'id': loan.id,
                'status': loan.status,
                'result': loan.result,
                'refused_policy': loan.refused_policy,
                'amount': None if not loan.proposal else loan.proposal.amount,  # noqa: WPS504
                'terms': None if not loan.proposal else loan.proposal.terms,   # noqa: WPS504
            },
            status=status.HTTP_200_OK,
        )
