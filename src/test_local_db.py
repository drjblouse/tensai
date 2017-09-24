""" Tests for the local dynamo db. """
from unittest import TestCase

from src.dynamo import test_client, test_service_resource


class TestLocalDB(TestCase):
    """ Test fixture for testing general local dynamo operations. """

    def test_client_access(self):
        """ Test local dynamo client access. """
        self.assertIsNotNone(test_client())
        self.assertIsNotNone(test_service_resource())
