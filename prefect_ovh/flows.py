"""This is an example flows module"""
import json

from prefect import flow

from prefect_ovh.tasks import (
    create_a_job,
    create_client,
    get_infos_of_job,
    get_logs_of_job,
    hello_prefect_ovh,
)


@flow(name="Hello Flow From Prefect")
def hello_world(token: str) -> dict:
    """
    Sample Flow that return your credentials

    Returns:
        Your Identification information in a json file or
        unauthorized id you provide wrong credentials
    """
    # Create the client
    client = create_client(token=token)
    # Get your crendentials
    credentials = hello_prefect_ovh(client=client)
    # Return this dict of the flow
    return credentials


@flow(name="Create your first Job")
def create_a_first_job(
    token: str,
) -> dict:
    """
    Sample Flow that create an AI Training Job
    Get the id of this job
    Make a call to get infos with state
    Get the logs of the job

    Returns:
        The response when calling job infos
    """
    # Create a client for job creation
    client = create_client(token=token)
    # Define the parameter to put in the job creation
    image = "ubuntu"
    http_port = 8080
    command = []
    listEnvVars = []
    dicLabels = {}
    name = None
    cpu = 0
    gpu = 1
    sshPublicKeys = []
    volumes = []
    # Launch the task create a job
    response = create_a_job(
        client=client,
        image=image,
        http_port=http_port,
        command=command,
        listEnvVars=listEnvVars,
        dicLabels=dicLabels,
        name=name,
        cpu=cpu,
        gpu=gpu,
        sshPublicKeys=sshPublicKeys,
        volumes=volumes,
    )
    # You can run the task with only the image as a parameter
    # response = create_a_job(client=client,image=image)
    response = json.loads(response)
    # Get the id
    id = response["id"]
    # Create a new client to get the infos of the job
    client = create_client(token=token)
    # Make a new call to the api
    result = get_infos_of_job(id_job=id, client=client)
    # Create a new client for the job's logs
    client = create_client(token=token)
    # Get the logs of the job
    result = get_logs_of_job(id_job=id, client=client)
    # Return this dict of the flow
    return result


if __name__ == "__main__":
    flow.run()
