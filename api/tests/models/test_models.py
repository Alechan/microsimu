from unittest import mock
from unittest.mock import patch, MagicMock

import django
from django.test import TestCase
from django.utils import timezone

from api.models.models import LAWMSimulation, LAWMResult
from api.std_lib.lawm.variables import *
from api.tests.api_test_mixin import ApiTestMixin


class LAWMSimulationTest(TestCase, ApiTestMixin):
    def test_created_time_is_automatically_set_to_now(self):
        # *) timezone.now() uses UTC and not the timezone set in django's settings.py
        # *) django stores dates in UTC and the serializer uses the timezone from settings.py
        time_before_creation = timezone.now()
        simulation = LAWMSimulation.objects.create()
        time_after_creation = timezone.now()
        self.assertGreater(simulation.created, time_before_creation)
        self.assertGreater(time_after_creation, simulation.created)

    @mock.patch('api.models.models.LAWMResult.get_variables_information')
    def test_get_variables_information_returns_results_variables_information_and_is_cached(self, method_mock):
        simulation_1, results_1 = self.create_simple_db_simulation(pop_values=[1])
        simulation_2, results_2 = self.create_simple_db_simulation(pop_values=[1])

        vars_info_mock = MagicMock()
        method_mock.return_value = vars_info_mock

        self.assertEqual(method_mock.call_count, 0)
        simu_1_vars_info   = simulation_1.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, simu_1_vars_info)

        simu_1_vars_info_2   = simulation_1.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, simu_1_vars_info_2)

        simu_2_vars_info   = simulation_2.get_variables_information()
        self.assertEqual(method_mock.call_count, 1)
        self.assertEqual(vars_info_mock, simu_2_vars_info)


