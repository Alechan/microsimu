from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer, SimulationDetailSerializer, RegionResultSerializer


class SimulationList(APIView):
    """
    List all simulations or create a new simulation.
    """
    renderer_classes = APIView.renderer_classes

    @staticmethod
    def get(request):
        simus = LAWMSimulation.objects.all()
        serializer = SimulationListSerializer(simus, many=True, context={"request": request})
        return Response(serializer.data)


class SimulationDetail(APIView):
    """
    Get the details of a simulation
    """
    renderer_classes = APIView.renderer_classes + [TemplateHTMLRenderer]

    @staticmethod
    def get(request, pk):
        simu = LAWMSimulation.objects.get(pk=pk)
        serializer = SimulationDetailSerializer(simu, context={"request": request})
        return Response(serializer.data)


class RegionResultDetail(APIView):
    """
    Get the results of a simulation for a region
    """
    renderer_classes = APIView.renderer_classes + [TemplateHTMLRenderer]

    @staticmethod
    def get(request, simu_pk, region_name):
        simu = LAWMSimulation.objects.get(pk=simu_pk)
        region_result = get_object_or_404(simu.region_results, region__name=region_name)
        serializer = RegionResultSerializer(region_result, context={"request": request})
        return Response(serializer.data)
