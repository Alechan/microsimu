from rest_framework.response import Response

from api.models import Simulation


def simulations(request):
    """
    GET: return all the simulations stored in the DB
    :param request:
    :return:
    """
    simulations = Simulation.objects.all()
    serializer = SimulationSerializer(simulations, many=True)
    return Response(serializer.data)
