import os

import pytest
from dotenv import load_dotenv
from ov_hcloud_ai_solution_client import AuthenticatedClient
from prefect import flow
from prefect.exceptions import PrefectException

from prefect_ovh.tasks import (
    check_if_job_has_failed,
    create_client,
    delete_job,
    get_infos_of_job,
    get_logs_of_job,
    get_state_job,
    start_an_existing_job,
    stop_job,
    submit_job,
)

# Load environments variables
load_dotenv()

TOKEN = os.getenv("TOKEN")


def test_good_client():
    @flow
    def client_flow():
        return create_client(token=TOKEN)

    result = client_flow()
    assert type(result) == AuthenticatedClient


def test_wrong_client():
    @flow
    def test_flow():
        return create_client(token="wrongToken")

    with pytest.raises(PrefectException, match=r"Your token is not valid .*"):
        test_flow()


def test_submit_good_job():
    @flow
    def test_flow():
        return submit_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            image="bash",
        )

    result = test_flow()
    assert "id" in result


def test_submit_wrong_job():
    @flow
    def test_flow():
        return submit_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            image="bash",
            http_port="should be a number",
        )

    with pytest.raises(
        PrefectException, match=r"Your Job can't be run !, here is the reason .*"
    ):
        test_flow()


def test_check_failed_wrong_id():
    @flow
    def test_flow():
        return check_if_job_has_failed(
            state="FAILED",
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
            telegram_webhook=None,
        )

    with pytest.raises(
        PrefectException, match=r"We can't access the logs of your job .*"
    ):
        test_flow()


def test_wrong_id_status():
    @flow
    def test_flow():
        return get_state_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id="wrong-id",
        )

    with pytest.raises(
        PrefectException,
        match=r"We can't get the infos of your job, here is the reason .*",
    ):
        test_flow()


def test_wrong_id_infos():
    @flow
    def test_flow():
        return get_infos_of_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
        )

    with pytest.raises(
        PrefectException, match=r"We can't get the infos of this job .*"
    ):
        test_flow()


def test_wrong_id_logs():
    @flow
    def test_flow():
        return get_logs_of_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
        )

    with pytest.raises(PrefectException, match=r"We can't get the logs of this job .*"):
        test_flow()


def test_wrong_id_start_job():
    @flow
    def test_flow():
        return start_an_existing_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
        )

    with pytest.raises(PrefectException, match=r"We can't start this job .*"):
        test_flow()


def test_wrong_id_stop_job():
    @flow
    def test_flow():
        return stop_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
        )

    with pytest.raises(PrefectException, match=r"We can't stop this job .*"):
        test_flow()


def test_wrong_id_delete_job():
    @flow
    def test_flow():
        return delete_job(
            client=AuthenticatedClient(
                base_url="https://gra.training.ai.cloud.ovh.net", token=TOKEN
            ),
            id_job="wrong-id",
        )

    with pytest.raises(PrefectException, match=r"We can't delete this job .*"):
        test_flow()
