"""This is an example tasks module"""
from ov_hcloud_ai_solution_client import AuthenticatedClient
from ov_hcloud_ai_solution_client.api.job import job_new
from ov_hcloud_ai_solution_client.api.me import me
from ov_hcloud_ai_solution_client.models import Job, JobSpec, Me
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


@task
def create_a_job(
    client,
    image,
    http_port=8080,
    command=[],
    listEnvVars=[],
    dicLabels={},
    name=None,
    cpu=0,
    gpu=1,
    sshPublicKeys=[],
    volumes=[],
) -> str:
    """
    Sample task that create an AI Training Job

    Returns:
        The json response when creating a job
    """
    # First of all we create the request
    request = {
        "command": command,
        "defaultHttpPort": http_port,
        "deletionRequested": False,
        "envVars": listEnvVars,
        "labels": dicLabels,
        "image": image,
        "name": name,
        "resources": {"cpu": cpu, "gpu": gpu},
        "sshPublicKeys": sshPublicKeys,
        "volumes": volumes,
    }
    if name is None:
        name = request.pop("name")
    if cpu != 0:
        request.update({"resources": {"cpu": cpu, "gpu": 0}})
    print(request)

    with client as client:
        # or if you need more info (e.g. status_code)
        response: Response[Job] = job_new.sync_detailed(
            client=client, json_body=JobSpec.from_dict(request)
        )
    return response.content.decode()
