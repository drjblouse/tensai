"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from neomodel import StructuredNode, StringProperty, \
    RelationshipTo, RelationshipFrom, config, IntegerProperty
from common.constants import Constants


config.DATABASE_URL = Constants.GRAPH_URL


class BaseNode(StructuredNode):
    @classmethod
    def category(cls):
        pass
    id = StringProperty(unique_index=True)
    confidence = IntegerProperty(default=Constants.DEFAULT_CONFIDENCE)
    priority = IntegerProperty(default=Constants.DEFAULT_PRIORITY)


class FactNode(BaseNode):
    rules = RelationshipTo(Constants.RULE_NODE, Constants.FACT_RULE_RELATION)


class ActionNode(BaseNode):
    rules = RelationshipFrom(
        Constants.RULE_NODE, Constants.FACT_RULE_RELATION)


class RuleNode(BaseNode):
    facts = RelationshipFrom(
        Constants.FACT_NODE, Constants.FACT_RULE_RELATION)
    actions = RelationshipTo(
        Constants.ACTION_NODE, Constants.RULE_ACTION_RELATION)


class Graph(object):
    def __init__(self, graph):
        self.graph = graph

    def create_rule(self, rule_id, facts, actions,
                    confidence=Constants.DEFAULT_CONFIDENCE,
                    priority=Constants.DEFAULT_PRIORITY):
        rule = RuleNode(id=rule_id, confidence=confidence, priority=priority)
        # for fact in facts:
        #     rule.facts.connect(fact)
        # for action in actions:
        #     rule.actions.connect(action)
