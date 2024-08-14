import os
import time
from collections.abc import Iterable
from posixpath import abspath

import docker
from docker.models.containers import Container  # noqa: TCH002

from remotebmi.client.client import RemoteBmiClient
from remotebmi.client.utils import DeadContainerError, get_unique_port


class BmiClientDocker(RemoteBmiClient):
    def __init__(
        self,
        image: str,
        work_dir: str,
        image_port=50051,
        host=None,
        input_dirs: Iterable[str] = (),
        user=os.getuid(),  # noqa: B008
        remove=False,
        delay=5,
    ):
        if isinstance(input_dirs, str):
            msg = (
                f'type of argument "input_dirs" must be collections.abc.Iterable; '
                f"got {type(input_dirs)} instead"
            )
            raise TypeError(msg)
        port = get_unique_port()
        client = docker.from_env()
        volumes = {}
        for raw_input_dir in input_dirs:
            input_dir = abspath(raw_input_dir)
            if not os.path.isdir(input_dir):  # noqa: PTH112
                raise NotADirectoryError(input_dir)
            volumes[input_dir] = {"bind": input_dir, "mode": "ro"}

        self.work_dir = abspath(work_dir)
        if self.work_dir in volumes:
            msg = "Found work_dir equal to one of the input directories. Please drop that input dir."
            raise ValueError(
                msg
            )
        if not os.path.isdir(self.work_dir):  # noqa: PTH112
            raise NotADirectoryError(self.work_dir)
        volumes[self.work_dir] = {"bind": self.work_dir, "mode": "rw"}
        self.container: Container = client.containers.run(
            image,
            ports={str(image_port) + "/tcp": port},
            volumes=volumes,
            working_dir=self.work_dir,
            user=user,
            remove=remove,
            detach=True,
        )
        time.sleep(delay)
        if not remove:
            # Only able to reload, read logs on exited container when remove=False
            self.container.reload()
            if self.container.status == "exited":
                exitcode = self.container.attrs["State"]["ExitCode"]
                logs = self.logs()
                msg = f"Failed to start Docker container with image {image}, Container log: {logs}"
                raise DeadContainerError(msg, exitcode, logs)

        url = f"http://{host}:{port}"
        super().__init__(url)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.stop()

    def logs(self) -> str:
        """Returns complete combined stdout and stderr written by the Docker container."""
        return self.container.logs().decode("utf8")
