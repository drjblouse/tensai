""" Settings for 10s ai. """
from logging import getLogger, FileHandler, Formatter, WARNING
from common.constants import Constants

LOGGER = getLogger(Constants.PLATFORM_NAME)
HANDLER = FileHandler('/var/tmp/myapp.log')
FORMATTER = Formatter('%(asctime)s %(levelname)s %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(WARNING)
DB_CONNECTION_URL = 'http://{0}:{1}'.format(
    Constants.LOCAL_IP, Constants.LOCAL_DB_PORT)
FACT_TABLE_NAME = 'facts'
TABLE_EXISTS = 'table_exists'
PAGE_SIZE = 25
KEY_SCHEMA = [
    {'AttributeName': 'key', 'KeyType': 'HASH'}
]
ATTRIBUTES = [
    {'AttributeName': 'key', 'AttributeType': 'S'}
]
DEFAULT_PROV_THROUGHPUT = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
