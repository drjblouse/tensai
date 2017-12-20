from unittest import TestCase
from unittest.mock import MagicMock
from common.types import Fact, Action
# from common.constants import Constants
from common.graph import Graph

TEST_RULE = 'dummy rule'
TEST_FACT = 'dummy fact'
TEST_ACTION = 'dummy action'


class TestGraph(TestCase):
    def test_graph_insert(self):
        mock = MagicMock()
        graph = Graph(mock)
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
