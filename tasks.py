""" Build module for building 10s ai."""
from time import sleep
from invoke import task

SLEEP_TIME = 5
START_DB = 'sudo neo4j start'
STOP_DB = 'sudo pkill -f neo4j'
TEST_CMD = 'py.test --cov-report term:skip-covered --cov=common -n 1'
LINT_CMD = 'pyflakes *.py && pylint *.py && flake8 *.py ' \
           '&& pycodestyle --statistics -qq *.py ' \
           '&& mypy --ignore-missing-imports *.py'
TEST_ALL_MESSAGE = 'If you are seeing coverage files without 100%, ' \
                   'you are not likely running tests against real services.' \
                   "\nRunning `inv tall` or `invoke test_all` " \
                   "will start and stop " \
                   'services and run tests against live services.'


@task
def start_db(ctx):
    """ Install pip requirements. """
    ctx.run(START_DB, warn=True)
    sleep(SLEEP_TIME)


@task
def stop_db(ctx):
    """ Stop the real graph db. """
    ctx.run(STOP_DB, warn=True)


@task
def lint(ctx):
    """ Perform lint checking. """
    ctx.run(LINT_CMD)


@task
def test(ctx):
    """ Run tests. """
    ctx.run(TEST_CMD)


@task(pre=[lint, start_db, test, stop_db])
def test_all(_):
    """ Start the graph db and then run the tests. """


@task(pre=[test_all])
def tall(_):
    """ Shorthand for test_app above. """


@task(default=True, pre=[lint, test])
def build(_):
    """ Perform the automated build process. """
    print(TEST_ALL_MESSAGE)
