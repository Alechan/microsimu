import django
from django.test import TestCase

from api.models.models import LAWMYearResult
from api.std_lib.lawm.variables import *
from api.tests.helpers.api_test_mixin import MicroSimuTestMixin


class LAWMYearResultTest(TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.region_result = db_tree.region_result_r1
        cls.year_1960_result = db_tree.year_results_reg_1[0]
        cls.year_1960_result_creation_kwargs = cls.get_year_result_creation_kwargs(cls.region_result, year=1960)

    def test_unique_together_year_and_simulation(self):
        try:
            _ = LAWMYearResult.objects.create(**self.year_1960_result_creation_kwargs)
            self.fail("Creating 2 year results with same year and region result should raise an error.")
        except django.db.utils.IntegrityError:
            pass

    def test_all_attributes_are_readable_and_casted_to_lawm_variables(self):
        y_res = self.year_1960_result
        var_values = self.year_1960_result_creation_kwargs

        self.assertEqual(y_res.region_result, self.region_result)
        self.assertEqual(y_res.year  , var_values["year"])
        self.assertEqual(y_res.pop   , Population(var_values["pop"]))
        self.assertEqual(y_res.popr  , PopulationGrowth(var_values["popr"]))
        self.assertEqual(y_res.exlife, LifeExpectancy(var_values["exlife"]))
        self.assertEqual(y_res.grmor , GrossMortality(var_values["grmor"]))
        self.assertEqual(y_res.birthr, BirthRate(var_values["birthr"]))
        self.assertEqual(y_res.chmor , ChildMortalityRate(var_values["chmor"]))
        self.assertEqual(y_res.calor , Calories(var_values["calor"]))
        self.assertEqual(y_res.prot  , Proteins(var_values["prot"]))
        self.assertEqual(y_res.hsexfl, HousesPerFamily(var_values["hsexfl"]))
        self.assertEqual(y_res.gnpxc , GNPPerPerson(var_values["gnpxc"]))
        self.assertEqual(y_res.enrol , EnrolmentPercentage(var_values["enrol"]))
        self.assertEqual(y_res.educr , MatriculationPercentage(var_values["educr"]))
        self.assertEqual(y_res.eapopr, Pop11To70LaborForcePercentage(var_values["eapopr"]))
        self.assertEqual(y_res.tlf   , TotalLaborForce(var_values["tlf"]))
        self.assertEqual(y_res.rlfd_1, LaborForceFoodSectorProportion(var_values["rlfd_1"]))
        self.assertEqual(y_res.rlfd_2, LaborForceHousingSectorProportion(var_values["rlfd_2"]))
        self.assertEqual(y_res.rlfd_3, LaborForceEducationSectorProportion(var_values["rlfd_3"]))
        self.assertEqual(y_res.rlfd_4, LaborForceOtherGoodsProportion(var_values["rlfd_4"]))
        self.assertEqual(y_res.rlfd_5, LaborForceCapitalGoodsSectorProportion(var_values["rlfd_5"]))
        self.assertEqual(y_res.capt  , TotalCapital(var_values["capt"]))
        self.assertEqual(y_res.capd_1, CapitalFoodSectorProportion(var_values["capd_1"]))
        self.assertEqual(y_res.capd_2, CapitalHousingSectorProportion(var_values["capd_2"]))
        self.assertEqual(y_res.capd_3, CapitalEducationSectorProportion(var_values["capd_3"]))
        self.assertEqual(y_res.capd_4, CapitalOtherGoodsSectorProportion(var_values["capd_4"]))
        self.assertEqual(y_res.capd_5, CapitalCapitalGoodsSectorProportion(var_values["capd_5"]))
        self.assertEqual(y_res._0_5  , Pop0to5Percentage(var_values["_0_5"]))
        self.assertEqual(y_res._6_17 , Pop6to17Percentage(var_values["_6_17"]))
        self.assertEqual(y_res._11_70, Pop11to70Percentage(var_values["_11_70"]))
        self.assertEqual(y_res.al    , ArableLand(var_values["al"]))
        self.assertEqual(y_res.excal , ExcessCalories(var_values["excal"]))
        self.assertEqual(y_res.fert  , FertilizersProduction(var_values["fert"]))
        self.assertEqual(y_res.rend  , AgricultureYield(var_values["rend"]))
        self.assertEqual(y_res.falu  , PotentialArableLandProportion(var_values["falu"]))
        self.assertEqual(y_res.urbanr, UrbanPopulationPercentage(var_values["urbanr"]))
        self.assertEqual(y_res.turbh , UrbanizationRate(var_values["turbh"]))
        self.assertEqual(y_res.sepopr, SecondaryLaborForcePercentage(var_values["sepopr"]))
        self.assertEqual(y_res.houser, HousesPerPersonPercentage(var_values["houser"]))
        self.assertEqual(y_res.perxfl, PeoplePerFamily(var_values["perxfl"]))
        self.assertEqual(y_res.gnp   , GNP(var_values["gnp"]))
        self.assertEqual(y_res.gnpd_1, GNPFoodSectorProportion(var_values["gnpd_1"]))
        self.assertEqual(y_res.gnpd_2, GNPHousingSectorProportion(var_values["gnpd_2"]))
        self.assertEqual(y_res.gnpd_3, GNPEducationSectorProportion(var_values["gnpd_3"]))
        self.assertEqual(y_res.gnpd_4, GNPOtherGoodsSectorProportion(var_values["gnpd_4"]))
        self.assertEqual(y_res.gnpd_5, GNPCapitalGoodsSectorProportion(var_values["gnpd_5"]))

    def test_get_variables_information_returns_collection_of_correct_vars_info(self):
        actual_vars_info = self.year_1960_result.get_variables_information()
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
