import os


class CredentialsNotConfiguredError(RuntimeError):
    pass


def get_assessment_credentials() -> tuple[str, str]:
    email = os.getenv("PZQA_EMAIL")
    password = os.getenv("PZQA_PASSWORD")
    if email and password:
        return email, password

    try:
        from credentials import VALID_CREDENTIALS
    except ModuleNotFoundError as error:
        if error.name != "credentials":
            raise
        raise CredentialsNotConfiguredError(
            "Set PZQA_EMAIL and PZQA_PASSWORD or provide tests/credentials.py "
            "to run authenticated checks"
        ) from error

    email = VALID_CREDENTIALS.get("username")
    password = VALID_CREDENTIALS.get("password")
    if not isinstance(email, str) or not email:
        raise CredentialsNotConfiguredError(
            "Provide a valid username in tests/credentials.py or set PZQA_EMAIL"
        )
    if not isinstance(password, str) or not password:
        raise CredentialsNotConfiguredError(
            "Provide a valid password in tests/credentials.py or set PZQA_PASSWORD"
        )

    return email, password
