from prefect import flow

from prefect_ovh.tasks import (
    goodbye_prefect_ovh,
    hello_prefect_ovh,
)


def test_hello_prefect_ovh():
    @flow
    def test_flow():
        return hello_prefect_ovh()

    result = test_flow()
    assert result == "Hello, prefect-OVHcloud!"


def goodbye_hello_prefect_ovh():
    @flow
    def test_flow():
        return goodbye_prefect_ovh()

    result = test_flow()
    assert result == "Goodbye, prefect-OVHcloud!"
