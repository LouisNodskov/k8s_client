from k8s_client import KubernetesController, Invoker, ListPodsCommand, RestartDeploymentCommand, PauseDeploymentCommand, ResumeDeploymentCommand

def main() -> None:
    Invoker() \
        .add_command(ListPodsCommand(KubernetesController())) \
        .add_command(RestartDeploymentCommand(KubernetesController(), "hello-minikube")) \
        .add_command(PauseDeploymentCommand(KubernetesController(), "hello-minikube")) \
        .add_command(ResumeDeploymentCommand(KubernetesController(), "hello-minikube")) \
        .run()