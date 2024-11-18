# mypy: disable-error-code="no-untyped-def"

import pytest

from remotebmi.client.client import RemoteBmiClient


@pytest.mark.parametrize(
    "url",
    [
        "invalid_url",
        "http://",
        "ws://somehost",
        "ftp://invalid",
        "12345",
        "",
        None,
    ],
)
def test_remote_bmi_client_init_invalid_url(url: str):
    with pytest.raises(ValueError):
        RemoteBmiClient(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://somehost",
        "https://somehost",
    ],
)
def test_remote_bmi_client_init_valid_url(url: str):
    client = RemoteBmiClient(url)
    assert client.client.base_url == url
