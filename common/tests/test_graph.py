from os import system
from unittest.mock import MagicMock
from pytest import raises
from common.constants import Constants
from common.types import Fact, Action
from common.graph import Graph


def graph_is_up(runner=system):
    output = runner('ps aux | grep neo | grep -v grep')
    print(type(output))
    if output == 0:
        return True
    else:
        return False


TEST_RULE = 'dummy rule'
TEST_RULE2 = 'dummy rule 2'
TEST_FACT = 'dummy fact'
TEST_ACTION = 'dummy action'
DEMO_RULE = 'account access not working'
DEMO_FACT1 = 'account is NOT locked out'
DEMO_FACT2 = 'invalid password attempt spotted'
DEMO_ACTION = 'ask user if password is forgotten'


def test_graph_is_up():
    mock = MagicMock()
    mock.return_value = 0
    assert(graph_is_up(mock))


def test_graph_is_down():
    mock = MagicMock()
    mock.return_value = 1
    assert(not graph_is_up(mock))


def test_graph_insert():
    mock = MagicMock()
    graph = Graph(mock)
    assert(graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)]) is not None)


def test_graph_insert_error():
    mock = MagicMock()
    mock.get_facts.side_effect = Exception
    graph = Graph(mock, mock)
    with raises(Exception):
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])


def test_graph_counts():
    mock = MagicMock()
    mock.labels.create.return_value = mock
    mock.get.return_value = [mock, mock]
    mock.relationships.all.return_value = [mock, mock]
    graph = Graph(mock)
    assert(graph.purge_graph() is None)
    assert(graph.get_rule_count() == 2)
    assert(graph.get_fact_count() == 2)
    assert(graph.get_action_count() == 2)


def test_get_fact():
    mock = MagicMock()
    mock.labels.create.return_value = mock
    mock.query.return_value = mock
    graph = Graph(mock)
    assert(graph.get_fact(TEST_FACT) == mock)
    assert(graph.get_fact(TEST_FACT) is not None)


def test_get_rules_by_fact():
    mock = MagicMock()
    mock.labels.create.return_value = mock
    mock.query.return_value = mock
    mock.rows = [[mock], [mock], [mock]]
    graph = Graph(mock)
    assert(len(graph.get_rules_by_fact(TEST_FACT)) == 3)
    assert (len(graph.get_rule_actions(TEST_RULE)) == 3)


def test_real_graph():
    if graph_is_up():
        graph = Graph()
        graph.purge_graph()
        print(graph.get_rule_count())
        assert(graph.get_rule_count() == 0)
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
        assert(graph.get_rule_count() == 1)
        assert(graph.get_fact_count() == 1)
        assert(graph.get_action_count() == 1)


def test_demo_graph():
    if graph_is_up():
        graph = Graph()
        graph.purge_graph()
        print(graph.get_rule_count())
        assert(graph.get_rule_count() == 0)
        graph.create_rule(DEMO_RULE, DEMO_RULE, [Fact(DEMO_FACT1), Fact(DEMO_FACT2)], [Action(DEMO_ACTION)])
        assert(graph.get_rule_count() == 1)
        assert(graph.get_fact_count() == 2)
        assert(graph.get_action_count() == 1)


def test_graph_fact_rules():
    if graph_is_up():
        graph = Graph()
        graph.purge_graph()
        graph.create_rule(TEST_RULE, TEST_RULE, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
        graph.create_rule(TEST_RULE2, TEST_RULE2, [Fact(TEST_FACT)], [Action(TEST_ACTION)])
        assert(graph.get_rule_count() == 2)
        assert(graph.get_fact_count() == 2)
        assert(graph.get_action_count() == 2)
        assert(graph.get_fact(TEST_FACT) is not None)
        assert(len(graph.get_rules_by_fact(TEST_FACT)) == 2)
        assert(TEST_RULE in graph.get_rules_by_fact(TEST_FACT)[0][Constants.NAME])
        assert (TEST_ACTION in graph.get_rule_actions(TEST_RULE)[0][Constants.NAME])
