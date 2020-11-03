from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api.models.models import LAWMSimulation
from api.serializers import SimulationListSerializer, SimulationDetailSerializer, RegionResultSerializer


class ApiRoot(APIView):
    """
    ## MicroSimu: A microservice that runs simulations
    ### TL;DR: Modern Browser (Firefox, Chrome)
    <{simulations_url}>

    <{simu_1_url}>

    <{simu_1_africa_url}>

    ### TL;DR: Command line
        # Using http (pip install httpie)
        http {simulations_url}

        http {simu_1_url}

        http {simu_1_africa_url}

    ### Description

    For more details on setup and how to use it, visit the [github page][github].

    [github]: http://github.com/Alechan/microsimu
    """
    @staticmethod
    def get(request, format=None):
        return Response({
            'simulations' : reverse('api:simulations', request=request, format=format),
            'simulate'    : reverse('api:simulate', request=request, format=format),
        })

    def get_view_name(self):
        return "API"

    @property
    def description(self):
        """
        Replace the variables in the description with the correct url. This way, the url of
        where the microservice is being accessed from doesn't need to be hardcoded and instead
        depends on the request.

        :return: A SafeString (probably) with the description in HTML
        """
        base_description = self.__class__.__doc__
        description = base_description.format(
            simulations_url  =self.request.build_absolute_uri(reverse("api:simulations")),
            simu_1_url       =self.request.build_absolute_uri(reverse("api:simulation-detail", args=[1])),
            simu_1_africa_url=self.request.build_absolute_uri(reverse("api:regionresult-detail", args=[1, "africa"])),
        )
        return description


class Simulate(APIView):
    @staticmethod
    def post(request):
        simu = LAWMSimulation.objects.create()
        return redirect('api:simulation-detail', pk=simu.id)

    @staticmethod
    def get(request):
        return Response({})


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
    Get a region's (Developed Countries, Latin-America, Africa, Asia) results for
    a simulation.
    """
    renderer_classes = APIView.renderer_classes + [TemplateHTMLRenderer]

    def get_view_name(self):
        return "Region Result"

    @staticmethod
    def get(request, simu_pk, region_name):
        simu = LAWMSimulation.objects.get(pk=simu_pk)
        region_result = get_object_or_404(simu.region_results, region__name=region_name)
        serializer = RegionResultSerializer(region_result, context={"request": request})
        return Response(serializer.data)
