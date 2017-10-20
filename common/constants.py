

class Messages(object):
    """ Defined Messages. """
    NO_LOCAL_DB = 'Local DB not running.'


class Constants(object):
    """Defined Constants."""
    PLATFORM_NAME = '10sai'
    DB_NAME = 'tensai'
    GRAPH_COLLECTION_NAME = 'knowledge'
    USER = 'root'
    PASSWORD = 'pwd'
    LOCAL_IP = '127.0.0.1'
    LOCAL_DB_PORT = 8529
    FACTS_COLLECTION = 'Facts'
    ACTIONS_COLLECTION = 'Actions'
    RULES_COLLECTION = 'Rules'
    KNOWLEDGE_GRAPH = 'Knowledge'

    DEFAULT_PRIORITY = 0
    DEFAULT_CONFIDENCE = 50.0
    PAGE_START = 0
    EMPTY = ''
    ID = '_id'
    FACT = 'fact'
    NAME = 'name'
    TEST = 'test'
    RULES = 'rules'
    DATE_FORMAT = '%m-%d-%Y-%T'
    CREATED_KEY = 'created'
    UPDATED_KEY = 'updated'
    CONFIDENCE_KEY = 'confidence'
    PRIORITY_KEY = 'priority'
    ACTIVATED_KEY = 'activated'
    VALUE_KEY = 'value'
    AQL_INSERT = 'INSERT @doc INTO {collection} LET newDoc = NEW RETURN newDoc'
    COMPANIES = 'companies'
    UNDEFINED = 'undefined'
    ASSERT_FACT = 'assert_fact'
    ADD_FACT = 'add_fact'
    UPDATE_FACT = 'update_fact'
    DELETE_FACT = 'delete_fact'
    ADD_RULE = 'add_rule'
    UPDATE_RULE = 'update_rule'
    DELETE_RULE = 'delete_rule'
    RUN_INFERENCE = 'run_inference'
    INFERENCE_STARTED = 'inference_started'
    RULE_FIRED = 'rule_fired'
    FACT_ASSERTED = 'fact_asserted'
    ASK_QUESTION = 'ask_question'
    ANSWER_QUESTION = 'answer_question'
    EXECUTE_CODE = 'execute_code'
    NORMAL = 'normal'
    ADVANCED = 'advanced'
    EXPERT = 'expert'
    TRAINING = 'training'
    STATEMENT = 'statement'
    MATH = 'math'
    SET_VARIABLE = 'set_variable'
    DEFINITION = 'definition'
