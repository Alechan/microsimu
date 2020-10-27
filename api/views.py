from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer, SimulationDetailSerializer, RegionResultSerializer


@api_view(('GET',))
@renderer_classes([JSONRenderer])
def simulations_list(request):
    """
    GET: return all the simulations stored in the DB
    :param request:
    :return:
    """
    simus = LAWMSimulation.objects.all()
    serializer = SimulationListSerializer(simus, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(('GET',))
@renderer_classes([JSONRenderer])
def simulations_detail(request, pk):
    """
    GET: return the details of a specific simulation
    :param pk:
    :param request:
    :return:
    """
    simu = LAWMSimulation.objects.get(pk=pk)
    serializer = SimulationDetailSerializer(simu, context={"request": request})
    return Response(serializer.data)


@api_view(('GET',))
@renderer_classes([JSONRenderer])
def region_result_detail(request, simu_pk, region_name):
    """
    GET: return the details of the results for a region and a simulation
    :param region_name:
    :param simu_pk:
    :param request:
    :return:
    """
    simu = LAWMSimulation.objects.get(pk=simu_pk)
    region_result = get_object_or_404(simu.region_results, region__name=region_name)
    serializer = RegionResultSerializer(region_result, context={"request": request})
    return Response(serializer.data)
