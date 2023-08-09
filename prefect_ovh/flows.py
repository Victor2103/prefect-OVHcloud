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
    start_an_existing_job,
    stop_job,
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
    return client


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
    result = stop_job(id_job=id, client=client)
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
def test_creation(token):
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


@flow
def test_client(token):
    """Generate a client and return it

    Args:
        token (_type_): Your Bearer token from OVHcloud

    Returns:
        _type_: Authenticated Client from the python SDK
    """
    client = create_client(token=token)
    return client


@flow
def test_infos(token: str, id_job: str):
    """Simple flow to get the infos of a job

    Args:
        token (str): your Bearer token
        id_job (str): your job id

    Returns:
        The infos with a good display
    """
    client = create_client(token=token)
    infos = get_infos_of_job(id_job=id_job, client=client)
    return json.dumps(infos, indent=4)


@flow
def test_logs(token: str, id_job: str):
    """Simple flow to get the logs of a job

    Args:
        token (str): your Bearer token
        id_job (str): your job id

    Returns:
        The logs as a string
    """
    client = create_client(token=token)
    logs = get_logs_of_job(id_job=id_job, client=client)
    return logs


@flow
def test_start_job(token: str, id_job: str):
    """Simple flow to start an existing job

    Args:
        token (str): your Bearer token
        id_job (str): your job id

    Returns:
        The infos of the job in a json format
    """
    client = create_client(token=token)
    response = start_an_existing_job(id_job=id_job, client=client)
    return json.dumps(response, indent=4)


@flow
def test_stop_job(token: str, id_job: str):
    """Simple flow to stop an existing job

    Args:
        token (str): your Bearer token
        id_job (str): your job id

    Returns:
        The infos of the job in a json format
    """
    client = create_client(token=token)
    response = stop_job(id_job=id_job, client=client)
    return json.dumps(response, indent=4)


if __name__ == "__main__":
    flow.run()
