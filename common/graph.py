"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from schematics.models import Model
from schematics.types import StringType, ListType, IntType, \
    BooleanType, DecimalType
from redis import Redis
from common.constants import Constants


class Entity(Model):
    name = StringType(required=True)


class Fact(Entity):
    activated = BooleanType(default=False)
    confidence = DecimalType(default=Constants.DEFAULT_CONFIDENCE)


class Action(Entity):
    action = StringType(required=True)


class Rule(Entity):
    priority = IntType(default=Constants.DEFAULT_PRIORITY)
    facts = ListType(StringType)
    actions = ListType(StringType)


class Knowledge(object):
    """ Knowledge class for managing knowledge. """
    def __init__(self,  client=Redis()):
        """ Initialize. """
        self.client = client

    def assert_fact(self, fact):
        """ Assert a new fact as being known knowledge. """
        key = Constants.get_key(Constants.FACTS_COLLECTION, fact.name)
        self.client.set(key, fact)

    def retract_fact(self, fact):
        """ Retract the fact as being now unknown. """
        key = Constants.get_key(Constants.FACTS_COLLECTION, fact.name)
        self.client.delete(key)

    def fact_exists(self, fact):
        """ Check to see if fact exists. """
        key = Constants.get_key(Constants.FACTS_COLLECTION, fact.name)
        return self.client.get(key) is not None

    def add_rule(self, rule):
        """ Add a new rule and create graph to facts. """
        key = Constants.get_key(Constants.RULES_COLLECTION, rule.name)
        if rule.facts:
            for fact in rule.facts:
                fact_key = Constants.get_key(Constants.RULE_TO_FACTS, key)
                self.client.rpush(fact_key, fact)
        if rule.actions:
            for action in rule.actions:
                action_key = Constants.get_key(Constants.RULE_TO_ACTIONS, key)
                self.client.rpush(action_key, action)
        self.client.set(key, rule)

    def rule_exists(self, rule):
        """ Check to see if rule exists. """
        key = Constants.get_key(Constants.RULES_COLLECTION, rule.name)
        return self.client.get(key) is not None

    def remove_rule(self, rule):
        """ Remove a rule from the knowledge tree. """
        key = Constants.get_key(Constants.RULES_COLLECTION, rule.name)
        self.client.delete(key)
        fact_key = Constants.get_key(Constants.RULE_TO_FACTS, key)
        self.client.delete(fact_key)
        action_key = Constants.get_key(Constants.RULE_TO_ACTIONS, key)
        self.client.delete(action_key)

    def process_agenda(self):
        pass
