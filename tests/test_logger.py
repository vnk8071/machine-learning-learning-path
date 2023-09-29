import pytest

try:
    from utils.logger import Logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from utils.logger import Logger


@pytest.fixture(scope="function")
def get_logger_fixture():
    logger = Logger.get_logger(__name__)
    return logger


def test_log(get_logger_fixture):
    get_logger_fixture.info("This is a info message")
    get_logger_fixture.debug("This is a debug message")
    get_logger_fixture.warning("This is a warning message")
    get_logger_fixture.error("This is a error message")
    get_logger_fixture.critical("This is a critical message")
    assert True
