import os

from dotenv import load_dotenv

from prefect_ovh.flows import test_creation

# Load environments variables
load_dotenv()

TOKEN = os.getenv("TOKEN")


def test_hello_and_goodbye_flow():
    result = test_creation(TOKEN)
    assert result != "DONE"
