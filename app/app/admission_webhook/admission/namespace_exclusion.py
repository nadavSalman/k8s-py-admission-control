import re
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from admission_webhook.logging_config.logging_config import configure_logging

# Configure logging
logger = configure_logging()

class NamespaceValidator:
    def __init__(self, mode="k8s"):
        self.excluded_namespaces = [
            "kube-*", "gem-master-latest", "dev-latest", "master-latest",
            "devops", "integration-ac", "iot-dev-latest",
            "ns-dev-int-sd-wan-qa", "ufuoma-allcloud"
        ]
        self.mode = mode
        if mode == "k8s":
            try:
                config.load_incluster_config() # Load the configuration from the service account mounted inside the pod.
                logger.info("Loaded in-cluster Kubernetes configuration.")
            except config.ConfigException:
                config.load_kube_config() # Load the configuration from the kubeconfig file
                logger.info("Loaded kubeconfig file.")

    def is_namespace_excluded(self, namespace):
        logger.debug(f"Checking if namespace '{namespace}' is excluded.")
        # Check if the namespace matches any of the excluded namespaces
        for pattern in self.excluded_namespaces:
            logger.debug(f"Checking pattern: {pattern} against namespace: {namespace}")
            if bool(re.match(pattern.replace("*", ".*"), namespace)):
                logger.info(f"Namespace '{namespace}' matches excluded pattern '{pattern}'.")
                return True

        if self.mode == "unittest":
            logger.debug("Running in unittest mode, no namespace exclusion.")
            return False

        # Query the Kubernetes API server for the namespace labels
        v1 = client.CoreV1Api()
        try:
            ns = v1.read_namespace(name=namespace)
            labels = ns.metadata.labels
            logger.debug(f"Namespace '{namespace}' labels: {labels}")
        except ApiException as e:
            logger.error(f"Exception when calling CoreV1Api->read_namespace: {e}")
            return False

        # Check if the namespace has the label admission.devop/ignore=true
        if labels and labels.get("admission.devop/ignore") == "true":
            logger.info(f"Namespace '{namespace}' has label 'admission.devop/ignore=true'.")
            return True

        logger.debug(f"Namespace '{namespace}' is not excluded.")
        return False