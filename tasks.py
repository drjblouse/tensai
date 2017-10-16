""" Build module for building 10s ai."""
from invoke import task

PIP_CMD = 'pip install -r requirements.pip'
TEST_CMD = 'rm .coverage && nosetests --with-coverage --cover-package=common ' \
           '--cover-min-percentage=80'
LINT_CMD = 'pyflakes *.py && pylint *.py'
LOCAL_DB_CMD = 'docker-compose -f local_db/docker-compose.yml up -d'
LOCAL_DB_DOWN_CMD = 'docker-compose -f local_db/docker-compose.yml down'


@task
def pip(ctx):
    """ Install pip requirements. """
    ctx.run(PIP_CMD)


@task
def local_db(ctx):
    """ Start up a local db instance. """
    ctx.run(LOCAL_DB_CMD)


@task
def stop_local_db(ctx):
    """ Stop the local db instance. """
    ctx.run(LOCAL_DB_DOWN_CMD)


@task
def lint(ctx):
    """ Perform lint checking. """
    ctx.run(LINT_CMD)


@task
def test(ctx):
    """ Run tests. """
    ctx.run(TEST_CMD)


@task(pre=[local_db])
def start(_):
    """ Start any services required for build/test. """
    pass


@task(pre=[stop_local_db])
def stop(_):
    """ Stop all services started for build/test. """
    pass


@task(default=True, pre=[lint, test])
def build(_):
    """ Perform the automated build process. """
    pass
