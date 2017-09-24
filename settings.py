""" Settings for 10s ai. """
DB_CONNECTION_URL = 'http://localhost:8000'
DB_MODULE_NAME = 'dynamodb'

# The following are build commands
PIP_CMD = 'pip install -r requirements.pip'
LOCAL_DB_CMD = 'cd local_db && docker-compose up -d'
LOCAL_DB_DOWN_CMD = 'cd local_db && docker-compose down'
TEST_CMD = 'nosetests --with-coverage --cover-package=src'
LINT_CMD = 'pyflakes *.py && pylint *.py'
