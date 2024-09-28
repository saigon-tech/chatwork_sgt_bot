import pytest


@pytest.fixture(autouse=True)
def enable_logging(caplog):
    caplog.set_level("DEBUG")
