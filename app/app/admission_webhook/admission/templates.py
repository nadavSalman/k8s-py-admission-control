import json
import base64
from admission_webhook.logging_config.logging_config import configure_logging

# Configure logging
logger = configure_logging()


class AdmissionResponse:
    """
    Represents a Kubernetes AdmissionReview response.
    Source : [https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#response]

    Attributes:
        uid (str): The unique identifier for the admission request.
        allowed (bool): Indicates whether the admission request is allowed.
        patch (list, optional): A list of JSONPatch operations to apply. Defaults to None.
        patch_type (str): The type of patch being used. Defaults to "JSONPatch".

    Methods:
        to_dict():
            Converts the AdmissionResponse instance to a dictionary format suitable for Kubernetes API responses.

        validation_response(uid, allowed):
            Creates a validation response dictionary for the given UID and allowed status.

        mutation_response(uid, allowed, patch):
            Creates a mutation response dictionary for the given UID, allowed status, and patch operations.
    """
    def __init__(self, uid, allowed, patch=None, warnings=None):
        self.api_version = "admission.k8s.io/v1"
        self.kind = "AdmissionReview"
        self.uid = uid
        self.allowed = allowed
        self.patch = patch
        self.patch_type = "JSONPatch"
        self.warnings = warnings
        logger.debug(f"Initialized AdmissionResponse with uid={uid}, allowed={allowed}, patch={patch}, warnings={warnings}")

    def to_dict(self):
        response = {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "response": {
                "uid": self.uid,
                "allowed": self.allowed
            }
        }
        if self.patch:
            patch_str = json.dumps(self.patch)
            patch_base64 = base64.b64encode(patch_str.encode()).decode()
            response["response"]["patch"] = patch_base64
            response["response"]["patchType"] = self.patch_type
            logger.debug(f"Added patch to response: {patch_base64}")

        if self.warnings:
            response["response"]["warnings"] = self.warnings
            logger.debug(f"Added warnings to response: {self.warnings}")

        logger.info(f"AdmissionResponse created: {json.dumps(response, indent=2)}")
        return response

    @staticmethod
    def validation_response(uid, allowed,warnings=None):
        logger.debug(f"Creating validation response with uid={uid}, allowed={allowed}")
        return AdmissionResponse(uid, allowed,warnings).to_dict()

    @staticmethod
    def mutation_response(uid, allowed, patch,warnings=None):
        logger.debug(f"Creating mutation response with uid={uid}, allowed={allowed}, patch={patch}")
        return AdmissionResponse(uid, allowed, patch,warnings).to_dict()

    # TBD : Add method to validate against k8s API if the JSONPatch is valid (dry-run !)

# # Example usage:
# # For validation response
# validation_response = AdmissionResponse.validation_response(uid="12345", allowed=True)

# # For mutation response with JSON patch
# patch = [
#     {"op": "add", "path": "/spec/containers/0/resources/requests/cpu", "value": "10m"},
#     {"op": "add", "path": "/spec/containers/0/resources/requests/memory", "value": "10Mi"}
# ]
# mutation_response = AdmissionResponse.mutation_response(uid="12345", allowed=True, patch=patch)
