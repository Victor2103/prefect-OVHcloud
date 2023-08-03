"""This is an example flows module"""
from prefect import flow

from prefect_ovh.blocks import OvhcloudBlock
from prefect_ovh.tasks import (
    goodbye_prefect_ovh,
    hello_prefect_ovh,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    OvhcloudBlock.seed_value_for_example()
    block = OvhcloudBlock.load("sample-block")

    print(hello_prefect_ovh())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_ovh())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
