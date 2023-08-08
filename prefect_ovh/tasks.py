"""This is an example tasks module"""
import json
import time

from ov_hcloud_ai_solution_client import AuthenticatedClient
from ov_hcloud_ai_solution_client.api.job import (
    job_delete,
    job_get,
    job_kill,
    job_log,
    job_new,
    job_start,
)
from ov_hcloud_ai_solution_client.api.me import me
from ov_hcloud_ai_solution_client.models import Job, JobSpec, Me
from ov_hcloud_ai_solution_client.types import Response
from prefect import task
from prefect.exceptions import PrefectException


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
    token,
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
    # First of all we create the request to send to the core API
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
    # Create a unique client for python SDK
    client = AuthenticatedClient(
        base_url="https://gra.training.ai.cloud.ovh.net", token=token
    )
    with client as client:
        response: Response[Job] = job_new.sync_detailed(
            client=client, json_body=JobSpec.from_dict(request)
        )
    # We check if the job is submitted to the AI Training tool
    if response.status_code != 200:
        raise PrefectException(
            "You Job can't be run !, here is the reason :", response.content.decode()
        )
    else:
        # We get the content of the response
        response_content = response.content.decode()
        # We transform the response as a dict
        response_dict = json.loads(response_content)
        # We get the id of the job
        id = response_dict["id"]
        # At regular intervals, we check whether the job has been completed
        state = response_dict["status"]["state"]
        while (
            state != "DONE"
            and state != "INTERRUPTED"
            and state != "FAILED"
            and state != "ERROR"
        ):
            print("salut")
            # Wait 5 minutes
            time.sleep(10)
            # Make a new call to get the status
            client = AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=token
            )
            with client as client:
                response: Response[Job] = job_get.sync_detailed(id=id, client=client)
            # We check if you have the new informations of the job
            if response.status_code != 200:
                raise PrefectException(
                    "You Job can't be run !, here is the reason :",
                    response.content.decode(),
                )
            # We get the content of the response
            response_content = response.content.decode()
            # We transform the response as a dict
            response_dict = json.loads(response_content)
            state = response_dict["status"]["state"]
            print(type(state))
            if state == "INTERRUPTED" or state == "FAILED" or state == "ERROR":
                # Get the logs of the application
                client = AuthenticatedClient(
                    base_url="https://gra.training.ai.cloud.ovh.net", token=token
                )
                with client as client:
                    logs = job_log.sync_detailed(id=id, client=client)
                if state == "INTERRUPTED":
                    raise PrefectException(
                        "Your job has been interrupted, here are the logs", logs
                    )
                if state == "FAILED":
                    raise PrefectException(
                        "Your job has failed, here are the logs", logs
                    )
                if state == "ERROR":
                    raise PrefectException(
                        "Your job has an error due to back end, here are the logs", logs
                    )
            else:
                print(state == "DONE")
                if state != "DONE":
                    print("Your job is in state", state)
        return response


@task
def get_infos_of_job(id_job: str, client) -> str:
    """
    Sample task that Send the infos of a job

    Returns:
        The json response asking infos of a job
    """
    with client as client:
        response: Response[Job] = job_get.sync_detailed(id=id_job, client=client)

    return response.content.decode()


@task
def get_logs_of_job(id_job: str, client) -> str:
    """Sample task that returns the logs of a given job

    Args:
        id_job (str): the id of the job
        client (_type_): An authenticated client with a token

    Returns:
        str: the logs of the jobs in a string
    """
    with client as client:
        response: Response[Job] = job_log.sync_detailed(id=id_job, client=client)
    return response.content.decode()


@task
def start_an_existing_job(id_job: str, client) -> str:
    """Start a job in interrupted or done state

    Args:
        id_job (str): the id of the job
        client (AuthenticatedClient): the authenticated Client

    Returns:
        str: The infos of the job running
    """
    with client as client:
        response: Response[Job] = job_start.sync_detailed(id=id_job, client=client)
    return response.content.decode()


@task
def stop_an_existing_job(id_job: str, client) -> str:
    """Stop an existing job

    Args:
        id_job (str): the id of the ovhai training job
        client (_type_): an authenticated client

    Returns:
        str: the infos of the job
    """
    with client as client:
        response: Response[Job] = job_kill.sync_detailed(id=id_job, client=client)
    return response.content.decode()


@task
def delete_an_existing_job(id_job: str, client) -> str:
    """Delete an existing job with his id

    Args:
        id_job (str): The id of the job
        client (_type_): The SDK client

    Returns:
        str: Nothing if the job is correctly deleted
    """
    with client as client:
        response: Response[Job] = job_delete.sync_detailed(id=id_job, client=client)
    return response
