from invoke import run


def check_local_db():
    """ Check if the local db is running. """
    try:
        return run(Constants.LOCAL_DB_RUNNING_CMD).ok
    except(ValueError, Exception):
        return False


class Messages(object):
    """ Defined Messages. """
    NO_LOCAL_DB = 'Local DB not running.'


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
    NAME = 'name'
    TEST = 'test'
    RULES = 'rules'
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
