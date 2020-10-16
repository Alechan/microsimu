from rest_framework import serializers

from api.models import Simulation


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = '__all__'
