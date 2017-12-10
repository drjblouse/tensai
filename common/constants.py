

class Messages(object):
    """ Defined Messages. """
    NO_LOCAL_DB = 'Local DB not running.'


class Constants(object):
    """Defined Constants."""
    PLATFORM_NAME = '10sai'
    DB_NAME = 'tensai'
    GRAPH_URL = 'bolt://neo4j:test@localhost:7687'
    USER = 'neo4j'
    PASSWORD = 'neo4j'
    CYPHER_LOG = 'CYPHER: {0}'
    EXCEPTION_DETAIL = 'EXCEPTION IN ({0}, LINE {1} "{2}"): {3}'
    FACTS_COLLECTION = 'Facts'
    ACTIONS_COLLECTION = 'Actions'
    RULES_COLLECTION = 'Rules'
    RULE_NODE = 'RuleNode'
    FACT_RULE_RELATION = 'RULE'
    FACT_NODE = 'FactNode'
    ACTION_NODE = 'ActionNode'
    RULE_ACTION_RELATION = 'ACTION'
    AGENDA_COLLECTION = 'Agenda'
    KNOWLEDGE_GRAPH = 'Knowledge'
    RULE_TO_FACTS = 'rule_facts'
    RULE_TO_ACTIONS = 'rule_actions'
    KEY_FORMAT = '{prefix}:{key}'
    UNKNOWN = 'UNKNOWN'
    NO_LINE = -1

    DEFAULT_PRIORITY = 0
    DEFAULT_CONFIDENCE = 50.0
    PAGE_START = 0
    EMPTY = ''
    ID = '_id'
    FACT = 'fact'
    FACTS = 'facts'
    ACTION = 'action'
    ACTIONS = 'actions'
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

    @staticmethod
    def get_key(prefix, key):
        return Constants.KEY_FORMAT.format(prefix=prefix, key=key)


class Queries:
    ######################################################################
    # QUERIES
    ######################################################################
    PURGE_GRAPH = 'MATCH (node) DETACH DELETE node'
    CREATE_FACT_QUERY = 'CREATE (f:fact {{ name: "{name}", ' \
                        'activated: "{activated}", ' \
                        'confidence: "{confidence}", ' \
                        'time: "{time}", type: "{type}" }})'
    UPDATE_FACT_QUERY = 'MATCH (f:fact) WHERE f.name = "{name}" ' \
                        'SET f.activated = "{activated}", ' \
                        'f.confidence = "{confidence}", ' \
                        'f.time = "{time}", f.type = "{type}" RETURN f'
    DELETE_FACT_QUERY = 'match (f:fact) where f.name="{name}" DETACH DELETE f'
    GET_FACT_QUERY = 'match (f:fact) where f.name="{name}" return f'
    GET_ACTIVATED_FACT_QUERY = 'MATCH (fact)<-[l:LHS]->(rule)<-[r:RHS]->' \
                               '(action), (facts)<-[LHS]->(rule) ' \
                               'WHERE fact.activated = "True" ' \
                               'RETURN rule'
    GET_FACTS_BY_RULE_QUERY = 'MATCH (r:rule {{name:"{rule_name}"}})' \
                              '<-[:LHS]->(fact) RETURN DISTINCT fact'
    GET_ACTIONS_BY_RULE_QUERY = 'MATCH (r:rule {{name:"{rule_name}"}})' \
                                '<-[:RHS]->(action) RETURN DISTINCT action'
    GET_MODE_QUERY = 'match (m:mode) return m'
    GET_RULE_QUERY = 'MATCH p =(r:rule {{ name: "{name}" }}) RETURN r'
    CREATE_MODE_QUERY = 'CREATE (m:mode {{ mode: "{mode}", time: "{time}"}})'
    UPDATE_MODE_QUERY = 'MATCH (m:mode) ' \
                        'SET m.mode="{mode}", m.time="{time}" return m'
    CREATE_RULE_QUERY = 'CREATE (r:rule {{ name: "{name}", ' \
                        'priority: {priority}, time: "{time}"}})'
    GET_ACTION_QUERY = 'match (a:action) where a.name="{name}" return a'
    CREATE_ACTION_QUERY = 'CREATE (a:action {{ name: "{name}", ' \
                          'type: "{type}", priority: "{priority}", ' \
                          'action: "{action}", time: "{time}"}})'
    UPDATE_ACTION_QUERY = 'MATCH (a:action) WHERE a.name = "{name}" ' \
                          'SET a.type = "{type}", a.priority = "{priority}", ' \
                          'a.action = "{action}", a.time = "{time}" RETURN a'
    UPDATE_RULE_QUERY = 'MATCH (r:rule) WHERE r.name = "{name}" ' \
                        'SET r.priority = "{priority}", ' \
                        'r.time = "{time}" RETURN r'
    DELETE_ACTION_QUERY = 'match (a:action) where a.name="{name}" ' \
                          'DETACH DELETE a'
    DELETE_RULE_QUERY = 'match (r:rule) where r.name="{name}" DETACH DELETE r'
    GET_FACT_RULE_EXISTS = 'MATCH (fact)<-[r:LHS]->(rule) ' \
                           'WHERE rule.name = "{rule_name}" AND ' \
                           'fact.name = "{fact_name}" RETURN fact'
    GET_RULE_ACTION_EXISTS = 'MATCH (action)<-[r:RHS]->(rule) ' \
                             'WHERE rule.name = "{rule_name}" AND ' \
                             'action.name = "{action_name}" RETURN rule'
    CREATE_RULE_FACT_RELATION_QUERY = \
        'MATCH (f:fact {{name:"{fact_name}"}}), ' \
        '(r:rule {{name:"{rule_name}"}}) ' \
        'CREATE (f)-[:LHS]->(r)'
    CREATE_RULE_ACTION_RELATION_QUERY = 'MATCH (a:action ' \
                                        '{{name:"{action_name}"}}), ' \
                                        '(r:rule {{name:"{rule_name}"}}) ' \
                                        'CREATE (r)-[:RHS]->(a)'
