class Node:
    def __init__(self, is_atomic_block_node):
        self.is_atomic_block_node = is_atomic_block_node


class AtomicBlockNode(Node):
    def __init__(self):
        super().__init__(is_atomic_block_node=True)


class ModelVariableNode(Node):
    def __init__(self):
        super().__init__(is_atomic_block_node=False)
