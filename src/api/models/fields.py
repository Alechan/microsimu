from django.db import models


class CastOnAssignDescriptor(object):
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.
    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class CustomLAWMFieldMixin:
    # Should be set by subclasses
    model_component       = None
    model_component_kwarg = None
    primitive_type        = None

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.model_component(value)

    def to_python(self, value):
        if isinstance(value, self.model_component):
            return value

        if value is None:
            return value

        return self.model_component(value)

    def get_prep_value(self, value):
        try:
            # Try to get the value if it's a ModelVariable
            return value.value
        except AttributeError:
            if isinstance(value, self.primitive_type):
                return value
            else:
                # This code should be unreachable as the "contribute_to_class" method
                #   should force the call to method "to_python" every time the field is
                #   created or modified
                raise AttributeError(f"This field expects a float or an instance of {self.model_component} but it "
                                     f"received {value}.")

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs[self.model_component_kwarg] = self.model_component
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Fix to call "to_python" on _every_ assignment to the field. For example,
        when calling "MyModel.objects.create(custom_field=323.32)" so the instance
        return has the "custom_field" attribute returned by "to_python" method instead of
        "323.32".
        """
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, CastOnAssignDescriptor(self))


class VariableFloatField(CustomLAWMFieldMixin, models.FloatField):
    """
    A float field that is linked to a specific variable from a model.
    """
    def __init__(self, model_variable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_component_kwarg = "model_variable"
        self.model_component       = model_variable
        self.primitive_type        = float


class BaseParameterField(CustomLAWMFieldMixin, models.IntegerField):
    """
    The base field for which al parameter fields will subclassify
    """
    def __init__(self, model_parameter, *args, **kwargs):
        kwargs["default"] = model_parameter.default
        super().__init__(*args, **kwargs)
        self.model_component       = model_parameter
        self.model_component_kwarg = "model_parameter"


class ParameterIntegerField(BaseParameterField):
    """
    An integer field that is linked to a specific parameter from a model.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.primitive_type        = int


class ParameterFloatField(BaseParameterField):
    """
    An integer field that is linked to a specific parameter from a model.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.primitive_type        = float
