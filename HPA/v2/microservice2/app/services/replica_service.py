from kubernetes import client, config


def get_replicas_detail():
    # Use this inside any pod running in the cluster
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace="default")

    list_of_pods = []
    for pod in pods.items:
        list_of_pods.append(pod)

    return list_of_pods
