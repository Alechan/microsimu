from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MaxValueParameterValidator(BaseValidator):
    message = _('Ensure this value is less than or equal to %(limit_value)s.'
                ' Send an OPTIONS request for more information.')
    code = 'max_value'

    def compare(self, model_parameter, b):
        return model_parameter.value > b


@deconstructible
class MinValueParameterValidator(BaseValidator):
    message = _('Ensure this value is greater than or equal to %(limit_value)s.'
                ' Send an OPTIONS request for more information.')
    code = 'min_value'

    def compare(self, model_parameter, b):
        return model_parameter.value < b
