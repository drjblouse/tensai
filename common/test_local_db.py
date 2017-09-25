""" Tests for the local dynamo db. """
# -*- coding: utf-8 -*-
from unittest import TestCase, skipIf
from common.graph import GraphStore
from common import types
from common.constants import Constants, check_local_db, Messages


@skipIf(not check_local_db(), Messages.NO_LOCAL_DB)
class TestLocalDB(TestCase):
    """ Test fixture for testing general local dynamo operations. """
    def test_simple(self):
        graph = GraphStore()
        self.assertIsNotNone(graph)
        fact = types.Fact()
        fact.name = Constants.UNDEFINED
        graph.create_table(fact.type())
        key = graph.put_item(fact.type(), fact)
        self.assertIsNotNone(key)
        self.assertEqual(key, fact.key)
        item = graph.get_item(fact.type(), key)
        self.assertEqual(item[Constants.NAME], fact.name)
        graph.delete_item(fact.type(), key)
        item = graph.get_item(fact.type(), key)
        self.assertIsNone(item)

    def test_table_create(self):
        dummy_table = Constants.TEST
        graph = GraphStore()
        self.assertFalse(graph.delete_table(dummy_table))
        self.assertFalse(graph.table_exists(dummy_table))
        graph.create_table(dummy_table)
        self.assertTrue(graph.table_exists(dummy_table))
        graph.delete_table(dummy_table)
        self.assertFalse(graph.table_exists(dummy_table))
