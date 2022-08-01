from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.utils import NATIONALITIES


@api_view(['GET'])
def read_nationalities(request):
    return Response(NATIONALITIES)