import unittest
from admission_webhook.admission.namespace_exclusion import NamespaceValidator

class TestNamespaceValidator(unittest.TestCase):
    def setUp(self):
        self.namespace_validator = NamespaceValidator(mode="unittest")

    def test_excluded_namespaces(self):
        # List of namespaces to test
        namespaces = [
            "kube-node-lease",
            "kube-public",
            "kube-system"
        ]

        for namespace in namespaces:
            with self.subTest(namespace=namespace):
                print(f"Testing namespace: {namespace}")
                self.assertTrue(self.namespace_validator.is_namespace_excluded(namespace))


if __name__ == '__main__':
    unittest.main()