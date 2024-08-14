import socket
from contextlib import closing


def get_unique_port(host=None):
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

    def __init__(self, message, exitcode, logs, *args):
        super().__init__(message, *args)
        #: Exit code of container
        self.exitcode = exitcode
        #: Stdout and stderr of container
        self.logs = logs
