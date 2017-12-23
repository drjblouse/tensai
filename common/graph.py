"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from neo4jrestclient.client import GraphDatabase
from common.constants import Constants
# from common.types import Logger


class GraphHelper(object):
    def __init__(self, facts, actions, rules):
        self.facts = facts
        self.actions = actions
        self.rules = rules

    @staticmethod
    def create_action_relations(action_nodes, rule):
        for action in action_nodes:
            rule.relationships.create(Constants.RULE_ACTION_RELATION, action)

    @staticmethod
    def create_fact_relations(fact_nodes, rule):
        for fact in fact_nodes:
            fact.relationships.create(Constants.FACT_RULE_RELATION, rule)

    def get_facts(self, facts):
        fact_nodes = list()
        for fact in facts:
            fact_nodes.append(self.facts.create(name=fact.name))
        return fact_nodes

    def get_actions(self, actions):
        action_nodes = list()
        for action in actions:
            action_nodes.append(self.actions.create(name=action.name))
        return action_nodes


class Graph(object):
    def __init__(self, graph=None, helper=None):
        self.graph = graph or GraphDatabase(Constants.GRAPH_URL)
        self.facts = self.graph.labels.create(Constants.FACTS)
        self.rules = self.graph.labels.create(Constants.RULES)
        self.actions = self.graph.labels.create(Constants.ACTIONS)
        self.helper = helper or GraphHelper(self.facts, self.actions, self.rules)

    def get_rule_count(self):
        return len(self.rules.get())

    def get_fact_count(self):
        return len(self.facts.get())

    def get_action_count(self):
        return len(self.actions.get())

    def purge_graph(self):
        self.purge_rules()
        self.purge_facts()
        self.purge_actions()

    def purge_rules(self):
        for rule in self.rules.get():
            self.delete_node(rule)

    def purge_facts(self):
        for fact in self.facts.get():
            self.delete_node(fact)

    def purge_actions(self):
        for action in self.actions.get():
            self.delete_node(action)

    def delete_node(self, node):
        self.remove_relationships(node)
        node.delete()

    @staticmethod
    def remove_relationships(rule):
        for relation in rule.relationships.all():
            relation.delete()

    def create_rule(self, rule_id, rule_name, facts, actions,
                    confidence=Constants.DEFAULT_CONFIDENCE,
                    priority=Constants.DEFAULT_PRIORITY):
        fact_nodes = self.helper.get_facts(facts)
        action_nodes = self.helper.get_actions(actions)
        rule = self.rules.create(id=rule_id, name=rule_name, confidence=confidence, priority=priority)
        self.helper.create_fact_relations(fact_nodes, rule)
        self.helper.create_action_relations(action_nodes, rule)
        return rule


