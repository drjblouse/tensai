"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from functools import lru_cache
from itertools import chain
from neo4jrestclient.client import GraphDatabase
from common.constants import Constants, Queries
from common.types import log_exceptions


class GraphHelper(object):
    @log_exceptions
    def __init__(self, graph, facts, actions, rules):
        self.graph = graph
        self.facts = facts
        self.actions = actions
        self.rules = rules

    @lru_cache(maxsize=32)
    @log_exceptions
    def execute_query(self, query):
        result = self.graph.query(query, data_contents=True)
        return list(chain.from_iterable(result.rows))

    @staticmethod
    @log_exceptions
    def create_action_relations(action_nodes, rule):
        for action in action_nodes:
            rule.relationships.create(Constants.RULE_ACTION_RELATION, action)

    @staticmethod
    @log_exceptions
    def create_fact_relations(fact_nodes, rule):
        for fact in fact_nodes:
            fact.relationships.create(Constants.FACT_RULE_RELATION, rule)

    @log_exceptions
    def get_facts(self, facts):
        fact_nodes = list()
        for fact in facts:
            fact_nodes.append(self.facts.create(name=fact.name))
        return fact_nodes

    @log_exceptions
    def get_actions(self, actions):
        action_nodes = list()
        for action in actions:
            action_nodes.append(self.actions.create(name=action.name))
        return action_nodes


class Graph(object):
    @log_exceptions
    def __init__(self, graph=None, helper=None):
        self.graph = graph or GraphDatabase(Constants.GRAPH_URL)
        self.facts = self.graph.labels.create(Constants.FACTS)
        self.rules = self.graph.labels.create(Constants.RULES)
        self.actions = self.graph.labels.create(Constants.ACTIONS)
        self.helper = helper or GraphHelper(
            self.graph, self.facts, self.actions, self.rules)

    @log_exceptions
    def get_rule_count(self):
        return len(self.rules.get())

    @log_exceptions
    def get_fact_count(self):
        return len(self.facts.get())

    @log_exceptions
    def get_action_count(self):
        return len(self.actions.get())

    @log_exceptions
    def purge_graph(self):
        self.purge_rules()
        self.purge_facts()
        self.purge_actions()

    @log_exceptions
    def purge_rules(self):
        for rule in self.rules.get():
            self.delete_node(rule)

    @log_exceptions
    def purge_facts(self):
        for fact in self.facts.get():
            self.delete_node(fact)

    @log_exceptions
    def purge_actions(self):
        for action in self.actions.get():
            self.delete_node(action)

    @log_exceptions
    def delete_node(self, node):
        self.remove_relationships(node)
        node.delete()

    @staticmethod
    @log_exceptions
    def remove_relationships(rule):
        for relation in rule.relationships.all():
            relation.delete()

    @log_exceptions
    def create_rule(self, rule_id, rule_name, facts, actions,
                    confidence=Constants.DEFAULT_CONFIDENCE,
                    priority=Constants.DEFAULT_PRIORITY):
        fact_nodes = self.helper.get_facts(facts)
        action_nodes = self.helper.get_actions(actions)
        rule = self.rules.create(id=rule_id, name=rule_name, confidence=confidence, priority=priority)
        self.helper.create_fact_relations(fact_nodes, rule)
        self.helper.create_action_relations(action_nodes, rule)
        return rule

    @lru_cache(maxsize=32)
    @log_exceptions
    def get_fact(self, fact_name):
        return self.graph.query(Queries.GET_FACT_QUERY.format(name=fact_name),
                                data_contents=True)

    @lru_cache(maxsize=32)
    @log_exceptions
    def get_rules_by_fact(self, fact_name):
        return self.helper.execute_query(
            Queries.GET_FACT_RULES.format(name=fact_name))

    @lru_cache(maxsize=32)
    @log_exceptions
    def get_rule_actions(self, rule_id):
        return self.helper.execute_query(
            Queries.GET_RULE_ACTIONS.format(name=rule_id))
