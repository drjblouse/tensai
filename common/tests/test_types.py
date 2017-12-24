from unittest.mock import MagicMock
from common.types import Knowledge, Rule, Fact, Action, Logger
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


def test_logger():
    mock = MagicMock()
    mock.tb_frame.f_code.co_filename = FACT1_NAME
    mock.tb_lineno = 111
    logger = Logger
    logger.debug(FACT1_NAME)
    logger.exception(FACT1_NAME)
    exc_obj, filename, line, lineno = logger.get_exception_details(
        lambda: (FACT1_NAME, FACT1_NAME, mock))
    assert(exc_obj == FACT1_NAME and filename == FACT1_NAME)


def test_rule():
    mock = MagicMock()
    knowledge = Knowledge(mock)
    knowledge.add_rule(Rule(TEST_RULE, mock))
    assert(knowledge.rule_exists(Rule(TEST_RULE, mock)))
    mock.set.assert_called_once()
    knowledge.remove_rule(Rule(TEST_RULE, mock))


def test_action():
    mock = MagicMock()
    action = Action(TEST_FACT1, mock)
    action.save()
    mock.set.assert_called_once()
    action.delete()
    mock.delete.assert_called_once()


def test_fact():
    mock = MagicMock()
    knowledge = Knowledge(mock)
    knowledge.assert_fact(Fact(TEST_FACT1, mock))
    assert(knowledge.fact_exists(Fact(TEST_FACT1, mock)))
    knowledge.retract_fact(Fact(TEST_FACT1, mock))
    mock.delete.assert_called_once()
    mock.get.return_value = None
    assert(not knowledge.fact_exists(Fact(TEST_FACT1, mock)))
