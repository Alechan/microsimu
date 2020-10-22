from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer


@api_view(('GET',))
@renderer_classes([JSONRenderer])
def simulations(request):
    """
    GET: return all the simulations stored in the DB
    :param request:
    :return:
    """
    simus = LAWMSimulation.objects.all()
    serializer = SimulationListSerializer(simus, many=True)
    return Response(serializer.data)
