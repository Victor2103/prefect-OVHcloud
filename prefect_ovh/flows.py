"""This is an example flows module"""
from prefect import flow

from prefect_ovh.tasks import create_a_job, create_client, hello_prefect_ovh


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

    Returns:
        The response when creating a job
    """
    # Create the client
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
    # Return this dict of the flow
    return response


if __name__ == "__main__":
    flow.run()
