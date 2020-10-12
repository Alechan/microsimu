import pinject


class DAGFactory:
    @pinject.copy_args_to_internal_fields
    def __init__(self, nx):
        pass

    def from_phase(self, phase):
        pass


class DAG:
    @pinject.copy_args_to_internal_fields
    def __init__(self, nx_dag):
        pass

    def nodes(self):
        pass
