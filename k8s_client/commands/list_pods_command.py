from .abstract_base_command import Command
from k8s_client.controller.kubernetes_controller import KubernetesController

class ListPodsCommand(Command):
    def __init__(self: 'ListPodsCommand', controller : 'KubernetesController', namespace : str = "default"):
        self.controller : 'KubernetesController' = controller
        self.namespace : str = namespace

    def execute(self) -> None:
        self.controller.list_pods_with_logs()