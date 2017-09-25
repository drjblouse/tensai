"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from inflect import engine
from common.constants import Constants
from common.graph import GraphStore
from schematics.models import Model
from schematics import types as fields


class PersistentType(Model):
    """ Base type for all other types. """
    key = fields.UUIDType(required=True, default=uuid.uuid4().hex)
    created = fields.DateTimeType(default=datetime.now())
    updated = fields.DateTimeType(default=datetime.now())

    def type(self):
        """ Default type initializer. """
        return engine().plural(type(self).__name__.lower(), 2)

    def create_table(self, graph=GraphStore()):
        """ Default create table function. """
        graph.create_table(self.type())

    def delete_table(self, graph=GraphStore()):
        """ Default delete table function. """
        graph.delete_table(self.type())

    def put_type(self, graph=GraphStore()):
        """ Default save function. """
        try:
            return graph.put_item(self.type(), self)
        except(ValueError, Exception):
            return None

    def get_type(self, graph=GraphStore()):
        """ Default save function. """
        return graph.get_item(self.type(), self.key)

    def delete_type(self, graph=GraphStore()):
        """ Default save function. """
        return graph.delete_item(self.type(), self.key)


class Fact(PersistentType):
    """This class defines the fact type for solomon."""
    name = fields.StringType(required=True, max_length=150)
    activated = fields.BooleanType(default=False)
    confidence = fields.DecimalType(default=Constants.DEFAULT_CONFIDENCE)
    fact_type = fields.StringType(default=Constants.STATEMENT)


class Action(PersistentType):
    """This class represents the possible actions for the right hand sides."""
    name = fields.StringType(required=True, max_length=150)
    action_type = fields.StringType(default=Constants.UNDEFINED,
                                    max_length=150)
    action = fields.StringType(required=True, max_length=150)
    priority = fields.IntType(default=Constants.DEFAULT_PRIORITY)


class Rule(PersistentType):
    """This class defines the rule type for solomon."""
    name = fields.StringType(required=True, max_length=150)
    priority = fields.IntType(default=Constants.DEFAULT_PRIORITY)
    facts = fields.ListType(fields.ModelType(Fact))
    actions = fields.ListType(fields.ModelType(Action))
