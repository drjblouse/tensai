from unittest import TestCase
from unittest.mock import MagicMock
# from common.types import Knowledge, Rule, Fact
# from common.constants import Constants
from common.graph import Graph, ActionNode, FactNode

TEST_RULE = 'dummy rule'
TEST_FACT = 'dummy fact'
TEST_ACTION = 'dummy action'


class TestGraph(TestCase):
    def test_graph_insert(self):
        mock = MagicMock()
        graph = Graph(mock)
        graph.create_rule(TEST_RULE, [FactNode(id=TEST_FACT)], [ActionNode(id=TEST_ACTION)])
