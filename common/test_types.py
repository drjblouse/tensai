from unittest import TestCase, skipIf
from pymongo import MongoClient, errors
from common.types import Fact, Action
from common.constants import Constants, Messages


def check_local_db():
    """ Check if the local db is running. """
    try:
        client = MongoClient(serverSelectionTimeoutMS=1)
        client.server_info()
        return True
    except errors.ServerSelectionTimeoutError:
        return False


TEST_KEY = 'test'
DUMMY_VALUE = 'fact_value'


@skipIf(not check_local_db(), reason=Messages.NO_LOCAL_DB)
class TestTypes(TestCase):
    def setUp(self):
        Fact().purge()
        Action().purge()

    def test_fact_creation(self):
        activated = False
        keys = list()
        for x in range(100):
            activated = not activated
            fact = Fact(value=DUMMY_VALUE+str(x), activated=activated)
            keys.append(fact.save())
        self.assertEqual(Fact().item_count(), 100)
        self.assertEqual(Fact().get(keys[5])[Constants.VALUE_KEY], DUMMY_VALUE+str(5))

    def test_action_creation(self):
        action = Action(test=DUMMY_VALUE)
        action[Constants.PRIORITY_KEY] = 80
        key = action.save()
        read_action = Action().get(key)
        self.assertEqual(read_action[TEST_KEY], action[TEST_KEY])
        self.assertEqual(read_action[Constants.PRIORITY_KEY], action[Constants.PRIORITY_KEY])
        self.assertEqual(Action().item_count(), 1)
        Action().delete(key)
        self.assertEqual(Action().item_count(), 0)
