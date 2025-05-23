from k8s_client.controller.kubernetes_controller import KubernetesController
from k8s_client.commands.invoker import Invoker
from k8s_client.commands.list_pods_command import ListPodsCommand
from k8s_client.commands.restart_deployment_command import RestartDeploymentCommand

def main() -> None:
    ctrlr = KubernetesController()
    invkr = Invoker()

    invkr.add_command(ListPodsCommand(ctrlr))
    invkr.add_command(RestartDeploymentCommand(ctrlr, "hello-minikube"))

    invkr.run()

if __name__ == "__main__":
    main()