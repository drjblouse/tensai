"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from common.constants import Constants


class KnowledgeItem(object):
    def __init__(self, collection, client=MongoClient()):
        """ Create the base type data. """
        self._client = client
        self.db = self._client.tensai
        self.collection = self.db[collection]
        self.doc = dict()
        created = datetime.now().strftime(Constants.DATE_FORMAT)
        self.doc[Constants.CREATED_KEY] = created
        self.doc[Constants.UPDATED_KEY] = created

    def __getitem__(self, k):
        """ Get an element from the document. """
        return self.doc[k]

    def __setitem__(self, k, v):
        """ Set an element in the document. """
        self.doc[k] = v

    def item_count(self):
        return self.collection.count()

    def save(self):
        self.doc[Constants.UPDATED_KEY] = datetime.now().strftime(Constants.DATE_FORMAT)
        return self.collection.insert_one(self.doc).inserted_id

    def get(self, object_id):
        return self.collection.find_one({Constants.ID: ObjectId(object_id)})

    def delete(self, object_id):
        self.collection.delete_one({Constants.ID: ObjectId(object_id)})

    def purge(self):
        self.collection.drop()


class KnowledgeItems(object):
    def __init__(self):
        self.Items = [KnowledgeItems.Fact,
                      KnowledgeItems.Rule,
                      KnowledgeItems.Action,
                      KnowledgeItems.Agenda]

    class Fact(KnowledgeItem):
        """ Fact type. """
        def __init__(self, client=MongoClient(), **kwargs):
            """ Initializer. """
            super().__init__(Constants.FACTS_COLLECTION, client)
            self.doc.update(kwargs)

    class Action(KnowledgeItem):
        """ Action type. """
        def __init__(self, client=MongoClient(), **kwargs):
            """ Initializer. """
            super().__init__(Constants.ACTIONS_COLLECTION, client)
            self.doc.update(kwargs)

    class Rule(KnowledgeItem):
        """ Rule type. """
        def __init__(self, client=MongoClient(), **kwargs):
            """ Initializer. """
            super().__init__(Constants.RULES_COLLECTION, client)
            self.doc.update(kwargs)

    class Agenda(KnowledgeItem):
        """ Agenda type. """
        def __init__(self, client=MongoClient(), **kwargs):
            """ Initializer. """
            super().__init__(Constants.AGENDA_COLLECTION, client)
            self.doc.update(kwargs)
