""" Tests for the local dynamo db. """
# -*- coding: utf-8 -*-
from unittest import TestCase, skipIf
from invoke import run
from common.graph import GraphStore
from common import types
from common.constants import Constants


def check_local_db():
    """ Check if the local db is running. """
    try:
        return run(Constants.LOCAL_DB_RUNNING_CMD).ok
    except(ValueError, Exception):
        return False


@skipIf(not check_local_db(), 'Local DB not running.')
class TestLocalDB(TestCase):
    """ Test fixture for testing general local dynamo operations. """
    def test_simple(self):
        graph = GraphStore()
        self.assertIsNotNone(graph)
        fact = types.Fact()
        fact.name = 'Dummy Fact'
        graph.create_table(fact.type())
        key = graph.put_item(fact.type(), fact)
        self.assertIsNotNone(key)
        self.assertEqual(key, fact.key)
        item = graph.get_item(fact.type(), key)
        self.assertEqual(item['name'], fact.name)
        graph.delete_item(fact.type(), key)
        item = graph.get_item(fact.type(), key)
        self.assertIsNone(item)

    def test_table_create(self):
        dummy_table = 'test'
        graph = GraphStore()
        self.assertFalse(graph.delete_table(dummy_table))
        self.assertFalse(graph.table_exists(dummy_table))
        graph.create_table(dummy_table)
        self.assertTrue(graph.table_exists(dummy_table))
        graph.delete_table(dummy_table)
        self.assertFalse(graph.table_exists(dummy_table))
