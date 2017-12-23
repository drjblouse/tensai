import sys
import logging
from datetime import datetime
from schematics.models import Model
from schematics.types import StringType, IntType, \
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
    def exception(ex):
        """Exception logging wrapper."""
        logger = logging.getLogger(__name__)
        logger.propagate = LOG_ENABLED
        if LOG_EXCEPTIONS:
            exc_obj, filename, line, lineno = Logger.get_exception_details()
            exception_detail = Constants.EXCEPTION_DETAIL.format(
                filename, lineno, line.strip(), exc_obj)
            print(ex)
            print(exception_detail)
            logger.exception(ex)
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


def log_exceptions(func):
    """
      A decorator that wraps the passed in function and logs
      exceptions should one occur
      """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, Exception) as ex:
            err = "There was an exception in {0}".format(func.__name__)
            Logger.debug(err)
            Logger.exception(ex)
            # re-raise the exception
            raise
    return wrapper


class Entity(Model):
    def __init__(self, collection, name, store=Redis()):
        super().__init__()
        self.collection = collection
        self.store = store
        self.name = name

    @classmethod
    @log_exceptions
    def read(cls, key, store=Redis()):
        return store.get(key)

    @log_exceptions
    def save(self):
        key = Constants.get_key(self.collection, self.name)
        self.store.set(key, self)

    @log_exceptions
    def delete(self):
        key = Constants.get_key(self.collection, self.name)
        self.store.delete(key)

    name = StringType(required=True)
    created = DateTimeType(default=datetime.now())
    updated = DateTimeType(default=datetime.now())


class Fact(Entity):
    @log_exceptions
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.FACTS_COLLECTION, name, store)
    activated = BooleanType(default=False)
    confidence = DecimalType(default=Constants.DEFAULT_CONFIDENCE)


class Action(Entity):
    @log_exceptions
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.ACTIONS_COLLECTION, name, store)
    action = StringType(required=True)


class Rule(Entity):
    @log_exceptions
    def __init__(self, name, store=Redis()):
        super().__init__(Constants.RULES_COLLECTION, name, store)
    priority = IntType(default=Constants.DEFAULT_PRIORITY)


class Knowledge(object):
    """ Knowledge class for managing knowledge. """
    @log_exceptions
    def __init__(self,  client=Redis()):
        """ Initialize. """
        self.client = client

    @staticmethod
    @log_exceptions
    def assert_fact(fact):
        """ Assert a new fact as being known knowledge. """
        fact.save()

    @staticmethod
    @log_exceptions
    def retract_fact(fact):
        """ Retract the fact as being now unknown. """
        fact.delete()

    @log_exceptions
    def fact_exists(self, fact):
        """ Check to see if fact exists. """
        key = Constants.get_key(Constants.FACTS_COLLECTION, fact.name)
        return Fact.read(key, self.client) is not None

    @staticmethod
    @log_exceptions
    def add_rule(rule):
        """ Add a new rule and create graph to facts. """
        rule.save()

    @log_exceptions
    def rule_exists(self, rule):
        """ Check to see if rule exists. """
        key = Constants.get_key(Constants.RULES_COLLECTION, rule.name)
        return Rule.read(key, self.client) is not None

    @staticmethod
    @log_exceptions
    def remove_rule(rule):
        """ Remove a rule from the knowledge tree. """
        rule.delete()
