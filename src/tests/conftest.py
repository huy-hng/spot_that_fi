from src.db.initializer import configure_db, delete_tables, get_testing_engine
from src.tests.fixtures import *


def pytest_configure(config):
	"""
	Allows plugins and conftest files to perform initial configuration.
	This hook is called for every plugin and initial conftest
	file after command line options have been parsed.
	"""


def pytest_sessionstart(session):
	"""
	Called after the Session object has been created and
	before performing collection and entering the run test loop.
	"""
	engine = get_testing_engine()
	configure_db(engine)


def pytest_sessionfinish(session, exitstatus):
	"""
	Called after whole test run finished, right before
	returning the exit status to the system.
	"""


def pytest_unconfigure(config):
	"""
	called before test process is exited.
	"""
