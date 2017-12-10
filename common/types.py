import sys
import logging
from datetime import datetime
from schematics.models import Model
from schematics.types import StringType, ListType, IntType, \
    BooleanType, DecimalType, DateTimeType
from redis import Redis
from linecache import getline, checkcache
from common.constants import Constants

LOG_ENABLED = True
LOG_EXCEPTIONS = True
LOG_QUERIES = True


class Logger:
    """Wrapper for controlling logging."""
    @staticmethod
    def debug(message):
        """Debug logging wrapper."""
        logger = logging.getLogger(__name__)
        logger.propagate = LOG_ENABLED
        if LOG_ENABLED:
            print(message)
            logger.debug(message)

    @staticmethod
    def exception(exception):
        """Exception logging wrapper."""
        logger = logging.getLogger(__name__)
        logger.propagate = LOG_ENABLED
        if LOG_EXCEPTIONS:
            exc_obj, filename, line, lineno = Logger.get_exception_details()
            exception_detail = Constants.EXCEPTION_DETAIL.format(
                filename, lineno, line.strip(), exc_obj)
            print(exception)
            print(exception_detail)
            logger.exception(exception)
            logger.exception(exception_detail)

    @staticmethod
    def get_exception_details(exc_detail=sys.exc_info):
        exc_type, exc_obj, tb = exc_detail()
        if tb:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            checkcache(filename)
            line = getline(filename, lineno, f.f_globals)
            return exc_obj, filename, line, lineno
        return exc_obj, Constants.UNKNOWN, Constants.UNKNOWN, Constants.NO_LINE


class Entity(Model):
    def __init__(self, collection, name, store=Redis()):
        super().__init__()
        self.collection = collection
        self.store = store
        self.name = name

    @classmethod
    def read(cls, key, store=Redis()):
        return store.get(key)

    def save(self):
        key = Constants.get_key(self.collection, self.name)
        self.store.set(key, self)

    def delete(self):
        key = Constants.get_key(self.collection, self.name)
        self.store.delete(key)

    name = StringType(required=True)
    created = DateTimeType(default=datetime.now())
    updated = DateTimeType(default=datetime.now())


class Fact(Entity):
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.FACTS_COLLECTION, name, store)
    activated = BooleanType(default=False)
    confidence = DecimalType(default=Constants.DEFAULT_CONFIDENCE)


class Action(Entity):
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.ACTIONS_COLLECTION, name, store)
    action = StringType(required=True)


class Rule(Entity):
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.RULES_COLLECTION, name, store)
    priority = IntType(default=Constants.DEFAULT_PRIORITY)


class Knowledge(object):
    """ Knowledge class for managing knowledge. """
    def __init__(self,  client=Redis()):
        """ Initialize. """
        self.client = client

    @staticmethod
    def assert_fact(fact):
        """ Assert a new fact as being known knowledge. """
        fact.save()

    @staticmethod
    def retract_fact(fact):
        """ Retract the fact as being now unknown. """
        fact.delete()

    def fact_exists(self, fact):
        """ Check to see if fact exists. """
        key = Constants.get_key(Constants.FACTS_COLLECTION, fact.name)
        return Fact.read(key, self.client) is not None

    @staticmethod
    def add_rule(rule):
        """ Add a new rule and create graph to facts. """
        rule.save()

    def rule_exists(self, rule):
        """ Check to see if rule exists. """
        key = Constants.get_key(Constants.RULES_COLLECTION, rule.name)
        return Rule.read(key, self.client) is not None

    @staticmethod
    def remove_rule(rule):
        """ Remove a rule from the knowledge tree. """
        rule.delete()
