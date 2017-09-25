""" Tests for the local dynamo db. """
# -*- coding: utf-8 -*-
import uuid
from unittest import TestCase, skipIf
from schematics.exceptions import DataError
from common.types import PersistentType, Fact, Rule, Action
from common.constants import check_local_db, Constants, Messages


class TestTypeHelpers(TestCase):
    """ Test fixture for testing general local dynamo operations. """

    def test_simple_type(self):
        rule = Rule()
        self.assertEqual(rule.type(), Constants.RULES)

    def test_plural(self):
        company = Company()
        self.assertEqual(company.type(), Constants.COMPANIES)

    def test_fact(self):
        fact = Fact()
        with self.assertRaises(expected_exception=DataError):
            self.assertIsNone(fact.validate())
        fact.name = Constants.UNDEFINED
        self.assertFalse(fact.activated)
        self.assertIsNone(fact.validate())
        print(type(fact.key))
        self.assertTrue(isinstance(fact.key, uuid.UUID))


@skipIf(not check_local_db(), Messages.NO_LOCAL_DB)
class TestTypeModifications(TestCase):
    """ Test fixture for testing general local dynamo operations on types. """

    def test_fact_type(self):
        self.general_save_check(Fact(), Fact())

    def test_rule_type(self):
        self.general_save_check(Rule(), Rule())

    def test_action_type(self):
        self.general_save_check(Action(), Action())

    def general_save_check(self, type1, type2):
        type1.create_table()
        type1.name = Constants.UNDEFINED
        key = type1.put_type()
        self.assertIsNotNone(key)
        type2.key = key
        self.assertIsNotNone(type2.get_type())
        type2.key = type2.name
        self.assertIsNone(type2.get_type())


class Company(PersistentType):
    pass
