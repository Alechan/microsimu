import pinject


class ModelVariablesDependencyGraphFactory:
    @pinject.copy_args_to_internal_fields
    def __init__(self, dag_factory):
        pass
