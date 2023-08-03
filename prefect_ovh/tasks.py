"""This is an example tasks module"""
from ov_hcloud_ai_solution_client import AuthenticatedClient
from ov_hcloud_ai_solution_client.api.me import me
from ov_hcloud_ai_solution_client.models import Me
from ov_hcloud_ai_solution_client.types import Response
from prefect import task


@task
def hello_prefect_ovh(token: str) -> str:
    """
    Sample task that create a client and test an endpoint

    Returns:
        Your Identification information in a json file or
        unauthorized id you provide wrong credentials
    """
    client = AuthenticatedClient(
        base_url="https://gra.training.ai.cloud.ovh.net", token=token
    )
    with client as client:
        # or if you need more info (e.g. status_code)
        response: Response[Me] = me.sync_detailed(client=client)
    return response.content.decode()
