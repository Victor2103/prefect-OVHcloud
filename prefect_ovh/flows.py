"""This is an example flows module"""
import json
import time

from prefect import flow

from prefect_ovh.tasks import (
    create_a_job,
    create_client,
    delete_an_existing_job,
    get_infos_of_job,
    get_logs_of_job,
    hello_prefect_ovh,
    start_an_existing_job,
    stop_an_existing_job,
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
    Stop the same job
    Restart the same job
    Returns:
        The response when calling job infos
    """
    # Create a client for job creation
    client = create_client(token=token)
    # Define the parameter to put in the job creation
    image = "bash"
    http_port = 8080
    command = ["sleep", "180"]
    listEnvVars = []
    dicLabels = {}
    name = None
    cpu = 0
    gpu = 1
    sshPublicKeys = []
    volumes = []
    # Launch the task create a job
    response = create_a_job(
        token=token,
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
    print("Here is your job created : \n", result)
    # Create a new client for the job's logs
    client = create_client(token=token)
    # Get the logs of the job
    result = get_logs_of_job(id_job=id, client=client)
    print("Here are your logs \n", result)
    # Create a new client
    client = create_client(token=token)
    # Stop the job
    result = stop_an_existing_job(id_job=id, client=client)
    print("Here is your job stopped : \n", f"{result}")
    # Create a new client
    client = create_client(token=token)
    # Whait that your job is really stopped
    time.sleep(20)
    # Restart the job
    result = start_an_existing_job(id_job=id, client=client)
    print(result)
    time.sleep(300)
    # Delete the job
    client = create_client(token=token)
    result = delete_an_existing_job(id_job=id, client=client)
    # Return this dict of the flow
    return result


@flow
def test(token):
    """
    Sample Flow that create an AI Training Job
    Get the id of this job
    Make a call to get infos with state
    Get the logs of the job
    Stop the same job
    Restart the same job
    Returns:
        The response when calling job infos
    """
    # Define the parameter to put in the job creation
    image = "bash"
    http_port = 8080
    command = ["sleep", "80"]
    listEnvVars = []
    dicLabels = {}
    name = None
    cpu = 1
    gpu = 0
    sshPublicKeys = []
    volumes = []
    timeout = 3600
    wait_seconds = 3
    response = create_a_job(
        token=token,
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
        timeout=timeout,
        wait_seconds=wait_seconds,
    )
    return response


if __name__ == "__main__":
    flow.run()
