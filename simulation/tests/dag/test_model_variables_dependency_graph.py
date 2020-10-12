from unittest import TestCase

from simulation.dag.model_variables_dependency_graph import ModelVariablesDependencyGraphFactory


class TestModelVariablesDependencyGraphFactory(TestCase):
    def setUp(self):
        # Dependencies
        self.dag_factory = self.FakeDagFactory()
        # Target
        self.model_variables_dependency_graph_factory = ModelVariablesDependencyGraphFactory()
    
    def test_phase_with_one_atomic_block(self):
        phase = self.FakePhase()

        dag = self.model_variables_dependency_graph_factory.from_phase(phase)

        self.assertTrue()

    class FakeDagFactory:
        pass

    class FakePhase:
        pass


