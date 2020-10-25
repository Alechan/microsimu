from django import test

from api.models.models import LAWMSimulation, LAWMResult
from api.serializers import ResultSerializer
from api.tests.api_test_mixin import ApiTestMixin


class ResultSerializerTest(test.TestCase, ApiTestMixin):
    def setUp(self):
        self.simulation = LAWMSimulation.objects.create()
        self.result_creation_kwargs = self.get_result_creation_kwargs(self.simulation)

    def test_serializer_result_correct_attributes(self):
        res = LAWMResult.objects.create(**self.result_creation_kwargs)

        serializer = ResultSerializer(res)
        data = serializer.data

        self.assertEqual(data["year"]   , self.result_creation_kwargs["year"])
        self.assertEqual(data["pop"]    , self.result_creation_kwargs["pop"])
        self.assertEqual(data["popr"]   , self.result_creation_kwargs["popr"])
        self.assertEqual(data["exlife"] , self.result_creation_kwargs["exlife"])
        self.assertEqual(data["grmor"]  , self.result_creation_kwargs["grmor"])
        self.assertEqual(data["birthr"] , self.result_creation_kwargs["birthr"])
        self.assertEqual(data["chmor"]  , self.result_creation_kwargs["chmor"])
        self.assertEqual(data["calor"]  , self.result_creation_kwargs["calor"])
        self.assertEqual(data["prot"]   , self.result_creation_kwargs["prot"])
        self.assertEqual(data["hsexfl"] , self.result_creation_kwargs["hsexfl"])
        self.assertEqual(data["gnpxc"]  , self.result_creation_kwargs["gnpxc"])
        self.assertEqual(data["enrol"]  , self.result_creation_kwargs["enrol"])
        self.assertEqual(data["educr"]  , self.result_creation_kwargs["educr"])
        self.assertEqual(data["eapopr"] , self.result_creation_kwargs["eapopr"])
        self.assertEqual(data["tlf"]    , self.result_creation_kwargs["tlf"])
        self.assertEqual(data["rlfd_1"] , self.result_creation_kwargs["rlfd_1"])
        self.assertEqual(data["rlfd_2"] , self.result_creation_kwargs["rlfd_2"])
        self.assertEqual(data["rlfd_3"] , self.result_creation_kwargs["rlfd_3"])
        self.assertEqual(data["rlfd_4"] , self.result_creation_kwargs["rlfd_4"])
        self.assertEqual(data["rlfd_5"] , self.result_creation_kwargs["rlfd_5"])
        self.assertEqual(data["capt"]   , self.result_creation_kwargs["capt"])
        self.assertEqual(data["capd_1"] , self.result_creation_kwargs["capd_1"])
        self.assertEqual(data["capd_2"] , self.result_creation_kwargs["capd_2"])
        self.assertEqual(data["capd_3"] , self.result_creation_kwargs["capd_3"])
        self.assertEqual(data["capd_4"] , self.result_creation_kwargs["capd_4"])
        self.assertEqual(data["capd_5"] , self.result_creation_kwargs["capd_5"])
        self.assertEqual(data["_0_5"]   , self.result_creation_kwargs["_0_5"])
        self.assertEqual(data["_6_17"]  , self.result_creation_kwargs["_6_17"])
        self.assertEqual(data["_11_70"] , self.result_creation_kwargs["_11_70"])
        self.assertEqual(data["al"]     , self.result_creation_kwargs["al"])
        self.assertEqual(data["excal"]  , self.result_creation_kwargs["excal"])
        self.assertEqual(data["fert"]   , self.result_creation_kwargs["fert"])
        self.assertEqual(data["rend"]   , self.result_creation_kwargs["rend"])
        self.assertEqual(data["falu"]   , self.result_creation_kwargs["falu"])
        self.assertEqual(data["urbanr"] , self.result_creation_kwargs["urbanr"])
        self.assertEqual(data["turbh"]  , self.result_creation_kwargs["turbh"])
        self.assertEqual(data["sepopr"] , self.result_creation_kwargs["sepopr"])
        self.assertEqual(data["houser"] , self.result_creation_kwargs["houser"])
        self.assertEqual(data["perxfl"] , self.result_creation_kwargs["perxfl"])
        self.assertEqual(data["gnp"]    , self.result_creation_kwargs["gnp"])
        self.assertEqual(data["gnpd_1"] , self.result_creation_kwargs["gnpd_1"])
        self.assertEqual(data["gnpd_2"] , self.result_creation_kwargs["gnpd_2"])
        self.assertEqual(data["gnpd_3"] , self.result_creation_kwargs["gnpd_3"])
        self.assertEqual(data["gnpd_4"] , self.result_creation_kwargs["gnpd_4"])
