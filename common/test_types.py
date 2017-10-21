from unittest import TestCase, skipIf
from pymongo import MongoClient, errors
from common.types import KnowledgeItems
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
        KnowledgeItems.Fact().purge()
        KnowledgeItems.Action().purge()
        KnowledgeItems.Rule().purge()

    def test_types(self):
        for item in KnowledgeItems().Items:
            self._test_item_type(item)

    def test_fact_creation(self):
        activated = False
        keys = list()
        for x in range(100):
            activated = not activated
            fact = KnowledgeItems.Fact(value=DUMMY_VALUE+str(x), activated=activated)
            keys.append(fact.save())
        self.assertEqual(KnowledgeItems.Fact().item_count(), 100)
        self.assertEqual(KnowledgeItems.Fact().get(keys[5])[Constants.VALUE_KEY], DUMMY_VALUE+str(5))

    def _test_item_type(self, item):
        type_item = item(test=DUMMY_VALUE)
        type_item[Constants.PRIORITY_KEY] = 80
        key = type_item.save()
        read_item = item().get(key)
        self.assertEqual(read_item[TEST_KEY], type_item[TEST_KEY])
        self.assertEqual(read_item[Constants.PRIORITY_KEY], type_item[Constants.PRIORITY_KEY])
        self.assertEqual(item().item_count(), 1)
        item().delete(key)
        self.assertEqual(item().item_count(), 0)
