from django.urls import reverse
from rest_framework import serializers

from api.models.models import LAWMSimulation


class SimulationListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:simulation-detail")

    class Meta:
        model = LAWMSimulation
        fields = ["url", "created"]


class SimulationDetailSerializer(serializers.HyperlinkedModelSerializer):
    url        = serializers.HyperlinkedIdentityField(view_name="api:simulation-detail")
    regions    = serializers.SerializerMethodField('get_regions_urls')
    # parameters = RunParametersSerializer('get_regions_urls')

    def get_regions_urls(self, obj):
        request = self.context['request']
        regions_urls = {
            reg_res.region_name: self.get_url_from_region_result(reg_res, request)
            for reg_res in obj.region_results.all()
        }
        return regions_urls

    @staticmethod
    def get_url_from_region_result(reg_res, request):
        args = [reg_res.simulation_id, reg_res.region_name]
        relative_url = reverse("api:regionresult-detail", args=args)
        absolute_url = request.build_absolute_uri(relative_url)
        return absolute_url

    class Meta:
        model = LAWMSimulation
        fields = '__all__'
