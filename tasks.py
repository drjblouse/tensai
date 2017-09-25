""" Build module for building 10s ai."""
from invoke import task
from common.constants import Constants


@task
def pip(ctx):
    """ Install pip requirements. """
    ctx.run(Constants.PIP_CMD)


@task
def local_db(ctx):
    """ Start up a local db instance. """
    ctx.run(Constants.LOCAL_DB_CMD)


@task
def stop_local_db(ctx):
    """ Stop the local db instance. """
    ctx.run(Constants.LOCAL_DB_DOWN_CMD)


@task
def lint(ctx):
    """ Perform lint checking. """
    ctx.run(Constants.LINT_CMD)


@task
def test(ctx):
    """ Run tests. """
    ctx.run(Constants.TEST_CMD)


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
    lint(ctx)
    test(ctx)
