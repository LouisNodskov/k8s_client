from k8s_client import KubernetesController
from .abstract_base_command import Command

class ResumeDeploymentCommand(Command):
    def __init__(self, controller : KubernetesController, name : str, namespace : str = "default"):
        self.controller : KubernetesController = controller
        self.namespace : str = namespace
        self.name : str = name

    def execute(self):
        self.controller.resume_deployment(self.namespace, self.name)