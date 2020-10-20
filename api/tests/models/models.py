from dataclasses import dataclass
from typing import Any

from django.db import models

from api.std_lib.lawm import variables
from api.models.fields import VariableFloatField


@dataclass
class CustomVariable(variables.ModelVariable):
    value       : Any
    name        : str = "The name"
    fortran_name: str = "The fortran name"
    unit        : str = "The unit"
    description : str = "The description"
    category    : str = "The category"


class DjangoModelWithCustomFields(models.Model):
    float_var = VariableFloatField(model_variable=CustomVariable)


