from prefect_ovh.flows import test_creation


def test_hello_and_goodbye_flow():
    result = test_creation(
        "SAnNu2i6R+K6JOYaAUDclnTWx1XH3Ck7+hIfr2dWj4oLEbt+XvhMnvUUegm0QFY9"
    )
    assert result != "DONE"
