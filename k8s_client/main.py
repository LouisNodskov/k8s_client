from k8s_client import KubernetesController, Invoker, ListPodsCommand, RestartDeploymentCommand

def main() -> None:
    Invoker() \
        .add_command(ListPodsCommand(KubernetesController())) \
        .add_command(RestartDeploymentCommand(KubernetesController(), "hello-minikube")) \
        .run()