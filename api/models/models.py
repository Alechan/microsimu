from django.db import models

from api.std_lib.lawm.variables import Population, PopulationGrowth
from api.models.fields import VariableFloatField


class LAWMSimulation(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class LAWMResult(models.Model):
    simulation = models.ForeignKey(LAWMSimulation, related_name="results", null=False, on_delete=models.CASCADE)
    pop        = VariableFloatField(model_variable=Population, null=False)
    popr       = VariableFloatField(model_variable=PopulationGrowth, null=False)


