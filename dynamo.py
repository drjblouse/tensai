""" Test dynamo db local connection. """
from boto3 import client, resource
from settings import DB_CONNECTION_URL, DB_MODULE_NAME


def test_client():
    """ For a Boto3 client. """
    dynamo_client = client(DB_MODULE_NAME, endpoint_url=DB_CONNECTION_URL)
    response = dynamo_client.list_tables()
    print(response)


def test_service_resource():
    """ For a Boto3 service resource. """
    dynamo_service = resource(DB_MODULE_NAME, endpoint_url=DB_CONNECTION_URL)
    print(list(dynamo_service.tables.all()))
