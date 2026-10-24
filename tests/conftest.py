import pytest

from assessment_auth import (
    CredentialsNotConfiguredError,
    get_assessment_credentials,
)


@pytest.fixture
def assessment_credentials():
    try:
        return get_assessment_credentials()
    except CredentialsNotConfiguredError as error:
        pytest.skip(str(error))
