from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models.models import LAWMGeneralParameters
from api.std_lib.lawm.general_parameters import *
from api.tests.api_test_mixin import MicroSimuTestMixin


class LAWMGeneralParametersTest(TestCase, MicroSimuTestMixin):
    @classmethod
    def setUpTestData(cls):
        db_tree = cls.create_full_simulation_db_tree()
        cls.general_parameters = db_tree.general_parameters

    def test_default_values_are_set_when_none_provided(self):
        gen_params = LAWMGeneralParameters()
        self.assertEqual(gen_params.simulation_stop     , SimulationStop(2000))
        self.assertEqual(gen_params.optimization_start  , OptimizationStart(1980))
        self.assertEqual(gen_params.payments_equilibrium, PaymentsEquilibrium(2000))
        self.assertEqual(gen_params.fertilizer_cost     , FertilizerCost(769230.8))
        self.assertEqual(gen_params.weight_constraint_1 , WeightConstraint1(6.0))
        self.assertEqual(gen_params.weight_constraint_2 , WeightConstraint2(8.0))
        self.assertEqual(gen_params.weight_constraint_3 , WeightConstraint3(6.0))
        self.assertEqual(gen_params.weight_constraint_4 , WeightConstraint4(6.0))
        self.assertEqual(gen_params.weight_constraint_5 , WeightConstraint5(6.0))
        self.assertEqual(gen_params.weight_constraint_6 , WeightConstraint6(6.0))
        self.assertEqual(gen_params.weight_constraint_7 , WeightConstraint7(4.0))
        self.assertEqual(gen_params.weight_constraint_8 , WeightConstraint8(4.0))
        self.assertEqual(gen_params.weight_constraint_9 , WeightConstraint9(6.0))
        self.assertEqual(gen_params.weight_constraint_10, WeightConstraint10(6.0))
        self.assertEqual(gen_params.weight_constraint_11, WeightConstraint11(6.0))
        self.assertEqual(gen_params.weight_constraint_12, WeightConstraint12(2.0))
        self.assertEqual(gen_params.weight_constraint_13, WeightConstraint13(4.0))
        self.assertEqual(gen_params.weight_constraint_14, WeightConstraint14(4.0))
        self.assertEqual(gen_params.weight_constraint_15, WeightConstraint15(7.0))
        self.assertEqual(gen_params.weight_constraint_16, WeightConstraint16(4.0))
        self.assertEqual(gen_params.weight_constraint_17, WeightConstraint17(4.0))
        self.assertEqual(gen_params.weight_constraint_18, WeightConstraint18(4.0))
        self.assertEqual(gen_params.weight_constraint_19, WeightConstraint19(8.0))
        self.assertEqual(gen_params.weight_constraint_20, WeightConstraint20(6.0))
        self.assertEqual(gen_params.weight_constraint_21, WeightConstraint21(4.0))
        self.assertEqual(gen_params.weight_constraint_22, WeightConstraint22(6.0))
        self.assertEqual(gen_params.weight_constraint_23, WeightConstraint23(8.0))
        self.assertEqual(gen_params.weight_constraint_24, WeightConstraint24(6.0))
        self.assertEqual(gen_params.weight_constraint_25, WeightConstraint25(2.0))
        self.assertEqual(gen_params.weight_constraint_26, WeightConstraint26(1.0))

    def test_default_values_can_be_overridden(self):
        gen_params = LAWMGeneralParameters.objects.create(simulation_stop=2)
        self.assertEqual(gen_params.simulation_stop, SimulationStop(2))

    def test_validators_are_automatically_added(self):
        # TODO: add tests for each LAWM parameter
        value = 1959
        invalid_params = LAWMGeneralParameters.objects.create(simulation_stop=value)
        try:
            invalid_params.full_clean()
            self.fail("An error should've been raised but wasn't.")
        except ValidationError:
            pass

    def test_get_metadata_returns_correct_information(self):
        expected_metadata = {
            "simulation_stop"     : SimulationStop.info_as_dict(),
            "optimization_start"  : OptimizationStart.info_as_dict(),
            "payments_equilibrium": PaymentsEquilibrium.info_as_dict(),
            "fertilizer_cost"     : FertilizerCost.info_as_dict(),
            "weight_constraint_1" : WeightConstraint1.info_as_dict(),
            "weight_constraint_2" : WeightConstraint2.info_as_dict(),
            "weight_constraint_3" : WeightConstraint3.info_as_dict(),
            "weight_constraint_4" : WeightConstraint4.info_as_dict(),
            "weight_constraint_5" : WeightConstraint5.info_as_dict(),
            "weight_constraint_6" : WeightConstraint6.info_as_dict(),
            "weight_constraint_7" : WeightConstraint7.info_as_dict(),
            "weight_constraint_8" : WeightConstraint8.info_as_dict(),
            "weight_constraint_9" : WeightConstraint9.info_as_dict(),
            "weight_constraint_10": WeightConstraint10.info_as_dict(),
            "weight_constraint_11": WeightConstraint11.info_as_dict(),
            "weight_constraint_12": WeightConstraint12.info_as_dict(),
            "weight_constraint_13": WeightConstraint13.info_as_dict(),
            "weight_constraint_14": WeightConstraint14.info_as_dict(),
            "weight_constraint_15": WeightConstraint15.info_as_dict(),
            "weight_constraint_16": WeightConstraint16.info_as_dict(),
            "weight_constraint_17": WeightConstraint17.info_as_dict(),
            "weight_constraint_18": WeightConstraint18.info_as_dict(),
            "weight_constraint_19": WeightConstraint19.info_as_dict(),
            "weight_constraint_20": WeightConstraint20.info_as_dict(),
            "weight_constraint_21": WeightConstraint21.info_as_dict(),
            "weight_constraint_22": WeightConstraint22.info_as_dict(),
            "weight_constraint_23": WeightConstraint23.info_as_dict(),
            "weight_constraint_24": WeightConstraint24.info_as_dict(),
            "weight_constraint_25": WeightConstraint25.info_as_dict(),
            "weight_constraint_26": WeightConstraint26.info_as_dict(),
        }
        actual_metadata = LAWMGeneralParameters.get_metadata()

        self.assertEqual(expected_metadata, actual_metadata)

