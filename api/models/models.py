from django.db import models

from api.std_lib.lawm.variables import Population, PopulationGrowth
from api.models.fields import VariableFloatField


class LAWMSimulation(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def get_variables_information(self):
        any_result = self.results.first()
        return any_result.get_variables_information()


class LAWMResult(models.Model):
    simulation = models.ForeignKey(LAWMSimulation, related_name="results", null=False, on_delete=models.CASCADE)
    pop        = VariableFloatField(model_variable=Population, null=False)
    popr       = VariableFloatField(model_variable=PopulationGrowth, null=False)

    def get_variables_information(self):
        fields_names    = [x.name for x in self._meta.get_fields() if isinstance(x, VariableFloatField)]
        extra_info_dict = {field : getattr(self, field).info_as_dict() for field in fields_names}
        return extra_info_dict


