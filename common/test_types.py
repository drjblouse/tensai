""" Tests for the local dynamo db. """
# -*- coding: utf-8 -*-
import uuid
from unittest import TestCase
from schematics.exceptions import DataError
from common.types import Mode, PersistentType, Fact


class TestTypeHelpers(TestCase):
    """ Test fixture for testing general local dynamo operations. """

    def test_mode_type(self):
        mode = Mode()
        self.assertEqual(mode.type(), 'modes')

    def test_plural(self):
        company = Company()
        self.assertEqual(company.type(), 'companies')

    def test_fact(self):
        fact = Fact()
        with self.assertRaises(expected_exception=DataError):
            self.assertIsNone(fact.validate())
        fact.name = 'Fact name'
        self.assertFalse(fact.activated)
        self.assertIsNone(fact.validate())
        print(type(fact.key))
        self.assertTrue(isinstance(fact.key, uuid.UUID))


class Company(PersistentType):
    pass
