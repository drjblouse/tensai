from unittest import TestCase, skipIf
from unittest.mock import MagicMock

from common.constants import Constants
from common.types import Fact, Action
from common.graph import Graph
from invoke import run

TEST_RULE = 'dummy rule'
TEST_FACT = 'dummy fact'
TEST_ACTION = 'dummy action'


def graph_is_down():
    try:
        result = run('wget localhost:7474 --timeout 05 -O - 2>/dev/null > /dev/null')
        return not result.ok
    except (ValueError, Exception):
        return True


class TestGraph(TestCase):
    def test_graph_insert(self):
        mock = MagicMock()
        graph = Graph(mock)
        self.assertIsNotNone(
            graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)]))

    def test_graph_insert_error(self):
        mock = MagicMock()
        mock.get_facts.side_effect = Exception
        graph = Graph(mock, mock)
        with self.assertRaises(Exception):
            graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])

    def test_graph_counts(self):
        mock = MagicMock()
        mock.labels.create.return_value = mock
        mock.get.return_value = [mock, mock]
        mock.relationships.all.return_value = [mock, mock]
        graph = Graph(mock)
        self.assertIsNone(graph.purge_graph())
        self.assertEqual(graph.get_rule_count(), 2)
        self.assertEqual(graph.get_fact_count(), 2)
        self.assertEqual(graph.get_action_count(), 2)

    def test_get_fact(self):
        mock = MagicMock()
        mock.labels.create.return_value = mock
        mock.query.return_value = mock
        graph = Graph(mock)
        self.assertIs(graph.get_fact(TEST_FACT), mock)
        self.assertIsNotNone(graph.get_fact(TEST_FACT))

    def test_get_rules_by_fact(self):
        mock = MagicMock()
        mock.labels.create.return_value = mock
        mock.query.return_value = mock
        mock.rows = [[mock], [mock], [mock]]
        graph = Graph(mock)
        self.assertIs(len(graph.get_rules_by_fact(TEST_FACT)), 3)

    @skipIf(graph_is_down(), 'Graph is not running so skipping...')
    def test_real_graph(self):
        graph = Graph()
        graph.purge_graph()
        print(graph.get_rule_count())
        self.assertEqual(graph.get_rule_count(), 0)
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
        self.assertEqual(graph.get_rule_count(), 1)
        self.assertEqual(graph.get_fact_count(), 1)
        self.assertEqual(graph.get_action_count(), 1)

    @skipIf(graph_is_down(), 'Graph is not running so skipping...')
    def test_graph_fact_rules(self):
        graph = Graph()
        graph.purge_graph()
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
        self.assertEqual(graph.get_rule_count(), 1)
        self.assertEqual(graph.get_fact_count(), 1)
        self.assertEqual(graph.get_action_count(), 1)
        self.assertIsNotNone(graph.get_fact(TEST_FACT))
        self.assertIs(len(graph.get_rules_by_fact(TEST_FACT)), 1)
        self.assertEqual(graph.get_rules_by_fact(TEST_FACT)[0][Constants.NAME], TEST_RULE)
