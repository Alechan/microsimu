from unittest import TestCase

from simulation.dag.node import AtomicBlockNode, ModelVariableNode


class TestNode(TestCase):
    def test_atomic_node_returns_that_is_atomic_node(self):
        node = AtomicBlockNode()
        self.assertTrue(node.is_atomic_block_node)

    def test_model_variable_node_returns_that_is_not_atomic_node(self):
        node = ModelVariableNode()
        self.assertFalse(node.is_atomic_block_node)
