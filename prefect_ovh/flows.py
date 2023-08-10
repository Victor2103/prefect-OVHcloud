"""This is an example flows module"""
import json
import time

from prefect import flow
from prefect.exceptions import PrefectException

from prefect_ovh.tasks import (
    check_if_job_has_failed,
    check_time_out_job,
    create_client,
    delete_job,
    get_infos_of_job,
    get_logs_of_job,
    get_state_job,
    send_message_with_state,
    start_an_existing_job,
    stop_job,
    submit_job,
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
def create_job_and_wait_until_is_done(
    token: str,
    image: str,
    http_port: int = 8080,
    command: list = [],
    listEnvVars: list = [],
    dicLabels: dict = {},
    name: str = None,
    cpu: int = 0,
    gpu: int = 1,
    sshPublicKeys: list = [],
    volumes: list = [],
    timeout: float = 3600,
    wait_seconds: float = 3,
    telegram: bool = False,
    api_telegram: str = None,
    chat_id: str = None,
) -> dict:
    """Create a job and send error if failed

    Args:
        token (str): The bearer token from OVHcloud
        image (str): your docker image
        http_port (int, optional): the default http port. Defaults to 8080.
        command (list, optional): command to run in container. Defaults to [].
        listEnvVars (list, optional): your env variables. Defaults to [].
        dicLabels (list, optional): the job's labels. Defaults to {}.
        name (str, optional): the name of the job. Defaults to None.
        cpu (int, optional): the number of cpu. Defaults to 0.
        gpu (int, optional): number of gpu. Defaults to 1.
        sshPublicKeys (list, optional): the ssh public keys. Defaults to [].
        volumes (list, optional): some volumes such as git repo or swift containers.
            Defaults to [].
        timeout (float, optional): max time to run the job. Defaults to 3600.
        wait_seconds (float, optional): the time beetween each call for the status.
            Defaults to 3.
        telegram (bool, optional): a boolean if you have a telegram api to send
            the message instead of terminal. Defaults to False.
        api_telegram (str): the api telegram if you want to send a message to your chat.
            Defaults to None.
        chat_id (str): the chat id of your telegram bot. Defaults to None.

    Raises:
        PrefectException: If we have error unknow.

    Returns:
        dict: the infos of the job with good display
    """
    # Create a client for job submission to the API
    client = create_client(token=token)
    # Define the parameter to put in the job creation

    # Launch the task to submit a job
    response = submit_job(
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
    # We get the status and the id of the job
    id = response["id"]
    state = response["status"]["state"]
    # We get a float for the time now (to check the timeout)
    start = time.monotonic()
    # We check with regular intervals if job is over
    while (
        state != "DONE"
        and state != "INTERRUPTED"
        and state != "FAILED"
        and state != "ERROR"
    ):
        # We create a new client
        client = create_client(token=token)
        # We check of the timeout is not exceeded
        if not check_time_out_job(timeout=timeout, start=start, id=id, client=client):
            raise PrefectException("We encountered an Error")
        # We send a message to the user
        send_message_with_state(
            state=state,
            id=id,
            telegram=telegram,
            api_telegram=api_telegram,
            chat_id=chat_id,
        )
        # We wait with param wait_seconds
        time.sleep(wait_seconds)
        # We get the new status
        client = create_client(token=token)
        state = get_state_job(id=id, client=client)
        # We check if the job has not failed
        client = create_client(token=token)
        if not check_if_job_has_failed(state=state, client=client, id_job=id):
            raise PrefectException("We encountered an error")
    # We get the infos of the job and send it in a good display
    client = create_client(token=token)
    infos = get_infos_of_job(id_job=id, client=client)
    return json.dumps(infos, indent=4)


@flow(name="Test the python client")
def test_client(token):
    """Generate a client and return it

    Args:
        token (_type_): Your Bearer token from OVHcloud

    Returns:
        _type_: Authenticated Client from the python SDK
    """
    client = create_client(token=token)
    return client


@flow(name="Test the task to get infos of a job")
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


@flow(name="Test the task to get the logs of the job")
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


@flow(name="Test the task to start an existing AI Training job")
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


@flow(name="Test the task to stop a job")
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


@flow(name="Test the task to delete a job")
def test_delete_job(token: str, id_job: str):
    """Simple flow to delete an existing job

    Args:
        token (str): your Bearer token
        id_job (str): your job id

    Returns:
        A str to confirm that your job with this id is delete
    """
    client = create_client(token=token)
    response = delete_job(id_job=id_job, client=client)
    return f"Your job {response} is deleted"


if __name__ == "__main__":
    flow.run()
