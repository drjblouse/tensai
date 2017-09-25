"""Support types for the 10s ai platform."""
# -*- coding: utf-8 -*-
import uuid
from enum import Enum
from datetime import datetime
from inflect import engine
from common.constants import Constants
from schematics.models import Model
from schematics import types as fields


class Modes(Enum):
    """Enumeration defining mode types."""
    UNDEFINED = 0
    NORMAL = 1
    ADVANCED = 2
    EXPERT = 3
    TRAINING = 4

    def __str__(self):
        """Override string method."""
        return {self.UNDEFINED.value: Constants.UNDEFINED,
                self.NORMAL.value: Constants.NORMAL,
                self.ADVANCED.value: Constants.ADVANCED,
                self.EXPERT.value: Constants.EXPERT,
                self.TRAINING.value: Constants.TRAINING}.\
            get(self.value, Constants.UNDEFINED)


class Actions(Enum):
    """Enumeration defining action types."""
    UNDEFINED = 0
    ASSERT_FACT = 1
    ASK_QUESTION = 2
    EXECUTE_CODE = 3

    def __str__(self):
        """Override string method."""
        return {self.UNDEFINED.value: Constants.UNDEFINED,
                self.ASSERT_FACT.value: Constants.ASSERT_FACT,
                self.ASK_QUESTION.value: Constants.ASK_QUESTION,
                self.EXECUTE_CODE.value: Constants.EXECUTE_CODE}.\
            get(self.value, Constants.UNDEFINED)


class Facts(Enum):
    """Enumeration defining fact types."""
    UNDEFINED = 0
    STATEMENT = 1
    MATH = 2
    EXECUTE_CODE = 3
    SET_VARIABLE = 4
    DEFINITION = 5

    def __str__(self):
        """Override string method."""
        return {self.UNDEFINED.value: Constants.UNDEFINED,
                self.STATEMENT.value: Constants.STATEMENT,
                self.MATH.value: Constants.MATH,
                self.EXECUTE_CODE.value: Constants.EXECUTE_CODE,
                self.SET_VARIABLE.value: Constants.SET_VARIABLE,
                self.DEFINITION.value: Constants.DEFINITION}.\
            get(self.value, Constants.UNDEFINED)


class PersistentType(Model):
    """ Base type for all other types. """
    key = fields.UUIDType(required=True, default=uuid.uuid4().hex)
    created = fields.DateTimeType(default=datetime.now())
    updated = fields.DateTimeType(default=datetime.now())

    def type(self):
        """ Default type initializer. """
        return engine().plural(type(self).__name__.lower(), 2)


class Mode(PersistentType):
    """This class defines the mode type for solomon."""
    mode = fields.StringType(default=str(Modes.UNDEFINED))


class Fact(PersistentType):
    """This class defines the fact type for solomon."""
    name = fields.StringType(required=True, max_length=150)
    activated = fields.BooleanType(default=False)
    confidence = fields.DecimalType(default=Constants.DEFAULT_CONFIDENCE)
    fact_type = fields.StringType(default=str(Facts.STATEMENT))


class Action(PersistentType):
    """This class represents the possible actions for the right hand sides."""
    name = fields.StringType(required=True, max_length=150)
    action_type = fields.StringType(default=str(Actions.UNDEFINED),
                                    max_length=150)
    action = fields.StringType(required=True, max_length=150)
    priority = fields.IntType(default=Constants.DEFAULT_PRIORITY)


class Rule(PersistentType):
    """This class defines the rule type for solomon."""
    name = fields.StringType(required=True, max_length=150)
    priority = fields.IntType(default=Constants.DEFAULT_PRIORITY)
    facts = fields.ListType(fields.ModelType(Fact))
    actions = fields.ListType(fields.ModelType(Action))
