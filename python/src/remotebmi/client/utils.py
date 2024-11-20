import getpass
import os
import socket
from contextlib import closing
from typing import Any
from urllib.parse import urlparse


def get_unique_port(host: str | None = None) -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("" if host is None else host, 0))
        return int(s.getsockname()[1])


class DeadContainerError(ChildProcessError):
    """Exception for when a container has died.

    Args:
        message (str): Human readable error message
        exitcode (int): The non-zero exit code of the container
        logs (str): Logs the container produced

    """

    def __init__(self, message: str, exitcode: int, logs: str, *args: Any):
        super().__init__(message, *args)
        #: Exit code of container
        self.exitcode = exitcode
        #: Stdout and stderr of container
        self.logs = logs


def validate_url(url: str) -> None:
    """
    Validates a given URL to ensure it has a valid scheme, network location,
    and that the scheme is either 'http' or 'https'.

    Args:
        url (str): The URL to validate.

    Raises:
        ValueError: If the URL is invalid, i.e., it does not have a scheme,
                    network location, or the scheme is not 'http' or 'https'.

    Example:
        validate_url("http://example.com")
    """
    parsed_url = urlparse(url)
    has_scheme = parsed_url.scheme != ""
    has_netloc = parsed_url.netloc != ""
    is_valid_scheme = parsed_url.scheme in ["http", "https"]
    if not (has_scheme and has_netloc and is_valid_scheme):
        msg = f"Invalid: {url}, should be http(s)://host[:port][/path]"
        raise ValueError(msg)


def getuser() -> int | str:
    """Windows-safe getuid implementation.

    Will return user ID on unix/macOS. Will return username on Windows.
    """
    if os.system == "nt":
        return getpass.getuser()
    return os.getuid()
