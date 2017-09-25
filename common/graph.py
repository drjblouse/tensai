""" Test dynamo db local connection. """
# -*- coding: utf-8 -*-
from boto3 import resource, client
from common.constants import Constants
from settings import LOGGER, DB_CONNECTION_URL, \
    DEFAULT_PROV_THROUGHPUT, TABLE_EXISTS, KEY_SCHEMA, ATTRIBUTES


class GraphStore(object):
    """ Graph storage manager. """
    def __init__(self, db_url=DB_CONNECTION_URL):
        """ Graph constructor. """
        LOGGER.debug('Creating graph store connection to url:{0}...')
        self._url = db_url
        self._client = client(Constants.DB_MODULE_NAME,
                              endpoint_url=DB_CONNECTION_URL)
        self._db = resource(Constants.DB_MODULE_NAME,
                            endpoint_url=DB_CONNECTION_URL)

    def table_exists(self, table_name):
        """ Check to see if a table exists. """
        try:
            self._client.describe_table(TableName=table_name)
            return True
        except(ValueError, Exception):
            return False

    def create_table(self, table_name, table_schema=KEY_SCHEMA,
                     table_attributes=ATTRIBUTES,
                     provisioned_throughput=DEFAULT_PROV_THROUGHPUT):
        """ Create a new table in the storage graph. """
        if self.table_exists(table_name):
            return self._db.Table(table_name)
        table = self._db.create_table(
            TableName=table_name,
            KeySchema=table_schema,
            AttributeDefinitions=table_attributes,
            ProvisionedThroughput=provisioned_throughput
        )
        # Wait until the table exists.
        table.meta.client.get_waiter(TABLE_EXISTS).wait(
            TableName=table_name)
        return table

    def delete_table(self, table_name):
        """ Delete a table that exists. """
        if self.table_exists(table_name):
            table = self._db.Table(table_name)
            table.delete()
            return True
        return False

    def put_item(self, table_name, item):
        """ Put an item into the graph store. """
        table = self._db.Table(table_name)
        table.put_item(TableName=table_name, Item=item.to_primitive())
        return item.key

    def delete_item(self, table_name, key):
        """ Delete an item from the graph. """
        table = self._db.Table(table_name)
        table.delete_item(Key={Constants.DB_KEY_KEY: str(key)})

    def get_item(self, table_name, key):
        """ Return an item from the graph store. """
        table = self._db.Table(table_name)
        response = table.get_item(Key={Constants.DB_KEY_KEY: str(key)})
        if Constants.DB_ITEM_KEY in response.keys():
            return response[Constants.DB_ITEM_KEY]
        return None
