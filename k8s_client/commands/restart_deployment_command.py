from k8s_client.commands.abstract_command_base import Command
from k8s_client.controller.kubernetes_controller import KubernetesController

class RestartDeploymentCommand(Command):
    def __init__(self, controller : KubernetesController, name : str, namespace : str = "default"):
        self.controller : KubernetesController = controller
        self.namespace : str = namespace
        self.name = name

    def execute(self):
        self.controller.restart_deployment(self.namespace, self.name)