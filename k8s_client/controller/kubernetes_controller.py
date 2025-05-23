from kubernetes import client, config
from kubernetes.client \
    import V1PodList, V1Pod, V1ObjectMeta, V1PodStatus, V1PodSpec, V1Container

import time

from typing import Any

class KubernetesController(object):
    def __init__(self: 'KubernetesController') -> None:
        config.load_kube_config()
        # Create Kubernetes API client
        self.controller_client = client.CoreV1Api()
        self.apps_client = client.AppsV1Api()

    def list_pods_with_logs(self: 'KubernetesController', namespace_filter: str = "default") -> None:
        pods : V1PodList = self.controller_client.list_namespaced_pod(namespace=namespace_filter, watch=False)
        items : list[V1Pod] = pods.items

        # Print details of each pod and retrieve logs
        pod : V1Pod
        for pod in items:
            metadata : V1ObjectMeta = pod.metadata
            status : V1PodStatus = pod.status
            spec : V1PodSpec = pod.spec

            pod_name : str = metadata.name
            namespace : str = metadata.namespace
            pod_ip : str = status.pod_ip
            node_name : str = spec.node_name

            containers : list[V1Container] = spec.containers
            for container in containers:
                container_name : str = container.name
                print(container.lifecycle)
                logs : str = self.controller_client.read_namespaced_pod_log(name=pod_name, namespace=namespace, container=container_name, tail_lines=5)
                if len(logs) > 0:
                    print(f"Name: {pod_name:<35} Namespace: {namespace:<12} IP: {pod_ip:<16} Node: {node_name:<10}")

    def restart_deployment(self: 'KubernetesController', namespace: str, deployment_name: str) -> None:
        patch = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                        }
                    }
                }
            }
        }
        self.__dispatch_patch(namespace, deployment_name, patch)

        print(f"Restarted deployment  '{deployment_name}' in namespace '{namespace}'.")

    def pause_deployment(self: 'KubernetesController', namespace: str, deployment_name: str) -> None:
        patch = {
            "spec": {
                "paused": True
            }
        }
        self.__dispatch_patch(namespace, deployment_name, patch)

    def resume_deployment(self: 'KubernetesController', namespace: str, deployment_name: str) -> None:
        patch = {
            "spec": {
                "paused": False
            }
        }
        self.__dispatch_patch(namespace, deployment_name, patch)

    def __dispatch_patch(self: 'KubernetesController', namespace: str, deployment_name: str, patch: dict[Any]) -> None:
        self.apps_client.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=patch
        )