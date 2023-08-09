from prefect import flow

from prefect_ovh.tasks import create_a_job


def test_hello_prefect_ovh():
    @flow
    def test_flow():
        return create_a_job(
            token="SAnNu2i6R+K6JOYaAUDclnTWx1XH3Ck7+hIfr2dWj4oLEbt+XvhMnvUUegm0QFY9",
            image="bash",
        )

    result = test_flow()
    assert result != "Hello, prefect-OVHcloud!"
