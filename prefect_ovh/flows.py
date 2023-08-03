"""This is an example flows module"""
from prefect import flow

from prefect_ovh.tasks import create_client, hello_prefect_ovh


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


if __name__ == "__main__":
    flow.run()
