from django.test import TestCase

from api.serializers.parameters_serializers import RunParametersSerializer


class BaseFortranTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.expected_cfg_content = cls.get_std_run_cfg_content()
        cls.validated_data = cls.get_POST_parameters_example()

    @staticmethod
    def get_POST_parameters_example():
        """
        Return an example of the validated data of a valid POST request to "simulate
        a model" endpoint
        """
        serialized_data = RunParametersSerializer.get_default_serialized_data()
        serializer = RunParametersSerializer(data=serialized_data)
        serializer.is_valid()
        deserialized_data = serializer.validated_data
        return deserialized_data

    @staticmethod
    def get_std_run_cfg_content():
        return \
"""CALMX
3200.0 3000.0 3000.0 3000.0
COSMAX
10.0 7.0 7.0 7.0
FCOST
769230.8
GAMMA
1.01 1.01 1.005 1.01 1.015
1.01 1.01 1.005 1.01 1.015
1.01 1.01 1.005 1.01 1.015
1.01 1.01 1.005 1.01 1.015
IAID
F
IPRIN
0
KPROJ
1980
KSTOP
2000
KTECST
3000.0 3000.0 3000.0 3000.0
KTRADE
2000
NHCGAP
40 40 40 40
NHIST
0
NQH34
10 10 20 20
NRESER
365.0 365.0 365.0 365.0
NSPGAP
40 40 40 40
SPAMAX
30.0 30.0 30.0 30.0
SPXPER
30.0 10.0 7.0 7.0
TRAID
0.02
UPTOIN
0.25 0.25 0.25 0.25
WTH
6.0 8.0 6.0 6.0 6.0
6.0 4.0 4.0 6.0 6.0
6.0 2.0 4.0 4.0 7.0
4.0 4.0 4.0 8.0 6.0
4.0 6.0 8.0 6.0 2.0
1.0 -1 -1 -1 -1
"""
