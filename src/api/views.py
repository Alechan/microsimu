from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework import mixins, status, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api import settings_api
from api.endpoint_metadata import DescriptiveFieldsMetadater
from api.migrations.helper.db_models_from_dfs import load_lawm_run_to_db
from api.models.models import LAWMSimulation, LAWMRunParameters
from api.serializers.parameters_serializers import RunParametersSerializer
from api.serializers.results_serializers import RegionResultSerializer
from api.serializers.simulation_serializers import SimulationListSerializer, SimulationDetailSerializer
from api.std_lib.lawm.regions import Africa
from api.std_lib.lawm.simulator.exceptions import ValidInputButSimulationError
from api.std_lib.lawm.simulator.fortran.lawm_fortran_simulator import LAWMFortranSimulator


class ApiRoot(APIView):
    """
    ## MicroSimu: A microservice that runs simulations
    MicroSimu is an open-source microservice that runs simulations of predefined models with user specified parameters.
    This is the [BrowsableAPI][BrowsableAPI] view, that can be used as a documentation of the endpoints but it does
    not intend to be a full fledged replacement of them. It can be used to *play* with reading simulation results and
    running new simulations, as the functionality is equivalent to sending requests directly to the microservice,
    but the user experience may seem lacking. Alongside the BrowsableAPI, MicroSimu also provides [OpenAPI][OpenAPI]
    specifications by [Swagger][microsimu-swagger] and [ReDoc][microsimu-redoc].

    MicroSimu's main purpose is to offer a way of easily running simulations remotely, when using this demo,
    and to simplify the local installation, when wanting more control. It makes a clear distinction between the
    "simulation run", its purpose, and the "simulation results visualization", not its purpose. Nevertheless,
    basic lines plots and tables can be automatically generated for each simulation result but the user is
    encouraged to create their own if these do not satisfy their needs (there are plans to expand the visualization
    capabilities in the future).

    In this first version, the only model available is the Latin-American World
    Model (Modelo Mundial Latinoamericano, MML), in its fortran version in pre-compiled form.
     A python translation of this model is in the works, as is the addition of other open-source
      models such as World3.

    This demo is *read-only* for non authorized users, meaning that retrieving past results and
    using the default visualizations is available to everyone but only registered users can
    run simulations. It is planned to allow up to 5 simulation runs to people from the public in the
    future, but for now your only choice is to run MicroSimu locally (which is really easy using
    the python or docker alternatives) or pestering me in [LinkedIn][LinkedIn] for a user.

    For more details on setup, usage and the models available visit the [github page][github].

    ### Examples: Modern Browser (Firefox, Chrome)
    Open these links in the browser and play with the resulting pages

    - List all simulations: <{simulations_url}>
    - Simulation 1 details: <{simu_1_url}>
    - Simulation 1 Region Africa details: <{simu_1_africa_url}>
    - Simulation 1 Region Africa example visualization: <{simu_1_africa_visualize_url}>
    - Simulate: <{simulate_url}>

    ### Examples: Command line
    The following examples use the python package *httpie* (`pip install httpie`) but it should be pretty
    straightforward to adapt these commands to others such as `CURL`.

        # List all the simulations
        http GET {simulations_url}

        # Get the details for simulation 1
        http GET {simu_1_url}

        # Get the details for the African region results of simulation 1
        http GET {simu_1_africa_url}

        # Get the parameters specifications to run a simulation (needs user and pass)
        http OPTIONS -a $USER:$PASS {simulate_url}

        # Get the default parameters to run a simulation
        http GET {simulate_url} > params.json

        # Trigger a simulation with parameters defined in params.json (needs user and pass)
        cat params.json | http POST -a $USER:$PASS {simulate_url}

    ### BrowsableAPI information about this endpoint
    Below, BrowsableAPI has automatically provided an example of a GET
    request to this endpoint, including the request's relative url, the response
    headers and the response JSON content. The links are clickable, meaning that you can
    *follow* the same path as when using it as a microservice, and this information can be automatically
     generated for for each endpoint.


    [github]: http://github.com/Alechan/microsimu
    [BrowsableAPI]: https://www.django-rest-framework.org/topics/browsable-api/
    [OpenAPI]: http://spec.openapis.org/oas/v3.0.3
    [microsimu-swagger]: {microsimu_swagger_url}
    [microsimu-redoc]: {microsimu_redoc_url}
    [LinkedIn]: https://www.linkedin.com/in/alejandro-dan%C3%B3s-058a57104/
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
            simulations_url            =self.request.build_absolute_uri(reverse("api:simulations")),
            simu_1_url                 =self.request.build_absolute_uri(reverse("api:simulation-detail", args=[1])),
            simu_1_africa_url          =self.request.build_absolute_uri(reverse("api:regionresult-detail", args=[1, Africa.name])),
            simu_1_africa_visualize_url=self.request.build_absolute_uri(reverse("api:visualize", args=[1, Africa.name])),
            simulate_url               =self.request.build_absolute_uri(reverse("api:simulate")),
            microsimu_swagger_url      =self.request.build_absolute_uri(reverse("schema-swagger-ui")),
            microsimu_redoc_url        =self.request.build_absolute_uri(reverse("schema-redoc")),
        )
        return description


class SimulateViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    Requests:

    - GET: example of valid data to send in POST request. Uses default values.

    - OPTIONS: descriptions of the parameters (name, minimum, maximum, category, ...). Requires user
    authentication.

    - POST: triggers a simulation with the provided data. Requires user authentication.

    If the user is logged in when using the BrowsableAPI, a form to post fre-form data
    with the same values as returned by a GET request can be found on the bottom.
    """
    metadata_class = DescriptiveFieldsMetadater
    queryset = LAWMRunParameters.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RunParametersSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simulator = LAWMFortranSimulator(settings_api.LAWM_RUNS_FOLDER_PATH)

    def create(self, request, *args, **kwargs):
        # The default method returns a response with the input data.
        # We want to redirect to the simulation detail of the new simulation.
        try:
            _ = super().create(request, *args, **kwargs)
            simu_id = self.new_simulation.id
            return HttpResponseRedirect(reverse('api:simulation-detail', args=(simu_id,)))
        except ValidInputButSimulationError:
            return Response(
                {"error": "The inputs were valid but the simulation still raised an error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Get an example of the data to send to the POST request. Includes default values.
        """
        default_params = RunParametersSerializer.get_default_serialized_data()
        return Response(default_params)

    def perform_create(self, serializer):
        """
        Once the serializer has validated the data and is ready to de-serializer and save to
        database, it will call this method to do it.
        """
        data = serializer.validated_data
        dfs_per_region = self.simulator.simulate(data)
        simu = load_lawm_run_to_db(dfs_per_region)
        serializer.save(simulation=simu)
        # We have no other way of "passing" the new simulation to the "create" response
        self.new_simulation = simu


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
    renderer_classes = APIView.renderer_classes

    @staticmethod
    def get(request, pk):
        simu = LAWMSimulation.objects.get(pk=pk)
        serializer = SimulationDetailSerializer(simu, context={"request": request})
        return Response(serializer.data)


class RegionResultDetail(APIView):
    """
    Get a region's (Developed Countries, Latin-America, Africa, Asia) results for
    a simulation.

    Append "/visualize" to this endpoint to get an HTML
    file with visualization examples using the data show
    below. 
    """
    renderer_classes = APIView.renderer_classes

    def get_view_name(self):
        return "Region Result"

    @staticmethod
    def get(request, simu_pk, region_name):
        simu = LAWMSimulation.objects.get(pk=simu_pk)
        region_result = get_object_or_404(simu.region_results, region__name=region_name)
        serializer = RegionResultSerializer(region_result, context={"request": request})
        return Response(serializer.data)


class VisualizeView(View):
    template_name = 'api/visualize.html'

    def get(self, request, simu_pk, region_name):
        relative_url = reverse('api:regionresult-detail', args=(simu_pk, region_name))
        endpoint_url = request.build_absolute_uri(relative_url)
        return render(request, self.template_name, {"endpoint_url" : endpoint_url})
