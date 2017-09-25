
class Constants(object):
    """Defined Constants."""
    PLATFORM_NAME = '10sai'
    DB_MODULE_NAME = 'dynamodb'
    DB_ITEM_KEY = 'Item'
    DB_KEY_KEY = 'key'
    LOCAL_IP = '127.0.0.1'
    LOCAL_DB_PORT = 8088

    # The following are build commands
    PIP_CMD = 'pip install -r requirements.pip'
    LOCAL_DB_CMD = 'cd local_db && DB_PORT={0} docker-compose up -d'.format(
        LOCAL_DB_PORT)
    LOCAL_DB_DOWN_CMD = 'cd local_db && DB_PORT={0} docker-compose down'.format(
        LOCAL_DB_PORT)
    TEST_CMD = 'nosetests --with-coverage --cover-package=common ' \
               '--cover-min-percentage=80'
    LINT_CMD = 'pyflakes *.py && pylint *.py'
    LOCAL_DB_RUNNING_CMD = 'docker ps --format "{{.Names}}" ' \
                           '| grep local_dynamo_db'

    DEFAULT_PRIORITY = 0
    DEFAULT_CONFIDENCE = 50.0
    PAGE_START = 0
    EMPTY = ''
    UNDEFINED = 'undefined'
    ASSERT_FACT = 'assert_fact'
    ADD_FACT = 'add_fact'
    UPDATE_FACT = 'update_fact'
    DELETE_FACT = 'delete_fact'
    ADD_RULE = 'add_rule'
    UPDATE_RULE = 'update_rule'
    DELETE_RULE = 'delete_rule'
    CHANGE_MODE = 'change_mode'
    RUN_INFERENCE = 'run_inference'
    INFERENCE_STARTED = 'inference_started'
    RULE_FIRED = 'rule_fired'
    FACT_ASSERTED = 'fact_asserted'
    ASK_QUESTION = 'ask_question'
    ANSWER_QUESTION = 'answer_question'
    EXECUTE_CODE = 'execute_code'
    FACT_KEY = 'fact'
    FACTS_KEY = 'facts'
    RULE_KEY = 'rule'
    BODY_KEY = 'body'
    ACTION_KEY = 'action'
    ACTIONS_KEY = 'actions'
    ACTION_TYPE_KEY = 'action_type'
    TYPE_KEY = 'type'
    MODE_KEY = 'mode'
    NAME_KEY = 'name'
    GRAPH_KEY = 'graph'
    PRIORITY_KEY = 'priority'
    CONFIDENCE_KEY = 'confidence'
    ACTIVATED_KEY = 'activated'
    TIME_KEY = 'time'
    FACT_TYPE_KEY = 'fact_type'
    NORMAL = 'normal'
    ADVANCED = 'advanced'
    EXPERT = 'expert'
    TRAINING = 'training'
    STATEMENT = 'statement'
    MATH = 'math'
    SET_VARIABLE = 'set_variable'
    DEFINITION = 'definition'
