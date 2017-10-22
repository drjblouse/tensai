from unittest import TestCase
from unittest.mock import MagicMock
from common.graph import Knowledge, Rule, Fact
from common.constants import Constants


FACT1_NAME = 'fact 1'
FACT2_NAME = 'fact 2'
RULE_NAME = 'test-rule'
ACTION_NAME = 'print test'
TEST_FACT1 = {Constants.NAME: FACT1_NAME}
TEST_FACT2 = {Constants.NAME: FACT2_NAME}
TEST_RULE = {Constants.NAME: RULE_NAME,
             Constants.FACTS: [FACT1_NAME, FACT2_NAME],
             Constants.ACTIONS: [ACTION_NAME]}
test_rule_key = Constants.get_key(Constants.RULES_COLLECTION, RULE_NAME)
test_rule_fact_key = Constants.get_key(Constants.RULE_TO_FACTS, test_rule_key)
test_rule_action_key = Constants.get_key(Constants.RULE_TO_ACTIONS, test_rule_key)
test_fact1_key = Constants.get_key(Constants.FACTS_COLLECTION, FACT1_NAME)
test_fact2_key = Constants.get_key(Constants.FACTS_COLLECTION, FACT2_NAME)


class TestGraph(TestCase):

    def test_rule(self):
        mock = MagicMock()
        knowledge = Knowledge(mock)
        knowledge.add_rule(Rule(TEST_RULE))
        self.assertTrue(knowledge.rule_exists(Rule(TEST_RULE)))
        mock.set.assert_called_once_with(test_rule_key, Rule(TEST_RULE))
        mock.rpush.assert_any_call(test_rule_fact_key, TEST_RULE[Constants.FACTS][0])
        mock.rpush.assert_any_call(test_rule_fact_key, TEST_RULE[Constants.FACTS][1])
        mock.rpush.assert_any_call(test_rule_action_key, TEST_RULE[Constants.ACTIONS][0])
        knowledge.remove_rule(Rule(TEST_RULE))
        mock.delete.assert_any_call(test_rule_key)
        mock.delete.assert_any_call(test_rule_fact_key)
        mock.delete.assert_any_call(test_rule_action_key)

    def test_fact(self):
        mock = MagicMock()
        knowledge = Knowledge(mock)
        knowledge.assert_fact(Fact(TEST_FACT1))
        self.assertTrue(knowledge.fact_exists(Fact(TEST_FACT1)))
        knowledge.retract_fact(Fact(TEST_FACT1))
        mock.delete.assert_called_once_with(test_fact1_key)
        mock.get.return_value = None
        self.assertFalse(knowledge.fact_exists(Fact(TEST_FACT1)))
