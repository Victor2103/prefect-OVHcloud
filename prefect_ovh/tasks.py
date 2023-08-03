"""This is an example tasks module"""
from ov_hcloud_ai_solution_client import AuthenticatedClient
from ov_hcloud_ai_solution_client.api.me import me
from ov_hcloud_ai_solution_client.models import Me
from ov_hcloud_ai_solution_client.types import Response
from prefect import task


@task
def create_client(token: str) -> str:
    """
    Sample task to create an OVHcloud Client

    Returns:
        A client object from SDK
    """
    client = AuthenticatedClient(
        base_url="https://gra.training.ai.cloud.ovh.net", token=token
    )
    return client


@task
def hello_prefect_ovh(client) -> str:
    """
    Sample task that test your credentials

    Returns:
        You credentials in json
        or wrong identification
    """
    with client as client:
        # or if you need more info (e.g. status_code)
        response: Response[Me] = me.sync_detailed(client=client)
    return response.content.decode()
