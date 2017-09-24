""" Build module for building 10s ai."""
from invoke import task
from settings import LOCAL_DB_CMD, LOCAL_DB_DOWN_CMD, \
    TEST_CMD, PIP_CMD, LINT_CMD


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


@task
def start(ctx):
    """ Start any services required for build/test. """
    local_db(ctx)


@task
def stop(ctx):
    """ Stop all services started for build/test. """
    stop_local_db(ctx)


@task(default=True)
def build(ctx):
    """ Perform the automated build process. """
    start(ctx)
    lint(ctx)
    test(ctx)
    stop(ctx)
