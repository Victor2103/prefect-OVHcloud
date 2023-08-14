import os

import pytest
from dotenv import load_dotenv
from prefect.exceptions import PrefectException

from prefect_ovh.flows import create_job_and_wait_until_is_done

# Load environments variables
load_dotenv()

TOKEN = os.getenv("TOKEN")


def test_create_and_wait_job():
    result = create_job_and_wait_until_is_done(token=TOKEN, image="bash")
    assert result["status"]["state"] == "DONE"


def test_failed_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Your job .* has failed, .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN, image="bash", command=["slepp", "180"]
        )


def test_interrupted_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Your job .* is interrupted, .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN, image="bash", command=["sleep", "180"], timeout_ovh=4
        )


def test_timeout_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Timeout exceeded for the job .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN, image="bash", command=["sleep", "180"], timeout_prefect=3
        )


def test_telegram_create_and_wait_job():
    result = create_job_and_wait_until_is_done(
        token=TOKEN,
        image="bash",
        telegram=True,
        api_telegram=os.getenv("API_TELEGRAM"),
        chat_id=os.getenv("CHAT_ID"),
    )
    assert result["status"]["state"] == "DONE"


def test_telegram_failed_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Your job .* has failed, .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN,
            image="bash",
            command=["slepp", "180"],
            telegram=True,
            api_telegram=os.getenv("API_TELEGRAM"),
            chat_id=os.getenv("CHAT_ID"),
        )


def test_telegram_interrupted_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Your job .* is interrupted, .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN,
            image="bash",
            command=["sleep", "180"],
            timeout_ovh=4,
            telegram=True,
            api_telegram=os.getenv("API_TELEGRAM"),
            chat_id=os.getenv("CHAT_ID"),
        )


def test_telegram_timeout_create_and_wait_job():
    with pytest.raises(PrefectException, match=r"Timeout exceeded for the job .*"):
        create_job_and_wait_until_is_done(
            token=TOKEN,
            image="bash",
            command=["sleep", "180"],
            timeout_prefect=3,
            telegram=True,
            api_telegram=os.getenv("API_TELEGRAM"),
            chat_id=os.getenv("CHAT_ID"),
        )
