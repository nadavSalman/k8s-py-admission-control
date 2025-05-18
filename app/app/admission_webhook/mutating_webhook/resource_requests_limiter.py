from flask import Blueprint, request, Response
import json
import base64
from kubernetes.client import V1ResourceRequirements
from kubernetes.utils.quantity import parse_quantity
from admission_webhook.admission.namespace_exclusion import NamespaceValidator
from admission_webhook.admission.templates import AdmissionResponse
from admission_webhook.logging_config.logging_config import configure_logging

resource_requests_limiter_bp = Blueprint('resource_requests_limiter', __name__)

namespace_validator = NamespaceValidator()

# Configure logging
logger = configure_logging()

@resource_requests_limiter_bp.route('/resource-request-limiter', methods=['POST'])
def resource_request_limiter():
    admission_review = request.get_json()
    uid = admission_review['request']['uid']
    namespace = admission_review['request']['object']['metadata']['namespace']
    containers = admission_review['request']['object']['spec']['containers']

    logger.info(f"Received admission review for UID: {uid}, Namespace: {namespace}")

    # Apply resource limits only if the namespace is not excluded
    if not namespace_validator.is_namespace_excluded(namespace):
        logger.info(f"Namespace {namespace} is not excluded. Applying resource limits.")
        patch = []
        for i, container in enumerate(containers):
            resources = container.get('resources', {})
            requests = resources.get('requests', {})

            # Convert CPU and memory requests to comparable format
            cpu_request = requests.get('cpu', '0')
            memory_request = requests.get('memory', '0')
            cpu_request_value = parse_quantity(cpu_request)
            memory_request_value = parse_quantity(memory_request)

            # Check and set default requests if not present
            if 'cpu' not in requests or cpu_request_value > parse_quantity('10m'):
                logger.info(f"Container {i} CPU request {cpu_request} exceeds limit. Setting to 10m.")
                patch.append({
                    "op": "add",
                    "path": f"/spec/containers/{i}/resources/requests/cpu",
                    "value": "10m"
                })
            if 'memory' not in requests or memory_request_value > parse_quantity('10Mi'):
                logger.info(f"Container {i} Memory request {memory_request} exceeds limit. Setting to 10Mi.")
                patch.append({
                    "op": "add",
                    "path": f"/spec/containers/{i}/resources/requests/memory",
                    "value": "10Mi"
                })

        if patch:
            logger.info('Patch: %s', json.dumps(patch, indent=2))
            worning = "Resource requests have been limited to 10m CPU and 10Mi memory."
            admission_response = AdmissionResponse.mutation_response(uid, True, patch, warnings=[worning])
        else:
            admission_response = AdmissionResponse.validation_response(uid, True)
            logger.info("No patch needed. Validation response generated.")
    else:
        admission_response = AdmissionResponse.validation_response(uid, True)
        logger.info(f"Namespace {namespace} is excluded. Validation response generated.")

    return Response(json.dumps(admission_response), status=200, mimetype='application/json')