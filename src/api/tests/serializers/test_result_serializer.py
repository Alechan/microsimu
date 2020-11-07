from django import test

from api.serializers.results_serializers import ResultSerializer
from api.tests.api_test_mixin import MicroSimuTestMixin


class ResultSerializerTest(test.TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.region_result = db_tree.region_result_r1
        cls.year_result = db_tree.year_results_reg_1[0]
        cls.year_result_creation_kwargs = cls.get_year_result_creation_kwargs(cls.region_result, year=1960)
        serializer = ResultSerializer(cls.year_result)
        cls.data = serializer.data

    def test_result_serializer_returns_correct_fields(self):
        temp_fields = set(self.year_result_creation_kwargs.keys())
        temp_fields.remove("region_result")

        expected_fields = temp_fields

        actual_fields = self.data.keys()
        self.assertEqual(expected_fields, actual_fields)

    def test_serializer_result_correct_attributes(self):

        self.assertEqual(self.data["year"]   , self.year_result_creation_kwargs["year"])
        self.assertEqual(self.data["pop"]    , self.year_result_creation_kwargs["pop"])
        self.assertEqual(self.data["popr"]   , self.year_result_creation_kwargs["popr"])
        self.assertEqual(self.data["exlife"] , self.year_result_creation_kwargs["exlife"])
        self.assertEqual(self.data["grmor"]  , self.year_result_creation_kwargs["grmor"])
        self.assertEqual(self.data["birthr"] , self.year_result_creation_kwargs["birthr"])
        self.assertEqual(self.data["chmor"]  , self.year_result_creation_kwargs["chmor"])
        self.assertEqual(self.data["calor"]  , self.year_result_creation_kwargs["calor"])
        self.assertEqual(self.data["prot"]   , self.year_result_creation_kwargs["prot"])
        self.assertEqual(self.data["hsexfl"] , self.year_result_creation_kwargs["hsexfl"])
        self.assertEqual(self.data["gnpxc"]  , self.year_result_creation_kwargs["gnpxc"])
        self.assertEqual(self.data["enrol"]  , self.year_result_creation_kwargs["enrol"])
        self.assertEqual(self.data["educr"]  , self.year_result_creation_kwargs["educr"])
        self.assertEqual(self.data["eapopr"] , self.year_result_creation_kwargs["eapopr"])
        self.assertEqual(self.data["tlf"]    , self.year_result_creation_kwargs["tlf"])
        self.assertEqual(self.data["rlfd_1"] , self.year_result_creation_kwargs["rlfd_1"])
        self.assertEqual(self.data["rlfd_2"] , self.year_result_creation_kwargs["rlfd_2"])
        self.assertEqual(self.data["rlfd_3"] , self.year_result_creation_kwargs["rlfd_3"])
        self.assertEqual(self.data["rlfd_4"] , self.year_result_creation_kwargs["rlfd_4"])
        self.assertEqual(self.data["rlfd_5"] , self.year_result_creation_kwargs["rlfd_5"])
        self.assertEqual(self.data["capt"]   , self.year_result_creation_kwargs["capt"])
        self.assertEqual(self.data["capd_1"] , self.year_result_creation_kwargs["capd_1"])
        self.assertEqual(self.data["capd_2"] , self.year_result_creation_kwargs["capd_2"])
        self.assertEqual(self.data["capd_3"] , self.year_result_creation_kwargs["capd_3"])
        self.assertEqual(self.data["capd_4"] , self.year_result_creation_kwargs["capd_4"])
        self.assertEqual(self.data["capd_5"] , self.year_result_creation_kwargs["capd_5"])
        self.assertEqual(self.data["_0_5"]   , self.year_result_creation_kwargs["_0_5"])
        self.assertEqual(self.data["_6_17"]  , self.year_result_creation_kwargs["_6_17"])
        self.assertEqual(self.data["_11_70"] , self.year_result_creation_kwargs["_11_70"])
        self.assertEqual(self.data["al"]     , self.year_result_creation_kwargs["al"])
        self.assertEqual(self.data["excal"]  , self.year_result_creation_kwargs["excal"])
        self.assertEqual(self.data["fert"]   , self.year_result_creation_kwargs["fert"])
        self.assertEqual(self.data["rend"]   , self.year_result_creation_kwargs["rend"])
        self.assertEqual(self.data["falu"]   , self.year_result_creation_kwargs["falu"])
        self.assertEqual(self.data["urbanr"] , self.year_result_creation_kwargs["urbanr"])
        self.assertEqual(self.data["turbh"]  , self.year_result_creation_kwargs["turbh"])
        self.assertEqual(self.data["sepopr"] , self.year_result_creation_kwargs["sepopr"])
        self.assertEqual(self.data["houser"] , self.year_result_creation_kwargs["houser"])
        self.assertEqual(self.data["perxfl"] , self.year_result_creation_kwargs["perxfl"])
        self.assertEqual(self.data["gnp"]    , self.year_result_creation_kwargs["gnp"])
        self.assertEqual(self.data["gnpd_1"] , self.year_result_creation_kwargs["gnpd_1"])
        self.assertEqual(self.data["gnpd_2"] , self.year_result_creation_kwargs["gnpd_2"])
        self.assertEqual(self.data["gnpd_3"] , self.year_result_creation_kwargs["gnpd_3"])
        self.assertEqual(self.data["gnpd_4"] , self.year_result_creation_kwargs["gnpd_4"])
