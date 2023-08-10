import os

from dotenv import load_dotenv
from prefect import flow

from prefect_ovh.tasks import create_a_job

# Load environments variables
load_dotenv()

TOKEN = os.getenv("TOKEN")


def test_hello_prefect_ovh():
    @flow
    def test_flow():
        return create_a_job(
            token=TOKEN,
            image="bash",
        )

    result = test_flow()
    assert result != "Hello, prefect-OVHcloud!"