class LAWMResultTest(TestCase, ApiTestMixin):
    def setUp(self):
        self.simulation = LAWMSimulation.objects.create()
        self.result_creation_kwargs = self.get_result_creation_kwargs(self.simulation)

    def test_unique_together_year_and_simulation(self):
        res_1 = LAWMResult.objects.create(**self.result_creation_kwargs)
        try:
            res_2 = LAWMResult.objects.create(**self.result_creation_kwargs)
            self.fail("Creating 2 results with same year and simulation should raise an error.")
        except django.db.utils.IntegrityError:
            pass

    def test_all_attributes_are_readable_and_casted_to_variables(self):
        res = LAWMResult.objects.create(**self.result_creation_kwargs)

        self.assertEqual(res.simulation, self.simulation)
        self.assertEqual(res.year      , self.result_creation_kwargs["year"])
        self.assertEqual(res.pop       , Population(self.result_creation_kwargs["pop"]))
        self.assertEqual(res.popr      , PopulationGrowth(self.result_creation_kwargs["popr"]))
        self.assertEqual(res.exlife    , LifeExpectancy(self.result_creation_kwargs["exlife"]))
        self.assertEqual(res.grmor     , GrossMortality(self.result_creation_kwargs["grmor"]))
        self.assertEqual(res.birthr    , BirthRate(self.result_creation_kwargs["birthr"]))
        self.assertEqual(res.chmor     , ChildMortalityRate(self.result_creation_kwargs["chmor"]))
        self.assertEqual(res.calor     , Calories(self.result_creation_kwargs["calor"]))
        self.assertEqual(res.prot      , Proteins(self.result_creation_kwargs["prot"]))
        self.assertEqual(res.hsexfl    , HousesPerFamily(self.result_creation_kwargs["hsexfl"]))
        self.assertEqual(res.gnpxc     , GNPPerPerson(self.result_creation_kwargs["gnpxc"]))
        self.assertEqual(res.enrol     , EnrolmentPercentage(self.result_creation_kwargs["enrol"]))
        self.assertEqual(res.educr     , MatriculationPercentage(self.result_creation_kwargs["educr"]))
        self.assertEqual(res.eapopr    , Pop11To70LaborForcePercentage(self.result_creation_kwargs["eapopr"]))
        self.assertEqual(res.tlf       , TotalLaborForce(self.result_creation_kwargs["tlf"]))
        self.assertEqual(res.rlfd_1    , LaborForceFoodSectorProportion(self.result_creation_kwargs["rlfd_1"]))
        self.assertEqual(res.rlfd_2    , LaborForceHousingSectorProportion(self.result_creation_kwargs["rlfd_2"]))
        self.assertEqual(res.rlfd_3    , LaborForceEducationSectorProportion(self.result_creation_kwargs["rlfd_3"]))
        self.assertEqual(res.rlfd_4    , LaborForceOtherGoodsProportion(self.result_creation_kwargs["rlfd_4"]))
        self.assertEqual(res.rlfd_5    , LaborForceCapitalGoodsSectorProportion(self.result_creation_kwargs["rlfd_5"]))
        self.assertEqual(res.capt      , TotalCapital(self.result_creation_kwargs["capt"]))
        self.assertEqual(res.capd_1    , CapitalFoodSectorProportion(self.result_creation_kwargs["capd_1"]))
        self.assertEqual(res.capd_2    , CapitalHousingSectorProportion(self.result_creation_kwargs["capd_2"]))
        self.assertEqual(res.capd_3    , CapitalEducationSectorProportion(self.result_creation_kwargs["capd_3"]))
        self.assertEqual(res.capd_4    , CapitalOtherGoodsSectorProportion(self.result_creation_kwargs["capd_4"]))
        self.assertEqual(res.capd_5    , CapitalCapitalGoodsSectorProportion(self.result_creation_kwargs["capd_5"]))
        self.assertEqual(res._0_5      , Pop0to5Percentage(self.result_creation_kwargs["_0_5"]))
        self.assertEqual(res._6_17     , Pop6to17Percentage(self.result_creation_kwargs["_6_17"]))
        self.assertEqual(res._11_70    , Pop11to70Percentage(self.result_creation_kwargs["_11_70"]))
        self.assertEqual(res.al        , ArableLand(self.result_creation_kwargs["al"]))
        self.assertEqual(res.excal     , ExcessCalories(self.result_creation_kwargs["excal"]))
        self.assertEqual(res.fert      , FertilizersProduction(self.result_creation_kwargs["fert"]))
        self.assertEqual(res.rend      , AgricultureYield(self.result_creation_kwargs["rend"]))
        self.assertEqual(res.falu      , PotentialArableLandProportion(self.result_creation_kwargs["falu"]))
        self.assertEqual(res.urbanr    , UrbanPopulationPercentage(self.result_creation_kwargs["urbanr"]))
        self.assertEqual(res.turbh     , UrbanizationRate(self.result_creation_kwargs["turbh"]))
        self.assertEqual(res.sepopr    , SecondaryLaborForcePercentage(self.result_creation_kwargs["sepopr"]))
        self.assertEqual(res.houser    , HousesPerPersonPercentage(self.result_creation_kwargs["houser"]))
        self.assertEqual(res.perxfl    , PeoplePerFamily(self.result_creation_kwargs["perxfl"]))
        self.assertEqual(res.gnp       , GNP(self.result_creation_kwargs["gnp"]))
        self.assertEqual(res.gnpd_1    , GNPFoodSectorProportion(self.result_creation_kwargs["gnpd_1"]))
        self.assertEqual(res.gnpd_2    , GNPHousingSectorProportion(self.result_creation_kwargs["gnpd_2"]))
        self.assertEqual(res.gnpd_3    , GNPEducationSectorProportion(self.result_creation_kwargs["gnpd_3"]))
        self.assertEqual(res.gnpd_4    , GNPOtherGoodsSectorProportion(self.result_creation_kwargs["gnpd_4"]))
        self.assertEqual(res.gnpd_5    , GNPCapitalGoodsSectorProportion(self.result_creation_kwargs["gnpd_5"]))

    def test_get_variables_information_returns_collection_of_correct_vars_info(self):
        res = LAWMResult.objects.create(**self.result_creation_kwargs)
        actual_vars_info = res.get_variables_information()
        expected_vars_info = {
            "pop"    : Population.info_as_dict(),
            "popr"   : PopulationGrowth.info_as_dict(),
            "exlife" : LifeExpectancy.info_as_dict(),
            "grmor"  : GrossMortality.info_as_dict(),
            "birthr" : BirthRate.info_as_dict(),
            "chmor"  : ChildMortalityRate.info_as_dict(),
            "calor"  : Calories.info_as_dict(),
            "prot"   : Proteins.info_as_dict(),
            "hsexfl" : HousesPerFamily.info_as_dict(),
            "gnpxc"  : GNPPerPerson.info_as_dict(),
            "enrol"  : EnrolmentPercentage.info_as_dict(),
            "educr"  : MatriculationPercentage.info_as_dict(),
            "eapopr" : Pop11To70LaborForcePercentage.info_as_dict(),
            "tlf"    : TotalLaborForce.info_as_dict(),
            "rlfd_1" : LaborForceFoodSectorProportion.info_as_dict(),
            "rlfd_2" : LaborForceHousingSectorProportion.info_as_dict(),
            "rlfd_3" : LaborForceEducationSectorProportion.info_as_dict(),
            "rlfd_4" : LaborForceOtherGoodsProportion.info_as_dict(),
            "rlfd_5" : LaborForceCapitalGoodsSectorProportion.info_as_dict(),
            "capt"   : TotalCapital.info_as_dict(),
            "capd_1" : CapitalFoodSectorProportion.info_as_dict(),
            "capd_2" : CapitalHousingSectorProportion.info_as_dict(),
            "capd_3" : CapitalEducationSectorProportion.info_as_dict(),
            "capd_4" : CapitalOtherGoodsSectorProportion.info_as_dict(),
            "capd_5" : CapitalCapitalGoodsSectorProportion.info_as_dict(),
            "_0_5"   : Pop0to5Percentage.info_as_dict(),
            "_6_17"  : Pop6to17Percentage.info_as_dict(),
            "_11_70" : Pop11to70Percentage.info_as_dict(),
            "al"     : ArableLand.info_as_dict(),
            "excal"  : ExcessCalories.info_as_dict(),
            "fert"   : FertilizersProduction.info_as_dict(),
            "rend"   : AgricultureYield.info_as_dict(),
            "falu"   : PotentialArableLandProportion.info_as_dict(),
            "urbanr" : UrbanPopulationPercentage.info_as_dict(),
            "turbh"  : UrbanizationRate.info_as_dict(),
            "sepopr" : SecondaryLaborForcePercentage.info_as_dict(),
            "houser" : HousesPerPersonPercentage.info_as_dict(),
            "perxfl" : PeoplePerFamily.info_as_dict(),
            "gnp"    : GNP.info_as_dict(),
            "gnpd_1" : GNPFoodSectorProportion.info_as_dict(),
            "gnpd_2" : GNPHousingSectorProportion.info_as_dict(),
            "gnpd_3" : GNPEducationSectorProportion.info_as_dict(),
            "gnpd_4" : GNPOtherGoodsSectorProportion.info_as_dict(),
            "gnpd_5" : GNPCapitalGoodsSectorProportion.info_as_dict(),

        }
        self.assertEqual(actual_vars_info, expected_vars_info)
