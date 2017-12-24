""" Build module for building 10s ai."""
from invoke import task

PIP_CMD = 'pip install -r requirements.pip'
TEST_CMD = 'py.test --cov-report term:skip-covered --cov=common -n 1'
LINT_CMD = 'pyflakes *.py && pylint *.py && flake8 *.py ' \
           '&& pycodestyle --statistics -qq *.py ' \
           '&& mypy --ignore-missing-imports *.py'


@task
def pip(ctx):
    """ Install pip requirements. """
    ctx.run(PIP_CMD)


@task
def lint(ctx):
    """ Perform lint checking. """
    ctx.run(LINT_CMD)


@task
def test(ctx):
    """ Run tests. """
    ctx.run(TEST_CMD)


@task(default=True, pre=[lint, test])
def build(_):
    """ Perform the automated build process. """
    pass
