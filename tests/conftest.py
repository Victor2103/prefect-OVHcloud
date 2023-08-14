import os

import pytest
from dotenv import load_dotenv
from prefect.testing.utilities import prefect_test_harness

# Load environments variables
load_dotenv()

TOKEN = os.getenv("TOKEN")


@pytest.fixture(scope="session", autouse=True)
def prefect_db():
    """
    Sets up test harness for temporary DB during test runs.
    """
    with prefect_test_harness():
        yield


@pytest.fixture(autouse=True)
def reset_object_registry():
    """
    Ensures each test has a clean object registry.
    """
    from prefect.context import PrefectObjectRegistry

    with PrefectObjectRegistry():
        yield
