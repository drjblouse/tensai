"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from neo4jrestclient.client import GraphDatabase
from common.constants import Constants


class Graph(object):
    def __init__(self, graph=None):
        self.graph = graph or GraphDatabase(Constants.GRAPH_URL)
        self.facts = self.graph.labels.create(Constants.FACTS)
        self.rules = self.graph.labels.create(Constants.RULES)
        self.actions = self.graph.labels.create(Constants.ACTIONS)

    def create_rule(self, rule_id, rule_name, facts, actions,
                    confidence=Constants.DEFAULT_CONFIDENCE,
                    priority=Constants.DEFAULT_PRIORITY):
        fact_nodes = list()
        action_nodes = list()
        for fact in facts:
            fact_nodes.append(self.facts.create(name=fact.name))
        for action in actions:
            action_nodes.append(self.actions.create(name=action.name))
        rule = self.rules.create(id=rule_id, name=rule_name, confidence=confidence, priority=priority)
        for fact in fact_nodes:
            fact.relationships.create(Constants.FACT_RULE_RELATION, rule)
        for action in action_nodes:
            rule.relationships.create(Constants.RULE_ACTION_RELATION, action)

